import numpy as np


def decimateData(array):
    x = np.array(array)
    x = np.delete(x,np.array(0,x.size,2))
    return x