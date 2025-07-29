def validate_inputs(data, weights, impacts):
    """
    Validate that weights and impacts match the number of columns in the dataset
    """
    num_criteria = data.shape[1] - 1  # Assuming first column is ID
    if len(weights) != num_criteria:
        raise ValueError(f"Number of weights ({len(weights)}) does not match number of criteria ({num_criteria}).")
    if len(impacts) != num_criteria:
        raise ValueError(f"Number of impacts ({len(impacts)}) does not match number of criteria ({num_criteria}).")
    if not all(i in ["+", "-"] for i in impacts):
        raise ValueError("Impacts must be '+' or '-' only.")
