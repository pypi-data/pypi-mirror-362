"""
CSA Relevance Engine: Internal Postmaster Module

This module provides internal functions for interacting with the Cambridge 
Sports Analytics (CSA) server API for prediction tasks. These functions 
are responsible for posting job inputs to the server, retrieving results, 
and handling different types of prediction tasks like partial sample 
regression, maximum fit, and grid optimization.

Note: This module is intended for internal use within the CSAnalytics PSR 
library and is not designed for direct interaction by end-users.

Functions Overview
------------------
- _post_predict_inputs(y, X, theta, ...):
    Posts prediction inputs for partial sample regression to the CSA server.

- _post_maxfit_inputs(y, X, theta, ...):
    Posts prediction inputs for maximum fit evaluation to the CSA server.

- _post_grid_inputs(y, X, theta, Options):
    Posts prediction inputs for grid grid predictions to the CSA server.

- _get_results(job_id, job_code):
    Polls the CSA server for results based on a given job ID and job code.

(c) 2023 - 2024 Cambridge Sports Analytics, LLC. All rights reserved.
support@csanalytics.io
"""

from csa_prediction_engine.helpers._auth_manager import _get_apikeys
from csa_prediction_engine.helpers._payload_handler import (
    post_job, 
    poll_for_results,
    get_quota
)

# Utlity function for processing ndarrays withing dictionaries
from csa_common_lib.helpers._conversions import (
        convert_ndarray_to_list
    ) 


from csa_common_lib.enum_types.functions import PSRFunction
from csa_common_lib.classes.prediction_options import PredictionOptions, MaxFitOptions, GridOptions


# PSR prediction
def _post_predict_inputs(y, X, theta, Options:PredictionOptions):
    """ Runs and evaluates a prediction using the partial sample regression 
    model. Returns yhat and model details. If threshold=0 for 
    is_threshold_percent=True, weights converge to full sample regression.
    

    Parameters
    ----------
    y : ndarray [N-by-1]
        Column vector of the dependent variable.
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta : [1-by-K]
        Row vector of circumstances.
    threshold : float or ndarray[1-by-T], optional (default=None)
        Threshold to evaluate relevant observations.
        If threshold=None, the model will evaluate across thresholds
        from [0, 0.90) in 0.10 increments.
    is_threshold_percent : bool, optional (default=True)
        Specify whether threshold is in percentage (decimal) units.
    most_eval : bool, optional (default=True)
        Specify the direction of threshold evluation.
        True:  relevance score > threshold
        False: relevance score < threshold
    eval_type : str, optional (default="relevance")
        Specify the censor signal type, relevance or similarity.
    cov_inv : ndarray [K-by-K], optional (default=None)
        Inverse covariance matrix, specify for speed.

    Returns
    -------
    job_id : int
        Job id number.
    job_code : str
        Job code response from server.
    """
    
    # Initialize results
    job_id = None
    job_code = None

    # Retrieve Options dictionary and convert any ndarrays to lists
    options_dict = convert_ndarray_to_list(Options.options)
    
    # Post partial-sample regression model inputs to the server and
    # let is calculate results.
    response, job_id, job_code = post_job(
        PSRFunction.PSR,
        y=y,
        X=X,
        theta=theta,
        **options_dict)
    
    # Print the response if it's not None and both job_id and job_code are None
    if response is not None and job_id is None and job_code is None:
        print(f"csanalytics:postmaster:_jobs:_post_predict_inputs:{response}")
    
    # Return results object
    return job_id, job_code
    
    
def _post_maxfit_inputs(y, X, theta, Options:MaxFitOptions):
    """ Runs and evaluates a prediction using the partial sample regression 
    model and solves for maximum adjusted fit. 
    Returns yhat and model details.
    

    Parameters
    ----------
    y : ndarray [N-by-1]
        Column vector of the dependent variable.
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta : [1-by-K]
        Row vector of circumstances.
    most_eval : bool, optional (default=True)
        Specify the direction of threshold evluation.
        True:  relevance score > threshold
        False: relevance score < threshold
    eval_type : str, optional (default="relevance")
        Specify the censor signal type, relevance or similarity.
    cov_inv : ndarray [K-by-K], optional (default=None)
        Inverse covariance matrix, specify for speed.

    Returns
    -------
    job_id : int
        Job id number.
    job_code : str
        Job code response from server.
    """
    
    
    # Initialize results
    job_id = None
    job_code = None

    # Retrieve Options dictionary and convert any ndarrays to lists
    options_dict = convert_ndarray_to_list(Options.options)
    
    # Post maximum fit job inputs and let the server compute
    response, job_id, job_code = post_job(
        PSRFunction.MAXFIT,
        y=y,
        X=X,
        theta=theta,
        **options_dict)
    
    # Print the response if it's not None and both job_id and job_code are None
    if response is not None and job_id is None and job_code is None:
        print(f"csanalytics:postmaster:_jobs:_post_maxfit_inputs:{response}")
    
    # Return results object
    return job_id, job_code
    
