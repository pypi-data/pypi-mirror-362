import numpy as np
np.bool=np.bool_
np.int=np.int_
np.object = object
import scanpy as sc
import scvelo as scv
sc.logging.print_versions()  # 打开日志
sc.settings.verbosity = 0   # 设置为 0 表示不输出日志和 warning
from joblib import Parallel, delayed
import pandas as pd
def hello():
    print("Hello from my package!")
def preprocess(adata_path,leiden_res=0.7):

    adata=sc.read(adata_path,sparse=True)

    scv.logging.print_version()
    scv.settings.verbosity = 3  # show errors(0), warnings(1), info(2), hints(3)
    scv.settings.presenter_view = True  # set max width size for presenter view
    scv.settings.set_figure_params('scvelo')  # for beautified visualization
    scv.set_figure_params()
    #filter genes
    scv.pp.filter_and_normalize(adata, min_shared_counts=20, n_top_genes=1000)
    scv.pp.moments(adata, n_pcs=30, n_neighbors=30)
    sc.tl.leiden(adata, resolution=leiden_res)
    min_cells = 20

    # 统计每个 cluster 中的细胞数
    leiden_counts = adata.obs['leiden'].value_counts()

    # 找出需要保留的 cluster（数目 >= min_cells）
    valid_clusters = leiden_counts[leiden_counts >= min_cells].index

    # 筛选 adata，只保留 valid_clusters
    adata = adata[adata.obs['leiden'].isin(valid_clusters)]
    adata.uns['valid_leiden']=valid_clusters
    adata_100=sc.pp.subsample(adata, fraction=None, n_obs=300, random_state=0, copy=True)
    min_cells = 7
    leiden_counts = adata_100.obs['leiden'].value_counts()
    valid_clusters = leiden_counts[leiden_counts >= min_cells].index
    adata_100= adata_100[adata_100.obs['leiden'].isin(valid_clusters)]
    adata=adata[adata.obs['leiden'].isin(valid_clusters)]

    gene_path='data/ChEA_2016.txt'
    adata_sub=adata_100
    gene_names = list(adata_sub.var_names)
    target_idx=np.zeros((len(gene_names),len(gene_names)))
    gene_names= [name.upper() for name in gene_names]
    with open(gene_path, "r") as f:
        for line in f.readlines():
            line = line.strip('\n')
            line = line.split('\t')
            TF_info = line[0]
            TF_name = TF_info.split(' ')[0]
            if not TF_name in gene_names:
                continue
            targets= line[2:]
            for target in targets:
                if target in gene_names:
                    target_idx[gene_names.index(TF_name),gene_names.index(target)]=1
    return adata,adata_100,target_idx

def mst(adata,adata_100):
    import numpy as np
    import pandas as pd

    # 设定最小细胞数阈值
    min_cells = 7
    leiden_counts = adata_100.obs['leiden'].value_counts()
    valid_clusters = leiden_counts[leiden_counts >= min_cells].index
    adata= adata[adata.obs['leiden'].isin(valid_clusters)]
    adata.uns['valid_leiden']=valid_clusters
    sc.pl.umap(adata,color='leiden')



# 使用 UMAP 坐标计算中心
    umap = adata.obsm['X_umap']
    leiden = adata.obs['leiden']

    # 每个 cluster 的中心
    df = pd.DataFrame(umap, columns=["UMAP1", "UMAP2"])
    df["leiden"] = adata.obs["leiden"].values  # 👈 这一行非常重要！

    # 按照 leiden 聚类计算中心点
    cluster_centers = df.groupby("leiden")[["UMAP1", "UMAP2"]].mean().values
    from scipy.spatial.distance import pdist, squareform

    # 计算所有 cluster 中心之间的欧氏距离
    dist_matrix = squareform(pdist(cluster_centers, metric='euclidean'))
    import networkx as nx

    # 创建无向图
    G = nx.Graph()

    # 添加边
    n_clusters = dist_matrix.shape[0]
    for i in range(n_clusters):
        for j in range(i + 1, n_clusters):
            G.add_edge(i, j, weight=dist_matrix[i, j])

    # 求最小生成树
    mst = nx.minimum_spanning_tree(G)
    import matplotlib.pyplot as plt


    plt.figure(figsize=(6, 6))
    plt.scatter(*umap.T, s=5, alpha=0.5)
    plt.scatter(*cluster_centers.T, c='red', s=100)

    # 在 UMAP 上画出最小生成树
    for i, j in mst.edges():
        xi, yi = cluster_centers[i]
        xj, yj = cluster_centers[j]
        plt.plot([xi, xj], [yi, yj], 'k-', lw=2)

    plt.title("MST between cluster centers")
    plt.show()
    return adata,mst
