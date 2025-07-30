import numpy as np
import pandas as pd
import scanpy as sc

from scipy.sparse import issparse
from scipy.sparse.linalg import svds
from scipy.sparse.linalg import ArpackNoConvergence


# 1. 生成模糊矩阵（Fuzzy Matrix）和行权重（Dc）
def mca_step1(X: np.ndarray) -> dict:
	"""
	功能：mca_step1: 对基因表达矩阵进行预处理，生成模糊矩阵（Fuzzy Matrix）和行权重（Dc）。
	
	参数:
		X: 基因表达矩阵 (genes x cells), numpy 数组或稀疏矩阵。
		
	返回:
		dict: 包含 Z(模糊矩阵)和 Dc(行权重)的字典。
	"""
	
	# 如果 X 是稀疏矩阵，则转换为稠密矩阵。
	if issparse(X):
		AM = X.toarray()
	else:
		AM = X  # if
	
	# 计算每行（基因）的最小值、最大值和范围
	rmin = np.min(AM, axis=1, keepdims=True)
	rmax = np.max(AM, axis=1, keepdims=True)
	range_vals = rmax - rmin
	
	# 归一化到 [0,1] 范围
	AM -= rmin
	# AM /= np.where(range_vals != 0, range_vals, 1.0)
	AM = np.divide(AM, np.where(range_vals != 0, range_vals, 1.0), dtype=np.float64)  # 避免除以零
	
	# 模糊矩阵由原始矩阵和其补集（1-AM）垂直堆叠而成，维度变为 2n_genes × n_cells
	FM = np.vstack([AM, 1 - AM])
	
	"""标准化"""
	# # 计算总和和行列和
	# total = np.sum(FM)
	# colsum = np.sum(FM, axis=0)
	# rowsum = np.sum(FM, axis=1)
	#
	# # 对模糊矩阵 FM 的每一列（代表一个细胞）进行标准化，消除细胞测序深度差异，避免某些细胞主导降维结果。
	# FM /= np.sqrt(colsum)
	# # 对模糊矩阵 FM 的每一行（代表一个基因或它的补集）进行标准化，消除基因表达量级差异，避免高表达基因主导结果。
	# FM /= np.sqrt(rowsum)[:, np.newaxis]
	#
	# # 计算行权重 (Dc)
	# Dc = 1 / np.sqrt(rowsum / total)
	# 替换原有的标准化操作为带保护的版本
	total = np.sum(FM)
	colsum = np.sum(FM, axis=0)
	rowsum = np.sum(FM, axis=1)
	
	colsum_safe = np.where(colsum == 0, 1.0, colsum)
	rowsum_safe = np.where(rowsum == 0, 1.0, rowsum)
	
	# 对模糊矩阵 FM 的每一列（代表一个细胞）进行标准化，消除细胞测序深度差异，避免某些细胞主导降维结果。
	FM /= np.sqrt(colsum_safe)
	# 对模糊矩阵 FM 的每一行（代表一个基因或它的补集）进行标准化，消除基因表达量级差异，避免高表达基因主导结果。
	FM /= np.sqrt(rowsum_safe)[:, np.newaxis]
	
	Dc = 1 / np.sqrt(rowsum_safe / total)
	
	# 以字典形式返回结果
	dict_Z_Dc = {
			"Z":  FM,  # 模糊矩阵：维度为 2n_genes x n_cells
			"Dc": Dc  # 行权重：维度为 2n_genes
	}
	
	return dict_Z_Dc


# 2. 计算细胞坐标和基因坐标
def mca_step2(
		Z: np.ndarray,
		V: np.ndarray,
		Dc: np.ndarray
) -> dict:
	"""
	功能：mca_step2：计算细胞坐标和基因坐标。
	
	参数:
		Z: 模糊矩阵 (from mca_step1, shape: 2n_genes x n_cells)
		V: SVD 的右奇异向量 (n_cells x components)
		Dc: 行权重 (from mca_step1, length: n_genes)
		
	返回:
		dict: 包含细胞坐标和基因坐标的字典
	"""
	
	AZ = Z  # 2n_genes x n_cells
	AV = V  # n_cells x components
	# 转化成列向量
	ADc = Dc.reshape(-1, 1)  # 2n_genes x 1
	
	# 计算基因坐标，AZ.shape = (2n_genes, n_cells), AV.shape = (n_cells, components)
	features_coordinates = AZ @ AV
	
	# features_coordinates.shape = (2n_genes, components)，ADc.shape = (2n_genes, 1)
	# numpy 会自动广播 ADc，将其扩展为 (2n_genes, components)
	features_coordinates *= ADc
	n_genes = features_coordinates.shape[0] // 2  # 恢复到 n_genes 维度
	features_coordinates = features_coordinates[:n_genes, :]
	
	# 计算细胞坐标
	AZcol = AZ.shape[1]  # 细胞数量
	cells_coordinates = np.sqrt(AZcol) * AV
	
	# 以字典形式返回结果
	dict_cells_features = {
			"cellsCoordinates":    cells_coordinates,  # 细胞坐标：维度为 n_cells x components
			"featuresCoordinates": features_coordinates  # 基因坐标：维度为 n_genes x components
	}
	return dict_cells_features


