"""
CSA Relevance Engine: Threaded Predictions Module

This module provides multi-threaded functions to interact with Cambridge 
Sports Analytics' API asynchronously. It leverages the `psrlib` library 
to manage input aggregation, upload, and result retrieval for various 
relevance-based prediction models. The module uses a pool of threads 
to handle multiple prediction tasks concurrently, allowing efficient 
execution of batch jobs.

Available Functions
-------------------
- `run_multi_y`: Runs multiple prediction tasks, each corresponding 
  to a different set of dependent variables (`y`), while keeping 
  the independent variables (`X`) and circumstances (`theta`) fixed.
- `run_multi_theta`: Runs multiple prediction tasks, each corresponding 
  to a different set of circumstances (`theta`), while keeping the 
  dependent variables (`y`) and independent variables (`X`) fixed.

Dispatcher Map
--------------
The module uses a dispatcher mapping (`_DISPATCHER_MAP`) to route the 
appropriate task function based on the `PSRFunction` type provided 
(e.g., `PSR`, `MAXFIT`, `GRID`, `GRID_SINGULARITY`). The dispatchers 
are responsible for handling the respective prediction tasks.

Usage
-----
The end-user functions, such as `predict_grid` and `predict_maxfit`, 
call the internal threading logic to execute multiple prediction jobs 
simultaneously. 

(c) 2023 - 2024 Cambridge Sports Analytics, LLC. All rights reserved.
support@csanalytics.io
"""


# Third-party library imports
from numpy import ndarray
import time

# Local application/library-specific imports
from csa_common_lib.enum_types.functions import PSRFunction
from csa_common_lib.classes.prediction_options import PredictionOptions
from csa_common_lib.classes.prediction_receipt import PredictionReceipt
from csa_common_lib.toolbox import _notifier
from csa_common_lib.toolbox.concurrency.parallel_helpers import get_process_limit as _par_limit
from csa_common_lib.toolbox.concurrency.parallel_executor import run_tasks_api
from csa_prediction_engine.helpers._payload_handler import route_X_input
from csa_prediction_engine.parallel._dispatchers import (
    dispatch_grid_task,
    dispatch_grid_singularity_task,
    dispatch_maxfit_task,
    dispatch_psr_task,
    dispatch_get_results
)

# Dispatcher mapping based on PSRFunction type.
# Maps different prediction tasks to their corresponding dispatcher functions.
_DISPATCHER_MAP = {
    PSRFunction.GRID: dispatch_grid_task,
    PSRFunction.GRID_SINGULARITY: dispatch_grid_singularity_task,
    PSRFunction.MAXFIT: dispatch_maxfit_task,
    PSRFunction.PSR: dispatch_psr_task
}


def run_multi_y(model_type:PSRFunction, y_matrix:ndarray, X:ndarray, theta:ndarray,
                Options:PredictionOptions, is_return_receipt:bool=False):
    """
    Entry point for running multiple prediction tasks stratified by 
    y (dependent variables).
    
    Parameters
    ----------
    model_type : PSRFunction
        Type of prediction model (PSR, MAXFIT, GRID, or GRID_SINGULARITY).
    y_matrix : ndarray [N-by-Q]
        Matrix of Q-column vectors of the dependent variable (prediction tasks).
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta : [1-by-K]
        Row vector of circumstances.
    Options : PredictionOptions
        Base class object containing all optional inputs.
        Use MaxFitOptions and GridOptions where applicable (inherits
        from PredictionOptions).
        
    Returns
    -------
    yhat : ndarray [Q-by-T]
        Prediction outcomes for Q-number of prediction tasks
    yhat_details : dict
        Model details accesible via key-value pairs.
    """

    # Start time for prediction 
    start_time = time.time()
    
    # Route X input matrix depending on payload size
    X = route_X_input(model_type=model_type, y=y_matrix, X=X, theta=theta, Options=Options)

    # Prepare the single prediction task for PPSR
    inputs_for_post = [
        (q, "y", y_matrix, X, theta, Options) for q in range(y_matrix.shape[1])
    ]
    
    # Get the corresponding dispatcher function
    dispatcher = _DISPATCHER_MAP.get(model_type)
    
    if dispatcher is None:
        raise ValueError(f"run_multi_y: Invalid prediction model type: {model_type}")

    # Execute the prediction tasks
    yhat, yhat_details = run_tasks_api(inputs_for_post, dispatcher, 
                                       dispatch_get_results, 
                                       _par_limit(), _notifier)

    # Current time after prediction is complete
    end_time = time.time()
    prediction_duration = end_time - start_time

    # conditionla return structure so as to not alter working logic 
    if is_return_receipt:
        # Capture relevant input info and generate a receipt
        receipt = PredictionReceipt(model_type=model_type, y=y_matrix, X=X, theta=theta, options=Options,
                                    yhat=yhat, prediction_duration=prediction_duration)
        # Return receipt in addition to yhat and yhat_details
        return yhat, yhat_details, receipt
    
    else:
         # Else, maintain normal return structure
         return yhat, yhat_details


def run_multi_theta(model_type:PSRFunction, y:ndarray, X:ndarray, theta_matrix:ndarray,
                    Options:PredictionOptions, is_return_receipt:bool=False):
    """
    Entry point for running multiple prediction tasks stratified by 
    theta (prediction circumstances).

    Parameters
    ----------
    model_type : PSRFunction
        Type of prediction model (PSR, MAXFIT, GRID, or GRID_SINGULARITY).
    y : ndarray [N-by-1]
        Column-vector of the dependent variable.
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta_matrix : [Q-by-K]
        Matrix of Q-row vectors of circumstances.
    Options : PredictionOptions
        Base class object containing all optional inputs.
        Use MaxFitOptions and GridOptions where applicable (inherits
        from PredictionOptions).
        
    Returns
    -------
    yhat : ndarray [Q-by-T]
        Prediction outcomes for Q-number of prediction tasks
    yhat_details : dict
        Model details accesible via key-value pairs.
    """

    # Start time for prediction 
    start_time = time.time()

    # Route X input matrix depending on payload size
    X = route_X_input(model_type=model_type, y=y, X=X, theta=theta_matrix, Options=Options)
           
    # Prepare the single prediction task stratified by circumstances (theta)
    inputs_for_post = [
        (q, "theta", y, X, theta_matrix, Options) for q in range(theta_matrix.shape[0])
    ]
    
    # Get the corresponding dispatcher function
    dispatcher = _DISPATCHER_MAP.get(model_type)
    
    if dispatcher is None:
        raise ValueError(f"run_multi_y: Invalid model type: {model_type}")

    # Execute the prediction tasks
    yhat, yhat_details = run_tasks_api(inputs_for_post, dispatcher, 
                                       dispatch_get_results, 
                                       _par_limit(), _notifier)
    

    # Current time after prediction is complete
    end_time = time.time()
    prediction_duration = end_time - start_time

    # conditionla return structure so as to not alter working logic 
    if is_return_receipt:
        # Capture relevant input info and generate a receipt
        receipt = PredictionReceipt(model_type=model_type, y=y, X=X, theta=theta_matrix, options=Options,
                                    yhat=yhat, prediction_duration=prediction_duration)
        # Return receipt in addition to yhat and yhat_details
        return yhat, yhat_details, receipt
    
    else:
         # Else, maintain normal return structure
         return yhat, yhat_details