def get_pseudotime(adata,root_cluster):
    sc.pp.neighbors(adata, n_neighbors=30)
    root_cell = adata[adata.obs['leiden'] == str(root_cluster)].obs_names[0]
    adata.uns['iroot'] = adata.obs_names.get_loc(root_cell)
    import warnings

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        sc.tl.dpt(adata)

    adata.obs['pseudotime'] = adata.obs['dpt_pseudotime']
    del adata.obs['dpt_pseudotime']
    return adata
def pl_pseudotime(adata):
    scv.pl.scatter(adata, color='pseudotime', color_map='gnuplot', size=80,basis='X_umap')
from scipy.spatial.distance import cdist
def find_optimal_sequence(points, max_iter=1000):
    num_points = len(points)
    dist_matrix = cdist(points, points)

    def nearest_neighbor_path(start_idx):
        visited = [False] * num_points
        path = [start_idx]
        visited[start_idx] = True
        for _ in range(1, num_points):
            last = path[-1]
            nearest = np.argmin([dist_matrix[last][j] if not visited[j] else np.inf for j in range(num_points)])
            path.append(nearest)
            visited[nearest] = True
        return path

    def path_length(path):
        return sum(dist_matrix[path[i], path[i+1]] for i in range(len(path)-1))

    def two_opt(path):
        best = path.copy()
        best_dist = path_length(best)

        for _ in range(max_iter):
            improved = False
            for i in range(0, num_points - 2):  # ✅ 包含起点扰动
                for j in range(i + 1, num_points):
                    if j - i == 1:
                        continue
                    new_path = best[:i] + best[i:j][::-1] + best[j:]
                    new_dist = path_length(new_path)
                    if new_dist < best_dist:
                        best = new_path
                        best_dist = new_dist
                        improved = True
                        break
                if improved:
                    break
            if not improved:
                break
        return best

    start = np.random.randint(num_points)
    init_path = nearest_neighbor_path(start)
    optimized_path = two_opt(init_path)
    return optimized_path

import torch
from torch import optim
def optimize_matrix_A(route,adata_sub,target_idx,epochs=10000, lr=0.001):


    x = adata_sub.X.toarray()
    n, m = x.shape
    X1=torch.tensor(x,device='cuda',dtype=torch.float32)


    # 初始化需要优化的矩阵A和矩阵W
    A = np.ones((m, m))  # 根据具体需求初始化
#     target_idx = np.random.randn(m, m)  # 这个变量需要定义或从数据中获取
    W = target_idx  # 假设W矩阵和target_idx相关

    # 根据W矩阵定义掩码矩阵
    mask = np.where(W != 0, 1, 0)
    mask_gpu = torch.tensor(mask, device='cuda', dtype=torch.float64)

    # 确保矩阵A中对应W为零的位置也为零
    A *= mask
    A_gpu = torch.tensor(A, requires_grad=True, device='cuda', dtype=torch.float64)

    # 初始化优化器
    optimizer = optim.Adam([A_gpu], lr=lr)

    # 定义目标函数
    def objective_function_A(A, route):
        scalar = torch.tensor(1, device='cuda', dtype=torch.float64)
        target_idx_gpu = torch.tensor(target_idx, device='cuda', dtype=torch.float64)
        dy_gpu = torch.tensor(dy(route, x), device='cuda', dtype=torch.float64)
        Ones = torch.ones(m, m, device='cuda', dtype=torch.float64)
        W_gpu = torch.tensor(W, device='cuda', dtype=torch.float64)
        X1=torch.tensor(x,device='cuda')

#         distance_matrix=distance_matrix2.cpu().detach().numpy()
#         total_distance = 0.0
#         for i in range(len(route) - 1):
#             total_distance += distance_matrix[route[i]-1, route[i + 1]-1]
        W_reciprocal = torch.reciprocal(100 * target_idx_gpu + scalar * Ones)

        x_t = np.zeros((n, m))
        for i in range(n):
            x_t[i] = x[route[i] - 1, :]
        x_t_gpu = torch.tensor(x_t[2:n-3, :], device='cuda', dtype=torch.float64)
