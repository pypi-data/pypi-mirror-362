import logging
import os
import traceback

import matplotlib.pyplot as plt
import numpy as np
import scanpy as sc
from scipy.stats import entropy
from sklearn.metrics import silhouette_score
from sklearn.neighbors import NearestNeighbors

import FeaSc as fsc

# 配置日志记录
logging.basicConfig(
		filename='batch_correction_processing.log',
		level=logging.INFO,
		format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('BatchCorrectionProcessor')

# 配置matplotlib
plt.rcParams['figure.figsize'] = [6, 4]
plt.rcParams['figure.dpi'] = 100

# 创建输出目录
os.makedirs("umap_plot", exist_ok=True)
os.makedirs("results", exist_ok=True)


def calculate_batch_kl(embedding, batch_labels, k=30):
	"""
	手动计算BatchKL
	:param embedding: 降维坐标 (n_cells x n_features)
	:param batch_labels: 批次标签 (n_cells,)
	:param k: 近邻数
	:return: BatchKL值
	"""
	try:
		# 获取唯一批次和全局批次分布
		unique_batches, global_counts = np.unique(batch_labels, return_counts=True)
		global_dist = global_counts / global_counts.sum()
		
		# 计算KNN
		nbrs = NearestNeighbors(n_neighbors=k).fit(embedding)
		distances, indices = nbrs.kneighbors(embedding)
		
		# 计算每个细胞的KL散度
		kl_values = []
		for i in range(len(batch_labels)):
			neighbor_batches = batch_labels[indices[i]]
			_, local_counts = np.unique(neighbor_batches, return_counts=True)
			local_dist = local_counts / local_counts.sum()
			
			# 确保local_dist和global_dist形状一致
			aligned_local = np.zeros(len(global_dist))
			for j, batch in enumerate(unique_batches):
				if batch in neighbor_batches:
					idx = np.where(neighbor_batches == batch)[0]
					aligned_local[j] = len(idx) / k
			
			# 避免零概率问题
			aligned_local = np.clip(aligned_local, 1e-10, 1.0)
			global_dist_clip = np.clip(global_dist, 1e-10, 1.0)
			
			# 计算KL散度
			kl = entropy(aligned_local, global_dist_clip)
			kl_values.append(kl)
		
		return np.mean(kl_values)
	except Exception as e:
		logger.error(f"Error in calculate_batch_kl: {str(e)}")
		raise


def process_h5ad_file(file_path, results_file):
	"""处理单个h5ad文件"""
	filename = os.path.basename(file_path)
	try:
		logger.info(f"开始处理文件: {filename}")
		
		# 读取数据
		adata = sc.read_h5ad(file_path)
		logger.info(f"成功读取文件: {filename}, 细胞数: {adata.n_obs}, 基因数: {adata.n_vars}")
		
		# 基本预处理
		adata.var_names_make_unique()
		sc.pp.filter_genes(adata, min_cells=3)
		sc.pp.filter_cells(adata, min_genes=200)
		logger.info(f"过滤后: 细胞数: {adata.n_obs}, 基因数: {adata.n_vars}")
		
		# 高度可变基因
		sc.pp.highly_variable_genes(adata, n_top_genes=3000, flavor="seurat_v3")
		adata = adata[:, adata.var.highly_variable]
		logger.info(f"选择高度可变基因后: 基因数: {adata.n_vars}")
		
		# 保存原始计数
		adata.layers['counts'] = adata.X.copy()
		
		# 设置细胞类型列
		if 'Celltype (major-lineage)' in adata.obs:
			adata.obs['cell'] = adata.obs['Celltype (major-lineage)'].astype(str)
		else:
			adata.obs['cell'] = 'unknown'
		logger.info(f"设置细胞类型列完成")
		
		# 确定批次列
		batch_col = "Sample" if "Sample" in adata.obs else adata.obs.columns[0]
		logger.info(f"使用批次列: {batch_col}，包含{len(adata.obs[batch_col].unique())}个批次")
		
		# 运行降维
		adata = fsc.run_multi_reduction(adata, n_comps=16, method="pca", batch_col=batch_col)
		logger.info("完成多重降维")
		
		# 可视化
		sc.pp.neighbors(adata, use_rep="multi_pca")
		sc.tl.umap(adata)
		logger.info("计算UMAP完成")
		
		# 保存UMAP图
		plt.figure(figsize=(12, 6))
		sc.pl.umap(adata, color=[batch_col, "cell"], show=False)
		plt.suptitle(filename, y=1.02)
		plt.savefig(f"umap_plot/{filename}_umap.png", bbox_inches='tight', dpi=150)
		plt.close()
		logger.info("保存UMAP图完成")
		
		# 计算指标
		embedding = adata.obsm["multi_pca"]
		batch_labels = adata.obs[batch_col].values
		n_batches = len(np.unique(batch_labels))
		logger.info(f"降维嵌入形状: {embedding.shape}, 批次数: {n_batches}")
		
		# ASW-batch
		asw_batch = silhouette_score(embedding, batch_labels, metric='euclidean')
		logger.info(f"ASW-batch计算完成: {asw_batch:.4f}")
		
		# iLISI
		k = min(90, int(0.03 * len(embedding)))
		logger.info(f"计算iLISI, 使用k={k}")
		nbrs = NearestNeighbors(n_neighbors=k).fit(embedding)
		distances, indices = nbrs.kneighbors(embedding)
		
		lisi_scores = []
		for i in range(len(batch_labels)):
			neighbor_batches = batch_labels[indices[i]]
			unique, counts = np.unique(neighbor_batches, return_counts=True)
			proportions = counts / counts.sum()
			simpson = np.sum(proportions ** 2)
			inv_simpson = 1 / simpson
			lisi_scores.append(inv_simpson)
		
		ilisi_score = np.mean(lisi_scores)
		logger.info(f"iLISI计算完成: {ilisi_score:.4f}")
		
		# BatchKL
		n_cells = adata.n_obs
		base_k = max(15, min(100, int(n_cells * 0.02)))
		logger.info(f"计算BatchKL, 使用k={base_k}")
		batch_kl_manual = calculate_batch_kl(embedding, batch_labels, k=base_k)
		logger.info(f"BatchKL计算完成: {batch_kl_manual:.4f}")
		
		# 写入结果
		with open(results_file, 'a') as f:
			f.write(f"\nFile: {filename}\n")
			f.write(f"Number of cells: {adata.n_obs}\n")
			f.write(f"Number of batches: {n_batches}\n")
			f.write(f"ASW-batch: {asw_batch:.4f}\n")
			f.write(f"iLISI: {ilisi_score:.4f} (ideal: {n_batches})\n")
			f.write(f"BatchKL: {batch_kl_manual:.4f} (ideal: close to 0)\n")
			f.write("-" * 50 + "\n")
		
		logger.info(f"文件{filename}处理完成")
		return True
	
	except Exception as e:
		# 记录完整的错误信息
		error_msg = f"处理文件{filename}时出错: {str(e)}\n{traceback.format_exc()}"
		logger.error(error_msg)
		
		# 在结果文件中记录错误
		with open(results_file, 'a') as f:
			f.write(f"\nError processing {filename}:\n")
			f.write(f"{error_msg}\n")
			f.write("-" * 50 + "\n")
		
		return False


# 主程序
h5ad_dir = "../data/h5ad/h5ad_data/"
results_file = "results/batch_correction_metrics.txt"

# 清空或创建结果文件
with open(results_file, 'w') as f:
	f.write("Batch Correction Metrics Report\n")
	f.write("=" * 50 + "\n")

# 处理所有h5ad文件
processed_count = 0
failed_count = 0

for file in os.listdir(h5ad_dir):
	if file.endswith(".h5ad"):
		file_path = os.path.join(h5ad_dir, file)
		logger.info(f"\n{'=' * 50}\n开始处理数据集: {file}\n{'=' * 50}")
		
		success = process_h5ad_file(file_path, results_file)
		
		if success:
			processed_count += 1
		else:
			failed_count += 1
		
		logger.info(f"处理状态: {'成功' if success else '失败'}\n{'-' * 50}")

# 最终报告
logger.info(f"\n{'=' * 50}\n处理完成!\n处理数据集数: {processed_count}\n失败数据集数: {failed_count}\n{'=' * 50}")
print(
		f"\n处理完成!\n处理数据集数: {processed_count}\n失败数据集数: {failed_count}\n日志文件: batch_correction_processing.log")
