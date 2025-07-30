import sctm
import anndata

import numpy as np
import pandas as pd
import scanpy as sc

from statsmodels.regression.linear_model import OLS
from statsmodels.tools import add_constant
from scipy.sparse import issparse
from sklearn.decomposition import NMF

from FeaSc.util_mca import run_mca
from FeaSc.util_stamp import scamp
from FeaSc.util_harmony import harmony


# 读取 gmt 文件（背景基因集）
def read_gmt(gmt_file: str) -> dict[str, list[str]]:
	"""
	功能：
		读取 GMT 格式文件并返回基因集字典
	参数：
		gmt_file: GMT 文件路径
	返回：
		字典：键（Key） 的类型是 str（字符串），代表基因集名称。
			 值（Value） 的类型是 list[str]（字符串列表），代表基因列表。
	"""
	gs_dict = {}
	with open(gmt_file, 'r', encoding='utf-8') as f:
		for line in f:
			# 移除行尾换行符并按制表符分割
			parts = line.strip().split('\t')
			if len(parts) < 3:
				continue  # 跳过不符合格式的行
			
			gs_name = parts[0]  # 第一列为基因集名称
			# 从第三列开始是基因列表，过滤掉空字符串
			genes = [gene for gene in parts[2:] if gene]
			gs_dict[gs_name] = genes
	
	return gs_dict


# 构建基因集频率矩阵
def build_gene_rate(
		bg_list: dict[str, list[str]],  # 背景基因字典
		gs_list: dict[str, list[str]] | None = None,  # 基因集字典
		gs_names: list[str] | str | None = None,  # 支持单基因或基因列表
) -> pd.DataFrame:
	"""
	功能：
		构建基因集频率矩阵，包含 'geneset' 和 'background' 两列。
		'geneset' 列表示基因集中包含的基因的频率，'background' 列表示背景基因集中包含的基因的频率。
	参数：
		gs_names: 要使用的基因集名称列表或单个基因集名称
		bg_list: 背景基因集字典
		gs_list: 基因集字典(可选)
	返回：
		基因集频率矩阵(DataFrame)，包含 'geneset' 和 'background' 两列
	"""
	# 处理输入参数
	if isinstance(gs_names, str):
		gs_names = [gs_names]
	
	if gs_list is None:
		# 检查所有基因集名称是否都在 bg_list 中
		missing = set(gs_names) - set(bg_list.keys())
		if missing:
			raise ValueError(f"以下基因集名称在 bg_list 中未找到: {missing}")
		gs_list = {name: bg_list[name] for name in gs_names}
	else:
		# 将 gs_list 中特有的基因集添加到 bg_list
		new_names = set(gs_list.keys()) - set(bg_list.keys())
		for name in new_names:
			bg_list[name] = gs_list[name]
	
	# 获取所有唯一基因
	all_genes = list({gene for genes in bg_list.values() for gene in genes})
	
	# 创建背景矩阵
	bg_matrix = pd.DataFrame(
			{name: [gene in bg_list[name] for gene in all_genes] for name in bg_list},
			index=all_genes
	)
	background = bg_matrix.mean(axis=1)
	
	# 创建基因集矩阵
	gs_matrix = pd.DataFrame(
			{name: [gene in gs_list[name] for gene in all_genes] for name in gs_list},
			index=all_genes
	)
	geneset = gs_matrix.mean(axis=1)
	
	# 组合结果
	result = pd.DataFrame({
			'geneset':    geneset,
			'background': background
	}, index=all_genes)
	
	return result


