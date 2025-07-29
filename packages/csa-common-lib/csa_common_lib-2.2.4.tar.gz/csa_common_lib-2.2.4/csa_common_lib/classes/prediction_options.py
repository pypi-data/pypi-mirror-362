import copy
import numpy as np
from random import getrandbits

class _OptionsMeta(type):
    """Internal Metaclass for preventing incorrect attribute references on Options classes"""

    def __init__(cls, name, bases, dct):
        if not hasattr(cls, '_allowed_keys'):
            cls._allowed_keys = set([])  # Initialize as an empty set if not defined
        super().__init__(name, bases, dct)

    def __call__(cls, *args, **kwargs):
        instance = super().__call__(*args, **kwargs)
        extra_keys = kwargs.keys() - cls._allowed_keys # Extra keys that don't belong. Ie. Mistaken attributes
        if extra_keys:
            # Throw error and list invalid keys for user to correct
            raise AttributeError(f"Invalid class attribute(s): {extra_keys}. Allowed keys are: {cls._allowed_keys}")
        return instance
    

class PredictionOptions(metaclass=_OptionsMeta):
    """A configurable options class for relevance-based predictions, including
    predict, maxfit, and grid models. This class provides a comprehensive 
    list of all possible input parameters, ensuring flexibility across 
    different prediction models. While some parameters are shared across 
    inherrited models, setting an unused option for a specific model 
    will have no effect, ensuring compatibility and ease of use.
    
    threshold : float or ndarray [1-by-T], optional (default=None)
        Evaluation threshold to determine whether observations will be 
        included or excluded from the censor function in the 
        partial-sample regression. If threshold = None, the model 
        will evaluate across thresholds from [0, 0.90) in 0.10 increments.
    is_threshold_percent : bool, optional (default=True)
        Specify whether threshold is in percentage (decimal) units.
    most_eval : bool, optional (default=True)
        Specify the direction of the censor evaluation of the threshold.
        True:  [eval_type] score > threshold
        False: [eval_type] score < threshold
    eval_type : str, optional (default="both")
        Specify evaluation censor type, relevance, similarity, or both.
    adj_fit_multiplier : str, optional (default='K')
        Adjusted fit multiplier. Specify either 'log', 'K', or '1'.
    cov_inv : ndarray [K-by-K], optional (default=None)
        Inverse covariance matrix, specify for speed.

    Returns
    -------
    PredictionsOptions
        Options class to organize and persist parameters used in the
        the prediction models.

    Raises
    ------
    AttributeError
        When attempting to set or get an attribute that does not 
        exist in the options dictionary.
    """

    def __init__(self, **kwargs):

        self.options = {
            'threshold': [0],
            'is_threshold_percent': True,
            'most_eval': True,
            'eval_type': 'both',
            'adj_fit_multiplier': 'K',
            'cov_inv': None,
            'verify_missing_data': False,
        }

        self.__class__._allowed_keys = set(self.options.keys())

        # Update the options dictionary with any provided kwargs
        self.options.update(kwargs)


    def __getattr__(self, name):
        # Avoid recursion by checking if the attribute is already present in __dict__
        if name in self.__dict__:
            return self.__dict__[name]

        # Check if 'options' is in self.__dict__ to avoid KeyError
        if 'options' in self.__dict__ and name in self.__dict__['options']:
            return self.__dict__['options'][name]

        # Raise an AttributeError if the attribute is not found
        raise AttributeError(f"'PredictionOptions' object has no attribute '{name}'")


    def __setattr__(self, name, value):
        if name == "options":
            super().__setattr__(name, value)
        elif 'options' in self.__dict__ and name in self.options:
            self.options[name] = value
        else:
            raise AttributeError(f"'PredictionOptions' object has no attribute '{name}'")


    def display(self):
        for key, value in self.options.items():
            print(f"{key}: {value}")



    def init_from_dict(self, inputs):
        """ Accepts a dictionary of inputs and returns a 
        PredictionOptions object updated with all passed optional values. 
        Essentially, this is an update method.

        Args:
            inputs (dict): Intakes a dictionary of inputs deconstructed 
            in an AWS Lambda function.

        Returns:
            PredictionOptions: PredictionOptions obj that 
            holds all passed optional values. Non-passed options 
            remain default setting
        """

        
        # Iterate through input dict key/value pairs
        for key, value in inputs.items():
            # If obj attribute matches key in input dict
            if hasattr(self, key):
                # Update corresponding attribute in options object to hold dictionary value
                super().__setattr__(key, value)  # Use super() to avoid calling custom __setattr__


    def clone_with(self, **kwargs):
        """ Returns a clone of the passed PredictionOptions object 
        with user-specified attribute overwrites (via key value pairs)

        Args:
            key/value pair (attr/value): Attributes to overwrite in 
            the cloned object lambda function

        Returns:
            PredictionOptions: PredictionOptions obj 
        """
        
         # Create a new instance of PredictionOptions to avoid recursive loop in .deepcopy()
        new_copy = self.__class__()

        # Copy attributes from the original instance to the new instance
        for attr, value in self.__dict__.items():
            setattr(new_copy, attr, copy.deepcopy(value))

        # Overwrite attributes with passed parameter
        for key, value in kwargs.items():
            setattr(new_copy, key, value)

        return new_copy


