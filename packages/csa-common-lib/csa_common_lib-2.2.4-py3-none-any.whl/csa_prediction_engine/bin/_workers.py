"""
CSA Relevance Engine: Single Task Prediction Workers

This module provides functionality for executing single task predictions
using the Cambridge Sports Analytics API. A single task is defined as a 
prediction where a single dependent variable (y) is evaluated with a 
single set of circumstances (theta).

Supported Functions:
--------------------
1. `predict_psr`: Performs a standard single task relevance-based prediction.
2. `predict_maxfit`: Executes a single task prediction optimized for maximum fit.
3. `predict_grid`: Calculates a composite prediction based on a grid evaluation.
4. `predict_grid_singularity`: Identifies the singularity of grid evaluations.

Usage:
------
These functions send prediction jobs to the server, either waiting for results 
synchronously (default) or returning a job ID and code for later polling.

(c) 2023 - 2024 Cambridge Sports Analytics, LLC. All rights reserved.
support@csanalytics.io
"""

# Local imports
from ..helpers import _postmaster

# Local application/library-specific imports
from csa_common_lib.classes.prediction_options import (
    PredictionOptions,
    MaxFitOptions,
    GridOptions
)


def predict_psr(y, X, theta, Options:PredictionOptions, poll_results:bool=False):
    """ 
    Runs and evaluates a prediction using the relevance-based model. 
    
    Parameters
    ----------
    y : ndarray [N-by-1]
        Column vector of the dependent variable.
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta : [1-by-K]
        Row vector of circumstances.
    Options : PredictionOptions
        Options object that contains the necessary key-value parameters
        for grid predictions.
    poll_results : boolean, optional (default=True)
        If true, wait for server to return results, computational time
        may vary. If false, the server will return job id and job code.

    Returns
    -------
    yhat : ndarray
        Prediction outcome(s).
    yhat_details : dict
        Model details accesible via key-value pairs.
    """
    
    # Send linear regression job to postmaster
    job_id, job_code = _postmaster._post_predict_inputs(
        y=y, X=X, theta=theta, Options=Options
    )
    
    # Get results from server
    if poll_results:
        yhat, yhat_details = _postmaster._get_results_worker(job_id, job_code)
    
        # Return results object
        return yhat, yhat_details
    
    else:
        return job_id, job_code
    
    
def predict_maxfit(y, X, theta, Options:MaxFitOptions, poll_results:bool=False):
    """ 
    Runs and evaluates a prediction using the relevance-based model 
    and solves for maximum (adjusted) fit.

    Parameters
    ----------
    y : ndarray [N-by-1]
        Column vector of the dependent variable.
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta : [1-by-K]
        Row vector of circumstances.
    Options : MaxFitOptions
        MaxFitOptions object that contains the necessary key-value parameters
        for grid predictions.
    poll_results : boolean, optional (default=True)
        If true, wait for server to return results, computational time
        may vary. If false, the server will return job id and job code.

    Returns
    -------
    yhat : ndarray
        Prediction outcome(s).
    yhat_details : dict
        Model details accesible via key-value pairs.
    """
    
    # Send maxfit partial sample regression job to postmaster
    job_id, job_code = _postmaster._post_maxfit_inputs(
        y=y, X=X, theta=theta, Options=Options)
    
    # Get results from server
    if poll_results:
        yhat, yhat_details = _postmaster._get_results_worker(job_id, job_code)
    
        # Return results object
        return yhat, yhat_details
    
    else:
        return job_id, job_code
    
    
def predict_grid(y, X, theta, Options:GridOptions, poll_results=False):
    """ 
    Runs and evaluates a grid prediction using the relevance-based
    model and weights each grid cell solution by its adjusted-fit to 
    solve for a composite prediction outcome. 
    
    Parameters
    ----------
    y : ndarray [N-by-1]
        Column vector of the dependent variable.
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta : [1-by-K]
        Row vector of circumstances.
    Options : GridOptions
        GridOptions object that contains the necessary key-value parameters
        for grid predictions.
    poll_results : boolean, optional (default=True)
        If true, wait for server to return results, computational time
        may vary. If false, the server will return job id and job code.

    Returns
    -------
    Returns yhat and yhat_details by default, if poll_results is False,
    then this function returns job id and job code.
    
    yhat : ndarray
        Prediction outcome(s).
    yhat_details : dict
        Model details accesible via key-value pairs.
    """
    
    # Send grid prediction job to postmaster
    job_id, job_code = _postmaster._post_grid_inputs(
        y, X, theta, Options=Options)
    
    # Get results from server
    if poll_results:
        yhat, yhat_details = _postmaster._get_results(job_id, job_code)
    
        # Return results object
        return yhat, yhat_details
    
    else:
        return job_id, job_code
    
    
def predict_grid_singularity(y, X, theta, Options:GridOptions, poll_results=False):
    """ 
    Runs and evaluates a grid singularity prediction using the 
    relevance-based model and solves for maximum adjusted fit with 
    optimal variable selection. 
    
    Parameters
    ----------
    y : ndarray [N-by-1]
        Column vector of the dependent variable.
    X : ndarray [N-by-K]
        Matrix of independent variables.
    theta : [1-by-K]
        Row vector of circumstances.
    Options : GridOptions
        GridOptions object that contains the necessary key-value parameters
        for grid predictions.
    poll_results : boolean, optional (default=True)
        If true, wait for server to return results, computational time
        may vary. If false, the server will return job id and job code.

    Returns
    -------
    Returns yhat and yhat_details by default, if poll_results is False,
    then this function returns job id and job code.
    
    yhat : ndarray
        Prediction outcome(s).
    yhat_details : dict
        Model details accesible via key-value pairs.
    """
    
    # Send grid prediction job to postmaster
    job_id, job_code = _postmaster._post_grid_inputs(
        y, X, theta, Options=Options)
    
    # Get results from server
    if poll_results:
        yhat, yhat_details = _postmaster._get_results(job_id, job_code)
    
        # Return results object
        return yhat, yhat_details
    
    else:
        return job_id, job_code