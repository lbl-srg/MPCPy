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
import sklearn.metrics as sklm

year = '2012'
for day in range(1,7):
    filename_train = year + '_train_' + str(day) + '.npy'
    filename_test = year + '_test_' + str(day) + '.npy'
    data_train = np.load(filename_train)
    print(data_train)
    data_test = np.load(filename_test)
    data_train_mean = np.mean(data_train,axis=0)
    data_test_mean = np.mean(data_test,axis=0)

    # how much the mean of training dataset deviates from the testing dataset
    # plt.plot(data_train_mean,label='Mean value of training data')
    # plt.plot(data_test_mean,label='Mean value of testing data')
    # plt.legend()
    # plt.show()


    # obtain the points that segment the day into some homogeneous pieces
    seg_point = adaptive_breakpoint_placement(data_train,res=3, margin=3, n_max=24)




    print 'breakpoints are ', seg_point



    outfile = 'temp.npy'
    np.save(outfile, seg_point)

    ##### learn the arrival and departure rates for each segment


    seg_point = np.sort(np.load(outfile))
    val_size = 6
    seg_num = len(seg_point)+1
    lam_all = np.empty((seg_num,val_size))
    mu_all = np.empty((seg_num,val_size))
    presence = np.where(np.mean(data_train,axis=0)!=0)
    empty_time = presence[0][-1]+1

    for i in range(val_size):
        x = data_train[i,:]
        [lam_temp, mu_temp] = parameter_inference_given_segment(x, seg_point,empty_time)
        lam_all[:,i] = lam_temp
        mu_all[:,i] = mu_temp

    lam = np.mean(lam_all,axis = 1)
    mu = np.mean(mu_all,axis = 1)

    print 'mu is ', mu
    print 'lambda is ', lam



    ##### monte carlo simulation using learned M/M/Inf queue model

    iter_num = 100

    seg_point_added = np.concatenate((np.array([0]),seg_point, np.array([data_train.shape[1]])))

    maxtime = 288

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


        if syssize is None:
            jmptimes_mc[iter_idx] = None
            syssize_mc[:, iter_idx] = np.zeros((maxtime,))
            continue

        if np.any(syssize <0):
            pdb.set_trace()
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

    offset = sklm.mean_squared_error(data_train_mean,data_test_mean)
    fitting_error = sklm.mean_squared_error(data_train_mean,prediction)
    prediction_error = sklm.mean_squared_error(data_test_mean,prediction)

    print str(day)
    print 'Offset', offset
    print 'Fitting error', fitting_error
    print 'Prediction error', prediction_error

    std = np.std(syssize_mc, axis=1);
    prediction_pstd = prediction+std;
    prediction_mstd = prediction-std;
    prediction_mstd = (prediction_mstd>=0)*prediction_mstd;
    time= range(len(prediction));
    hours = [h/12 for h in time];
    
    plt.plot(hours, prediction,label='prediction', color = 'r')
    plt.plot(hours, prediction_pstd, color = 'r', alpha = 0.5)    
    plt.plot(hours, prediction_mstd, color = 'r', alpha = 0.5)      
    plt.fill_between(hours, prediction_pstd, prediction_mstd, color = 'r', alpha = 0.15)
    plt.plot(hours, data_train_mean,label='training data average', color = 'k')
    plt.plot(hours, data_test_mean,label='test data average', color = 'b')
    # plt.scatter(seg_point,data_train_mean[seg_point],s = 40,color = 'red')
    plt.legend()
    plt.show()



