"""
CSA Router Module

This module provides routing utility function(s) for classifying 
prediction tasks based on the dimensions of the input data. It 
categorizes the task as either a single prediction, a multi-y 
prediction (multiple dependent variables), or a multi-theta prediction 
(multiple circumstances). The determined task type is returned as an 
enumerated value from the `JobType` enum.

(c) 2023 - 2024 Cambridge Sports Analytics, LLC. All rights reserved.
support@csanalytics.io
"""

# Third-party library imports
from numpy import ndarray  # Importing the ndarray class from NumPy for type annotations

# Local application/library specific imports
from csa_common_lib.enum_types.job_types import JobType  # Importing JobType enumeration for task type classification


def determine_task_type(y: ndarray, X: ndarray, theta: ndarray):
    """
    Determine the task type based on the input data dimensions.

    This function evaluates the dimensions of the input data (`y`, `X`)
    and the prediction circumstances (`theta`) to determine the type of 
    prediction task to be performed. It distinguishes between single prediction 
    tasks, multi-y tasks (batch prediction over multiple dependent variables), 
    and multi-theta tasks (batch prediction over multiple circumstances).

    Parameters
    ----------
    y : np.ndarray [N-by-1] or [N-by-Q]
        Column vector or matrix of  dependent variable(s)
    X : np.ndarray [N-by-K]
        Matrix of independent variables.
    theta : np.ndarray [1-by-K] or [Q-by-K]
        Row vector or matrix of the prediction circumstances.

    Returns
    -------
    JobType
        The type of prediction task: either 
            `JobType.SINGLE` for single predictions, 
            `JobType.MULTI_Y` for multi-y tasks, or
            `JobType.MULTI_THETA` for multi-theta tasks.

    Raises
    ------
    ValueError
        If the dimensions of `y`, `X`, and `theta` do not match 
        the expected shapes, or if both multi-y and multi-theta tasks 
        are specified simultaneously.
    """
    
    # Get the dimensions of y, X, and theta
    X_rows, X_columns = X.shape    
    y_rows, y_columns = y.shape    
    theta_rows, theta_columns = theta.shape
    
    # Ensure the number of samples in y and X match
    if X_rows != y_rows:
        raise ValueError("GURU MEDITATION ERROR 48: The number of rows in y and X must be the same.")
    
    # Ensure the number of features in X and theta match
    if theta_columns != X_columns:
        raise ValueError("GURU MEDITATION ERROR 52: The number of columns in theta and the number of columns in X must be the same.")
    
    # Check for invalid combination of multi-y and multi-theta
    if y_columns > 1 and theta_rows > 1:
        raise ValueError(
            "GURU MEDITATION ERROR 57: y cannot have multiple columns "
            "and theta cannot have multiple rows at the same time. "
            "This indicates both multi-y and multi-theta are specified. "
            "Only one job type can be set at a time."
        )

    # Determine task type based on dimensions
    if theta_rows > 1 and y_columns == 1:
        # Multi-theta task: multiple parameter sets, single target variable
        return JobType.MULTI_THETA
    elif y_columns > 1 and theta_rows == 1:
        # Multi-y task: single parameter set, multiple target variables
        return JobType.MULTI_Y
    elif y_columns == 1 and theta_rows == 1:
        # Single task: single parameter set, single target variable
        return JobType.SINGLE
    else:
        # Catch-all error for unexpected dimension configurations
        raise ValueError(
            "GURU MEDITATION ERROR 76: Invalid job type. "
            "Please check dimensions of y, X, and theta."
        )