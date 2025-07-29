

def get_idx_from_dense(i, j, M, n_obs):
    idx = n_obs*i+j-((i+2)*(i+1))//2
    return M[idx]