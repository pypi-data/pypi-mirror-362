"""
CSA Relevance Engine: Parallel Workers Module

This module provides a set of worker functions for parallel execution of
prediction models using the Cambridge Sports Analytics (CSA) API.
Each worker function handles a specific prediction model type, allowing
for efficient, multi-threaded execution of posting payloads from the 
local workstation.

The available worker functions include:
    - _grid_predict_worker: Executes a Grid model prediction task.
    - _grid_singularity_worker: Executes a Grid Singularity model prediction task.
    - _maxfit_predict_worker: Executes a maximum fit prediction task.
    - _predict_worker: Executes a standard relevance-based prediction task.
    
For end-user use, please refer to the high-level functions provided 
in the corresponding threaded_predictions module.

(c) 2023 - 2024 Cambridge Sports Analytics, LLC. All rights reserved.
support@csanalytics.io
"""


# Standard library imports
import threading

# Third-party library imports
from numpy import ndarray

# Import prediction options classes from the common library
from csa_common_lib.classes.prediction_options import (
        PredictionOptions,
        MaxFitOptions,
        GridOptions
    )


# Import concurrency utilities for parallel processing
from csa_common_lib.toolbox.concurrency.parallel_helpers import (
        slice_matrices,
        thread_safe_print
    )


# Import prediction-related functions from the local psrlib module
from csa_prediction_engine.helpers._postmaster import (
        _post_grid_inputs,              # Function to post grid prediction inputs
        _post_grid_singularity_inputs,  # Function to post grid singularity inputs
        _post_maxfit_inputs,            # Function to post maxfit inputs
        _post_predict_inputs,           # Function to post predict inputs
        _get_results                    # Function to retrieve results for a given job id
    )


# Create a single lock to synchronize print statements across threads
PRINT_LOCK = threading.Lock()


def _psr_predict_worker(q:int, slice_type:str, y_matrix:ndarray, X:ndarray, 
                    theta_matrix:ndarray, Options:PredictionOptions):
    """
    Executes a single relevance-based prediction task.

    This function runs a single prediction task using the CSA API
    relevance-based model. It is executed as part of a multi-threaded workflow.

    Parameter
    ----------
    q : int
        Slice index counter, see also slice_type
    slice_type : str
        Slice type, either "y" or "theta". Indicates whether the 
        asynchronous parent will be iterating over Q-prediction tasks
        stratifying y or theta (not both).
    y_matrix : ndarray [N-by-1 or N-by-Q]
        Column vector or matrix of dependent variable(s).
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta_matrix : ndarray [1-by-K or Q-by-K]
        Row vector or matrix of circumstances.
    Options : PredictionOptions
        Options object that contains the necessary key-value parameters
        for grid predictions.

    Returns
    -------
    int
        Job id from database/server.
    str
        Job code from database/server.
    """    
    
    # Extract the relevant (pun-intended) y and theta vectors for a single task
    y, theta = slice_matrices(q, slice_type, y_matrix, theta_matrix, X)
    _worker_progress_printout(q, theta_matrix)
    
    # Call relevance-based predict for a single task and send inputs to CSA's API
    job_id, job_code = _post_predict_inputs(y=y, X=X, theta=theta, Options=Options)
    
    # Return the job_id and job_code from the server
    return job_id, job_code


def _maxfit_predict_worker(q:int, slice_type:str, y_matrix:ndarray, 
                           X:ndarray, theta_matrix:ndarray, 
                           Options:MaxFitOptions):
    """
    Executes a single maximum fit prediction task.

    This function runs a single prediction task using the CSA API 
    maximum fit model. It is executed as part of a multi-threaded workflow.

    Parameters
    ----------
    q : int
        Slice index counter, see also slice_type
    slice_type : str
        Slice type, either "y" or "theta". Indicates whether the 
        asynchronous parent will be iterating over Q-prediction tasks
        stratifying y or theta (not both).
    y_matrix : ndarray [N-by-1 or N-by-Q]
        Column vector or matrix of dependent variable(s).
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta_matrix : ndarray [1-by-K or Q-by-K]
        Row vector or matrix of circumstances.
    Options : MaxFitOptions
        Options object that contains the necessary key-value parameters
        for grid predictions.

    Returns
    -------
    int
        Job id from database/server.
    str
        Job code from database/server.
    """    
    
    # Extract the relevant (pun-intended) y and theta vectors for a single task
    y, theta = slice_matrices(q, slice_type, y_matrix, theta_matrix, X)
    _worker_progress_printout(q, theta_matrix)

    # Call maxfit prediction for a single task and send inputs to CSA's API
    job_id, job_code = _post_maxfit_inputs(y=y, X=X, theta=theta, Options=Options)
    
    # Return the job_id and job_code from the server
    return job_id, job_code


