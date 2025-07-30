import numpy as np
import pandas as pd
import scanpy as sc
import squidpy as sq
import sctm
import inspect

from anndata import AnnData
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from scipy.sparse import issparse
from combat.pycombat import pycombat
from FeaSc.util_mca import run_mca


# 批次感知标准化
def batch_aware_standardization(adata: AnnData, batch_col: str):
	"""
	批次感知的标准化：在每个批次内进行 Z-score 标准化
	:param adata: AnnData 对象
	:param batch_col: 批次信息列名
	"""
	
	# 创建副本避免修改原始数据
	adata_standardized = adata.copy()
	
	# 如果是稀疏矩阵，转换为密集矩阵进行标准化
	if issparse(adata.X):
		adata_standardized.X = adata.X.toarray()
	
	# 获取所有批次标签
	batches = adata_standardized.obs[batch_col].unique()
	
	# 对每个批次独立进行标准化
	for batch in batches:
		# 取出当前批次所有细胞的表达矩阵
		batch_idx = adata_standardized.obs[batch_col] == batch
		batch_data = adata_standardized[batch_idx, :].X
		
		# 批次内 Z-score 标准化
		scaler = StandardScaler()
		standardized_data = scaler.fit_transform(batch_data)
		
		# 处理可能的 NaN 值（清零）
		standardized_data = np.nan_to_num(standardized_data)
		
		# 更新数据
		adata_standardized[batch_idx, :].X = standardized_data
	
	return adata_standardized


# 批次感知 Harmony 校正
def apply_harmony(embedding: np.ndarray, batch_labels: np.ndarray):
	"""
	应用 Harmony 进行批次效应校正
	:param embedding: 原始嵌入矩阵，形状为 (n_cells, n_features)
	:param batch_labels: 批次标签，形状为 (n_cells,)
	:return: 校正后的嵌入矩阵
	"""
	
	# 全局中心（所有细胞均值）
	global_mean = np.mean(embedding, axis=0)
	
	# 校正每个批次
	corrected_embedding = np.zeros_like(embedding)  # 初始化校正后的嵌入矩阵
	for batch in np.unique(batch_labels):
		# 取出当前批次所有细胞
		batch_idx = batch_labels == batch
		batch_data = embedding[batch_idx]
		
		# 计算批次中心
		batch_mean = np.mean(batch_data, axis=0)
		
		# 校正：相对全局中心的偏移（减去批次中心，加上全局中心）
		corrected_embedding[batch_idx] = batch_data - batch_mean + global_mean
	
	return corrected_embedding


# 批次数据分割
def split_by_batch(adata: AnnData, batch_col: str = "batch"):
	"""
	按批次分裂 AnnData（保留元信息）
	:param adata: AnnData 对象
	:param batch_col: 批次信息列名
	:return: 字典，键为批次名，值为对应批次的 AnnData 对象
	"""
	
	# 判定批次列是否存在
	if batch_col not in adata.obs.columns:
		raise ValueError(
				f"line: {inspect.currentframe().f_lineno} split_by_batch; adata.obs 中不存在批次列 '{batch_col}'")
	
	batch_dict = {}
	# 按批次分组并创建子 AnnData
	for batch_name, indices in adata.obs.groupby(batch_col, observed=True).groups.items():
		batch_adata = adata[indices, :].copy()
		batch_dict[batch_name] = batch_adata
	
	return batch_dict


# 基于 PCA 降维
def compute_pca(adata: AnnData, k: int = 20):
	"""
	计算带基因名/细胞名的 PCA 结果
	:param adata: AnnData 对象
	:param k: 降维后的维度
	:return: 细胞数 × k 的 DataFrame，基因数 × k 的 DataFrame
	"""
	
	# 计算 PCA
	pca = PCA(n_components=k)
	
	# 处理稀疏矩阵
	if issparse(adata.X):
		data = adata.X.toarray()
	else:
		data = adata.X
	
	embedding = pca.fit_transform(data)  # 细胞数 × k
	loading = pca.components_.T  # 基因数 × k
	
	embedding_df = pd.DataFrame(
			embedding,
			index=adata.obs_names,
			columns=[f"PC{i + 1}" for i in range(k)]
	)
	loading_df = pd.DataFrame(
			loading,
			index=adata.var_names,
			columns=[f"PC{i + 1}" for i in range(k)]
	)
	
	return embedding_df, loading_df


