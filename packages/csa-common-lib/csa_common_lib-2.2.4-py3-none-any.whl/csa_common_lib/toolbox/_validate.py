"""Validator utility functions to validate inputs, types, structs,
options, classes, and matrices.
"""

import warnings

import numpy as np

from csa_common_lib.enum_types.functions import PSRFunction


def validate_inputs(is_strict:bool, function_type:PSRFunction, **varargin):
    """Validates expected set of inputs and object values to process
    PSR payload / jobs.

    Parameters
    ----------
    is_strict : bool
        True to raise ValueError on invalid inputs
        False raises warnings on invalid inputs
    function_type : PSRFunction
        PSR Function type
    **varargins: Variable number of inputs
        y, X, theta, threshold, etc. See PSR library docs.

    Raises
    ------
    ValueError
        If invalid input (when is_strict)
    Warning
        If invalid input (when !is_strict)
    """    
    # region Input(s) Exist: Do the required input(s) exist
    # mandatory requirements for both client and serverside
    _check_key(varargin, 'y', is_strict)
    _check_key(varargin, 'X', is_strict)
    _check_key(varargin, 'theta', is_strict)
    
    if is_strict:
        # if strict (exhaustive) requirements are enforced (example API serverside)
        # then we want to validate optional arguments as well.
        _check_key(varargin, 'cov_inv', is_strict)
        
        if function_type == PSRFunction.PSR:
            _check_key(varargin, 'threshold', is_strict)
            _check_key(varargin, 'most_eval', is_strict)
            _check_key(varargin, 'eval_type', is_strict)
            _check_key(varargin, 'is_threshold_percent', is_strict)
            
        elif function_type == PSRFunction.MAXFIT:
            _check_key(varargin, 'stepsize', is_strict)
            _check_key(varargin, 'most_eval', is_strict)
            _check_key(varargin, 'eval_type', is_strict)
            
        elif function_type == PSRFunction.GRID_SINGULARITY or function_type == PSRFunction.GRID:
            _check_key(varargin, 'stepsize', is_strict)
            _check_key(varargin, 'most_eval', is_strict)
            _check_key(varargin, 'eval_type', is_strict)
            
            _check_key(varargin, 'attribute_combi', is_strict)
            _check_key(varargin, 'k', is_strict)
        else:
            response_str = f'Invalid function type {function_type}'
            if is_strict:
                raise ValueError(response_str)
            else:
                warnings.warn(response_str, Warning)
    # endregion
    
    validate_args = {
        'y': lambda key, obj, K: _validate_ndarray(obj, obj_name=key, allow_none=False),
        'X': lambda key, obj, K: _validate_ndarray(obj, obj_name=key, allow_none=False),
        'theta': lambda key, obj, K: _validate_ndarray(obj, 1, K, obj_name=key, allow_none=False),
        'cov_inv': lambda key, obj, K: _validate_ndarray(obj, K, K, obj_name=key),
        'threshold': lambda key, obj, K: _validate_numeric_or_ndarray(obj, obj_name=key),
        'threshold_range': lambda key, obj, K: _validate_ndarray(obj, obj_name=key),
        'is_threshold_percent': lambda key, obj, K: _validate_bool(obj, obj_name=key), 
        'most_eval': lambda key, obj, K: _validate_bool(obj, obj_name=key),
        'eval_type': lambda key, obj, K: _validate_str(obj, obj_name=key),
        'stepsize': lambda key, obj, K: _validate_numeric(obj, 0, 1, obj_name=key),
        'attribute_combi': lambda key, obj, K:  _validate_ndarray(obj, cols=K, obj_name=key),
        'k': lambda key, obj, K: _validate_numeric(obj, obj_name=key),
        'max_iter': lambda key, obj, K: _validate_numeric_or_ndarray(obj, obj_name=key),
        'adjusted_fit_multiplier': lambda key, obj, K: _validate_str(obj, obj_name=key),
        'objective': lambda key, obj, K: _validate_str(obj, obj_name=key),
    }
    
    # initialize
    y_N = None # number of observations (rows) of dependent variable
    N = None # number of observations (rows)
    K = None # number of variables (columns)
    
    
    # region Input Type and Dimensions    
    for key, value in varargin.items():
        
        # DEBUG: Uncomment to view validation
        # print(f'Validating {key}: {value}')
        
        # y is a column vector
        if key == 'y':
            _validate_ndarray(value, np.ndarray)
            y_N = value.size
        
        # X is a [N-by-K] matrix

        if key == 'X':
            # if X is a reference file, skip validation. (X validation was already done upstream in this case)
            if isinstance(value, str):
                if '.json' in value:
                    pass
            else:
                _validate_ndarray(value, np.ndarray)
                (N, K) = value.shape

                if N <= K:                
                    raise ValueError("X: The number of observations (rows) must be greater than the number of variables (columns)")

                if y_N != N:
                    raise ValueError("Inputs X and Y must have the same number of observations (rows)")

        
        # validate the rest of the arguments
        validate_args.get(key, value)
        
        # # attribute_combi is a [1-by-K] vector of zeros and ones
        if key == 'attribute_combi':
            _validate_ndarray(value, cols=K)
        
        # # k = None or an int
        if key == 'k':
            _validate_numeric(value, min_value=1, max_value=K)
        
        
    # endregion

        
