# Adaptive breakpoint placement algorithm
from __future__ import division
import numpy as np
import random as rd
from simulate_queue import simulate_queue
from interp1 import interp1
from parameter_inference import param_inference
from unique_last import unique_last
import matplotlib.pyplot as plt


def adaptive_breakpoint_placement(data, res, margin, n_max):
    n = 1
    valSize, l = data.shape
    seg_point = []
    stack = [(0, l)]
    stack_error = [1e6]
    presence = np.where(np.mean(data, axis = 0)!=0)
    empty_time = presence[0][-1]+1
    iter_num = 10
    flag = 1

    while n < n_max:
        print n
        # if the stack is empty, then break
        if len(stack) == 0 & flag == 0:
            break

        flag = 0


        # pop out the last segment in the stack
        left, right = stack.pop()
        err_now = stack_error.pop()

        # if the segment is too short, do not break down anymore
        if right - left < 2*margin:
            continue



        # define leftmost and rightmost breakpoints
        a = left + margin
        b = right - margin

        ind_vec = np.arange(a, b, res)
        ind_length = ind_vec.size
        err_vec = np.empty(ind_length,) # fitting error of each breakpoint
        err_vec[:] = np.NAN
        err_1 = np.empty(ind_length,) # fitting error of the first segment
        err_1[:] = np.NAN
        err_2 = np.empty(ind_length,) # fitting error of the second segment
        err_2[:] = np.NAN


        syssize_min = np.empty(ind_length,) # record the simulated time series with smallest fitting error
        lambda_mat = np.zeros((2,ind_length))
        mu_mat = np.zeros((2,ind_length))

        for j in range(ind_length):
            lambda_1_vec = []
            lambda_2_vec = []
            mu_1_vec = []
            mu_2_vec = []

            for i in range(valSize):
                x = data[i,:]
                if x[left:ind_vec[j]].size == 0:
                    raise ValueError('x[left:ind_vec[j]].size == 0')
                else:
                    lambda_1,mu_1 = param_inference(x[left:ind_vec[j]], round((left+ind_vec[j])/2), empty_time)
                if x[ind_vec[j]:right].size == 0:
                    raise ValueError('x[ind_vec[j]:right].size == 0')
                else:
                    lambda_2, mu_2 = param_inference(x[ind_vec[j]:right], round((ind_vec[j] + 1 + right) / 2),
                                                     empty_time)

                lambda_1_vec.append(lambda_1)
                lambda_2_vec.append(lambda_2)
                mu_1_vec.append(mu_1)
                mu_2_vec.append(mu_2)


            lambda_mat[0,j] = np.mean(lambda_1_vec)
            lambda_mat[1,j] = np.mean(lambda_2_vec)
            mu_mat[0,j] = np.mean(mu_1_vec)
            mu_mat[1,j] = np.mean(mu_2_vec)

            seg_point_temp = np.array([left,ind_vec[j],right])-left
            jmptimes_mc = [None]*iter_num # create an empty list of size iter_num
            syssize_mc = np.empty((right-left,iter_num))
            syssize_mc[:] = np.NAN
            maxtime = right-left
            lam = np.empty((maxtime,))
            mu = np.empty((maxtime,))

            for i in range(2):
                lam[seg_point_temp[i]:seg_point_temp[i+1]] = lambda_mat[i,j]
                mu[seg_point_temp[i]:seg_point_temp[i+1]] = mu_mat[i,j]

            time_int = np.array(range(right-left))

            if right < empty_time:
                empty_time_relative = None
            else:
                empty_time_relative = empty_time-left+1

            for iter_idx in range(iter_num):


                if left == 0:
                    nstart = 0
                else:
                    nstart = data[rd.randint(0,valSize-1),left-1]


                jmptimes,syssize = simulate_queue(maxtime,lam,mu,nstart,empty_time_relative)



                if jmptimes is None:
                    jmptimes_mc[iter_idx] = 0
                    syssize_mc[:,iter_idx] = nstart*np.ones((len(time_int),))
                else:
                    # round jmptimes to the nearest integer

                    jmptimes_d, ia  = unique_last(np.round(jmptimes))
                    syssize_d = syssize[ia]
                    if jmptimes_d[0] != 0:
                        jmptimes_int = np.insert(jmptimes_d,0,0)
                        syssize_int =  np.insert(syssize_d,0,0)
                    else:
                        jmptimes_int = jmptimes_d
                        syssize_int = syssize_d


                    vq = interp1(jmptimes_int,syssize_int,time_int)
                    jmptimes_mc[iter_idx] = jmptimes_d
                    syssize_mc[:,iter_idx] = vq


            err_vec[j] = np.linalg.norm(np.mean(syssize_mc,axis=1) \
                                        - np.mean(data[:,left:right],axis=0) ,ord=2)

            err_1[j] = np.linalg.norm(np.mean(syssize_mc[:ind_vec[j]-left,:],axis=1) \
                                      - np.mean(data[:,left:ind_vec[j]],axis=0),ord=2)
            err_2[j] = np.linalg.norm(np.mean(syssize_mc[ind_vec[j]-left:,:],axis=1) \
                                      - np.mean(data[:,ind_vec[j]:right],axis=0),ord=2)

            err_vec_min= min(err_vec[:j+1])

            if err_vec[j] == err_vec_min:
                syssize_min = np.mean(syssize_mc,axis=1)




        # if all elements in the error vector is larger than the fitting error without further segmenting
        # then terminate segmentation

        if all(err_vec >= err_now) & (right-left+1 < 200):
            continue

        min_ind_vec = np.where(np.logical_and(err_vec == min(err_vec),\
                                              np.logical_and(np.not_equal(lambda_mat[0,:],lambda_mat[1,:]), \
                                                             np.not_equal(mu_mat[0,:], mu_mat[1,:]))))

        if min_ind_vec[0].size == 0:
            if left < empty_time & right > empty_time:
                seg_point.append(empty_time)
            continue

        min_ind = min_ind_vec[rd.randint(0,len(min_ind_vec)-1)]



        if ind_vec[min_ind][0] > empty_time:
            seg_point.append(empty_time)
            continue
        else:
            seg_point.append(ind_vec[min_ind][0])


        # push the two new segments associated witht he new segment point into the stack
        if err_1[min_ind][0]>0:
            stack.append((left,ind_vec[min_ind][0]))
            stack_error.append(err_1[min_ind][0])

        if err_2[min_ind][0]>0:
            stack.append((ind_vec[min_ind][0]+1,right))
            stack_error.append(err_2[min_ind][0])


        n += 1
        print n

        # x_mean = np.mean(data,axis=0)

        # fig = plt.figure()
        # plt.plot(x_mean)
        # plt.scatter(seg_point, x_mean[seg_point], s=20, color='red')
        # plt.plot(np.arange(left,right),syssize_min)
        # plt.show()
        #
        # plt.close(fig)
    return seg_point