# 基于 stamp 的降维
def run_scamp(adata: sc.AnnData,
              method: str = 'pca',
              n_topics: int = 20,
              n_comps_0: int = 50,
              n_comps_1: int = 40,
              batch: str = None,
              flag: bool = False,
              device: str = "cpu"):
	"""
	功能：使用 SCAMP 算法进行细胞降维，并使用 STAMP 算法进行主题建模。
	:param adata: anndata 对象
	:param method: 降维方法，可选 'pca', 'nmf','mca','mca_pca'
	:param n_comps_0: 第一次降维 （pca, nmf, mca) 后的维数
	:param n_comps_1: 第二次降维后的维数 （如果 method='mca_pca'）
	:param n_topics: stamp 后的主题数
	:param batch: 如果有分批次数据，则指定 batch 列名
	:param flag: 是否分批次降维
	:param device: 选择运行设备，'cpu' 或 'cuda:0'
	:return: topic_prop：每个细胞的主题分布，(n_cells, n_topics)，beta：每个特征的主题分布，(n_hv_genes, n_topics)
	"""
	
	# 预处理前备份
	adata.layers['raw'] = adata.X.copy()
	
	# 第一层降维（mca, pca, mca_pca）
	if flag:
		batch_list = list(adata.obs[batch].unique())
		adata_batch_list = [adata[adata.obs[batch] == b] for b in batch_list]
		if method == 'pca':
			# 分别对每个 batch 进行 pca 降维
			for adata_batch in adata_batch_list:
				sc.pp.pca(adata_batch, n_comps=n_comps_0)
			adata = adata_batch_list[0].concatenate(adata_batch_list[1:], batch_key="batch_list", index_unique=None)
			adata.obsm['spatial'] = adata.obsm['X_pca']  # 使用 PCA 坐标
		elif method == 'mca':
			# 分别对每个 batch 进行 mca 降维
			for adata_batch in adata_batch_list:
				# print(adata_batch.shape)
				# print(adata_batch.X)
				out = run_mca(adata_batch, nmcs=n_comps_0)
				adata_batch.obsm['X_mca'] = out[0]
			adata = adata_batch_list[0].concatenate(adata_batch_list[1:], batch_key="batch_list", index_unique=None)
			adata.obsm['spatial'] = adata.obsm['X_mca']  # 使用 MCA 坐标
		elif method == 'mca_pca':
			# 分别对每个 batch 进行 mca 降维
			for adata_batch in adata_batch_list:
				out = run_mca(adata_batch, nmcs=n_comps_0)
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
		if method == 'mca':
			out = run_mca(adata, nmcs=n_comps_0)
			adata.obsm['spatial'] = out[0]  # 使用 MCA 坐标
		elif method == 'pca':
			sc.tl.pca(adata, n_comps=n_comps_0)
			adata.obsm['spatial'] = adata.obsm['X_pca']  # 使用 PCA 坐标
		elif method == 'mca_pca':
			out = run_mca(adata, nmcs=n_comps_0)
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
				adata,
				n_topics=n_topics,
		)
	model.train(batch_size=4096, device=device)
	
	# 获取结果
	topic_prop = model.get_cell_by_topic()  # (n_cells, n_topics)
	beta = model.get_feature_by_topic()  # (n_hv_genes, n_topics)
	
	return topic_prop, beta


# 获取批次间的共同基因
def get_common_genes(batch_loading_dict: dict):
	"""
	计算所有批次的共同基因
	:param batch_loading_dict: 字典，键为批次名，值为对应批次的 loading DataFrame
	:return: 共同基因列表
	"""
	
	all_gene_sets = [set(loading_df.index) for loading_df in batch_loading_dict.values()]
	return sorted(set.intersection(*all_gene_sets))