def _grid_predict_worker(q:int, slice_type:str, y_matrix:ndarray, 
                         X:ndarray, theta_matrix:ndarray, Options:GridOptions):
    """
    Executes a single Grid model prediction task.

    This function runs a single prediction task using the CSA API 
    Grid model. It is executed as part of a multi-threaded workflow.

    Parameters
    ----------
    q : int
        Slice index counter, see also slice_type
    slice_type : str
        Slice type, either "y" or "theta". Indicates whether the 
        asynchronous parent will be iterating over Q-prediction tasks
        stratifying y or theta (not both).
    y_matrix : ndarray [N-by-1 or N-by-Q]
        Column vector or matrix of dependent variable(s).
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta_matrix : ndarray [1-by-K or Q-by-K]
        Row vector or matrix of circumstances.
    Options : GridOptions
        Options object that contains the necessary key-value parameters
        for grid predictions.

    Returns
    -------
    int
        Job id from database/server.
    str
        Job code from database/server.
    """    
    
    # Extract the relevant (pun-intended) y and theta vectors for a single task
    y, theta = slice_matrices(q, slice_type, y_matrix, theta_matrix, X)
    _worker_progress_printout(q, theta_matrix)
    
    # Call grid prediction for a single task and send inputs to CSA's API
    job_id, job_code = _post_grid_inputs(y=y, X=X, theta=theta, Options=Options)

    # Return job_id and job_code
    return job_id, job_code


def _grid_singularity_worker(q:int, slice_type:str, y_matrix:ndarray, 
                             X:ndarray, theta_matrix:ndarray, Options:GridOptions):
    """
    Executes a single Grid Singularity model prediction task.

    This function runs a single prediction task using the CSA API 
    Grid Singularity model. It is executed as part of a multi-threaded workflow.

    Parameters
    ----------
    q : int
        Slice index counter, see also slice_type
    slice_type : str
        Slice type, either "y" or "theta". Indicates whether the 
        asynchronous parent will be iterating over Q-prediction tasks
        stratifying y or theta (not both).
    y_matrix : ndarray [N-by-1 or N-by-Q]
        Column vector or matrix of dependent variable(s).
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta_matrix : ndarray [1-by-K or Q-by-K]
        Row vector or matrix of circumstances.
    Options : GridOptions
        Options object that contains the necessary key-value parameters
        for grid predictions.

    Returns
    -------
    int
        Job id from database/server.
    str
        Job code from database/server.
    """    
    
    # Extract the relevant (pun-intended) y and theta vectors for a single task
    y, theta = slice_matrices(q, slice_type, y_matrix, theta_matrix, X)
    _worker_progress_printout(q, theta_matrix)

    # Call grid singularity for a single task and send inputs to CSA's API
    job_id, job_code = _post_grid_singularity_inputs(y=y, X=X, theta=theta, Options=Options)

    # Return job_id and job_code
    return job_id, job_code


def _get_results_worker(job_id:int, job_code:str):
    """
    Executes retrieval of results from the CSA server. It is executed 
    as part of a multi-threaded workflow.

    Parameters
    ----------
    job_id : int
        Job id on server / database.
    job_code : str
        Job code on server / database.

    Returns
    -------
    yhat : ndarray
        Prediction outcome(s).
    output_details : dict
        Model details accesible via key-value pairs.
    """    
    
    # Get the results from CSA API
    #thread_safe_print(f"Retrieving results for job_id {job_id}.", PRINT_LOCK)
    yhat, output_details = _get_results(job_id, job_code)
    
    # Return results object
    return yhat, output_details


def _worker_progress_printout(q:int, theta_matrix):
    """Prints out progress updates to the user from the terminal

    Parameters
    ----------
    q : int
        Slice index counter, see also slice_type
    theta_matrix : ndarray [1-by-K or Q-by-K]
        Row vector or matrix of circumstances.
        
    """

    thread_safe_print(
        f"CSA Prediction Tasks: {q+1}/{theta_matrix.shape[0]} submitted; 0/{theta_matrix.shape[0]} processed; 0/{theta_matrix.shape[0]} failed; 0/{theta_matrix.shape[0]} retrieved.",
        PRINT_LOCK
    )