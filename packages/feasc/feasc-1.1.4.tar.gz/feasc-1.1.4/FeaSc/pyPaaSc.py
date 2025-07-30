import numpy as np
import pandas as pd

from sklearn.mixture import GaussianMixture
from sklearn.cluster import KMeans
from sklearn.feature_selection import mutual_info_regression


# 将通路活性分数二值化为正负标签
def do_binarization(score_data, n_cluster=2, method="GMM"):
	"""
	将连续分数二值化为 "positive" 和 "negative" 标签

	参数:
	- score_data: 包含连续分数的 pandas DataFrame
	- n_cluster: 聚类数量(默认为 2)
	- method: 聚类方法('GMM'或'kmeans'，默认为 'GMM')

	返回:
	- 带有二值化标签的 DataFrame(与输入形状相同)
	"""
	label_data = score_data.copy()
	label_data.columns = [f"{col}.label" for col in score_data.columns]
	
	for pathway_score_name in label_data.columns:
		pathway_score_data = label_data[[pathway_score_name]]
		
		if method == "GMM":
			# 为GMM准备数据(sklearn需要2D数组)
			data = pathway_score_data.values.reshape(-1, 1)
			gmm = GaussianMixture(n_components=n_cluster, max_iter=1000, tol=1e-5)
			gmm.fit(data)
			
			# 获取并排序均值
			means = gmm.means_.flatten()
			means_sorted = np.sort(means)
			
			# 计算两个最大均值之间的阈值
			threshold = (means_sorted[-2] + means_sorted[-1]) / 2
		
		elif method == "kmeans":
			# 为KMeans准备数据
			data = pathway_score_data.values.reshape(-1, 1)
			kmeans = KMeans(n_clusters=n_cluster)
			kmeans.fit(data)
			
			# 获取并排序中心点
			centers = kmeans.cluster_centers_.flatten()
			centers_sorted = np.sort(centers)
			
			# 计算两个最大中心点之间的阈值
			threshold = (centers_sorted[-2] + centers_sorted[-1]) / 2
		else:
			raise ValueError("方法必须是'GMM'或'kmeans'")
		
		# 根据阈值分配标签
		label_data[pathway_score_name] = np.where(
				pathway_score_data > threshold, "positive", "negative"
		)
	
	return label_data


# 空间互信息计算
def calculate_mi(x, y, num_bins=20, num_permutations=1000):
	if not isinstance(y, pd.DataFrame):
		y = pd.DataFrame({'y': y})
	
	if len(x) != len(y):
		raise ValueError("x and y must have the same length")
	
	result = pd.DataFrame(0.0, index=y.columns, columns=['MI', 'pvalue'])
	
	# 对每一列 y 变量进行计算
	x_binned_arr = None
	for col in y.columns:
		x_binned = pd.cut(x, bins=num_bins, labels=False)
		y_binned = pd.cut(y[col], bins=num_bins, labels=False)
		
		# 将 x 和 y 变量转换为 numpy 数组
		x_binned_arr = np.array(x_binned).reshape(-1, 1)
		y_binned_arr = np.array(y_binned)
		
		# 使用 sklearn 的 mutual_info_regression 计算 MI
		mi = mutual_info_regression(x_binned_arr, y_binned_arr)[0]
		result.loc[col, 'MI'] = mi
	
	if num_permutations > 0:
		for col in y.columns:
			observed_mi = result.loc[col, 'MI']
			permuted_mis = []
			
			for _ in range(num_permutations):
				permuted_y = y[col].sample(frac=1, replace=False).reset_index(drop=True)
				y_perm_binned = pd.cut(permuted_y, bins=num_bins, labels=False)
				
				# 计算随机化后的 MI
				y_perm_binned_arr = np.array(y_perm_binned)
				perm_mi = mutual_info_regression(x_binned_arr, y_perm_binned_arr)[0]
				permuted_mis.append(perm_mi)
			
			# 计算 p-value
			p_value = (np.sum(np.array(permuted_mis) >= observed_mi) + 1) / (num_permutations + 1)
			result.loc[col, 'pvalue'] = p_value
	
	else:
		result['pvalue'] = np.nan
	
	return result