#         distance_matrix2=torch.cdist(X1A,X1A,p=2)
        X1A_gpu = torch.mm(x_t_gpu, A)
        W_hadamard_A_gpu = torch.mul(W_reciprocal, A)
        matrix = dy_gpu - X1A_gpu
        matrix_norm = torch.norm(matrix, p='fro')
        W_hadamard_A_norm = torch.norm(W_hadamard_A_gpu, p='fro')
        x_t_minus=torch.diff(x_t_gpu, dim=0)
        total_distance=torch.norm(torch.mm(x_t_minus,A),p='fro')
        loss = matrix_norm+W_hadamard_A_norm+total_distance
        return loss

    def dy(route, x):
        m, n = x.shape
        dy1 = np.zeros((m-5, n))
        deltat = 1 / (m-1)
        for t in range(2, m - 3):
            dy1[t - 2, :] = (8 * x[route[t + 1]-1, :] - 8 * x[route[t - 1]-1, :] + x[route[t - 2]-1, :] - x[route[t + 2]-1, :]) / (12 * deltat)
        return dy1

    # 进行优化迭代
    for i in range(epochs):
        optimizer.zero_grad()  # 每次迭代前将梯度清零
        loss = objective_function_A(A_gpu, route)
        loss.backward()  # 计算梯度
        optimizer.step()  # 更新矩阵A的数值
        
        # 应用掩码，使非优化元素保持为零
        with torch.no_grad():
            A_gpu *= mask_gpu
        
        # if i % 1000 == 0:  # 每1000次迭代打印一次损失
        #     print(f"Iteration {i}, loss: {loss.item()}")

#     print("Optimized matrix A:")
    return A_gpu.cpu().detach().numpy()

def getdistance(A,adata_sub):
    u, s, v = np.linalg.svd(A)
    n,m=adata_sub.shape
    X1=torch.tensor(adata_sub,device='cuda',dtype=torch.float32)

    A=torch.tensor(A,device='cuda',dtype=torch.float32)
    X1A=torch.mm(X1, A)
# print(XA.shape,XB.shape,type(XA),type(XB))
    distance_matrix1=torch.cdist(X1, X1, p=2)
    distance_matrix2=torch.dist(X1A,X1A,p=2)
    # print(distance_matrix1,distance_matrix2)
    distance_matrix=distance_matrix1+distance_matrix2/(s[0]+1)
    distance=np.array(distance_matrix.cpu())
    return distance
# from python_tsp.exact import solve_tsp_dynamic_programming
# from python_tsp.heuristics import solve_tsp_simulated_annealing
# from python_tsp.heuristics import solve_tsp_local_search
def get_cluster_pseudotime(adata_100,cluster,target_idx):
    adata_sub = adata_100[adata_100.obs['leiden'] == str(cluster)].copy()
    x = adata_sub.X.toarray()
    n, m = x.shape
    A = np.ones((m, m))

    for iteration in range(3):
        distance_matrix = getdistance(A, x)
        route=find_optimal_sequence(x)
        # route, _ = solve_tsp_simulated_annealing(distance_matrix)
        # route, _ = solve_tsp_local_search(distance_matrix)
        A = optimize_matrix_A(route,adata_sub,target_idx)
    Answer=route
    n=len(Answer)
    n=len(Answer)
    q=0
    U=np.zeros(n)
    for i in range(n):
        
        U[Answer[i]-1]=1/n*q
        q+=1
    adata_sub.obs['latent_time']=U

    return adata_sub
def get_all_cluster_adata_subs(adata,target_idx, n_jobs=4):
    min_cells = 7
    leiden_counts = adata.obs['leiden'].value_counts()
    valid_clusters = leiden_counts[leiden_counts >= min_cells].index
    adata = adata[adata.obs['leiden'].isin(valid_clusters)]
    clusters = adata.obs['leiden'].unique()
    print(clusters)
    results = Parallel(n_jobs=n_jobs)(
        delayed(get_cluster_pseudotime)(adata, cluster,target_idx) for cluster in clusters
    )
    return [r for r in results if r is not None]
import networkx as nx

