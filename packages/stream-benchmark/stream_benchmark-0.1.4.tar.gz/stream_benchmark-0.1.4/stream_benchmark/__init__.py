import stream_benchmark.evals as evals
import numpy as np

tasks = [
    'sinus_forecasting',
    'chaotic_forecasting',
    'discrete_postcasting',
    'continuous_postcasting',
    'discrete_pattern_completion',
    'continuous_pattern_completion',
    'bracket_matching',
    'simple_copy',
    'selective_copy',
    'adding_problem',
    'sorting_problem',
    'sequential_mnist',
]

def compute_score(Y, Y_hat, prediction_timesteps, classification):
    """
    Compute the accuracy of the model.

    Parameters:
    - Y (np.ndarray): Target array [B, T, O]
    - Y_hat (np.ndarray): Predicted array [B, T, O]
    - prediction_timesteps (list): List of prediction timesteps
    - classification (bool): Whether the task is a classification task -> accuracy or MSE

    Returns:
    - accuracy (float): Accuracy value
    """
    # Make sure Y_hat and Y are numpy arrays
    if not isinstance(Y_hat, np.ndarray) or not isinstance(Y, np.ndarray):
        Y = np.array(Y, dtype=np.float32)
        Y_hat = np.array(Y_hat, dtype=np.float32)

    # Select only the prediction timesteps
    preds = []
    truths = []
    for j in range(Y.shape[0]):
        preds.append(Y_hat[j, prediction_timesteps[j], :])
        truths.append(Y[j, prediction_timesteps[j], :])

    if classification:
        # Compute the accuracy
        preds = np.argmax(np.stack(preds, axis=0), axis=-1)  # [B, prediction_timesteps] int: class
        truths = np.argmax(np.stack(truths, axis=0), axis=-1)  # [B, prediction_timesteps] int: class
        score = np.sum(preds == truths) / (truths.shape[0] * len(prediction_timesteps[0]))
        score = 1 - score

    else:
        # Compute the MSE
        preds = np.stack(preds, axis=0).reshape(-1, Y.shape[-1])  # [B * prediction_timesteps, O] float: logits
        truths = np.stack(truths, axis=0).reshape(-1, Y.shape[-1])
        score = np.mean((preds - truths) ** 2)

    return score

def build_task(task_name, difficulty='small', seed=None, **kwargs):
    """
    Build the task.

    Parameters:
    - task_name (str): Name of the task between 'sinus_forecasting', 'chaotic_forecasting', 'discrete_postcasting',
        'continuous_postcasting', 'discrete_pattern_completion', 'continuous_pattern_completion', 'bracket_matching',
        'simple_copy', 'selective_copy', 'adding_problem', 'sorting_problem', and 'sequential_mnist'
    - difficulty (str): Difficulty level of the task ('small', 'medium' or 'large')
    - seed (int, optional): Seed for reproducibility. Default is None.

    The other optional parameters are given as arguments in the task generation function.

    Returns:
    - Task: Task object
    """
    # Check if the task name is valid 
    if task_name not in evals.stream_small:
        raise ValueError(f"Task {task_name} not found. Available tasks are: {list(evals.stream_small.keys())}")
    # Check if the difficulty level is valid
    if difficulty not in ['small', 'medium', 'large']:
        raise ValueError("Difficulty level must be 'small', 'medium' or 'large'.")

    # Get the corresponding stream configuration
    stream = {
        'small': evals.stream_small,
        'medium': evals.stream_medium,
        'large': evals.stream_large,
    }[difficulty]

    # Get the function and parameters from the stream config
    fct = stream[task_name]['fct']
    params = stream[task_name]['params']
    params['seed'] = seed

    # Update params with optional arguments
    params |= kwargs

    # Generate the task
    return fct(**params)