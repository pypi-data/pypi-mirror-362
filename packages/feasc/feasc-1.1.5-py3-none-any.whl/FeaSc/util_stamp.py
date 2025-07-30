import anndata as ad
import scanpy as sc
import squidpy as sq
import sctm

from sklearn.decomposition import NMF, PCA
from FeaSc.util_mca import run_mca


def scamp(adata: ad.AnnData,
          n_topics: int = 16,
          batch: str = "batch",
          method: str = 'pca',
          n_comps: int = 50,
          n_comps_1: int = 40,
          flag: bool = False,
          device: str = "cpu"):
	"""
	功能：使用 SCAMP 算法进行细胞降维，并使用 STAMP 算法进行主题建模。
	:param adata: anndata 对象
	:param method: 降维方法，可选 'pca', 'nmf','mca','mca_pca'
	:param n_comps: 第一次降维 （pca, nmf, mca) 后的维数
	:param n_comps_1: 第二次降维后的维数 （如果 method='mca_pca'）
	:param n_topics: stamp 后的主题数
	:param batch: 如果有分批次数据，则指定 batch 列名
	:param flag: 是否分批次降维
	:param device: 选择运行设备，'cpu' 或 'cuda:0'
	:return: topic_prop：每个细胞的主题分布，(n_cells, n_topics)，beta：每个特征的主题分布，(n_hv_genes, n_topics)
	"""
	
	# 预处理前备份
	adata.layers['raw'] = adata.X.copy()
	
	# 归一化
	sc.pp.normalize_total(adata, target_sum=1e4)  # 归一化
	sc.pp.log1p(adata)  # 对数转换
	
	# 降维（pca， nmf， mca， mca_pca）
	if flag:
		# batch_list = list(adata.obs.batch.unique())
		batch_list = list(adata.obs[batch].unique())
		# adata_batch_list = [adata[adata.obs.batch == batch] for batch in batch_list]
		adata_batch_list = [adata[adata.obs[batch] == b] for b in batch_list]
		
		if method == 'pca':
			# 分别对每个 batch 进行 pca 降维
			for adata_batch in adata_batch_list:
				sc.pp.pca(adata_batch, n_comps=n_comps)
			adata = adata_batch_list[0].concatenate(adata_batch_list[1:], batch_key="batch_list", index_unique=None)
			adata.obsm['spatial'] = adata.obsm['X_pca']  # 使用 PCA 坐标
		elif method == 'nmf':
			# 分别对每个 batch 进行 nmf 降维
			for adata_batch in adata_batch_list:
				nmf = NMF(n_components=n_comps)
				adata_batch.obsm['X_nmf'] = nmf.fit_transform(adata_batch.X)
			adata = adata_batch_list[0].concatenate(adata_batch_list[1:], batch_key="batch_list", index_unique=None)
			adata.obsm['spatial'] = adata.obsm['X_nmf']  # 使用 NMF 坐标
		elif method == 'mca':
			# 分别对每个 batch 进行 mca 降维
			for adata_batch in adata_batch_list:
				# print(adata_batch.shape)
				# print(adata_batch.X)
				out = run_mca(adata_batch, nmcs=n_comps)
				adata_batch.obsm['X_mca'] = out[0]
			adata = adata_batch_list[0].concatenate(adata_batch_list[1:], batch_key="batch_list", index_unique=None)
			adata.obsm['spatial'] = adata.obsm['X_mca']  # 使用 MCA 坐标
		elif method == 'mca_pca':
			# 分别对每个 batch 进行 mca 降维
			for adata_batch in adata_batch_list:
				out = run_mca(adata_batch, nmcs=n_comps)
				adata_batch.obsm['X_mca'] = out[0]
			# 再对每个 batch 的 mca 结果进行 pca 降维
			for adata_batch in adata_batch_list:
				pca = PCA(n_components=n_comps_1)
				adata_batch.obsm['X_pca'] = pca.fit_transform(adata_batch.obsm['X_mca'])
			adata = adata_batch_list[0].concatenate(adata_batch_list[1:], batch_key="batch_list", index_unique=None)
			adata.obsm['spatial'] = adata.obsm['X_pca']  # 使用 MCA->PCA 坐标
		else:
			raise ValueError("Invalid method. Choose from 'pca', 'nmf', 'mca', or'mca_pca'.")
	else:
		if method == 'nmf':
			nmf = NMF(n_components=n_comps)
			adata.obsm['X_nmf'] = nmf.fit_transform(adata.X)
			adata.obsm['spatial'] = adata.obsm['X_nmf']  # 将结果存入 Spatial
		elif method == 'pca':
			sc.tl.pca(adata, n_comps=n_comps)
			adata.obsm['spatial'] = adata.obsm['X_pca']  # 使用 PCA 坐标
		elif method == 'mca':
			out = run_mca(adata, nmcs=n_comps)
			adata.obsm['spatial'] = out[0]  # 使用 MCA 坐标
		elif method == 'mca_pca':
			out = run_mca(adata, nmcs=n_comps)
			pca = PCA(n_components=n_comps_1)
			adata.obsm['X_pca'] = pca.fit_transform(out[0])
			adata.obsm['spatial'] = adata.obsm['X_pca']  # 使用 MCA->PCA 坐标
		else:
			raise ValueError("Invalid method. Choose from 'pca', 'mca', 'nmf', or 'mca_pca'.")
	
	# 计算空间邻居关系
	sq.gr.spatial_neighbors(adata)
	
	# 恢复原始表达矩阵
	adata.X = adata.layers['raw']
	
	# 初始化并训练模型（stamp）
	if batch:
		model = sctm.stamp.STAMP(
				# adata[:, adata.var.highly_variable],
				adata,
				n_topics=n_topics,
				# categorical_covariate_keys=["batch"],
				categorical_covariate_keys=[batch],
				gene_likelihood="nb",
				dropout=0.1,
		)
	else:
		model = sctm.stamp.STAMP(
				# adata[:, adata.var.highly_variable],
				adata,
				n_topics=n_topics,
		)
	model.train(batch_size=4096, device=device)
	
	# 获取结果
	topic_prop = model.get_cell_by_topic()  # (n_cells, n_topics)
	beta = model.get_feature_by_topic()  # (n_hv_genes, n_topics)
	
	return topic_prop, beta

# # 使用方法
# if __name__ == '__main__':
# 	adata = sc.read_h5ad('../data/h5ad/GSE96583.h5ad')  # batch 列名为 "stim"
# 	adata.var_names_make_unique()
#
# 	sc.pp.filter_cells(adata, min_genes=50)
# 	sctm.pp.filter_genes(adata, min_cutoff=0.03, expression_cutoff_99q=1)
# 	# sc.pp.filter_cells(adata, min_genes=200)
# 	sc.pp.highly_variable_genes(adata, n_top_genes=3000, flavor="seurat_v3")
# 	adata = adata[:, adata.var.highly_variable]
# 	print(adata.shape)
#
# 	topic_prop, beta = scamp(adata, method='mca', batch="stim", device="cuda:0")
# 	print(topic_prop.shape, beta.shape)
# 	print(topic_prop[0:5])
# 	print(beta[0:5])
