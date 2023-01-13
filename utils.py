import numpy as np

def normalise(vector:np.ndarray):
    if magnitude := np.sqrt(np.sum(vector**2)):
        return vector/magnitude
    return vector

def zero_vector():
    return np.zeros([2],dtype='float')

def distance(v1,v2):
    return np.sqrt(np.sum((v2-v1)**2))