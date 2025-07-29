import numpy as np
import pandas as pd

def ahp(pairwise_matrix):
    """
    Compute AHP weights from a pairwise comparison matrix.
    Converts fractional strings like '1/3' to float.
    """
    # Convert fractional strings (like '1/3') to float
    matrix = pairwise_matrix.applymap(lambda x: eval(str(x)) if isinstance(x, str) else x).astype(float)

    n = matrix.shape[0]
    col_sum = matrix.sum(axis=0)
    norm_matrix = matrix / col_sum
    weights = norm_matrix.mean(axis=1)
    return weights
