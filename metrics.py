def calculate_mae(actual_counts, predicted_counts):
    if len(actual_counts) != len(predicted_counts):
        raise ValueError("actual_counts and predicted_counts must have the same length")
    if len(actual_counts) == 0:
        raise ValueError("actual_counts and predicted_counts must not be empty")
    total_error = 0.0
    for actual, predicted in zip(actual_counts, predicted_counts):
        total_error += abs(actual - predicted)
    return total_error / len(actual_counts)
