"""
CSA Relevance Engine: Dispatcher Module for parallel task execution

This module provides dispatcher functions to facilitate the execution of 
prediction tasks in a parallel computing environment. Each dispatcher function 
wraps a specific worker function and allows arguments to be passed in a format 
suitable for multi-threaded or multi-process execution.

Available Dispatcher Functions:
    - dispatch_predict_task: Dispatches a single prediction task to a worker.
    - dispatch_maxfit_task: Dispatches a maximum fit prediction task to a worker.
    - dispatch_grid_task: Dispatches a Grid model prediction task to a worker.
    - dispatch_grid_singularity_task: Dispatches a singularity task for the Grid model.

(c) 2023 - 2024 Cambridge Sports Analytics, LLC. All rights reserved.
support@csanalytics.io
"""


from ._workers import (
    _psr_predict_worker,
    _maxfit_predict_worker,
    _grid_predict_worker,
    _grid_singularity_worker,
    _get_results_worker
)


def dispatch_psr_task(args):
    """
    Dispatches a single prediction task to the _psr_predict_worker function.

    This function takes a tuple of arguments and passes them to the 
    _psr_predict_worker function for execution in a parallel environment.

    Parameters
    ----------
    args : tuple
        The arguments required by the _psr_predict_worker function, 
        which include all necessary parameters for the partial sample
        regression prediction task.

    Returns
    -------
    result : Any
        The result returned by the _psr_predict_worker function after 
        executing the prediction task.
    """
    
    return _psr_predict_worker(*args)


def dispatch_maxfit_task(args):
    """
    Dispatches a maximum fit prediction task to the _maxfit_predict_worker function.

    This function takes a tuple of arguments and passes them to the 
    _maxfit_predict_worker function to perform a maximum fit prediction 
    task in a parallel context.

    Parameters
    ----------
    args : tuple
        The arguments required by the _maxfit_predict_worker function, 
        including parameters specific to the maximum fit prediction task.

    Returns
    -------
    result : Any
        The result returned by the _maxfit_predict_worker function after 
        executing the maximum fit prediction task.
    """
    
    return _maxfit_predict_worker(*args)
    

def dispatch_grid_task(args):
    """
    Dispatches a Grid prediction model task to the _grid_predict_worker function.

    This function unpacks a tuple of arguments and passes them to the 
    _grid_predict_worker function, facilitating its use with parallel 
    processing frameworks such as concurrent.futures.ProcessPoolExecutor.

    Parameters
    ----------
    args : tuple
        The arguments required by the _grid_predict_worker function, 
        which include all necessary parameters for the Grid prediction 
        model task.

    Returns
    -------
    result : Any
        The result returned by the _grid_predict_worker function after 
        executing the Grid prediction model task.
    """
    
    return _grid_predict_worker(*args)


def dispatch_grid_singularity_task(args):
    """
    Dispatches a Grid Singularity prediction model task 
    to the _grid_singularity_worker function.

    This function unpacks a tuple of arguments and passes them to the 
    _grid_singularity_worker function, facilitating its use with parallel 
    processing frameworks such as concurrent.futures.ProcessPoolExecutor.

    Parameters
    ----------
    args : tuple
        The arguments required by the _grid_predict_worker function, 
        which include all necessary parameters for the Grid Singularity
        prediction model task.

    Returns
    -------
    result : Any
        The result returned by the _get_results_worker function after 
        executing the Grid Singularity prediction model task.
    """
    
    return _grid_singularity_worker(*args)


def dispatch_get_results(args):
    """
    Dispatches get results to retrieve prediction results from the
    CSA API.

    This function unpacks a tuple of arguments and passes them to the 
    _get_results_worker function, facilitating its use with parallel 
    processing frameworks such as concurrent.futures.ProcessPoolExecutor.

    Parameters
    ----------
    args : tuple
        The arguments required by the _get_results_worker function, 
        which include all necessary parameters for retrieving
        a prediction task result(s) from the server.

    Returns
    -------
    result : Any
        The result returned by the _get_results_worker.
    """
    
    return _get_results_worker(*args)