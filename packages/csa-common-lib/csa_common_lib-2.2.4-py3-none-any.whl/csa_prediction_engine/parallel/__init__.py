"""
Initialization module for the end-user (API) parallel package.

This module re-exports key functions from the threaded_predictions module
for simplified access.
"""


from csa_prediction_engine.parallel._threaded_predictions import (
    run_multi_theta,
    run_multi_y
)