# 单样本降维方法 (pca, mca, nmf)
def run_reduction(
		adata: anndata.AnnData,
		features: list[str] | None = None,
		slot: str = "count",
		run_normalize: bool = True,
		method: str = 'mca',
		n_dim: int = 64
) -> anndata.AnnData:
	"""
	功能：在 AnnData 对象上运行降维方法，并添加降维结果到 AnnData 对象中。
	参数:
		adata: AnnData 对象
		features: 使用的特征列表，默认为所有基因
		run_normalize: 是否归一化数据，默认为 True
		method: 降维方法('mca', 'pca', 'nmf', 'all')
		n_dim: 计算的维度数
	返回:
		添加了降维结果的 AnnData 对象
	"""
	# 检查输入, 确保 adata 为 AnnData 对象
	if not isinstance(adata, anndata.AnnData):
		raise ValueError('please input a valid AnnData object')
	
	# 检查 method 参数
	if method not in ['mca', 'pca', 'nmf', 'all']:
		raise ValueError("method should be'mca', 'pca', 'nmf', or 'all'")
	
	# 获取想要使用的特征，默认为所有基因
	use_features = features if features is not None else adata.var_names.tolist()
	
	# 归一化每个细胞总表达量，让每个细胞的总表达为 1e4
	if run_normalize:
		sc.pp.normalize_total(adata, target_sum=1e4)
		sc.pp.log1p(adata)
	
	# 获取数据矩阵
	if slot == 'count':
		adata = adata[:, use_features].copy()
	else:
		adata = adata.layers[slot][:, use_features].copy()
	data = adata.X.copy()
	
	# mca 降维
	if method in ['mca', 'all']:
		out = run_mca(adata, n_dim)
		adata.obsm['mca'] = out[0]
		adata.varm['mca'] = out[1]
		adata.uns['mca'] = {
				'stdev':  out[2],
				'params': {'n_components': n_dim}
		}
	
	# pca 降维
	if method in ['pca', 'all']:
		# 标准化消除基因间表达量尺度的差异：不同基因的表达值可能有不同的量纲。
		adata_scale = adata.copy()
		sc.pp.scale(adata_scale)
		# 运行 PCA
		sc.tl.pca(adata_scale, n_comps=n_dim)
		# 将结果复制回原对象
		adata.obsm['pca'] = adata_scale.obsm['X_pca']
		adata.varm['pca'] = adata_scale.varm['PCs']
		adata.uns['pca'] = adata_scale.uns['pca']
	
	# nmf 降维
	if method in ['nmf', 'all']:
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
	
	return adata


# 多样本整合降维方法-1 (pca, mca, scamp)
def run_multi_reduction(adata: anndata.AnnData,
                        n_comps=16,
                        batch_col: str = "batch",
                        method: str = 'pca',
                        apply_combat: bool = True):
	
	mf_embedding, mf_loading = harmony(adata,
	                                   n_comps=n_comps,
	                                   batch_col=batch_col,
	                                   method=method,
	                                   apply_combat=apply_combat)
	adata.obsm.clear()
	adata.varm.clear()
	adata.obsm[f"multi_{method}"] = mf_embedding.to_numpy()
	adata.obs_names = mf_embedding.index.tolist()
	
	adata.varm[f"multi_{method}"] = mf_loading.to_numpy()
	adata.var_names = mf_loading.index.tolist()
	
	return adata


# 多样本整合降维方法-2 (基于 stamp)
def run_scamp(adata,
              n_dim: int = 16,
              n_comps: int = 64,
              method: str = 'pca',
              batch: str = 'batch',
              flag: bool = True,
              device: str = 'cpu'):
	"""
	功能：
		在 AnnData 对象上运行 SCAMP 算法，并添加降维结果到 AnnData 对象中。
	参数:
		adata: AnnData 对象
		n_dim: 降维后的维度数
		n_comps: 计算的基因数量
		method: 降维方法('pca', 'nmf')
		batch: 批次标签列名
		device: 默认使用 cpu 计算，可选 'cuda:0' 加速
	返回:
		添加了降维结果的 AnnData 对象
	"""
	n_comps_1 = int(n_comps * 0.8)
	
	topic_prop, beta = scamp(adata,
	                         n_topics=n_dim,
	                         method=method,
	                         n_comps=n_comps,
	                         n_comps_1=n_comps_1,
	                         batch=batch,
	                         flag=flag,
	                         device=device)
	adata.obsm.clear()
	adata.varm.clear()
	adata.obsm[f"multi_{method}"] = topic_prop.to_numpy()
	adata.obs_names = topic_prop.index.tolist()
	
	adata.varm[f"multi_{method}"] = beta.to_numpy()
	adata.var_names = beta.index.tolist()
	
	return adata