def _check_key(kamus: dict, key:str, is_strict: bool = False):
    """Checks to see if a key exist in a dictionary

    Parameters
    ----------
    kamus : dict
        Dictionary of key/value of inputs
    key : str
        Name of key (input)
    is_strict: bool (optional, default=False)
        Raises ValueError if check fails when True, otherwise
        displays a warning.
    
    Raises
    ------
    ValueError
        If key is not present in the dictionary. (when is_strict)
    Warning
        If key is not present in the dictionary. (when !is_strict)
    """    
    
    # Initialize the return flag
    input_exist = True
    
    if key not in kamus:
        # The key is not in the dictionary
        input_exist = False

        # Construct response string
        response_str = f'Missing input {key}'
        
        if is_strict:
            # Raise Warning exception with details
            warnings.warn(response_str, Warning)
        else:
            # Raise value exception with details
            raise ValueError(response_str)
    
    return input_exist


def _validate_ndarray(obj, rows:int=None, cols:int=None, 
                      obj_name:str=None, allow_none:bool=True):
    """Validates ndarrays.

    Parameters
    ----------
    obj : any
        Object to validate as an ndarray
    rows : int, optional
        Expected number of rows, by default None
    cols : int, optional
        Expected number of columns, by default None
    obj_name : str, optional
        Object variable name, by default None
    allow_none : bool, optional
        Is the object allowed to be None/null, by default True

    Returns
    -------
    bool
        Validation exit flag.
    """    
    valid_type = False
    valid_dim = False
    
    # Check if we allow none for this object
    if allow_none & (obj is None):
        return True
    else:
        # Check to see if object is an ND array with dimensions dim
        if isinstance(obj, np.ndarray):
            valid_type = True
            
            dim = (rows, cols)
            if dim == (None, None):
                return True
            else:
                valid_dim = False
                valid_rows = False
                valid_cols = False
                
                obj_dim = obj.shape
                if rows is not None:
                    valid_rows = (obj_dim[0] == rows)
                
                if cols is not None:
                    valid_cols = (obj_dim[1] == cols)
                
                # Valid dimensions flag
                valid_dim = valid_rows and valid_cols
                
        if obj_name is not None:
            if valid_dim is False:
                r = ':' if rows is None else rows
                c = ':' if cols is None else cols
                warnings.warn(f'Invalid {obj_name}, expecting ({r},{c}) numpy.ndarray.' , Warning)
                
        # Return valid object type and valid dimension verification
        return valid_type & valid_dim
    
    
def _validate_bool(obj, obj_name:str=None, allow_none:bool=True):
    """Validates a boolean object

    Parameters
    ----------
    obj : any
        Object to validate as a boolean
    obj_name : str, optional
        Object variable name, by default None
    allow_none : bool, optional
        Allows the object to be None/null, by default True

    Returns
    -------
    bool
        Validation exit flag
    """    
    
    
    if allow_none & (obj is None):
        return True
    else:
        if obj_name is not None:
            if not isinstance(obj, bool):
                warnings.warn(f'Invalid {obj_name}, expecting bool.' , Warning)    
        return isinstance(obj, bool)
    
    
def _validate_numeric(obj, min_value:float=None, max_value:float=None, 
                      obj_name:str=None, allow_none:bool=True):
    """Validate a numeric object and set expected minimum and upper bounds.

    Parameters
    ----------
    obj : any
        Object to validate
    min_value : float, optional
        Lower bound, by default None
    max_value : float, optional
        Upper bound, by default None
    obj_name : str, optional
        Object variable name, by default None
    allow_none : bool, optional
        Is the object allowed to be None or null, by default True

    Returns
    -------
    bool
        Validation exit flag
    """ 
    
       
    if allow_none & (obj is None):
        return True
    else:
    
        valid_type = isinstance(obj, (int, float)) or _validate_ndarray(obj, (1,1))
        valid_range = True
        
        if valid_type:
            if min_value is not None:
                valid_range = obj >= min_value
            if max_value is not None:
                valid_range = obj <= max_value

        valid_flag = valid_type & valid_range
        if isinstance(valid_flag, np.ndarray):
            if valid_flag.ndim == 2:
                valid_flag = valid_flag[0,0]
            else:
                valid_flag = valid_flag[0]
        
        if obj_name is not None:
            a = '\u221E' if min_value is None else min_value
            b = '\u221E' if max_value is None else max_value
            
            if not valid_flag:
                warnings.warn(f'Invalid {obj_name}, expecting int/float \u2208 (a,b).' , Warning)
        
        # Return the valid object type flag
        return valid_flag


