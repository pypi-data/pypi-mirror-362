import os
import pandas as pd
import numpy as np
import scanpy as sc
import matplotlib.pyplot as plt
import seaborn as sns

from typing import Literal
from scipy.sparse import issparse
from sklearn.decomposition import NMF
from sklearn.preprocessing import StandardScaler
from statsmodels.api import OLS
from statsmodels.stats.multitest import multipletests

from FeaSc.util_mca import run_mca


# 1. 计算基因频率
# 读取 GMT 文件
def read_gmt(filepath: str) -> dict[str, set[str]]:
	"""
	读取 GMT 文件
	:param filepath: GMT 文件路径
	:return: 基因集字典
	"""
	gene_sets = {}
	with open(filepath, 'r') as f:
		for line in f:
			parts = line.strip().split('\t')
			if len(parts) >= 3:
				pathway_name = parts[0]
				# 跳过description（parts[1]），从第3列开始是基因
				genes = set(parts[2:])
				if pathway_name not in gene_sets:  # 去重
					gene_sets[pathway_name] = genes
	return gene_sets


# 计算基因频率
def get_gene_rate(
		background_geneset: str | dict[str, set[str]] | None = None,
		signature_geneset: dict[str, set[str]] | list[set[str]] | None = None,
		mode: str = "single"
) -> pd.DataFrame:
	"""
	计算基因频率。

	参数:
		background_geneset: 背景基因集，可以是GMT文件路径或dict
		signature_geneset: 特征基因集，可以是dict或list
		mode: "single" - 对每个signature分别计算
			  "multiple" - 合并多个signature计算整体比例

	返回:
		基因频率DataFrame
	"""
	if mode not in ("single", "multiple"):
		raise ValueError("get_gene_rate: mode must be 'single' or 'multiple'")
	
	# 读取背景基因集
	bg_sets = _load_background_geneset(background_geneset)
	
	# 处理signature基因集
	sig_sets = _process_signature_geneset(signature_geneset)
	
	# 获取所有唯一基因（使用集合操作优化）
	all_genes_set = set()
	for genes in bg_sets.values():
		all_genes_set.update(genes)
	for genes in sig_sets.values():
		all_genes_set.update(genes)
	
	all_genes = sorted(all_genes_set)
	n_genes = len(all_genes)
	gene_to_idx = {gene: idx for idx, gene in enumerate(all_genes)}
	
	# 使用numpy数组构建矩阵（比DataFrame构建更快）
	bg_matrix = _build_matrix_numpy(bg_sets, all_genes, gene_to_idx, n_genes)
	sig_matrix = _build_matrix_numpy(sig_sets, all_genes, gene_to_idx, n_genes)
	
	# 计算背景频率
	background_col = bg_matrix.mean(axis=1)
	
	# 构建结果DataFrame
	if mode == "single":
		result_data = {"background": background_col}
		for i, name in enumerate(sig_sets.keys()):
			result_data[name] = sig_matrix[:, i]
		result = pd.DataFrame(result_data, index=all_genes)
	else:  # mode == "multiple"
		sig_avg = sig_matrix.mean(axis=1)
		result = pd.DataFrame({
				"background": background_col,
				"signature":  sig_avg
		}, index=all_genes)
	
	return result


def _load_background_geneset(
		background_geneset: str | dict[str, set[str]] | None
) -> dict[str, set[str]]:
	"""加载背景基因集"""
	if isinstance(background_geneset, dict):
		# 确保值是集合类型
		return {k: set(v) if not isinstance(v, set) else v
		        for k, v in background_geneset.items()}
	elif isinstance(background_geneset, str):
		if not os.path.exists(background_geneset):
			raise FileNotFoundError(f"_load_background_geneset: Cannot find file: {background_geneset}")
		return read_gmt(background_geneset)
	else:
		return {}


def _process_signature_geneset(
		signature_geneset: dict[str, set[str]] | list[set[str]] | None
) -> dict[str, set[str]]:
	"""处理signature基因集"""
	if isinstance(signature_geneset, list):
		return {f"signature{i + 1}": set(s) if not isinstance(s, set) else s
		        for i, s in enumerate(signature_geneset)}
	elif isinstance(signature_geneset, dict):
		return {k: set(v) if not isinstance(v, set) else v
		        for k, v in signature_geneset.items()}
	elif signature_geneset is None:
		return {}
	else:
		return {"signature1": set(signature_geneset)}