# 3. 运行 mca 算法，计算细胞坐标和基因坐标
def run_mca(
		adata: sc.AnnData,
		nmcs: int = 64,
		features: list | None = None,
		meta: bool = False,
) -> tuple[np.ndarray, np.ndarray, np.ndarray] | tuple[pd.DataFrame, pd.DataFrame, np.ndarray]:
	"""
	功能：run_mca: 整合 mca 分析流程，从 AnnData 对象中提取数据并返回降维结果。
	
	参数:
		adata: AnnData 对象，包含基因表达矩阵 X
		nmcs: 降维后的维度
		features: 需要分析的基因列表，如果为 None，则选择所有基因
		include_meta: 是否包含 meta 信息，如果为 True，则返回 DataFrame 形式的细胞坐标和基因载荷信息
		
	返回:
		tuple: 包含细胞坐标、基因载荷、标准差的元组，或者包含细胞坐标、基因载荷 DataFrame 以及标准差的元组
	"""
	print("run mca...")
	
	# 当 features 为 None 时，选择需要分析的基因
	if features is not None:
		adata = adata[:, adata.var_names & features]
	
	# 从 AnnData 对象中加载数据
	X = adata.X
	# 如果 X 是稀疏矩阵，则转换为密集矩阵
	if issparse(X):
		X = X.toarray()
	X = X.T  # 转置，使得 X.shape = (n_genes, n_cells)
	
	# mca step1
	print("mca step 1: Construct the Fuzzy Matrix and Row Weights")
	step1_result = mca_step1(X)
	print("mca step 1 completed: Fuzzy Matrix and Row Weights constructed")
	# 返回结果包含 Z(模糊矩阵 shape: 2n_genes x n_cells) 和 Dc(行权重 shape: 为 2n_genes)
	
	# svd
	print("svd started")
	num_components = nmcs + 1
	# u, s, vt = svds(step1_result["Z"], k=num_components, which='LM')
	try:
		u, s, vt = svds(step1_result["Z"], k=num_components, which='LM')
		# 检查结果是否有效
		if len(s) < num_components:
			raise ValueError(f"Only {len(s)} singular values converged, requested {num_components}")
	except ArpackNoConvergence as e:
		print(f"ARPACK did not converge: {e}")
		# 可以尝试使用截断的结果（如果有部分收敛）
		if hasattr(e, 'eigenvalues'):
			u, s, vt = e.eigenvectors, e.eigenvalues, e.eigenvectors.T
			print(f"Using partial results with {len(s)} components")
		else:
			raise  # 如果没有部分结果，重新抛出异常
	except ValueError as e:
		print(f"Value error in svds: {e}")
		raise
	except Exception as e:
		print(f"Unexpected error in svds: {e}")
		raise
	
	sort_indices = np.argsort(s)[::-1]  # 对奇异值（s）进行降序排序，并返回排序后的索引
	s_desc = s[sort_indices]  # len: num_components
	# u_desc = u[:, sort_indices]
	v_desc = vt.T[:, sort_indices]
	V = v_desc[:, 1:]  # shap: (2n_genes, nmcs)
	print("svd completed")
	
	# mca step2
	print("mca step 2: Calculate Cell Coordinates and Feature Loadings")
	step2_result = mca_step2(step1_result["Z"], V, step1_result["Dc"])
	cell_embedding = step2_result["cellsCoordinates"]  # cell_embedding.shape = (n_cells, nmcs)
	gene_loading = step2_result["featuresCoordinates"]  # gene_loading.shape = (n_genes, nmcs)
	stdev = s_desc[1:]  # stdev.shape = (nmcs,)
	print("mca step 2 completed: Cell Coordinates and Feature Loadings calculated")
	
	# 如果选择包含 meta 信息，则以 DataFrame 的形式返回结果，结果中包含细胞的信息
	if meta:
		df_embedding = pd.DataFrame(cell_embedding, index=adata.obs_names)
		# for i in df_embedding.columns:
		# 	adata.obs[f"MC_{i}"] = df_embedding[i]
		df_embedding.columns = [f"MC_{col}" for col in df_embedding.columns]
		
		df_loadings = pd.DataFrame(gene_loading, index=adata.var_names)
		df_loadings.index.name = "Gene"  # 添加索引名称
		df_loadings.columns = [f"MC_{col}" for col in df_loadings.columns]
		
		# return adata.obs, df_loadings, stdev
		return df_embedding, df_loadings, stdev
	
	return cell_embedding, gene_loading, stdev

# # 参数配置
# class Config:
# 	def __init__(self, path, nmcs, meta):
# 		self.path = path
# 		self.nmcs = nmcs
# 		self.meta = meta
#
#
# # 使用方法
# if __name__ == '__main__':
#
# 	# config 配置
# 	config = Config(
# 			path="../data/h5ad/GSE96583.h5ad",
# 			nmcs=16,
# 			meta=False
# 	)
#
# 	print("loading data...")
# 	adata = sc.read_h5ad(config.path)
# 	adata.var_names_make_unique()
#
# 	# 过滤掉低质量的基因和低表达的细胞
# 	print("filtering data...")
# 	sc.pp.filter_genes(adata, min_cells=3)
# 	sc.pp.filter_cells(adata, min_genes=200)
# 	sc.pp.highly_variable_genes(adata, n_top_genes=3000, flavor="cell_ranger")
# 	adata = adata[:, adata.var.highly_variable]
#
# 	# # 归一化
# 	# sc.pp.normalize_total(adata, target_sum=1e4)
# 	# sc.pp.log1p(adata)
#
# 	# 降维
# 	cell_embedding, gene_loading, stdev = run_mca(adata, config.nmcs, meta=config.meta)
# 	print()
#
# 	print("cell_embedding:", cell_embedding.shape)
# 	print("cell_embedding:", cell_embedding[0:5])
#
# 	print("gene_loading:", gene_loading.shape)
# 	print("gene_loading:", gene_loading[0:5])
#
# 	print("stdev:", stdev.shape)
# 	print("stdev:", stdev[0:5])