def _post_grid_inputs(y, X, theta, Options:GridOptions):
    """ Runs and evaluates a prediction using the partial sample regression 
    model and solves for maximum adjusted fit with optimal variable selection. 
    This is also known as the grid optimal partial sample regression.
    Returns yhat and model details.
    

    Parameters
    ----------
    y : ndarray [N-by-1]
        Column vector of the dependent variable.
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta : [1-by-K]
        Row vector of circumstances.
    threshold_range : tuple or ndarray
        Min/max range for evaluating maxfit threshold, by default (0,1)
    stepsize : float, optional (default=0.20)
        Stepsize to evaluate range of thresholds to solve for max fit.
        Decreasing stepsize will increase the granularity of the search.
    most_eval : bool, optional (default=True)
        Specify the direction of threshold evluation.
        True:  relevance score > threshold
        False: relevance score < threshold
    eval_type : str, optional (default="all")
        Specify the censor signal type, relevance, similarity, or all.
    k : int, optional (default=None)
        Lower bound for the number of variables to include, by default None.
        None would be equivalent to an unconstraint optimization.
    return_grid : boolean, optional (default=False)
        Returns grid of adjusted_fits, yhats, and weights via output_details
        for all the combinations evaluated.

    Returns
    -------
    job_id : int
        Job id number.
    job_code : str
        Job code response from server.
    """
    
    
    # Initialize results
    job_id = None
    job_code = None

    # Retrieve Options dictionary and convert any ndarrays to lists
    options_dict = convert_ndarray_to_list(Options.options)

    # Post the grid prediction job and let the server compute everything
    response, job_id, job_code = post_job(
        PSRFunction.GRID,
        y=y,
        X=X,
        theta=theta,
        **options_dict)
    
    # Print the response if it's not None and both job_id and job_code are None
    if response is not None and job_id is None and job_code is None:
        print(f"csanalytics:postmaster:_jobs:_post_grid_inputs:{response}")
    
    # Return results object
    return job_id, job_code


def _post_grid_singularity_inputs(y, X, theta, Options:GridOptions):
    """ Runs and evaluates a grid singularity prediction using the 
    partial sample regression model and solves for maximum adjusted 
    fit with optimal variable selection.
    Returns yhat and model details.
    

    Parameters
    ----------
    y : ndarray [N-by-1]
        Column vector of the dependent variable.
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta : [1-by-K]
        Row vector of circumstances.
    threshold_range : tuple or ndarray
        Min/max range for evaluating maxfit threshold, by default (0,1)
    stepsize : float, optional (default=0.20)
        Stepsize to evaluate range of thresholds to solve for max fit.
        Decreasing stepsize will increase the granularity of the search.
    most_eval : bool, optional (default=True)
        Specify the direction of threshold evluation.
        True:  relevance score > threshold
        False: relevance score < threshold
    eval_type : str, optional (default="all")
        Specify the censor signal type, relevance, similarity, or all.
    k : int, optional (default=None)
        Lower bound for the number of variables to include, by default None.
        None would be equivalent to an unconstraint optimization.
    return_grid : boolean, optional (default=False)
        Returns grid of adjusted_fits, yhats, and weights via output_details
        for all the combinations evaluated.

    Returns
    -------
    job_id : int
        Job id number.
    job_code : str
        Job code response from server.
    """
    
    
    # Initialize results
    job_id = None
    job_code = None

    # Retrieve Options dictionary and convert any ndarrays to lists
    options_dict = convert_ndarray_to_list(Options.options)
    
    # Post the grid singularity job and let the server compute everything
    response, job_id, job_code = post_job(
        PSRFunction.GRID_SINGULARITY,
        y=y,
        X=X,
        theta=theta,
        **options_dict) # Will need to update api endpoints  
    
    # Print the response if it's not None and both job_id and job_code are None
    if response is not None and job_id is None and job_code is None:
        print(f"csanalytics:postmaster:_jobs:_post_grid_inputs:{response}")
    
    # Return results object
    return job_id, job_code


def _get_results(job_id: int, job_code:str):
    """Polls and waits for the server to return results for given
    job id and job code.

    Parameters
    ----------
    job_id : int
        Job id.
    job_code : str
        Job code.

    Returns
    -------
    yhat : ndarray [1-by-T]
        Prediction outcome.
    output_details : dict
        Model details accesible via key-value pairs.
    """    
    
    # Initialize result(s) data structures
    yhat = None
    output_details = None
    
    # if successful, then query results for job_id after expected_eta elapsed
    # continuous poll until TIMEOUT, lock thread
    if job_id is not None and job_code is not None:
        # if successful, then query results for job_id after expected_eta elapsed
        output_details = poll_for_results(job_id, job_code)

        yhat = output_details.get('yhat', None)
        
    # Return results
    return yhat, output_details

def _get_quota(quota_type:str='summary', api_key:str=None):
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

    if api_key is None: 
        api_key, _ = _get_apikeys() # Retreive api keys from os environment variables
    
    return get_quota(quota_type=quota_type, api_key=api_key)