def _build_matrix_numpy(
		gene_sets: dict[str, set[str]],
		all_genes: list[str],
		gene_to_idx: dict[str, int],
		n_genes: int
) -> np.ndarray:
	"""使用numpy构建基因矩阵（更高效）"""
	n_sets = len(gene_sets)
	matrix = np.zeros((n_genes, n_sets), dtype=np.float32)
	
	for col_idx, genes in enumerate(gene_sets.values()):
		# 批量设置基因存在的位置为1
		indices = [gene_to_idx[g] for g in genes if g in gene_to_idx]
		if indices:
			matrix[indices, col_idx] = 1
	
	return matrix


# 2. 降维与重构
# 降维
def rebuild_matrix(adata: sc.AnnData,
                   features: list[str] | None = None,
                   method: str | list[str] = 'mca',
                   n_dim: int = 16):
	"""
	使用指定的降维方法（PCA、MCA、NMF）对 AnnData 对象进行降维重建。

	参数说明：
		adata        : AnnData 对象（scanpy的主数据结构）
		features     : 基因名列表（可选，仅选择这些基因）
		assay_layer  : 用于分析的层（默认为 "X"）
		method       : 降维方法列表，如 ["pca", "mca", "nmf"]
		n_dim          : 降维后保留的维数（与 avc 互斥）

	返回值：
		修改后的 AnnData 对象，降维结果存储在 obsm，元数据存储在 uns 中。
	"""
	
	# 筛选特定特征（基因）
	if features is not None:
		adata = adata[:, features]
	data = adata.X.copy()
	
	# 数据预处理：标准化并 log 转换
	sc.pp.normalize_total(adata)
	sc.pp.log1p(adata)
	
	# 初始化元数据
	adata.uns['active_method'] = []
	adata.uns['active_dim'] = n_dim
	
	for m in method:
		if m == "pca":
			# 标准化消除基因间表达量尺度的差异：不同基因的表达值可能有不同的量纲。
			adata_scale = adata.copy()
			sc.pp.scale(adata_scale)
			# 运行 PCA
			sc.tl.pca(adata_scale, n_comps=n_dim)
			# 将结果复制回原对象
			adata.obsm['pca'] = adata_scale.obsm['X_pca']
			adata.varm['pca'] = adata_scale.varm['PCs']
			adata.uns['pca'] = adata_scale.uns['pca']
		
		elif m == "mca":
			out = run_mca(adata, n_dim)
			adata.obsm['mca'] = out[0]
			adata.varm['mca'] = out[1]
			adata.uns['mca'] = {
					'stdev':  out[2],
					'params': {'n_components': n_dim}
			}
		
		elif m == "nmf":
			# 确保数据为非负
			if issparse(data):
				data_nmf = np.abs(data.toarray())
			else:
				data_nmf = np.abs(data)
			
			# 运行 nmf
			nmf_model = NMF(n_components=n_dim, tol=1e-5, max_iter=500)
			W = nmf_model.fit_transform(data_nmf)  # 细胞嵌入
			H = nmf_model.components_  # 基因载荷
			
			# 计算重构误差
			X_hat = W @ H
			s = np.linalg.svd(X_hat, compute_uv=False, full_matrices=False)
			stdev = s[0:n_dim]
			
			# 存储结果
			adata.obsm['nmf'] = W
			adata.varm['nmf'] = H.T
			adata.uns['nmf'] = {
					'stdev':  stdev,
					'params': {'n_components': n_dim}
			}
		
		else:
			raise ValueError(f"rebuild_matrix: 未识别的方法: {m}")
		
		# 记录使用过的方法
		adata.uns['active_method'].append(m)
	
	return adata


