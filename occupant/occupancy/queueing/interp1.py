import numpy as np
def interp1(x,v,xq):
    xv_comb = np.array([x,v])
    xv_sorted = xv_comb[0:2,xv_comb[0,:].argsort()]
    x_sorted = xv_sorted[0,:]
    v_sorted = xv_sorted[1,:]
    vq = np.empty(xq.size)
    vq[:] = np.NAN
    for i in range(len(x_sorted)):
        if i == 0:
            idx = np.where(xq <= x_sorted[0])[0]
            if idx.size == 0:
                continue
            else:
                vq[idx] = v_sorted[0]
        else:
            idx = np.where(np.logical_and(xq > x_sorted[i-1], xq <= x_sorted[i]))[0]
            vq[idx] = v_sorted[i-1]

    idx = np.where(np.logical_and(xq > x_sorted[-1], np.isnan(vq)))[0]
    vq[idx] = v_sorted[-1]
    return vq
