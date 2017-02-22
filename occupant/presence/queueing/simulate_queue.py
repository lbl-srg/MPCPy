from __future__ import division
import numpy as np
import pdb
from unique_last import unique_last
import matplotlib.pyplot as plt
import warnings



def simulate_queue(maxtime,lam,mu,nstart,empty_time):
    # Function for simulate queue system size given the queue parameters
    # Inputs: maxtime - the time range for simualtion
    # lam - arrival rate (vector for nonhomogeneous queue), a numpy array
    # mu - departure rate (vector for nonhomogeneous queue), a numpy array
    # nstart - the number of customers in the system at the beginning of simulation
    # empty_time - the time when the queue system is known to have zero customer


    # First, generate arrivals from homogeneous Poisson process with parameter 1
    lam_max = max(lam)
    # with warnings.catch_warnings():
    #     warnings.filterwarnings('error')
    #
    #     try:
    #         lam = lam/lam_max
    #     except Warning as e:
    #         pdb.set_trace()
    #         print('error found:',e)
    if lam_max == 0:
        jmptimes = None
        syssize = None
        return jmptimes,syssize
    else:
        lam = lam/lam_max


    # print 'lambda is', lam

    npoints = np.random.poisson(maxtime*lam_max)

    # Given that the number of arrivals is npoints, the arrivals are distributed uniformly
    if npoints>0:
        arrtimes = np.sort(np.random.uniform(0,1,npoints)*maxtime)
    else:
        jmptimes = None
        syssize = None
        return jmptimes,syssize

    # the actual non-homogenous arrival rate at the arrival events
    arrtimes_floor = np.floor(arrtimes).astype(int)
   # pdb.set_trace()
    lam_vec = lam[arrtimes_floor]


    # the set of accepted events
    r = np.random.uniform(0,1,arrtimes.size)
    if empty_time == None: # if the segment does not contain the empty region
        E = arrtimes[np.where(r-lam_vec <0)]
    else:
        # with warnings.catch_warnings():
        #     warnings.filterwarnings('error')
        #
        #     try:
        E = arrtimes[np.where(np.logical_and(r - lam_vec < 0, arrtimes_floor < empty_time))]
            # except Warning as e:
            #     pdb.set_trace()
            #     print('error found:',e)


    if not E.size:
        jmptimes = None
        syssize = None
        return jmptimes,syssize

    # total number of customers
    E = np.insert(E,0,np.zeros((nstart,)))
    ntotal = E.size
    keeptimes = np.floor(E).astype(int)

    servtimes = []
    if not empty_time:
        for i in range(ntotal):
            serv_sample = simulate_service(keeptimes[i],mu)
            if serv_sample is None:
                serv_sample = maxtime-1
            servtimes.append(serv_sample)
    else:
        trunc_length = empty_time-keeptimes
        for i in range(ntotal):
            if trunc_length[i] == 0:
                raise NameError('Truncation length zero')
            serv_sample = simulate_service_with_trunc(keeptimes[i],mu,trunc_length[i])
            servtimes.append(serv_sample)
    servtimes_array = np.array(servtimes)
    deptimes = np.add(keeptimes,servtimes_array)

    # sort all the arrivals and departures
    arrate = np.array([np.concatenate((keeptimes,deptimes)),\
                       np.concatenate((np.ones((ntotal,)),-np.ones((ntotal,))))])
    arrate = arrate[0:2,arrate[0,:].argsort()]
    jmptimes,unique_idx = unique_last(arrate[0,:])
    syssize = np.cumsum(arrate[1,:])[unique_idx]

    # drop the events falling outside of the time window of interest
    ci = np.where(jmptimes < maxtime)
    if ci[0].size != 0:
        jmptimes = jmptimes[ci]
        syssize = syssize[ci]
        # # set the last event to be at maxtime
        # jmptimes = jmptimes.append(maxtime-1)
        # syssize = syssize.append(syssize[-1])

    return jmptimes,syssize




def simulate_service(arrtime, mu):
    mu_used = mu[arrtime:]
    mu_cum = np.cumsum(mu_used)
    cdf = 1- np.exp(-mu_cum)
    r = np.random.uniform(0,1,1)
    temp = np.where(cdf > r)
    if temp[0].size!=0:
        return temp[0][0]
    else:
        return None


def simulate_service_with_trunc(arrtime,mu,trunc_length):
    mu_used = mu[arrtime:arrtime+trunc_length]
    mu_cum = np.cumsum(mu_used)
    try:
        cdf = (1-np.exp(-mu_cum))/(1-np.exp(-mu_cum[-1]))
    except:
        pdb.set_trace()
    r = np.random.uniform(0,1,1)
    temp = np.where(cdf > r)

    try:
        answer = temp[0][0]
        return answer
    except:
        pdb.set_trace()