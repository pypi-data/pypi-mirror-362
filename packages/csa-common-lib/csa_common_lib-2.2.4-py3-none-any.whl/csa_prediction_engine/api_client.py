"""
CSA Relevance Engine

This module provides a set of functions for performing relevance-based 
predictions using the Cambridge Sports Analytics (CSA) API. The relevance 
engine offers flexible prediction models that support single prediction 
tasks, multi-y prediction tasks (multiple dependent variables), and 
multi-theta prediction tasks (multiple sets of circumstances).

Key Features
------------
- **Single Task Prediction**: Supports predictions with one dependent 
  variable and one set of circumstances.
- **Multi-y Task Prediction**: Allows for predictions with multiple 
  dependent variables and a single set of circumstances.
- **Multi-theta Task Prediction**: Enables predictions with one dependent 
  variable and multiple sets of circumstances.
- **Relevance-Based Grid Prediction**: Generates optimal predictions by 
  evaluating various thresholds and variable combinations.
- **MaxFit Prediction**: Finds the best fit model based on adjusted 
  relevance.
- **Grid Singularity Prediction**: Analyzes the grid prediction to find 
  the singular optimal solution.

Important
---------
Multi-y and multi-theta tasks cannot be executed simultaneously. Please 
structure your inputs accordingly or loop through multiple calls to handle 
these cases separately.

Usage
-----
The main functions in this module include:

1. **predict**: For general relevance-based predictions.
2. **predict_maxfit**: For finding the best fit model based on relevance.
3. **predict_grid**: For generating composite predictions across various 
   thresholds.
4. **predict_grid_singularity**: For finding the singular optimal solution 
   in grid predictions.

Each function takes inputs in the form of NumPy arrays for `y`, `X`, and 
`theta`, and utilizes option classes (`PredictionOptions`, `MaxFitOptions`, 
`GridOptions`) to configure the prediction task.

(c) 2023 - 2024 Cambridge Sports Analytics, LLC. All rights reserved.
For support, please contact: support@csanalytics.io
"""

# Third-party imports
from numpy import ndarray
import time

# Local application/library specific imports
from .helpers import (
    _postmaster,  # Manages internal communication and notifications
    _router       # Routes tasks or functions based on input types
)

# Importing prediction option classes from the common library
from csa_common_lib.classes.prediction_options import (
    PredictionOptions,  # General prediction options
    MaxFitOptions,      # Options for maximum fit predictions
    GridOptions         # Options for grid-based predictions
)

# Importing enumerations from the common library
from csa_common_lib.enum_types.functions import PSRFunction  # Function type enumeration
from csa_common_lib.enum_types.job_types import JobType      # Job type enumeration
from csa_common_lib.classes.prediction_receipt import PredictionReceipt # Receipts class

# Importing single prediction task modules
from .bin import single_tasks # Module for single task predictions

# Import parallelization modules
from .parallel._threaded_predictions import (
    run_multi_theta,
    run_multi_y
)

# Use a mapping to call the appropriate function based on task type
_TASK_MAP = {
    JobType.SINGLE: single_tasks.predict,
    JobType.MULTI_THETA: run_multi_theta,
    JobType.MULTI_Y: run_multi_y
}


def predict_psr(y:ndarray, X:ndarray, theta:ndarray, Options:PredictionOptions, is_return_receipt:bool=False):
    """
    Calculates partial sample regression predictions based on relevance
    using the CSA API. 
    
    This function supports three types of prediction tasks:   
    1. Single prediction task: A single dependent variable and a single set of circumstances.
    2. Multi-y prediction task: Multiple dependent variables (y) with a single set of circumstances (theta). 
    3. Multi-theta prediction task: A single dependent variable with multiple sets of circumstances (theta).

    Note: Multi-y and multi-theta prediction tasks cannot be performed 
    simultaneously. Ensure that your input dimensions are structured 
    accordingly, i.e., you can loop through multiple calls to handle 
    these cases separately.

    Parameters
    ----------
    y : ndarray
        Dependent variable(s) represented as either:
        - Single task: Column vector [N-by-1].
        - Multi-y task: Matrix [N-by-Q], where Q is the number of dependent variables.
    X : ndarray
        Independent variables matrix of shape [N-by-K], where K is the number of features.
    theta : ndarray
        Circumstances represented as either:
        - Single task: Row vector [1-by-K].
        - Multi-theta task: Matrix [Q-by-K], where Q is the number of different sets of circumstances.
    options : PredictionOptions
        Configuration object containing key-value parameters required 
        for the prediction task.

    Returns
    -------
    yhat : ndarray
        Predicted outcome(s) based on the input data and circumstances.
    yhat_details : dict
        Dictionary containing additional details about the prediction model and results.

    Raises
    ------
    ValueError
        If both multi-y and multi-theta are specified simultaneously, 
        or if the dimensions of `y`, `X`, and `theta` are not compatible.
    """

    # Start time for prediction 
    start_time = time.time()
    
    # Get the function based on the task type and call it
    prediction_function = _TASK_MAP.get(_router.determine_task_type(y, X, theta))
    yhat, yhat_details = prediction_function(PSRFunction.PSR, y, X, theta, Options)
    
    # Current time after prediction is complete
    end_time = time.time()
    prediction_duration = end_time - start_time

    # conditionla return structure so as to not alter working logic 
    if is_return_receipt:
        # Capture relevant input info and generate a receipt
        receipt = PredictionReceipt(model_type=PSRFunction.PSR, y=y, X=X, theta=theta, options=Options,
                                    yhat=yhat, prediction_duration=prediction_duration)
        # Return receipt in addition to yhat and yhat_details
        return yhat, yhat_details, receipt
    
    else:
         # Else, maintain normal return structure
         return yhat, yhat_details
    
    
