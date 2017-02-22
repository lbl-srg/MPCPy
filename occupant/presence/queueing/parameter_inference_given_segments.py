import numpy as np
from parameter_inference import param_inference

def parameter_inference_given_segment(x, seg_point, empty_time):
    if any(x <0):
        neg_ind = np.where(x <0)
        raise ValueError('negative occupancy')

    segs = np.concatenate((np.array([0]),seg_point, np.array([len(x)])))
    lam_vec = np.empty((len(segs)-1,))
    mu_vec = np.empty((len(segs)- 1,))

    for i in range(1,len(segs)-1):
        x_seg = x[segs[i-1]:segs[i]]
        h = segs[i]
        [lam_vec[i-1],mu_vec[i-1]] = param_inference(x_seg,h,empty_time)
    return lam_vec,mu_vec