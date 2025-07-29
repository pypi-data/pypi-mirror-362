import numpy as np

def entropy_weights(matrix):
    """
    Compute weights automatically using entropy method.
    """
    matrix = np.array(matrix, dtype=float)
    m, n = matrix.shape
    P = matrix / matrix.sum(axis=0)
    E = -np.nansum(P * np.log(P + 1e-12), axis=0) / np.log(m)
    d = 1 - E
    weights = d / d.sum()
    return weights