def predict_maxfit(y:ndarray, X:ndarray, theta:ndarray, Options:MaxFitOptions, is_return_receipt:bool=False):
    """
    Performs a relevance-based maxfit prediction using the CSA API.

    This method determines the optimal relevance-based prediction by 
    evaluating adjusted fit across various thresholds for the input data. 
    
    This function supports three types of prediction tasks:   
    1. Single prediction task: A single dependent variable and a single set of circumstances.
    2. Multi-y prediction task: Multiple dependent variables (y) with a single set of circumstances (theta). 
    3. Multi-theta prediction task: A single dependent variable with multiple sets of circumstances (theta).

    Note: Multi-y and multi-theta prediction tasks cannot be performed 
    simultaneously. Ensure that your input dimensions are structured 
    accordingly, i.e., you can loop through multiple calls to handle 
    these cases separately.

    Parameters
    ----------
    y : ndarray
        Dependent variable(s) represented as either:
        - Single task: Column vector [N-by-1].
        - Multi-y task: Matrix [N-by-Q], where Q is the number of dependent variables.
    X : np.ndarray
        Independent variables matrix of shape [N-by-K], where K is the number of features.
    theta : ndarray
        Circumstances represented as either:
        - Single task: Row vector [1-by-K].
        - Multi-theta task: Matrix [Q-by-K], where Q is the number of different sets of circumstances.
    options : MaxFitOptions
        Configuration object containing key-value parameters required 
        for the maxfit prediction task.

    Returns
    -------
    yhat : ndarray
        Predicted outcome(s) based on the input data and circumstances.
    yhat_details : dict
        Dictionary containing additional details about the prediction model and results.

    Raises
    ------
    ValueError
        If both multi-y and multi-theta are specified simultaneously, 
        or if the dimensions of `y`, `X`, and `theta` are not compatible.
    """

    # Start time for prediction 
    start_time = time.time()
    
    # Get the function based on the task type and call it
    prediction_function = _TASK_MAP.get(_router.determine_task_type(y, X, theta))
    yhat, yhat_details = prediction_function(PSRFunction.MAXFIT, y, X, theta, Options)
    
    # Current time after prediction is complete
    end_time = time.time()
    prediction_duration = end_time - start_time

    # conditionla return structure so as to not alter working logic 
    if is_return_receipt:
        # Capture relevant input info and generate a receipt
        receipt = PredictionReceipt(model_type=PSRFunction.MAXFIT, y=y, X=X, theta=theta, options=Options,
                                    yhat=yhat, prediction_duration=prediction_duration)
        # Return receipt in addition to yhat and yhat_details
        return yhat, yhat_details, receipt
    
    else:
         # Else, maintain normal return structure
         return yhat, yhat_details