class MaxFitOptions(PredictionOptions):
    """
    MaxFitOptions Class:
    Inherits from PredictionOptions and adds additional options specific
    max fit problems.
    
    threshold : not applicable
        Max fit solves for the optimal threshold that maximizes the 
        fit (or adjusted fit) value.
    threshold_range : tuple or ndarray
        Min/max range for evaluating maxfit threshold, by default (0, 0.20, 0.50, 0.80)
        If an ndarray is passed in, max fit evaluates over the specified
        threshold values in the ndarray
    stepsize : float, optional (default=0.20)
        Stepsize to evaluate range of thresholds to solve for max fit.
        Decreasing stepsize will increase the grid resolution.
    most_eval : bool, optional (default=True)
        Specify the direction of threshold evluation on the censor score.
        The censor score is determined by eval_type.
        True:  censor score > threshold
        False: censor score < threshold
    eval_type : str, optional (default="both")
        Specify censor threshold type, relevance, similarity, or both.
    cov_inv : ndarray [K-by-K], optional (default=None)
        Inverse covariance matrix, specify for speed.
    objective : str, optional (default="adjusted_fit)
        Objective function to optimize, either fit or adjusted_fit.
    
    Returns
    -------
    MaxFitOptions
        Options class to organize and persist parameters used for the
        maximum fit prediction model.

    Raises
    ------
    AttributeError
        When attempting to set or get an attribute that does not 
        exist in the options dictionary.        
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        maxfit_options = {
                        'threshold': None,
                        'threshold_range': np.array((0, 0.20, 0.50, 0.80), dtype='float32'),
                        'stepsize': 0.20,
                        'objective': 'kfit',
                        }
        
        self.__class__._allowed_keys = self.__class__._allowed_keys.union(maxfit_options.keys())

        self.options.update(maxfit_options)
        
        # Update the options dictionary with any provided kwargs
        self.options.update(kwargs)


class GridOptions(MaxFitOptions):
    """
    GridOptions Class:
    Inherits from MaxFitOptions and adds additional options.
    
    threshold_range : tuple or ndarray
        Min/max range for evaluating maxfit threshold, by default (0, 0.20, 0.50, 0.80)
        If an ndarray is passed in, max fit evaluates over the specified
        threshold values in the ndarray
    stepsize : float, optional (default=0.20)
        Stepsize to evaluate range of thresholds to solve for max fit.
        Decreasing stepsize will increase the granularity of the search.
        Not applicable if threshold_range is an ndarray.
    most_eval : bool, optional (default=True)
        Specify the direction of threshold evluation on the censor score.
        The censor score is determined by eval_type.
        True:  censor score > threshold
        False: censor score < threshold
    eval_type : str, optional (default="both")
        Specify censor threshold type, relevance, similarity, or both.
    cov_inv : ndarray [K-by-K], optional (default=None)
        Inverse covariance matrix, specify for speed.
    objective : str, optional (default="adjusted_fit)
        Objective function to optimize, either fit or adjusted_fit.
    attribute_combi : ndarray [Q-by-K], optional (default=None)
        Matrix of binary row vectors to indicate variable choices.
        Each row is a combination of variables to evaluate.
        If not specified, function will evaluate all possible combinations.
    max_iter : int, optional (default=1_000_000)
        Maximum number of grid cells to evaluate. Since this is a O(n^K)
        computational time, we suggest balancing computation time
        and memory with the maximum number of cells to evaluate.
    k : int, optional (default=1)
        Lower bound for the number of variables to include for any 
        combination Q, by default 1.
    _is_retain_all_grid_objects : boolean, optional (default=False)
        Saves and returns the weights grid for all censors, this is the
        the largest matrix in yhat_details. This is typically set to True
        for audit or deep research and development purposes.
        
    Returns
    -------
    GridOptions
        Options class to organize and persist parameters used for the
        grid (and grid singularity) prediction model.

    Raises
    ------
    AttributeError
        When attempting to set or get an attribute that does not 
        exist in the options dictionary.      
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        grid_options = {
                        'attribute_combi': None,
                        'max_iter': 1_000,
                        'k': 1,
                        '_is_retain_all_grid_objects': False, # Set this to True to retain memory expensive objects for audits or deep R&D
                        '_seed': getrandbits(32) # initialize for combi 
                    }
        
        self.__class__._allowed_keys = self.__class__._allowed_keys.union(grid_options.keys())

        self.options.update(grid_options)
        
        # Update the options dictionary with any provided kwargs
        self.options.update(kwargs)