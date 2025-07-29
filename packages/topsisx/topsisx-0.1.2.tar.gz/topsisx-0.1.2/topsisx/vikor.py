import numpy as np
import pandas as pd

def vikor(matrix, weights, impacts, v=0.5):
    """
    VIKOR ranking method for multi-criteria decision-making.
    """
    matrix = np.array(matrix, dtype=float)
    weights = np.array(weights, dtype=float)

    ideal = np.max(matrix, axis=0) if impacts[0] == '+' else np.min(matrix, axis=0)
    anti_ideal = np.min(matrix, axis=0) if impacts[0] == '+' else np.max(matrix, axis=0)

    S = np.sum(weights * (ideal - matrix) / (ideal - anti_ideal), axis=1)
    R = np.max(weights * (ideal - matrix) / (ideal - anti_ideal), axis=1)
    Q = v * (S - np.min(S)) / (np.max(S) - np.min(S)) + \
        (1 - v) * (R - np.min(R)) / (np.max(R) - np.min(R))

    ranking_df = pd.DataFrame({
        'VIKOR Score': Q,
        'Rank': Q.argsort().argsort() + 1
    })
    return ranking_df