# 单样本基因集活性得分
def calculate_activity(
		adata: anndata.AnnData,
		gene_rate: pd.DataFrame,
		method: str = 'mca',
		n_dim: int = 64,
		p_value: float = 0.05,
		sd_weight: bool = True,
		normalize: int = 1
) -> pd.DataFrame:
	"""
	功能：
		计算基因集活性得分
	参数:
		adata: AnnData对象(包含降维结果)
		gene_rate: 基因频率矩阵
		method: 使用的降维方法
		n_dim: 使用的维度数
		p_value: 显著性阈值
		sd_weight: 是否使用标准差加权
		normalize: 标准化方法(0=无,1=Z-score,2=背景标准化)
	返回:
		细胞活性得分数组(失败时返回None)
	"""
	# 检查降维方法是否存在
	if method not in adata.obsm:
		print(f"calculate_activity 错误: 未找到指定的降维方法: {method}")
		return None
	
	# 运行回归分析
	reg_out = _run_regression(adata, gene_rate=gene_rate, method=method)
	
	# 获取嵌入矩阵
	embeddings = adata.obsm[method][:, :n_dim]
	
	# 准备回归结果
	pV = reg_out['pV'].iloc[:n_dim]
	zV = reg_out['zV'].iloc[:n_dim]
	bV = reg_out['bV'].iloc[:n_dim]
	
	# 获取维度权重(标准差)
	if method == 'pca':
		dV = adata.uns['pca']['variance'][:n_dim]
	elif method == 'mca':
		dV = adata.uns['mca']['stdev'][:n_dim]
	elif method == 'nmf':
		dV = adata.uns['nmf']['stdev'][:n_dim]
	else:
		dV = np.ones(n_dim)  # 默认等权重
	
	dV = dV / dV.sum()  # 归一化
	
	# 计算得分
	scores = _scoring(
			embeddings=embeddings,
			pV=pV,
			zV=zV,
			bV=bV,
			dV=dV,
			pvalue=p_value,
			sd_weight=sd_weight,
			normalize=normalize
	)
	
	scores = pd.Series(scores, index=adata.obs_names)
	scores.name = 'activity_score'  # 为 Series 命名
	
	return scores


# 多样本基因集活性得分
def calculate_multi_activity(
		adata: anndata.AnnData,
		gene_rate: pd.DataFrame,
		method: str = 'mca',
		n_dim: int = 64,
		p_value: float = 0.05,
		sd_weight: bool = False,
		normalize: int = 1
) -> pd.DataFrame:
	"""
	功能：
		计算基因集活性得分
	参数:
		adata: AnnData对象(包含降维结果)
		gene_rate: 基因频率矩阵
		method: 使用的降维方法
		n_dim: 使用的维度数
		p_value: 显著性阈值
		sd_weight: 是否使用标准差加权
		normalize: 标准化方法(0=无,1=Z-score,2=背景标准化)
	返回:
		细胞活性得分数组(失败时返回None)
	"""
	# 检查降维方法是否存在
	if f"multi_{method}" not in adata.obsm:
		print(f"错误: 未找到指定的降维方法: multi_{method}")
		return None
	
	# 运行回归分析
	reg_outs = _run_multi_regression(adata, gene_rate=gene_rate, method=method)
	
	scores_list = []
	for reg_out in reg_outs:
		# 获取嵌入矩阵
		embeddings = adata.obsm[f"multi_{method}"][:, :n_dim]
		
		# 准备回归结果
		pV = reg_out['pV'].iloc[:n_dim]
		zV = reg_out['zV'].iloc[:n_dim]
		bV = reg_out['bV'].iloc[:n_dim]
		# 获取维度权重(标准差)
		dV = np.ones(n_dim)  # 默认等权重
		dV = dV / dV.sum()  # 归一化
		
		# 计算得分
		scores = _scoring(
				embeddings=embeddings,
				pV=pV,
				zV=zV,
				bV=bV,
				dV=dV,
				pvalue=p_value,
				sd_weight=sd_weight,
				normalize=normalize
		)
		
		scores = pd.Series(scores, index=adata.obs_names)
		scores_list.append(scores)
	
	# 合并所有结果
	scores_df = pd.concat(scores_list, axis=1)
	scores_df.columns = [f"condition_{i + 1}" for i in range(len(scores_list))]
	
	return scores_df


