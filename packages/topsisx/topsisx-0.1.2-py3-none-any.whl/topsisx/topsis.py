import numpy as np
import pandas as pd

def topsis(data, weights, impacts):
    """
    Perform TOPSIS (Technique for Order of Preference by Similarity to Ideal Solution).

    Parameters:
    - data: Pandas DataFrame or 2D list/array with numerical criteria values.
    - weights: List of criteria weights (should sum to 1 or will be normalized).
    - impacts: List of '+' (benefit) or '-' (cost) for each criterion.

    Returns:
    - DataFrame with scores and ranks.
    """

    # Convert to DataFrame if needed
    if isinstance(data, (list, np.ndarray)):
        data = pd.DataFrame(data)
    elif not isinstance(data, pd.DataFrame):
        raise ValueError("Input data must be a DataFrame, list, or NumPy array.")

    # Validate weights
    weights = np.array(weights, dtype=float)
    if weights.sum() != 1:
        weights = weights / weights.sum()

    # Validate impacts
    impacts = [1 if i == '+' else -1 for i in impacts]
    if len(impacts) != data.shape[1]:
        raise ValueError("Impact list must match number of criteria.")

    # Step 1: Normalize data
    norm_data = data / np.sqrt((data ** 2).sum())

    # Step 2: Apply weights
    weighted_data = norm_data * weights

    # Step 3: Determine ideal & anti-ideal
    ideal_best = weighted_data.max() * impacts
    ideal_worst = weighted_data.min() * impacts

    # Step 4: Calculate distances
    dist_best = np.sqrt(((weighted_data - ideal_best) ** 2).sum(axis=1))
    dist_worst = np.sqrt(((weighted_data - ideal_worst) ** 2).sum(axis=1))

    # Step 5: Calculate similarity scores
    scores = dist_worst / (dist_best + dist_worst)

    # Step 6: Rank alternatives
    ranks = scores.rank(ascending=False).astype(int)

    result = data.copy()
    result['Topsis Score'] = scores
    result['Rank'] = ranks

    return result.sort_values(by='Rank')
