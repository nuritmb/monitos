import numpy as np

def shuffle_along_axis(a:np.ndarray, axis:int) -> np.ndarray:
    idx = np.random.rand(*a.shape).argsort(axis=axis)
    return np.take_along_axis(a,idx,axis=axis)