# 回归分析，评估基因集对降维维度的贡献
def _run_regression(
		adata: sc.AnnData,
		gene_rate: pd.DataFrame,
		method: str = 'mca',
		min_genes: int = 0
) -> dict:
	"""
	功能：
		执行回归分析，评估基因集对降维维度的贡献
	参数：
		adata: 包含降维结果的AnnData对象
		method: 降维方法名称（必须存在于adata.obsm中）
		gene_rate: 包含'geneset'和'background'两列的DataFrame
		min_genes: 基因集中富集至少有 min_genes 才会被评估
	返回：
		包含以下内容的字典：
		- pV: 各维度基因集贡献的p值
		- zV: 各维度基因集贡献的z分数
		- bV: 各维度背景基因贡献的z分数
	异常：
		ValueError: 当输入验证失败时抛出
	"""
	# 检查 gene_rate 是否包含必需的列
	if not {'geneset', 'background'}.issubset(gene_rate.columns):
		raise ValueError("_run_regression_422: 基因频率矩阵必须包含'geneset'和'background'两列")
	
	# 检查指定的降维方法是否存在
	if method not in adata.obsm:
		raise ValueError(f"找不到指定的降维方法: {method}")
	
	# 从 AnnData 对象中获取指定方法的基因载荷
	if method in adata.varm:
		# 创建包含基因载荷的DataFrame，索引为基因名
		LD = pd.DataFrame(adata.varm[method],
		                  index=adata.var_names)
	else:
		raise ValueError(f"找不到方法 {method} 的基因载荷")
	
	# 获取同时存在于载荷矩阵和基因频率矩阵中的基因
	shared_genes = LD.index.intersection(gene_rate.index)
	
	# 检查共有基因数量是否足够
	if len(shared_genes) < 300:
		raise ValueError("基因表达数据和基因频率数据之间共享基因少于300个")
	
	# 只保留共有的基因
	LD = LD.loc[shared_genes]
	gene_rate = gene_rate.loc[shared_genes]
	
	# 检查基因集中富集的基因数量
	if (gene_rate['geneset'] > 0).sum() < min_genes:
		raise ValueError(f"基因表达数据中找到的基因少于 {min_genes}")
	
	# 对载荷矩阵和基因频率矩阵进行标准化（均值为0，标准差为1）
	LD = (LD - LD.mean()) / LD.std()
	gene_rate = (gene_rate - gene_rate.mean()) / gene_rate.std()
	
	# 创建用于存储结果的Series，初始值为默认值
	pV = pd.Series(1.0, index=LD.columns)  # p值初始化为1
	zV = pd.Series(0.0, index=LD.columns)  # z分数初始化为0
	bV = pd.Series(0.0, index=LD.columns)  # 背景z分数初始化为0
	
	# 每个降维维度执行回归分析
	for dim in LD.columns:
		# 准备回归数据
		data = pd.DataFrame({
				method:       LD[dim],  # 当前维度的基因载荷
				'geneset':    gene_rate['geneset'],  # 基因集频率
				'background': gene_rate['background']  # 背景基因频率
		})
		
		# 构建线性模型
		# 因变量：当前维度的基因载荷
		# 自变量：基因集频率 + 背景基因频率
		model = OLS(data[method], add_constant(data[['geneset', 'background']]))
		results = model.fit()  # 拟合模型
		
		# 提取并存储统计结果
		coeff = results.tvalues  # 获取t值（这里作为z分数使用）
		pvals = results.pvalues  # 获取p值
		
		pV[dim] = pvals['geneset']  # 存储基因集的p值
		zV[dim] = coeff['geneset']  # 存储基因集的z分数
		bV[dim] = coeff['background']  # 存储背景基因的z分数
	
	# 8. 返回结果字典
	return {
			'pV': pV,  # 各维度基因集的p值
			'zV': zV,  # 各维度基因集的z分数
			'bV': bV  # 各维度背景基因的z分数
	}