# 合并所有批次的共同基因 loading
def merge_batch_loadings(batch_loading_dict: dict, common_genes: list, k: int):
	"""
	合并所有批次的共同基因 loading
	:param batch_loading_dict: 字典，键为批次名，值为对应批次的 loading DataFrame
	:param common_genes: 共同基因列表
	:param k: 降维后的维度
	:return: 合并后的 loading DataFrame
	"""
	
	merged_list = []
	for batch_name, loading_df in batch_loading_dict.items():
		# 提取当前批次的共同基因 loading
		batch_loading_common = loading_df.loc[common_genes, :]
		# 重命名列，添加批次前缀
		batch_loading_common.columns = [f"{batch_name}_PC{i + 1}" for i in range(k)]
		merged_list.append(batch_loading_common)
	
	return pd.concat(merged_list, axis=1)


# 生成 mf_loading 矩阵
def generate_mf_loading(merge_loading: pd.DataFrame, C: int):
	"""
	生成 C 维的综合 loading 矩阵
	:param merge_loading: 合并后的 loading DataFrame
	:param C: 目标维度
	:return: C 维的综合 loading 矩阵
	"""
	
	# 聚类
	kmeans = KMeans(n_clusters=C, random_state=42)
	cluster_labels = kmeans.fit_predict(merge_loading.T)
	
	# 重组矩阵使同类成分相邻
	sorted_indices = np.argsort(cluster_labels)
	cluster_merge_loading = merge_loading.iloc[:, sorted_indices]
	
	# 创建新的列名反映聚类信息
	new_columns = [f"Cluster{cluster_labels[i]}_PC{col.split('_PC')[1]}"
	               for i, col in enumerate(cluster_merge_loading.columns)]
	cluster_merge_loading.columns = new_columns
	
	mf_loading = pd.DataFrame(
			np.zeros((len(merge_loading.index), C)),
			index=merge_loading.index,
			columns=[f"Cluster_{c}" for c in range(C)]
	)
	
	for c in range(C):
		# 获取当前聚类的所有列
		cluster_cols = [col for col in cluster_merge_loading.columns if f"Cluster{c}_" in col]
		
		if not cluster_cols:
			continue
		
		cluster_block = cluster_merge_loading.loc[:, cluster_cols]
		
		if len(cluster_cols) > 1:
			# 对聚类内的成分进行PCA降维
			pca_block = PCA(n_components=1)
			pca_block.fit(cluster_block.T)
			mf = pca_block.components_[0]
		else:
			# 如果只有一个成分，直接使用
			mf = cluster_block.values.flatten()
		
		mf_loading[f"Cluster_{c}"] = mf
	
	return mf_loading


# 对齐嵌入空间
def align_embeddings(embedding_df: pd.DataFrame,
                     loading_df: pd.DataFrame,
                     common_genes: list,
                     mf_loading: pd.DataFrame):
	"""
	将 embedding 投影到 C 维空间
	:param embedding_df: 原始 embedding DataFrame
	:param loading_df: 原始 loading DataFrame
	:param common_genes: 共同基因列表
	:param mf_loading: C 维的综合 loading 矩阵
	:return: 对齐后的 embedding DataFrame
	"""
	
	# 提取共同基因的 loading
	aligned_loading = loading_df.loc[common_genes, :]
	
	# mf_loading = 原始 loading × projection
	# projection = (原始 loading⁺ × mf_loading)
	# ⁺表示伪逆（Moore-Penrose pseudoinverse）
	# projected_embedding = 原始 embedding × projection
	projection = np.linalg.pinv(aligned_loading.values) @ mf_loading.values
	projected_embedding = embedding_df.values @ projection
	
	return pd.DataFrame(
			projected_embedding,
			index=embedding_df.index,
			columns=mf_loading.columns
	)


# 应用 ComBat 进行批次效应校正
def apply_combat_correction(feature_matrix: pd.DataFrame, batch_info: pd.Series):
	"""
	应用 ComBat 进行批次效应校正
	:param feature_matrix: 特征矩阵，每行是一个细胞，每列是一个特征
	:param batch_info: 批次信息，每行对应于 feature_matrix 的行，每列是一个批次
	:return: 校正后的特征矩阵
	"""
	
	# 确保批次信息与特征矩阵的行顺序一致
	batch_info = batch_info.loc[feature_matrix.index]
	
	# 转换数据格式为 ComBat 所需形式
	data_df = feature_matrix.T  # ComBat 需要特征 × 样本的格式
	corrected_data = pycombat(data_df, batch_info.values)
	
	# 转置回原始格式
	corrected_feature_matrix = corrected_data.T
	
	return pd.DataFrame(corrected_feature_matrix,
	                    index=feature_matrix.index,
	                    columns=feature_matrix.columns)


