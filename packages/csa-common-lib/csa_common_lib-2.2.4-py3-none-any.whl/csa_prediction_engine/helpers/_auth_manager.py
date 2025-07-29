"""
CSA Relevance Engine: Authentication Manager Module

This module provides utility functions for retrieving API keys 
and access credentials from environment variables. These keys 
are necessary for authenticating API requests to the Cambridge 
Sports Analytics platform.

Functions
---------
_get_apikeys()
    Retrieves required environment variables (`CSA_API_KEY` and 
    `CSA_ACCESS_ID`) stored in the operating system. Ensures that 
    these variables are set and not null.

Raises
------
EnvironmentError
    Raised when required environment variables are missing or null.

Example
-------
>>> api_key, access_id = _get_apikeys()
>>> print(api_key, access_id)

(c) 2023 - 2024 Cambridge Sports Analytics, LLC. All rights reserved.
support@csanalytics.io
"""


# Standard library import(s)
import os


def _get_apikeys():
    """Retrieves required environment variables CSA_ACCESS_ID 
    and CSA_ACCESS_KEY that is set and stored in the OS.

    Returns
    -------
    str
        Organization API key.
    str
        User Access ID.

    Raises
    ------
    Exception
        If CSA_API_KEY is null or not defined.
    Exception
        If CSA_ACCESS_ID is null or not defined.
    """   
    
    # Retrieve the required user environment variables
    api_key = os.getenv('CSA_API_KEY')
    access_id = os.getenv('CSA_ACCESS_ID')
    
    if api_key:
        pass
    else:
        raise Exception("CSA_API_KEY environment variable is not set or null.")
    
    if access_id:
        pass
    else:
        raise Exception("CSA_ACCESS_ID environment variable is not set or null.")
    
        
    # Return the api key, access id, and access key
    return api_key, access_id