# 多样本回归分析
def _run_multi_regression(
		adata: sc.AnnData,
		gene_rate: pd.DataFrame,
		method: str = 'mca',
		min_genes: int = 0
) -> dict:
	"""
	功能：
		执行回归分析，评估基因集对降维维度的贡献
	参数：
		adata: 包含降维结果的AnnData对象
		method: 降维方法名称（必须存在于adata.obsm中）
		gene_rate: 包含'geneset'和'background'两列的DataFrame
		min_genes: 基因集中富集至少有 min_genes 才会被评估
	返回：
		包含以下内容的字典：
		- pV: 各维度基因集贡献的p值
		- zV: 各维度基因集贡献的z分数
		- bV: 各维度背景基因贡献的z分数
	异常：
		ValueError: 当输入验证失败时抛出
	"""
	# 检查 gene_rate 是否包含必需的列
	if not {'geneset', 'background'}.issubset(gene_rate.columns):
		raise ValueError("基因频率矩阵必须包含'geneset'和'background'两列")
	
	# 从 AnnData 对象中获取指定方法的基因载荷
	LDs = []
	for i in adata.varm.keys():
		LD = pd.DataFrame(adata.varm[i], index=adata.var_names)
		LDs.append(LD)
	
	# 获取同时存在于载荷矩阵和基因频率矩阵中的基因
	# print(LDs[0].index)
	shared_genes = LDs[0].index.intersection(gene_rate.index)
	# print(shared_genes)
	
	# 检查共有基因数量是否足够
	if len(shared_genes) < 200:
		raise ValueError("基因表达数据和基因频率数据之间共享基因少于200个")
	# print(len(shared_genes))
	
	# 只保留共有的基因
	LDs_shared = []
	for LD in LDs:
		LD = LD.loc[shared_genes]
		LDs_shared.append(LD)
	gene_rate = gene_rate.loc[shared_genes]
	
	# 检查基因集中富集的基因数量
	if (gene_rate['geneset'] > 0).sum() < min_genes:
		raise ValueError(f"_run_multi_regression_546: 基因表达数据中找到的基因少于 {min_genes}")
	# print((gene_rate['geneset'] > 0).sum())
	
	# 对载荷矩阵和基因频率矩阵进行标准化（均值为0，标准差为1）
	LDs_std = []
	for LD in LDs_shared:
		LD = (LD - LD.mean()) / LD.std()
		LDs_std.append(LD)
	gene_rate = (gene_rate - gene_rate.mean()) / gene_rate.std()
	
	# 创建用于存储结果的Series，初始值为默认值
	pVs = []
	zVs = []
	bVs = []
	for LD in LDs_std:
		pV = pd.Series(1.0, index=LD.columns)  # p值初始化为1
		zV = pd.Series(0.0, index=LD.columns)  # z分数初始化为0
		bV = pd.Series(0.0, index=LD.columns)  # 背景z分数初始化为0
		pVs.append(pV)
		zVs.append(zV)
		bVs.append(bV)
	
	reg_outs = []
	for i, LD in enumerate(LDs_std):
		pV = pVs[i]
		zV = zVs[i]
		bV = bVs[i]
		for dim in LD.columns:
			# 准备回归数据
			data = pd.DataFrame({
					method:       LD[dim],  # 当前维度的基因载荷
					'geneset':    gene_rate['geneset'],  # 基因集频率
					'background': gene_rate['background']  # 背景基因频率
			})
			
			# 构建线性模型
			# 因变量：当前维度的基因载荷
			# 自变量：基因集频率 + 背景基因频率
			model = OLS(data[method], add_constant(data[['geneset', 'background']]))
			results = model.fit()  # 拟合模型
			
			# 提取并存储统计结果
			coeff = results.tvalues  # 获取t值（这里作为z分数使用）
			pvals = results.pvalues  # 获取p值
			
			pV[dim] = pvals['geneset']  # 存储基因集的p值
			zV[dim] = coeff['geneset']  # 存储基因集的z分数
			bV[dim] = coeff['background']  # 存储背景基因的z分数
		
		reg_out = {
				'pV': pV,  # 各维度基因集的p值
				'zV': zV,  # 各维度基因集的z分数
				'bV': bV  # 各维度背景基因的z分数
		}
		reg_outs.append(reg_out)
	
	return reg_outs


