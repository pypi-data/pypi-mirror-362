"""
CSA Relevance Engine: Single Task Prediction Module

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
from csa_common_lib.enum_types.functions import PSRFunction
from csa_common_lib.classes.prediction_options import (
    PredictionOptions,
    MaxFitOptions,
    GridOptions
)
from csa_common_lib.classes.prediction_receipt import PredictionReceipt
from csa_prediction_engine.helpers._payload_handler import route_X_input

# Import single prediction workers
from ._workers import (
    predict_grid,
    predict_grid_singularity,
    predict_maxfit,
    predict_psr
)

# Dispatcher mapping based on PSRFunction type.
# Maps different prediction tasks to their corresponding dispatcher functions.
_DISPATCHER_MAP = {
    PSRFunction.GRID: predict_grid,
    PSRFunction.GRID_SINGULARITY: predict_grid_singularity,
    PSRFunction.MAXFIT: predict_maxfit,
    PSRFunction.PSR: predict_psr
}


def predict(model_type:PSRFunction, y, X, theta, Options:PredictionOptions):
    """
    Entry point for running multiple prediction tasks stratified by 
    y (dependent variables).
    
    Parameters
    ----------
    model_type : PSRFunction
        Type of prediction model (PSR, MAXFIT, GRID, or GRID_SINGULARITY).
    y : ndarray [N-by-1]
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
    yhat : ndarray [1-by-T]
        Prediction outcomes, T thresholds if multiple tresholds specified.
    yhat_details : dict
        Model details accesible via key-value pairs.
    """
    
    # Get the corresponding dispatcher function
    dispatcher = _DISPATCHER_MAP.get(model_type)
    
    # Route X input matrix depending on payload size
    X = route_X_input(model_type=model_type, y=y, X=X, theta=theta, Options=Options)

    # Call the dispatcher function with the provided arguments
    yhat, yhat_details = dispatcher(y=y, X=X, theta=theta, Options=Options, poll_results=True)
    
    # Return results
    return yhat, yhat_details
    


