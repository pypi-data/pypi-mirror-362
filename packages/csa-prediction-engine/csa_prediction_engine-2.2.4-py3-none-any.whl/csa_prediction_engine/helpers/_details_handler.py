"""
CSA Relevance Engine: Details Handler Module

This module provides utility functions for extracting specific detail 
types from a list of prediction output details dictionaries. The 
functions are designed to handle different types of values such as 
scalars, column vectors, and row vectors, which are typically generated 
from multiple prediction task calls in relevance-based modeling. 

Functions
---------
gather_scalars(output_details, detail_type)
    Retrieves scalar values for a specified detail type from a list 
    of output details dictionaries.
gather_column_vectors(output_details, detail_type)
    Retrieves column vector values for a specified detail type from a 
    list of output details dictionaries.
gather_row_vectors(output_details, detail_type)
    Retrieves row vector values for a specified detail type from a 
    list of output details dictionaries.

Raises
------
AssertionError
    Raised when the specified detail type is not valid for the 
    corresponding function.

Example
-------
>>> output_details = [{'fit': 0.95, 'yhat_compound': np.array([1.2, 3.4])}, {'fit': 0.87}]
>>> gather_scalars(output_details, 'fit')
array([[0.95],
       [0.87]])

>>> gather_column_vectors(output_details, 'yhat_compound')
array([[1.2, 3.4]])

(c) 2023 - 2024 Cambridge Sports Analytics, LLC. All rights reserved.
support@csanalytics.io
"""


# Third-party library imports
import numpy as np


def gather_scalars(output_details:list, detail_type:str):
    """Retrieve detail_type scalar value keys from a list of 
    output_details dictionaries. This function is useful for 
    unpacking a scalar value from  multiple prediction task calls.

    Parameters
    ----------
    output_details : list
        List of output_details dictionaries. Each dictionary must 
        contain a <detail_type> key with a ndarray float value.
    detail_type : str
        The detail_type key to be retrieved from each dictionary. 
        E.g. 'fit' or 'yhat_compound'

    Returns
    -------
    ndarray [N-by-1]
        Column vector of detail_type values as a result of 
        Grid optimizations. If no detail_type values are found, 
        returns None.
    """
    
    
    # The following are valid scalar value types in a details dictionary
    valid_types = ['K', 'n', 'fit', 'phi', 'rho', 'yhat', 'r_star', 
                   'agreement', 'asymmetry', 'eval_type', 'lambda_sq',
                   'most_eval', 'adjusted_fit', 'fit_compound', 
                   'yhat_compound', 'r_star_percent', 
                   'outlier_influence','adjusted_fit_compound']
    
    # Check if detail_type is valid
    assert detail_type in valid_types, f"Invalid detail_type: {detail_type}. Must be one of {valid_types}"
    
    # Using list comprehension to filter and collect detail_type values
    detail_values = [
        details[detail_type] for details in output_details 
        if isinstance(details, dict) and detail_type in details and details[detail_type] is not None
    ]
    
    # Return the stacked array if detail_values is not empty, else return None
    return np.vstack(detail_values) if detail_values else None


def gather_column_vectors(output_details:list, detail_type:str):
    """Retrieve detail_type column vector keys from a list of 
    output_details dictionaries. This function is useful for 
    unpacking column vectors from multiple prediction task calls.

    Parameters
    ----------
    output_details : list
        List of output_details dictionaries. Each dictionary must 
        contain a <detail_type> key with a ndarray float value.
    detail_type : str
        The detail_type key to be retrieved from each dictionary. 
        E.g. 'weights' or 'yhat_compound'

    Returns
    -------
    ndarray [N-by-1]
        Column vector of detail_type values as a result of 
        Grid optimizations. If no detail_type values are found, 
        returns None.
    """
    
    
    # The following are valid scalar value types in a details dictionary
    valid_types = ['info_x', 'include', 'weights', 'relevance', 
                   'info_theta', 'similarity', 'weights_compound']
    
    # Check if detail_type is valid
    assert detail_type in valid_types, f"Invalid detail_type: {detail_type}. Must be one of {valid_types}"
    
    # Using list comprehension to filter and collect detail_type values
    detail_values = [
        details[detail_type] for details in output_details 
        if isinstance(details, dict) and detail_type in details and details[detail_type] is not None
    ]
    
    # Return the stacked array if detail_values is not empty, else return None
    return np.hstack(detail_values) if detail_values else None


def gather_row_vectors(output_details:list, detail_type:str):
    """Retrieve detail_type row vector keys from a list of 
    output_details dictionaries. This function is useful for 
    unpacking row vectors from multiple prediction task calls.

    Parameters
    ----------
    output_details : list
        List of output_details dictionaries. Each dictionary must 
        contain a <detail_type> key with a ndarray float value.
    detail_type : str
        The detail_type key to be retrieved from each dictionary. 
        E.g. 'weights' or 'yhat_compound'

    Returns
    -------
    ndarray [N-by-1]
        Column vector of detail_type values as a result of 
        Grid optimizations. If no detail_type values are found, 
        returns None.
    """
    
    
    # The following are row vector types in a details dictionary
    valid_types = ['rho', 'combi_compound', 'max_attributes']
    
    # Check if detail_type is valid
    assert detail_type in valid_types, f"Invalid detail_type: {detail_type}. Must be one of {valid_types}"
    
    # Using list comprehension to filter and collect detail_type values
    detail_values = [
        details[detail_type] for details in output_details 
        if isinstance(details, dict) and detail_type in details and details[detail_type] is not None
    ]
    
    # Return the stacked array if detail_values is not empty, else return None
    return np.vstack(detail_values) if detail_values else None