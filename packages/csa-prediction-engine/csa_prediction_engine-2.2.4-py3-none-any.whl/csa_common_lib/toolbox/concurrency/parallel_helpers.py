# Standard library imports
import os # To get the number of available CPU cores
import threading # For creating and managing threads

# Third-party library imports
import numpy as np # For numerical computations and array operations

# Local application-specific imports
from csa_common_lib.toolbox._validate import _validate_ndarray # For validation of ndarray inputs


def get_process_limit():
    """Get the process limits based on the CPU power.

    Returns
    -------
    int
    The process limit
    """    

    # Initialize the default number of threads
    max_threads = 1
    
    # Get the number of CPUs hyper threads available
    num_cpus = os.cpu_count()
    
    # Set the number of maximum threads available
    # Allow 2 cores for OS and main application.
    max_threads = max(1, min(num_cpus - 2, 10))
    
    # Return
    return max_threads    
    

def thread_safe_print(message: str, print_lock:threading.Lock):
    """
    Thread-safe print function.

    Ensures that the provided message is printed to the console without
    interference from other threads by using the specified lock.

    Parameters
    ----------
    message : str
        The message to be printed to the console.
    print_lock : threading.Lock
        A threading lock used to synchronize access to the print statement.
    """
    with print_lock:
        print(f"\r{message}", end='', flush=True)


def slice_matrices(q:int, slice_type:str, y_matrix, theta_matrix, X):
    """ Slices either the y_matrix or theta_matrix based on the specified
    slice_type and q index. The slice_type can be either "y" or "theta".
    The q index specifies which column or row of the matrix to extract
    and corresponds to a prediction task the parent caller is working on.
    
    Parameters
    ----------
    q : int
        Prediction task index.
    slice_type : str
        Slice type, either "y" or "theta". Indicates whether the 
        asynchronous parent will be iterating over Q-prediction tasks
        stratifying y or theta (not both).
    y_matrix : ndarray
        Column vector or matrix of dependent variable(s).
    theta_matrix : ndarray
        Row vector or matrix of circumstances.
    X : ndarray
        Matrix of independent variables

    Returns
    -------
    ndarray [N-by-1]
        Column vector of dependent variable (y).
    ndarray [1-by-K]
        Row vector of circumstances (theta).

    Raises
    ------
    ValueError
        If dimensions of sliced matrices are incorrect. This typically
        happens if q or input variables are specified incorrectly.
    """    
    
    
    # Initialize output variables
    y = None
    theta = None
    
    match slice_type.lower():
        case "y":
            # Extract the q-th column vector from y_matrix
            y = np.atleast_2d(y_matrix[:, q])
            theta = np.atleast_2d(theta_matrix)
        
        case "theta":
            y = np.atleast_2d(y_matrix)
            # Extract the q-th row vector from theta_matrix
            theta = np.atleast_2d(theta_matrix[q])
        
        case _:
            raise ValueError("psrlib_async:slice_matrices:Invalid slice_type")
    
    # Get the number of variables
    num_obs, num_var = y_matrix.shape[0], theta_matrix.shape[1]
    
    # Ensure that theta is a row vector
    if not _validate_ndarray(theta, 1, num_var):
        raise ValueError("psrlib_async:slice_matrices:Theta argument must be a row vector of length X.shape[1].")  
    
    # Ensure that y is a column vector
    if not _validate_ndarray(y, num_obs, 1):
        raise ValueError("psrlib_async:slice_matrices:y argument must be a column vector of length X.shape[0].")
    
    # Return y column vector and a theta row vector
    return y, theta

def get_results_progress(processing_jobs, failed_jobs:int):
        """Progress printout of get-jobs results collection.

        Parameters
        ----------
        processing_jobs : list
            List of booleans describing the number of jobs currently 
            being processed
        """

        num_processing = processing_jobs.count(True)
        num_completed = processing_jobs.count(False)
        total_jobs = len(processing_jobs)
        
        # Calculate percentages
        percent_processing = (num_processing / total_jobs) * 100
        percent_completed = (num_completed / total_jobs) * 100
        percent_failed = (failed_jobs / total_jobs) * 100
        
        # Print the progress
        print(
            f"\rCSA Prediction Tasks: {total_jobs}/{total_jobs} submitted; {total_jobs-num_processing}/{total_jobs} processed; {failed_jobs}/{total_jobs} failed; {num_completed}/{total_jobs} retrieved.", end='')