# 重构
def _get_rebuild_matrix(adata: sc.AnnData) -> pd.DataFrame:
	# 获取使用的降维方法
	active_method = adata.uns.get('active_method', None)
	
	if active_method is None:
		# 未使用降维方法时返回原始数据
		return pd.DataFrame(adata.X.T, index=adata.var_names, columns=adata.obs_names)
	
	# 获取降维参数
	dim = adata.uns.get('active_dim', None)
	
	# 获取特征 loadings 和细胞 embeddings
	loadings = pd.DataFrame(adata.varm[active_method[0]], index=adata.var_names)
	embeddings = pd.DataFrame(adata.obsm[active_method[0]], index=adata.obs_names)
	
	if dim is not None:
		topk = dim
	else:
		topk = 50
	
	# 重建矩阵（基因 x 细胞）
	reduced_expr = np.dot(loadings.iloc[:, :topk], embeddings.iloc[:, :topk].T)
	rebuild_gem = pd.DataFrame(reduced_expr, index=loadings.index, columns=embeddings.index)
	
	# 对称 log 变换
	rebuild_gem = np.log1p(np.abs(rebuild_gem)) * np.sign(rebuild_gem)
	
	# 每个基因中心化
	rebuild_gem = rebuild_gem.sub(rebuild_gem.mean(axis=1), axis=0)
	
	return rebuild_gem


