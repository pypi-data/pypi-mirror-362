"""
CSA Relevance Engine Package

The CSA Relevance Engine provides a comprehensive suite of relevance-based 
prediction tools that interact with Cambridge Sports Analytics' API. This 
package allows users to perform various predictive modeling tasks, 
including basic predictions, maximum fit calculations, grid-based 
optimizations, and grid singularity analysis using advanced relevance-based 
methods.

Available Modules
-----------------
- `relevance_engine`: Core module containing functions for different 
  prediction tasks, including `predict_psr`, `predict_maxfit`, `predict_grid`, 
  and `predict_grid_singularity`.
- `csa_common_lib`: Shared library that includes common classes, enums, 
  and validation tools to support the prediction engine's functionality.

Key Components
--------------
- `PSRFunction`: Enumeration of the available prediction function types 
  such as `PSR`, `MAXFIT`, `GRID`, and `GRID_SINGULARITY`.
- `PSRResult`: Enumeration of the expected result types for each prediction function.
- `PSRStatus`: Enumeration for exit flags that indicate the status of the 
  prediction process.

Classes
-------
- `PredictionOptions`: Base class for general prediction options.
- `MaxFitOptions`: Class for options specific to maximum fit predictions.
- `GridOptions`: Class for options specific to grid-based predictions.

Utilities
---------
- `is_full_rank`: Checks if a matrix has full rank, which is necessary for 
  ensuring the correctness of input data.
- `validate_inputs`: Verifies the integrity of inputs to the prediction 
  functions, ensuring they meet the required criteria for successful execution.

Version Information
-------------------
- `__version__`: The current version of the CSA Relevance Engine package.

(c) 2023 - 2024 Cambridge Sports Analytics, LLC. All rights reserved.
For support, contact: support@csanalytics.io
"""

# Version information
from .version import __version__

# # Enumeration types
# from csa_common_lib.enum_types.functions import PSRFunction
# from csa_common_lib.enum_types.results import PSRResult
# # from csa_common_lib.enum_types.exit_flags import PSRStatus # commented out bc does not exist at the moment

try:
  # csa_common_lib imports
  from csa_common_lib.classes.prediction_options import (
      PredictionOptions,
      MaxFitOptions,
      GridOptions
  )

  # Prediction receipts and results classes
  from csa_common_lib.classes.prediction_results import PredictionResults
  from csa_common_lib.classes.prediction_receipt import PredictionReceipt
  # Validators
  from csa_common_lib.toolbox._validate import (
      is_full_rank,
      validate_inputs
  )
# Raise Error if imports fail
except Exception as e:
  raise Exception(f"csa_prediction_engine requires csa_common_lib. Please pip install or update csa_common_lib to use this package. Error:{e}")

# End-points
from .api_client import (
    predict_psr,
    predict_maxfit,
    predict_grid,
    predict_grid_singularity,
    get_api_quota
)