def harmony(adata: AnnData,
            n_comps=25,
            batch_col: str = "batch",
            method: str = 'pca',
            apply_combat: bool = True):
	"""
	主流程函数：返回 mf_embedding 和 mf_loading，包含批次效应去除
	:param adata: AnnData 对象
	:param n_comps: 降维后的维度
	:param batch_col: 批次信息列名
	:param method: 降维方法，可选 'pca', 'mca','scamp'
	:param apply_combat: 是否应用 ComBat 进行批次效应校正
	:return: mf_embedding 和 mf_loading
	"""
	
	# 步骤 0: 批次感知标准化 (pca)
	if method == 'pca':
		sc.pp.normalize_total(adata, target_sum=1e4)
		sc.pp.log1p(adata)
		adata_std = batch_aware_standardization(adata, batch_col)
	elif method == 'scamp' or method == 'mca':
		adata_std = adata.copy()
	else:
		raise ValueError(f"line {inspect.currentframe().f_lineno}: harmony; Invalid method.")
	
	# 步骤 1: 按批次分裂数据
	batch_dict = split_by_batch(adata_std, batch_col)
	
	# 步骤 2: 批次级分解（返回各批次的 embedding 和 loading）
	batch_embedding, batch_loading = {}, {}
	for batch_name, batch_adata in batch_dict.items():
		if method == 'pca':
			embedding_df, loading_df = compute_pca(batch_adata, k=n_comps)
		elif method == 'mca':
			embedding_df, loading_df, _ = run_mca(batch_adata, nmcs=n_comps, meta=True)
		elif method == 'scamp':
			embedding_df, loading_df = run_scamp(batch_adata, n_topics=n_comps, device="cuda:0")
		else:
			raise ValueError(f" line {inspect.currentframe().f_lineno}: big_harmony; Invalid method.")
		batch_embedding[batch_name] = embedding_df
		batch_loading[batch_name] = loading_df
	
	# 步骤 3: 计算共同基因
	common_genes = get_common_genes(batch_loading)
	if not common_genes:
		raise ValueError(f"line {inspect.currentframe().f_lineno}: harmony; 各批次无共同基因，无法继续分析！")
	
	# 步骤 4: 合并批次 loading
	merge_loading = merge_batch_loadings(batch_loading, common_genes, n_comps)
	
	# 步骤 5: 生成 mf_loading 矩阵
	mf_loading = generate_mf_loading(merge_loading, n_comps)
	
	# 步骤 6: 对齐各批次特征
	aligned_features_dict = {}
	for batch_name, embedding_df in batch_embedding.items():
		aligned_features = align_embeddings(
				embedding_df,
				batch_loading[batch_name],
				common_genes,
				mf_loading
		)
		aligned_features_dict[batch_name] = aligned_features
	# 合并所有批次的嵌入
	mf_embedding = pd.concat(aligned_features_dict.values(), axis=0)
	
	# 步骤 7: ComBat 校正
	if apply_combat:
		batch_info = adata.obs[batch_col]
		mf_embedding = apply_combat_correction(mf_embedding, batch_info)
	
	return mf_embedding, mf_loading


if __name__ == '__main__':
	path_gse = "../data/h5ad/GSE96583.h5ad"
	# 读取数据
	adata = sc.read_h5ad(path_gse)
	adata.var_names_make_unique()
	
	sc.pp.filter_cells(adata, min_genes=50)
	sctm.pp.filter_genes(adata, min_cutoff=0.03, expression_cutoff_99q=1)
	sc.pp.highly_variable_genes(adata, n_top_genes=3000, flavor="seurat_v3")
	adata = adata[:, adata.var.highly_variable]
	
	# 运行主流程，获取所有结果
	mf_embedding, mf_loading = harmony(adata, batch_col="stim", method="pca")
	# 用于下游分析
	adata.obsm["X_integrated"] = mf_embedding
	
	# 可视化
	sc.pp.neighbors(adata, use_rep="X_integrated")
	sc.tl.umap(adata)
	sc.pl.umap(adata, color=["stim", "cell"])