# 计算细胞的通路活性得分
def _scoring(
		embeddings: np.ndarray | pd.DataFrame,  # 细胞×维度矩阵
		pV: np.ndarray | pd.Series,  # 各维度 P 值
		zV: np.ndarray | pd.Series,  # 基因集 Z 分数
		bV: np.ndarray | pd.Series,  # 背景 Z 分数
		dV: np.ndarray | pd.Series,  # 维度权重 stdev
		pvalue: float = 0.05,  # 显著性阈值
		sd_weight: bool = False,  # 标准差加权
		normalize: int = 1  # 标准化方式
) -> np.ndarray:
	"""
	功能：
		基于基因集活性计算细胞得分
	参数：
		embeddings: 细胞嵌入矩阵 (n_cells x n_dims)
		pV: 各维度的P值向量
		zV: 基因集Z分数向量
		bV: 背景Z分数向量
		dV: 维度权重向量
		pvalue: P值阈值
		sd_weight: 是否应用标准差加权
		normalize: 标准化方法(0=无,1=Z-score,2=背景标准化)
	返回:
		细胞得分向量 (n_cells,)
	"""
	# 转换为pandas Series统一处理索引
	pV = pd.Series(pV)
	zV = pd.Series(zV)
	bV = pd.Series(bV)
	dV = pd.Series(dV)
	
	# 选择显著维度或前两个最显著维度
	sig_dims = pV[pV < pvalue].index
	if len(sig_dims) == 0:
		sig_dims = pV.sort_values().index[:2]
	
	# 提取对应的权重和嵌入
	zweight = zV[sig_dims]
	bweight = bV[sig_dims]
	dweight = dV[sig_dims]
	
	if isinstance(embeddings, pd.DataFrame):
		wm = embeddings.loc[:, sig_dims].values
	else:
		# 假设embeddings是numpy数组且列顺序与索引对应
		wm = embeddings[:, [i for i, name in enumerate(pV.index) if name in sig_dims]]
	
	# 计算加权得分
	score = _weighting(wm, zweight.values, dweight.values, sd_weight)
	
	# 标准化
	if normalize == 1:
		score = (score - np.mean(score)) / np.std(score)
	elif normalize == 2:
		bscore = _weighting(wm, bweight.values, dweight.values, sd_weight)
		score = (score - np.mean(bscore)) / np.std(bscore)
	
	return score


# 计算加权得分向量
def _weighting(
		wm: np.ndarray | pd.DataFrame,  # 权重矩阵 (cells x dimensions)
		zw: np.ndarray | pd.Series,  # Z 权重向量 (per dimension)
		dw: np.ndarray | pd.Series,  # 维度权重向量 (per dimension)
		sd_weight: bool = True  # 是否应用标准差加权
) -> np.ndarray:
	"""
	功能：
		计算加权得分向量
	参数:
		wm: 权重矩阵 (n_cells x n_dims)
		zw: Z权重向量 (n_dims,)
		dw: 维度权重向量 (n_dims,)
		sd_weight: 是否应用标准差加权
	返回:
		加权得分向量 (n_cells,)
	"""
	# 转换为numpy数组确保兼容性
	wm = np.asarray(wm)
	zw = np.asarray(zw)
	dw = np.asarray(dw)
	
	# 第一步：用zw加权 (按列相乘)
	weighted = wm * zw
	
	# 第二步：可选地用dw加权
	if sd_weight:
		weighted *= dw
	
	# 计算得分 (按行求和后标准化)
	score = np.sum(weighted, axis=1) / np.sum(np.abs(zw))
	
	return score

