from sys import flags
import numpy as np
import scipy.io as sp_io
import scipy.spatial as sp_spatial
import warnings
warnings.filterwarnings("ignore")

import bct_duzc

coordinates = sp_io.loadmat("./bct_duzc_test_data/dk_coordinates.mat")['coordinates']
binarised_connectomes = sp_io.loadmat("./bct_duzc_test_data/example_binarised_connectomes.mat")['example_binarised_connectomes']

proportion = 0.2
Atgt_set = np.array(binarised_connectomes)
connections = Atgt_set.mean(axis=0)
A = np.zeros(connections.shape)
A[connections==proportion] = 1

n_sub = binarised_connectomes.shape[0]
nz = (binarised_connectomes.sum(axis=(1, 2)) // 2).astype(int)
D = sp_spatial.distance.squareform(sp_spatial.distance.pdist(coordinates, metric="euclidean"))

binarised_connectomes

model_type = ['euclidean', 'neighbors', 'matching', 
              'clu-avg', 'clu-min', 'clu-max', 'clu-diff', 'clu-prod',
              'deg-avg', 'deg-min', 'deg-max', 'deg-diff', 'deg-prod']
model_var  = ['powerlaw', 'powerlaw']
eta_limits = [-7, 7] 
gam_limits = [-7, 7]
n_run = 64
eta = np.linspace(eta_limits[0], eta_limits[1], num=np.sqrt(n_run).astype(int) )
gam = np.linspace(gam_limits[0], gam_limits[1], num=np.sqrt(n_run).astype(int) )
p, q = np.meshgrid(eta, gam)
params = np.array([p.ravel(), q.ravel()]).T

n_run = params.shape[0]
n_params = params.shape[0]
for i in range(n_sub):
    
    Atgt = binarised_connectomes[i]
    m = nz[i]
    n = Atgt.shape[0]
    x = [Atgt.sum(axis=1), 
         bct_duzc.clustering_coef_bu(Atgt), 
         bct_duzc.betweenness_bin(Atgt), 
         D[np.triu(Atgt, k=1).astype(bool)] ]
    #np.disp(f"running generative model for subject {i}")
    
    for mt in model_type[2:]:
        B = bct_duzc.generative_model(A, D, m, eta=params[:, 0], gamma=params[:, 1], model_type=mt, model_var=model_var[0]) # 返回值是各种参数下生成的网络
        print(f"sub_{i}", mt)
        
        # 检测生成的边数是否符合目标边数
        for j in range(n_run):
            if B[:, :, j].sum()//2 != m:
                print(f"\t Invalide generation {j+1, params[j, 0], params[j, 1]}, {B[:, :, j].sum()//2} edges generated, target {m} edges")
                exit()
        print(f"\ttarget edge number is satisfied")
        
        # 检测每个生成网络之间是否相同
        total_num, same_num = 0, 0
        for k1 in range(n_run-1):
            for k2 in range(k1+1, n_run):
                total_num += 1
                if np.alltrue(B[:, :, k1]==B[:, :, k2]):
                    same_num += 1
                    
        if same_num == total_num:
            print("\t Invalide generation, all generated networks are identity")
            exit()
        else:
            print("\tsame_numer=", same_num, same_num/total_num)
        #break

    #break