def assign_global_pseudotime_by_size(cluster_dict, mst_graph, root_cluster):
    visited = set()
    cluster_offsets = {}
    global_pseudotime = {}

    # Step 1: 归一化每个 cluster 内部 latent_time 到 [0, 1]
    for cid, ad in cluster_dict.items():
        ad.obs['latent_time'] = (ad.obs['latent_time'] - ad.obs['latent_time'].min()) / \
                                   (ad.obs['latent_time'].max() - ad.obs['latent_time'].min() + 1e-8)

    # Step 2: 计算每个 cluster 的大小
    cluster_sizes = {cid: ad.shape[0] for cid, ad in cluster_dict.items()}
    total_size = sum(cluster_sizes.values())

    # Step 3: 计算每个 cluster 的长度比例
    cluster_lengths = {cid: size / total_size for cid, size in cluster_sizes.items()}

    def dfs(cluster, offset):
        visited.add(cluster)
        cluster_offsets[cluster] = offset
        ad = cluster_dict[cluster]

        length = cluster_lengths[cluster]
        global_pseudotime[cluster] = ad.obs['latent_time'] * length + offset

        for neighbor in mst_graph.neighbors(cluster):
            if neighbor not in visited:
                dfs(neighbor, offset + length)

    dfs(root_cluster, offset=0.0)
    return global_pseudotime

def get_adata_100_pseudo(adata,adata_100,root_cluster,target_idx):
    import pandas as pd
    adata_list=get_all_cluster_adata_subs(adata_100,target_idx, n_jobs=4)
    _,mst_adata=mst(adata,adata_100)
    

    # 初始化一个全为 NaN 的 pseudotime 列
    adata_100.obs['pseudotime'] = pd.NA
    min_cells = 7
    leiden_counts = adata_100.obs['leiden'].value_counts()
    valid_clusters = leiden_counts[leiden_counts >= min_cells].index
    adata_100 = adata_100[adata_100.obs['leiden'].isin(valid_clusters)]
    leiden_clusters = adata_100.obs['leiden'].unique()
    # adata_subs 是 get_all_cluster_adata_subs 的返回值
    cluster_dict = dict(zip(leiden_clusters, adata_list))
    cluster_dict = {int(k): v for k, v in cluster_dict.items()}
    global_pseudotime=assign_global_pseudotime_by_size(cluster_dict, mst_adata, root_cluster)

    # 逐个 cluster 把 pseudotime 值填进去
    for cluster_id, pseudo_series in global_pseudotime.items():
        adata_100.obs.loc[pseudo_series.index, 'pseudotime'] = pseudo_series


    adata_100.obs['pseudotime'] = adata_100.obs['pseudotime'].astype(float)
    adata_100.obs['pseudotime'] = (adata_100.obs['pseudotime'] - adata_100.obs['pseudotime'].min()) / \
                            (adata_100.obs['pseudotime'].max() - adata_100.obs['pseudotime'].min())
    return adata_100
def get_adata_all_pseudotime(adata,adata_100,root_cluster,target_idx):
    import numpy as np
    from scipy.spatial.distance import cdist
    def interpolate_pseudotime_full(adata, adata_subset, k=5):
        # 1. 全部点的表达数据
        X_all = adata.X.toarray()
        X_sub = adata_subset.X.toarray()
        print(X_all.shape,X_sub.shape)
        # 2. 找出子集在原始 adata 中的 index
        anchor_indices = [adata.obs_names.get_loc(name) for name in adata_subset.obs_names]
        
        # 3. 获取 anchor 的 pseudotime
        pseudotime_anchor = adata_subset.obs["pseudotime"].values
        N = X_all.shape[0]
        
        # 4. 计算距离
        dists = cdist(X_all, X_sub)
        
        # 5. 插值 pseudotime
        pseudotime_full = np.full(N, np.nan)
        pseudotime_full[anchor_indices] = pseudotime_anchor
        
        for i in range(N):
            if not np.isnan(pseudotime_full[i]):
                continue
            nearest_idx = np.argsort(dists[i])[:k]
            nearest_dists = dists[i][nearest_idx]
            nearest_times = pseudotime_anchor[nearest_idx]

            weights = 1 / (nearest_dists + 1e-6)
            weights /= weights.sum()
            pseudotime_full[i] = np.dot(weights, nearest_times)
        
        # 6. 写入 adata.obs
        adata.obs["pseudotime"] = pseudotime_full
    adata_100=get_adata_100_pseudo(adata,adata_100,root_cluster,target_idx)
    interpolate_pseudotime_full(adata, adata_100, k=50)
    scv.pp.neighbors(adata, n_neighbors=100)
    neighbor_matrix=adata.uns['neighbors']['indices']
    neighbor_matrix=adata.uns['neighbors']['indices']

    k=100
    n=adata.X.toarray().shape[0]
    U_KNN=np.zeros(n)
    U=adata.obs['pseudotime'].values
    for i in range(n):
        for j in range(k):
            U_KNN[i]+=U[neighbor_matrix[i,j]]
        U_KNN[i]=U_KNN[i]/k
    adata.obs['pseudotime']=U_KNN/U_KNN.max()
    return adata
        
