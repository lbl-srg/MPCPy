from __future__ import division
from simulate_queue import simulate_queue
from parameter_inference import param_inference
import numpy as np
import matplotlib.pyplot as plt
import pdb
import scipy.io
from adaptive_breakpoint_placement import adaptive_breakpoint_placement
from interp1 import interp1
from unique_last import unique_last
from parameter_inference_given_segments import parameter_inference_given_segment
from tempfile import TemporaryFile


mat = scipy.io.loadmat('lab_spring_2010_occupancy.mat')

data = mat['hist_occupancy_list'][0][6][0:4,:] # 6th day in a weeks, 0:4 out of all for training


# seg_point = adaptive_breakpoint_placement(data,100)
data_mean = np.mean(data,axis=0)

# print seg_point
# plt.plot(data_mean)
# plt.scatter(seg_point,data_mean[seg_point],s = 20)
# plt.show()

outfile = 'temp.npy'
# np.save(outfile, seg_point)

##### learn the arrival and departure rates for each segment


seg_point = np.sort(np.load(outfile))
val_size = 4
seg_num = len(seg_point)+1
lam_all = np.empty((seg_num,val_size))
mu_all = np.empty((seg_num,val_size))
presence = np.where(np.mean(data,axis=0)!=0)
empty_time = presence[0][-1]+1

for i in range(val_size):
    x = data[i,:]
    [lam_temp, mu_temp] = parameter_inference_given_segment(x, seg_point,empty_time)
    lam_all[:,i] = lam_temp
    mu_all[:,i] = mu_temp

lam = np.mean(lam_all,axis = 1)
mu = np.mean(mu_all,axis = 1)





##### monte carlo simulation using learned M/M/Inf queue model

iter_num = 100

seg_point_added = np.concatenate((np.array([0]),seg_point, np.array([len(x)])))

maxtime = 1440

lam_vec = np.empty((maxtime,))
lam_vec[:] = np.NAN
mu_vec = np.empty((maxtime,))
mu_vec[:] = np.NAN

jmptimes_mc = [None]*iter_num # create an empty list of size iter_num
syssize_mc = np.empty((maxtime,iter_num))
syssize_mc[:] = np.NAN

time_int = np.arange(maxtime)
nstart = 0

for i in range(len(seg_point_added)-1):
    lam_vec[seg_point_added[i]:seg_point_added[i+1]] = lam[i]
    mu_vec[seg_point_added[i]:seg_point_added[i+1]] = mu[i]

for iter_idx in range(iter_num):
    jmptimes, syssize = simulate_queue(maxtime, lam_vec, mu_vec, nstart, empty_time)

    if any(syssize <0):
        raise ValueError('negative syssize')

    if jmptimes == None:
        jmptimes_mc[iter_idx] = 0
        syssize_mc[:, iter_idx] = 0
    else:
        # round jmptimes to the nearest integer
        jmptimes_d, ia = unique_last(np.round(jmptimes))
        syssize_d = syssize[ia]
        if jmptimes_d[0] != 0:
            jmptimes_int = np.insert(jmptimes_d, 0, 0)
            syssize_int = np.insert(syssize_d, 0, 0)
        else:
            jmptimes_int = jmptimes_d
            syssize_int = syssize_d

        vq = interp1(jmptimes_int, syssize_int, time_int)

        jmptimes_mc[iter_idx] = jmptimes_d
        syssize_mc[:, iter_idx] = vq

prediction = np.mean(syssize_mc, axis=1)
plt.plot(prediction)
plt.plot(data_mean)
plt.show()