def _validate_numeric_or_ndarray(obj, rows:int=None, cols:int=None, 
                                 obj_name:str=None, allow_none:bool=True):
    """Validate numeric or ndarray. Object can either be a single numeric
    scalar number, or a matrix of numbers.

    Parameters
    ----------
    obj : any
        Object to validate as numeric or an ndarray
    rows : int, optional
        Expected number of rows, by default None
    cols 1: int, optional
        Expected number of columns, by default None
    obj_name : str, optional
        Object variable name, by default None
    allow_none : bool, optional
        Allow object to be none/null, by default True

    Returns
    -------
    bool
        Validation exit flag
    """    
    
    
    if allow_none & (obj is None):
        return True
    else:
        return (
            _validate_numeric(obj) or 
            _validate_ndarray(obj, rows, cols, obj_name, allow_none)
        )
    
    
def _validate_str(obj, obj_name:str=None, allow_none:bool=True):
    """Validate string objects

    Parameters
    ----------
    obj : any
        Object to validate
    obj_name : str, optional
        Object variable name, by default None
    allow_none : bool, optional
        Is the object allowed to be null, by default True

    Returns
    -------
    bool
        Validation exit flag, True if object is a string
    """    
        
    if allow_none & (obj is None):
        return True
    else:
        return isinstance(obj, str)
    
    
def is_full_rank(X):
    """Checks to see if a given matrix is full rank.

    Parameters
    ----------
    X : ndarray
        Matrix to evaluate.

    Returns
    -------
    bool
        True if X is full rank (no linearly dependent variables)
    """    
    
    
    # Calculate the rank of the matrix
    rank = np.linalg.matrix_rank(X)
    
    # Determine the smallest dimension of the matrix
    min_dim = min(X.shape)
    
    # Check if the matrix is full rank
    return rank == min_dim


def _check_missing_data(matrix:np.ndarray, threshold:float=0.80):
    """Checks for missing data for a given 2d matrix. This validator
    will also restore damaged columns if their missing data ratio is
    below a certain threshold.

    Parameters
    ----------
    matrix : numpy.ndarray
        Matrix to check for missing data (and address as necessary).

    Returns
    -------
    bool    
        True if missing data of any kind (except empty which is handled downstream)
        False if checks pass.
    """

    # Check for None values and turn them into NaN so we can use built-in Numpy features
    if np.any(matrix == None):
        # Replace None or null values with np.nan
        matrix = np.where(matrix == None, np.nan, matrix)    

    # Check for NaN values
    if np.any(np.isnan(matrix)):
        return _restore_data(matrix=matrix, threshold=threshold)

    # If all checks pass, return matrix without restoring
    return matrix


def _restore_data(matrix:np.ndarray, threshold:float=0.80):
    """Restore missing data in a numpy 2D matrix by replacing NaN, None, 
    or null values with the column mean, unless more than 80% of the 
    column is missing.

    Parameters
    ----------
    matrix : numpy.ndarray
        Matrix with missing data to restore
    threshold : float, optional
        Missing data ratio per column, by default 0.80

    Returns
    -------
    numpy.ndarray
        Restored matrix with missing values replaced,
        and warnings issued for damaged columns.
    
    Raises
    ------
    ValueError
        If ratio of missing data per column exceeds the tolerance threshold.
    """    
    
    
    # Constants for restoring data
    observations, cols = matrix.shape

    # Create a boolean matrix missing Nan
    missing_values = np.isnan(matrix)
    missing_counts = np.sum(missing_values, axis=0) # Count missing values for each column

    # Calculate the damage percent for each column
    damage_percent = missing_counts / observations

    # Find columns with damage that crosses threshold. 
    high_damage_columns = np.where(damage_percent > threshold)[0] # Index 0 accesses index array of columns from np.where

    # Raise warning for columns with significant damage
    if high_damage_columns.size > 0:
        raise ValueError(f"Columns at indices: {str(high_damage_columns)} have significant amounts of missing data")

    # Compute column averages, ignoring NaN values
    column_averages = np.nanmean(matrix, axis=0)

    # Replace missing values with column averages
    matrix = np.where(missing_values, column_averages, matrix)
        
    # Return restored matrix
    return matrix