from __future__ import division
import numpy as np
import pdb

def param_inference(x,h,empty_time):
    # Input: x - data (np array)
    #        h - hour
    #        empty_time - the time when the space is known to be empty

    t = x.size
    pos = np.where(x != 0)[0] # assume x[0] must be zero?
    A = 0 # arrival count
    for i in range(len(pos)):
        if pos[i] == 0:
            continue
        if x[pos[i]-1] < x[pos[i]]:
            A += x[pos[i]]-x[pos[i]-1]

    D = 0 # departure count
    for i in range(2,t):
        if x[i-1] > x[i]:
            D += x[i-1]-x[i]
    lam = A/t;
    queue_length = sum(x)
    if queue_length == 0:
        if h > empty_time:
            mu = 100
        else:
            mu = 0
    else:
        mu = D/queue_length

   # pdb.set_trace()
    return lam, mu