def calculate_spatial_mi(x, y, z, num_bins=20, num_permutations=1000):
	if not isinstance(z, pd.DataFrame):
		z = pd.DataFrame({'z': z})
	
	# Input validation
	if len(x) != len(y) or len(x) != len(z):
		raise ValueError("x, y, and z must have the same length")
	
	result = pd.DataFrame(0.0, index=z.columns, columns=['MI', 'pvalue'])
	
	x_binned = None
	y_binned = None
	for col in z.columns:
		x_binned = pd.cut(x, bins=num_bins, labels=False)
		y_binned = pd.cut(y, bins=num_bins, labels=False)
		z_binned = pd.cut(z[col], bins=num_bins, labels=False)
		
		mi = _compute_3d_mi(x_binned, y_binned, z_binned)
		result.loc[col, 'MI'] = mi
	
	if num_permutations > 0:
		for col in z.columns:
			observed_mi = result.loc[col, 'MI']
			permuted_mis = []
			
			for _ in range(num_permutations):
				permuted_z = z[col].sample(frac=1, replace=False).reset_index(drop=True)
				z_perm_binned = pd.cut(permuted_z, bins=num_bins, labels=False)
				
				perm_mi = _compute_3d_mi(x_binned, y_binned, z_perm_binned)
				permuted_mis.append(perm_mi)
			
			# Calculate empirical p-value
			p_value = (np.sum(np.array(permuted_mis) >= observed_mi) + 1) / (num_permutations + 1)
			result.loc[col, 'pvalue'] = p_value
	
	else:
		result['pvalue'] = np.nan
	
	return result


def _compute_3d_mi(x_bins, y_bins, z_bins):
	xy_bins = [f"{x}_{y}" for x, y in zip(x_bins, y_bins)]
	joint_freq = pd.crosstab(xy_bins, z_bins)
	
	p_xy = joint_freq.sum(axis=1) / joint_freq.sum().sum()
	p_z = joint_freq.sum(axis=0) / joint_freq.sum().sum()
	p_xyz = joint_freq / joint_freq.sum().sum()
	
	mi = 0
	for i in range(len(p_xyz)):
		for j in range(len(p_xyz.columns)):
			if p_xyz.iloc[i, j] > 0:
				mi += p_xyz.iloc[i, j] * np.log(p_xyz.iloc[i, j] / (p_xy.iloc[i] * p_z.iloc[j]))
	
	return mi


# # 测试
# if __name__ == '__main__':
# 	# 设置随机种子保证可重复性
# 	np.random.seed(42)
#
# 	# 生成相关数据
# 	n = 30
# 	x = np.random.normal(size=n)
# 	y = 0.5 * x + np.random.normal(scale=0.5, size=n)  # y与x相关
# 	z = pd.DataFrame({
# 			'z1': 0.3 * x + 0.3 * y + np.random.normal(scale=0.5, size=n),  # z1与x,y都相关
# 			'z2': np.random.normal(size=n),  # z2与x,y无关
# 			'z3': 0.5 * x + np.random.normal(scale=0.5, size=n)  # z3只与x相关
# 	})
#
# 	# 生成空间坐标数据
# 	spatial_x = np.random.uniform(size=n)
# 	spatial_y = np.random.uniform(size=n)
# 	spatial_z = pd.DataFrame({
# 			'sz1': 0.5 * spatial_x + 0.5 * spatial_y + np.random.normal(scale=0.2, size=n),  # 与空间位置强相关
# 			'sz2': np.random.normal(size=n),  # 与空间位置无关
# 			'sz3': 0.3 * spatial_x + np.random.normal(scale=0.5, size=n)  # 只与x坐标相关
# 	})
#
# 	# 测试 y 与 x 的互信息
# 	mi_result = calculate_mi(x, y)
# 	print("MI between x and y:")
# 	print(mi_result)
#
# 	# 测试z与x的互信息
# 	mi_result_z = calculate_mi(x, z)
# 	print("\nMI between x and z:")
# 	print(mi_result_z)
#
# 	# 测试空间互信息
# 	spatial_mi_result = calculate_spatial_mi(spatial_x, spatial_y, spatial_z)
# 	print("\nSpatial MI:")
# 	print(spatial_mi_result)