def predict_grid(y:ndarray, X:ndarray, theta:ndarray, Options:GridOptions, is_return_receipt:bool=False):
    """
    Performs a relevance-based grid prediction using the CSA API.

    This method generates an optimal composite prediction by evaluating
    all thresholds and all variable combinations for the input data. 
    
    This function supports three types of prediction tasks:   
    1. Single prediction task: A single dependent variable and a single set of circumstances.
    2. Multi-y prediction task: Multiple dependent variables (y) with a single set of circumstances (theta). 
    3. Multi-theta prediction task: A single dependent variable with multiple sets of circumstances (theta).

    Note: Multi-y and multi-theta prediction tasks cannot be performed 
    simultaneously. Ensure that your input dimensions are structured 
    accordingly, i.e., you can loop through multiple calls to handle 
    these cases separately.

    Parameters
    ----------
    y : ndarray
        Dependent variable(s) represented as either:
        - Single task: Column vector [N-by-1].
        - Multi-y task: Matrix [N-by-Q], where Q is the number of dependent variables.
    X : ndarray
        Independent variables matrix of shape [N-by-K], where K is the number of features.
    theta : ndarray
        Circumstances represented as either:
        - Single task: Row vector [1-by-K].
        - Multi-theta task: Matrix [Q-by-K], where Q is the number of different sets of circumstances.
    options : GridOptions
        Configuration object containing key-value parameters required 
        for the grid prediction task.

    Returns
    -------
    yhat : ndarray
        Predicted outcome(s) based on the input data and circumstances.
    yhat_details : dict
        Dictionary containing additional details about the prediction model and results.

    Raises
    ------
    ValueError
        If both multi-y and multi-theta are specified simultaneously, 
        or if the dimensions of `y`, `X`, and `theta` are not compatible.
    """

    # Start time for prediction 
    start_time = time.time()
    
    # Get the function based on the task type and call it
    prediction_function = _TASK_MAP.get(_router.determine_task_type(y, X, theta))
    yhat, yhat_details = prediction_function(PSRFunction.GRID, y, X, theta, Options)
    
    # Current time after prediction is complete
    end_time = time.time()
    prediction_duration = end_time - start_time

    # conditionla return structure so as to not alter working logic 
    if is_return_receipt:
        # Capture relevant input info and generate a receipt
        receipt = PredictionReceipt(model_type=PSRFunction.GRID, y=y, X=X, theta=theta, options=Options,
                                    yhat=yhat, prediction_duration=prediction_duration)
        # Return receipt in addition to yhat and yhat_details
        return yhat, yhat_details, receipt
    
    else:
         # Else, maintain normal return structure
         return yhat, yhat_details


def predict_grid_singularity(y:ndarray, X:ndarray, theta:ndarray, Options:GridOptions, is_return_receipt:bool=False):
    """
    Performs a relevance-based grid prediction using the CSA API.

    This method determines the singularity of a grid prediction. 
    
    This function supports three types of prediction tasks:   
    1. Single prediction task: A single dependent variable and a single set of circumstances.
    2. Multi-y prediction task: Multiple dependent variables (y) with a single set of circumstances (theta). 
    3. Multi-theta prediction task: A single dependent variable with multiple sets of circumstances (theta).

    Note: Multi-y and multi-theta prediction tasks cannot be performed 
    simultaneously. Ensure that your input dimensions are structured 
    accordingly, i.e., you can loop through multiple calls to handle 
    these cases separately.

    Parameters
    ----------
    y : ndarray
        Dependent variable(s) represented as either:
        - Single task: Column vector [N-by-1].
        - Multi-y task: Matrix [N-by-Q], where Q is the number of dependent variables.
    X : ndarray
        Independent variables matrix of shape [N-by-K], where K is the number of features.
    theta : ndarray
        Circumstances represented as either:
        - Single task: Row vector [1-by-K].
        - Multi-theta task: Matrix [Q-by-K], where Q is the number of different sets of circumstances.
    options : GridOptions
        Configuration object containing key-value parameters required 
        for the grid prediction task.

    Returns
    -------
    yhat : ndarray
        Predicted outcome(s) based on the input data and circumstances.
    yhat_details : dict
        Dictionary containing additional details about the prediction model and results.

    Raises
    ------
    ValueError
        If both multi-y and multi-theta are specified simultaneously, 
        or if the dimensions of `y`, `X`, and `theta` are not compatible.
    """

    # Start time for prediction 
    start_time = time.time()
    
    # Get the function based on the task type and call it
    prediction_function = _TASK_MAP.get(_router.determine_task_type(y, X, theta))
    yhat, yhat_details = prediction_function(PSRFunction.GRID_SINGULARITY, y, X, theta, Options)

    # Current time after prediction is complete
    end_time = time.time()
    prediction_duration = end_time - start_time

    # conditionla return structure so as to not alter working logic 
    if is_return_receipt:
        # Capture relevant input info and generate a receipt
        receipt = PredictionReceipt(model_type=PSRFunction.GRID_SINGULARITY, y=y, X=X, theta=theta, options=Options,
                                    yhat=yhat, prediction_duration=prediction_duration)
        # Return receipt in addition to yhat and yhat_details
        return yhat, yhat_details, receipt
    
    else:
         # Else, maintain normal return structure
         return yhat, yhat_details
    

def get_api_quota(quota_type:str="summary", api_key:str=None):
    """Returns a json response body containing data for the selected
    quota_type.

    Parameters
    ----------
    quota_type : str, optional
        Select between "summary", "used", "remaining" or "quota". By default "summary"
    api_key : str, optional
        CSA_API_KEY, by default None. If not supplied, the function will search for CSA_API_KEY
        in the the os environment variables.

    Returns
    -------
    dict
        json response body containing data for the selected quota_type
    """

    return _postmaster._get_quota(quota_type=quota_type, api_key=api_key)