# 3. 岭回归
def _ridge_regression(
		X: np.ndarray | pd.DataFrame,
		Y: np.ndarray | pd.Series,
		scale: bool = True,
		lambd: float = 0.0,
		num_permutations: int | None = None,
		test_method: Literal["two-sided", "greater", "less"] = "two-sided"
) -> np.ndarray:
	"""
	等价于R中的 ridgeRegression 函数
	X: gene x signature
	Y: gene x cell
	返回: signature x cell 矩阵（t值矩阵 或 permutation z-score）
	"""
	
	X = np.asarray(X)
	Y = np.asarray(Y)
	# 是否标准化
	if scale:
		X = StandardScaler().fit_transform(X)
		if Y.ndim == 1:
			Y = Y.reshape(-1, 1)
		Y = StandardScaler().fit_transform(Y)
	
	# tmp1 = X.T @ X
	XtX = X.T @ X
	try:
		tmp2 = np.linalg.inv(XtX + lambd * np.eye(X.shape[1])) @ X.T
	except np.linalg.LinAlgError:
		raise ValueError("_ridge_regression: X.T @ X 不可逆，无法进行回归")
	# β = (X^T X + λI)^(-1) X^T Y
	beta = tmp2 @ Y  # shape: [num_features, num_cells]
	
	if not num_permutations or num_permutations <= 0:
		# 计算残差
		residuals = Y - X @ beta
		dof = Y.shape[0] - X.shape[1] + 1  # 自由度
		# 残差方差（每列计算）
		sigma_squared = np.sum(residuals ** 2, axis=0) / dof  # shape: [num_cells]
		
		# 计算标准误差
		XtX_inv = np.linalg.inv(X.T @ X)
		se_beta = np.sqrt(np.outer(np.diag(XtX_inv), sigma_squared))  # shape: [num_features, num_cells]
		
		# t值
		t_values = beta / se_beta
		result = t_values.T  # 返回 shape: [num_cells, num_features]
	else:
		step = max(1, num_permutations // 10)
		beta_shape = beta.shape
		avg_matrix = np.zeros(beta_shape)
		avg_sq_matrix = np.zeros(beta_shape)
		pval_matrix = np.zeros(beta_shape)
		
		for i in range(1, num_permutations + 1):
			if i % step == 0:
				print(f"Process {int(100 * i / num_permutations)}%")
			
			Y_rand = Y[np.random.permutation(Y.shape[0]), :]
			beta_rand = tmp2 @ Y_rand
			
			if test_method == "two-sided":
				pval_matrix += (np.abs(beta) >= np.abs(beta_rand))
			elif test_method == "greater":
				pval_matrix += (beta >= beta_rand)
			elif test_method == "less":
				pval_matrix += (beta <= beta_rand)
			else:
				raise ValueError("test_method 应为 'two-sided', 'greater', 或 'less'")
			
			avg_matrix += beta_rand
			avg_sq_matrix += beta_rand ** 2
		
		avg_matrix /= num_permutations
		avg_sq_matrix /= num_permutations
		pval_matrix /= num_permutations
		
		std_matrix = np.sqrt(avg_sq_matrix - avg_matrix ** 2)
		zscore_matrix = (beta - avg_matrix) / std_matrix
		zscore_matrix[np.isnan(zscore_matrix)] = 0
		result = zscore_matrix.T  # shape: [num_cells, num_features]
	
	return result


# 4. 计算 细胞-基因集 响应评分
def compute_response(adata: sc.AnnData,
                     gene_rate: pd.DataFrame | None = None,
                     celltype: list[str] | str | None = None,
                     signature: str | None = None,
                     obs_celltype: str = "celltype"):
	"""
	计算指定细胞类型中每个细胞对某个特征基因集的响应评分（response score）

	参数:
		adata (anndata.AnnData): 包含重建后表达矩阵的 AnnData 对象
		gene_rate (pd.DataFrame): 基因在背景和特征集合中的出现率矩阵，由 get_gene_rate() 生成
		celltype (str or None): 要计算响应评分的细胞类型（如 "CD8T"），若为 None 则使用所有细胞
		signature (str or None): 特征名称（如 "Tcell_activation"）

	返回:
		pd.DataFrame: 每个细胞对应的响应评分，行名为细胞名，列名为 signature
	"""
	
	if gene_rate is None:
		raise ValueError("Please input the gene_rate args")
	
	# Step 1: 筛选目标细胞
	if celltype is None:
		use_cell = adata.obs_names
	else:
		if obs_celltype not in adata.obs.columns:
			raise KeyError("compute_response:Column 'celltype' not found in adata.obs")
		if celltype not in adata.obs[obs_celltype].unique():
			raise ValueError(f"compute_response: Celltype '{celltype}' not exist in adata.obs['celltype']")
		use_cell = adata.obs_names[adata.obs[obs_celltype] == celltype]
	
	# Step 2: 获取重建后的表达矩阵
	rebuild_gem = _get_rebuild_matrix(adata)
	
	# Step 3: 筛选共有的基因
	use_gene = list(set(gene_rate.index) & set(rebuild_gem.index))
	if not use_gene:
		raise ValueError("No overlapping genes between gene_rate and rebuild matrix")
	
	# 提取子矩阵
	use_expr = rebuild_gem.loc[use_gene, use_cell]
	use_gene_rate = gene_rate.loc[use_gene, :]
	
	# Step 4: 构建回归数据
	X = use_gene_rate.values.astype(float)
	Y = use_expr.values.astype(float)
	
	# Step 5: 执行 Ridge 回归（无正则、无置换检验）
	response = _ridge_regression(X, Y, scale=True, lambd=0.0)
	
	# Step 6: 整理结果
	response_df = pd.DataFrame(response[:, 1], index=use_cell, columns=[signature])
	
	return response_df


# 5. 计算 细胞-细胞因子 信号活性
def compute_signaling(adata: sc.AnnData,
                      model_file: str | None = None,
                      celltype: list[str] | str | None = None,
                      cytokine: list[str] | str | None = None,
                      lambd: float = 10000,
                      num_permutations: int = 1000,
                      test_method: Literal["two-sided", "greater", "less"] = "two-sided"):
	"""
	计算指定细胞类型的细胞对指定细胞因子的信号活性
	"""
	
	if model_file is None:
		raise ValueError("Please input the model_file argument")
	
	if not os.path.exists(model_file):
		raise FileNotFoundError(f"Cannot find file: {model_file}")
	
	# Step 1: 读取模型数据
	model_data = pd.read_csv(model_file, sep='\t', index_col=0)
	
	# Step 2: 检查并筛选有效的细胞因子
	if cytokine is not None:
		valid_cytokines = [c for c in cytokine if c in model_data.columns]
		invalid_cytokines = list(set(cytokine) - set(valid_cytokines))
		if len(invalid_cytokines) > 0:
			print(f"The following cytokines not exist in model file: {invalid_cytokines}")
		use_cytokine = valid_cytokines
		if not use_cytokine:
			raise ValueError("No valid cytokines found in model file")
		model_data = model_data[use_cytokine]
	else:
		use_cytokine = model_data.columns.tolist()
	
	# Step 3: 检查并筛选目标细胞
	if celltype is None:
		use_cell = adata.obs_names
	else:
		if not isinstance(celltype, list):
			celltype = [celltype]
		valid_celltype = [ct for ct in celltype if ct in adata.obs['celltype'].unique()]
		invalid_celltype = list(set(celltype) - set(valid_celltype))
		if len(invalid_celltype) > 0:
			print(f"The following celltypes not exist in adata: {invalid_celltype}")
		use_celltype = valid_celltype
		if not use_celltype:
			raise ValueError("No valid celltypes found in adata")
		use_cell = adata.obs_names[adata.obs['celltype'].isin(use_celltype)]
	
	# Step 4: 获取重建后的表达矩阵
	rebuild_gem = _get_rebuild_matrix(adata)
	
	# Step 5: 筛选共有的基因
	use_gene = list(set(model_data.index) & set(rebuild_gem.index))
	if not use_gene:
		raise ValueError("No overlapping genes between model_data and rebuild matrix")
	
	use_expr = rebuild_gem.loc[use_gene, use_cell]
	use_model_data = model_data.loc[use_gene, :]
	
	# Step 6: 构建回归数据
	X = use_model_data.values.astype(float)
	Y = use_expr.values.astype(float)
	
	# Step 7: 执行 Ridge 回归
	signaling = _ridge_regression(
			X, Y,
			scale=True,
			lambd=lambd,
			num_permutations=num_permutations,
			test_method=test_method
	)
	signaling_df = pd.DataFrame(signaling, index=use_cell, columns=use_cytokine)
	signaling_df.index.name = 'barcode'
	
	return signaling_df


# 6. 计算相互作用和 Tres 分数
def do_interaction(adata: sc.AnnData,
                   response_data: pd.DataFrame = None,
                   signaling_data: pd.DataFrame = None,
                   signature: list[str] = None,
                   cytokine: list[str] = None,
                   threshold: int = 100):
	"""
	分析基因表达与细胞因子信号传导之间的交互作用

	参数:
	object: 包含单细胞数据的对象(需有meta.data和RNA.data属性)
	response_data: 响应数据(DataFrame, 行=细胞, 列=特征)
	signaling_data: 信号数据(DataFrame, 行=细胞, 列=细胞因子)
	signature: 要分析的特征列表
	cytokine: 要分析的细胞因子列表
	threshold: 最小细胞数阈值

	返回:
	DataFrame包含交互作用分析结果
	"""
	
	# 1. 输入验证
	if not set(response_data.index) == set(signaling_data.index):
		raise ValueError("Cell names of response_data and signaling_data are not consistent.")
	cell_names = list(set(response_data.index) & set(adata.obs_names))
	
	# signature 参数检查
	if signature is None:
		raise ValueError("Please input the signature args.")
	else:
		valid_signature = [s for s in signature if s in response_data.columns]
		if not valid_signature:
			raise ValueError("signature not exist in response_data.")
		if len(valid_signature) < len(signature):
			invalid = set(signature) - set(valid_signature)
	
	# cytokine 参数检查
	if cytokine is None:
		raise ValueError("Please input the cytokine args.")
	else:
		valid_cytokine = [c for c in cytokine if c in signaling_data.columns]
		if not valid_cytokine:
			raise ValueError("cytokine not exist in signaling_data.")
		if len(valid_cytokine) < len(cytokine):
			invalid = set(cytokine) - set(valid_cytokine)
			print(f"The following cytokine not exist in signaling.data: {invalid}")
	
	# 2. 初始化结果存储
	results = []
	rebuild_gem = _get_rebuild_matrix(adata)
	
	# 获取样本信息
	sample_names = adata.obs.loc[response_data.index, 'Sample']
	
	# 3. 按样本分析
	for use_sample in sample_names.unique():
		sample_cells = sample_names[sample_names == use_sample].index
		n_cell = len(sample_cells)
		
		if n_cell < threshold:
			print(f"Cell count of sample {use_sample} less than threshold, continue...")
			continue
		
		for use_signature in valid_signature:
			for use_cytokine in valid_cytokine:
				# 准备数据
				response_subset = response_data.loc[sample_cells, use_signature].values
				signaling_subset = signaling_data.loc[sample_cells, use_cytokine].values
				
				# 对每个基因进行回归
				for gene in rebuild_gem.index:
					expr = rebuild_gem.loc[gene, sample_cells].values
					
					# 构建交互项
					interaction = signaling_subset * expr
					
					# 构建设计矩阵
					X = np.column_stack([
							np.ones_like(signaling_subset),  # 截距
							signaling_subset,  # 信号
							expr,  # 基因表达
							interaction  # 交互项
					])
					
					# 拟合线性模型
					try:
						model = OLS(response_subset, X).fit()
						t_value = model.tvalues[3]  # 交互项 t 值
						p_value = model.pvalues[3]  # 交互项 p 值
					except:
						t_value = np.nan
						p_value = np.nan
					
					results.append({
							'sample':    use_sample,
							'signature': use_signature,
							'cytokine':  use_cytokine,
							'gene':      gene,
							't':         t_value,
							'pvalue':    p_value
					})
		
		print(f"Process sample: {use_sample} end.")
	
	# 转换为 DataFrame
	interaction_df = pd.DataFrame(results)
	pvalues = interaction_df['pvalue']
	qvalues = multipletests(pvalues, method='fdr_bh')[1]
	interaction_df['qvalue'] = qvalues
	# interaction_df = interaction_df.dropna()
	
	return interaction_df


def get_tres_signature(
		interaction_dataset: pd.DataFrame,
		signature_cytokine: list[str] = None,
		qvalue: float = 0.05,
		cutoff: float = 0.5,
		method: str = "median"
) -> pd.DataFrame:
	"""
	从交互作用分析结果中提取Tres特征基因

	参数:
	interaction_dataset: 交互作用分析结果(DataFrame、DataFrame列表或文件路径)
	signature_cytokine: 用于构建特征的细胞因子列表
	qvalue: q值阈值(默认0.05)
	cutoff: 样本比例阈值(默认0.5)
	method: 汇总方法("median"或"mean", 默认median)

	返回:
	包含基因和Tres得分的数据框
	"""
	# 1. 输入数据验证和处理
	if interaction_dataset is None:
		raise ValueError("Please input the interaction_dataset argument")
	
	if isinstance(interaction_dataset, str):
		if not os.path.exists(interaction_dataset):
			raise FileNotFoundError(f"Cannot find file: {interaction_dataset}")
		interaction_df = pd.read_csv(interaction_dataset, sep='\t')
	elif isinstance(interaction_dataset, list):
		interaction_df = pd.concat(interaction_dataset, ignore_index=True)
	else:
		interaction_df = interaction_dataset.copy()
	
	# 2. 验证 signature_cytokine 参数
	all_cytokine = interaction_df['cytokine'].unique()
	if signature_cytokine is None:
		raise ValueError("Please input the signature_cytokine argument")
	else:
		valid_cytokine = [c for c in signature_cytokine if c in all_cytokine]
		if not valid_cytokine:
			raise ValueError("signature_cytokine not exist in interaction.data")
		if len(valid_cytokine) < len(signature_cytokine):
			invalid = set(signature_cytokine) - set(valid_cytokine)
			print(f"The following signature.cytokine not exist in interaction.data: {invalid}")
	
	# 3. 验证 method 参数
	if method is None:
		raise ValueError("Please input the method argument")
	if method not in ["median", "mean"]:
		raise ValueError("Input method must be median or mean")
	
	# 4. 筛选指定的细胞因子
	if valid_cytokine:
		interaction_df = interaction_df[interaction_df['cytokine'].isin(valid_cytokine)]
	
	# 5. 基于 cutoff 的基因筛选
	if cutoff is not None:
		# 计算每个基因的总样本数
		gene_sample_counts = interaction_df.groupby('gene')['sample'].nunique().reset_index()
		gene_sample_counts.columns = ['gene', 'total_samples']
		
		# 计算每个基因通过q值筛选的样本数
		filtered_samples = interaction_df[interaction_df['qvalue'] <= qvalue]
		gene_filtered_counts = filtered_samples.groupby('gene')['sample'].nunique().reset_index()
		gene_filtered_counts.columns = ['gene', 'filtered_samples']
		
		# 合并并计算比例
		merged_data = pd.merge(
				gene_sample_counts,
				gene_filtered_counts,
				on='gene',
				how='left'
		).fillna(0)
		merged_data['proportion'] = merged_data['filtered_samples'] / merged_data['total_samples']
		
		# 筛选达到 cutoff 比例的基因
		filtered_genes = merged_data[merged_data['proportion'] >= cutoff]['gene']
		interaction_df = interaction_df[interaction_df['gene'].isin(filtered_genes)]
	
	# 6. 计算 Tres 得分
	if method == "median":
		# 先按基因和样本分组计算中位数，再按基因汇总
		aggregated_by_cytokine = interaction_df.groupby(['gene', 'sample'])['t'].median().reset_index()
		result = aggregated_by_cytokine.groupby('gene')['t'].median().reset_index()
	else:  # mean
		# 先按基因和样本分组计算均值，再按基因汇总
		aggregated_by_cytokine = interaction_df.groupby(['gene', 'sample'])['t'].mean().reset_index()
		result = aggregated_by_cytokine.groupby('gene')['t'].mean().reset_index()
	
	result.columns = ['gene', 'tres_score']
	return result


# 测试函数
# 绘制 Tcell_activation 分数 与 TGFB1 活性 的散点图并标注相关系数
def plot_response_signaling(res_list,
                            signature='Tcell_activation',
                            cytokine='TGFB1'):
	"""
	绘制 Tcell_activation 与 TGFB1 的散点图并标注相关系数。

	Parameters:
		res_list (dict): 键为方法名（如 'none', 'mca'），值为 DataFrame 包含 'Tcell_activation' 和 'TGFB1'
		:param res_list: 细胞类型-信号通路-基因-Tcell_activation-TGFB1 交互作用分析结果
		:param cytokine: 细胞因子名
		:param signature: 标志基因集名
	"""
	fig, axes = plt.subplots(nrows=1, ncols=len(res_list), figsize=(6 * len(res_list), 5), sharey=True)
	if len(res_list) == 1:
		axes = [axes]  # 兼容单个子图的情况
	
	for ax, (name, df) in zip(axes, res_list.items()):
		x = df[cytokine]
		y = df[signature]
		corr = np.corrcoef(x, y)[0, 1]
		title = f"{name} (cor: {corr:.2f})"
		
		# 散点图
		sns.scatterplot(x=cytokine, y=signature, data=df, alpha=0.7, color='blue', ax=ax)
		
		# 回归线
		sns.regplot(x=cytokine, y=signature, data=df, scatter=False, color='red', ci=True, ax=ax)
		
		# 设置标题和样式
		ax.set_title(title, fontsize=12, ha='center')
		ax.set_xlabel(cytokine, fontsize=10)
		ax.set_ylabel(signature, fontsize=10)
		ax.tick_params(axis='both', labelsize=8)
		ax.grid(False)
	
	plt.tight_layout()
	plt.show()


# 读取 TSV 文件的第一行并按制表符分割
def read_tsv_header(filepath):
	with open(filepath, 'r') as f:
		first_line = f.readline()
		return first_line.strip().split('\t')


# 绘制 Wnt 信号通路活性中位数柱状图
def plot_activity(signaling, adata, cytokine='Wnt'):
	"""
	绘制每种细胞类型的 Wnt 信号通路活性中位数柱状图，x 轴按 y 从高到低排序。
	Parameters:
		signaling (pd.DataFrame): 行为细胞，列为信号通路（必须包含 'Wnt' 列）
		adata (AnnData or DataFrame): 包含 'celltype' 注释的对象
		:param adata:
		:param signaling:
		:param cytokine:
	"""
	
	# 获取 celltype 注释信息
	if hasattr(adata, 'obs'):  # AnnData 对象
		celltypes = adata.obs.loc[signaling.index, 'celltype']
	else:  # pandas DataFrame
		celltypes = adata.loc[signaling.index, 'celltype']
	
	# 创建包含 Wnt 数据的 DataFrame
	cyto_data = pd.DataFrame({
			"celltype":    celltypes,
			f"{cytokine}": signaling[f"{cytokine}"]
	})
	
	# 计算每个 celltype 的中位数
	grouped = cyto_data.groupby('celltype', observed=False)[f"{cytokine}"].median().reset_index()
	grouped = grouped.sort_values(by=f"{cytokine}", ascending=False)
	
	# 添加颜色列
	grouped['color'] = grouped[f"{cytokine}"].apply(lambda x: "Positive" if x > 0 else "Negative")
	
	# 设置 Seaborn 风格
	sns.set_theme(style="whitegrid")
	
	# 开始绘图
	plt.figure(figsize=(10, 6))
	
	# 明确指定 x 轴的顺序
	sns.barplot(data=grouped,
	            x='celltype',
	            y=f"{cytokine}",
	            hue='color',
	            dodge=False,
	            order=grouped['celltype'].tolist(),  # 明确指定顺序
	            palette={'Positive': 'red', 'Negative': 'blue'})
	
	plt.xlabel("Cell Type")
	plt.ylabel(f"{cytokine} Pathway Activity (Median)")
	plt.title(f"cytokine Activity per Cell Type")
	plt.xticks(rotation=45, ha='right')
	plt.legend(title="", loc='upper right')
	plt.tight_layout()
	plt.show()


# # 使用示例
# def main():
#
# 	# 读取数据
# 	adata = sc.read_h5ad("../data/h5ad/AML_GSE154109.h5ad")
# 	adata.var_names_make_unique()
# 	adata.obs['celltype'] = adata.obs['Celltype (major-lineage)'].astype('category')
#
# 	# 计算基因频率
# 	gs = read_gmt('../data/maker/CD8_Tcells_activation.gmt')
# 	grate = get_gene_rate(background_geneset='../data/gmt/Tres.kegg', signature_geneset=gs, mode="multiple")
# 	print("打印 grate 的前 5 行数据：\n", grate.head())
#
# 	# 降维重构, 计算 Tcell_activation 响应值, 计算细胞因子信号通路活性
# 	adata = rebuild_matrix(adata, method=['pca'], n_dim=16)
# 	response_data = compute_response(adata, gene_rate=grate, celltype="CD8T", signature="Tcell_activation")
# 	print("打印 response_data 的前 5 行数据：\n", response_data.head())
#
# 	signaling_data = compute_signaling(adata, model_file="../data/signature.centroid.expand", celltype="CD8T",
# 	                                   cytokine=None, lambd=10000, num_permutations=0, test_method="two-sided")
# 	print("打印 signaling_data 的前 5 行数据：\n", signaling_data.head())
#
# 	res = pd.concat([response_data, signaling_data[["TGFB1"]]], axis=1)
# 	plot_response_signaling({'none': res})
#
# 	# Wnt 信号通路活性
# 	columns = read_tsv_header('../data/SPEED2_signaling.tsv')
# 	print(columns)
# 	Signaling = compute_signaling(adata, model_file="../data/SPEED2_signaling.tsv", celltype=None,
# 	                              cytokine=None, lambd=10000, num_permutations=0, test_method="two-sided")
# 	plot_activity(Signaling, adata)
#
# 	"""
# 	交互作用分析和 Tres 得分计算
# 	"""
# 	# # 交互作用分析
# 	# interaction_results = do_interaction(
# 	# 		adata=adata,
# 	# 		response_data=response_data,
# 	# 		signaling_data=signaling_data,
# 	# 		signature=['Tcell_activation'],
# 	# 		cytokine=['TGFB1'],
# 	# 		threshold=10
# 	# )
# 	# print("打印interaction_results的前5行数据：\n", interaction_results.head())
# 	#
# 	# # 计算 Tres 分数
# 	# tres_genes = get_tres_signature(
# 	# 		interaction_dataset=interaction_results,
# 	# 		signature_cytokine=['TGFB1'],
# 	# 		qvalue=0.05,
# 	# 		cutoff=0.5,
# 	# 		method='median'
# 	# )
# 	# print("打印 tres_genes 的前5行数据：\n", tres_genes.head())
# 	#
# 	# # 绘制 Tres 得分分布图
# 	# plt.figure(figsize=(10, 6))
# 	#
# 	# # 直方图 + 密度曲线
# 	# plt.hist(tres_genes.iloc[:, 1], bins=30, alpha=0.7, color='steelblue', edgecolor='white', density=True)
# 	# plt.title('Tres Score Distribution')
# 	# plt.xlabel('Tres Score')
# 	# plt.ylabel('Density')
# 	#
# 	# # 添加密度曲线
# 	# from scipy.stats import gaussian_kde
# 	#
# 	# density = gaussian_kde(tres_genes.iloc[:, 1])
# 	# xs = np.linspace(tres_genes.iloc[:, 1].min(), tres_genes.iloc[:, 1].max(), 200)
# 	# plt.plot(xs, density(xs), 'r-', linewidth=2)
# 	#
# 	# # 添加均值线
# 	# mean_val = tres_genes.iloc[:, 1].mean()
# 	# plt.axvline(mean_val, color='k', linestyle='--', label=f'Mean: {mean_val:.2f}')
# 	# plt.legend()
# 	#
# 	# plt.grid(True, alpha=0.3)
# 	# plt.show()
# 	...
#
#
# if __name__ == '__main__':
# 	main()
