

# modify the built-in function "unique"
# To handle the case where there are more than one jump during 1 minute interval

import numpy as np


def unique_last(x):
    C, ia, ic = np.unique(x,return_index=True,return_inverse=True)
    ic_unique = np.unique(ic)
    for i in range(len(ic_unique)):
        ic_idx = np.where(ic == ic_unique[i])
        ic_idx_last = ic_idx[0][-1]
        ic_idx_first = ic_idx[0][0]
        ia_idx = np.where(ia == ic_idx_first)
        ia[ia_idx] = ic_idx_last
    ia = np.sort(ia)
    return C,ia