# # 参数配置类
# class Config:
# 	def __init__(
# 			self,
# 			path_matrix: str,
# 			path_maker: str,
# 			path_gmt: str,
# 			method: str = "mca",
# 			n_dim: int = 16,
# 			design: str = "~ stim",
# 			batch: str = "stim",
# 			flag: bool = True,
# 			p_value: float = 0.05,
# 			sd_weight: bool = False,
# 			normalize: int = 1,
# 	):
# 		"""
# 		SCAMP 分析配置参数类
# 		参数:
# 			path_matrix: 矩阵数据路径（如基因表达矩阵）
# 			path_maker: 特征标记路径
# 			path_gmt: GMT文件路径（基因集文件）
# 			method: 分析方法（默认'mca'）
# 			n_dim: 降维维度数（默认16）
# 			design: 实验设计公式（默认"~ stim"）
# 			batch: 批次变量名（默认"stim"）
# 			flag: 是否启用标志（默认True）
# 			p_value: 显著性阈值（默认0.05）
# 			sd_weight: 是否使用标准差权重（默认False）
# 			normalize: 归一化方式（默认1）
# 		"""
# 		self.path_matrix = path_matrix
# 		self.path_maker = path_maker
# 		self.path_gmt = path_gmt
# 		self.method = method
# 		self.n_dim = n_dim
# 		self.design = design
# 		self.batch = batch
# 		self.flag = flag
# 		self.p_value = p_value
# 		self.sd_weight = sd_weight
# 		self.normalize = normalize
#
# 	def to_dict(self) -> dict:
# 		"""将配置转换为字典格式（兼容旧代码）"""
# 		return {
# 				"path_matrix": self.path_matrix,
# 				"path_maker":  self.path_maker,
# 				"path_gmt":    self.path_gmt,
# 				"method":      self.method,
# 				"n_dim":       self.n_dim,
# 				"design":      self.design,
# 				"batch":       self.batch,
# 				"flag":        self.flag,
# 				"p_value":     self.p_value,
# 				"sd_weight":   self.sd_weight,
# 				"normalize":   self.normalize,
# 		}
#
#
# def main():
# 	from pathlib import Path
#
# 	# 表达矩阵路径
# 	path_matrix = "../data/h5ad/GSE96583.h5ad"
# 	# 标志基因集路径
# 	path_maker = "../data/maker/B-cell_marker.txt"
# 	# 背景基因集路径
# 	path_gmt = "../data/gmt/kegg.gmt"
#
# 	# 设置参数
# 	config = Config(path_matrix, path_maker, path_gmt)
# 	config.method = 'mca'
# 	config.n_dim = 16
# 	config.batch = "stim"
# 	config.flag = True
# 	config.p_value = 0.05
# 	config.sd_weight = False
# 	config.normalize = 1
#
# 	""" 读取数据 """
# 	adata = sc.read_h5ad(config.path_matrix)
# 	adata.var_names_make_unique()
#
# 	""" 过滤数据 """
# 	sc.pp.filter_cells(adata, min_genes=200)
# 	# sc.pp.filter_genes(adata, min_cells=3)
# 	sctm.pp.filter_genes(adata, min_cutoff=0.03, expression_cutoff_99q=1)
# 	sc.pp.highly_variable_genes(adata, n_top_genes=3000, flavor="seurat_v3")
# 	adata = adata[:, adata.var.highly_variable]
#
# 	""" 构建基因频率矩阵 """
# 	gs = pd.read_table(config.path_maker, header=0).iloc[:, 0].tolist()
# 	gsList = {'gs': gs}
# 	bgList = read_gmt(config.path_gmt)
# 	grate = build_gene_rate(bg_list=bgList, gs_list=gsList)
#
# 	"""单样本分析"""
# 	# # 单样本降维
# 	# adata = run_reduction(adata, method=config.method, n_dim=config.n_dim)
# 	# # 计算活性得分
# 	# activity_scores = calculate_activity(
# 	# 		adata=adata,
# 	# 		gene_rate=grate,
# 	# 		method=config.method,
# 	# 		n_dim=config.n_dim,
# 	# 		p_value=config.p_value,
# 	# 		sd_weight=config.sd_weight,
# 	# 		normalize=config.normalize
# 	# )
# 	# filename = Path(config.path_matrix).stem  # 'CHOL_GSE142784'
# 	# markername = Path(config.path_matrix).stem  # 'B-cell_marker'
# 	# activity_scores.to_csv(f'../dout/{filename}_{config.method}_{markername}_scores.csv')
#
# 	"""多样本分析"""
# 	# 多样本整合降维 (scamp)
# 	adata = run_scamp(adata, n_dim=config.n_dim, method=config.method, batch="stim")
#
# 	# 计算活性得分
# 	activity_scores = calculate_multi_activity(
# 			adata,
# 			grate,
# 			method=config.method,
# 			n_dim=config.n_dim,
# 	)
#
# 	filename = Path(config.path_matrix).stem  # 'CHOL_GSE142784'
# 	markername = Path(config.path_maker).stem  # 'B-cell_marker'
# 	activity_scores.to_csv(f'../dout/{filename}_multi_{config.method}_{markername}_scores.csv')
#
#
# if __name__ == '__main__':
# 	main()
