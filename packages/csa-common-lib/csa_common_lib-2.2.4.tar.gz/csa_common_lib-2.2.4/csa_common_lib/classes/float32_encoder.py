"""
Optimized JSON Encoder for Float Precision

This module defines the `Float32Encoder` class, an optimized JSON encoder
that formats floating-point numbers to a specified precision. It is designed for
efficient performance with support for `float`, `np.float32`, and `np.float64`
types. This encoder is optimized to handle nested data structures containing
floats, lists, dictionaries, and numpy arrays.

Classes
-------
Float32Encoder : json.JSONEncoder
    A JSON encoder for encoding floats to 8 decimal places with optimized performance.
"""

import json
import numpy as np
from decimal import (
    Decimal, 
    ROUND_HALF_EVEN, 
    DecimalException
)


class Float32Encoder(json.JSONEncoder):
    """
    JSON encoder for encoding floats to a specific precision with optimized performance.

    This encoder is optimized by pre-compiling a decimal precision context for
    truncation, reducing the need for redundant computations. It processes nested
    structures like lists and dictionaries to ensure consistent float precision
    throughout the JSON output.

    Attributes
    ----------
    quantize_exp : Decimal
        Decimal object representing the precision for truncation to 8 decimal places.

    Methods
    -------
    _truncate(x):
        Truncates a float to 8 decimal places using a predefined decimal precision.
    _process(obj):
        Recursively processes nested objects, applying truncation to all float values.
    encode(obj):
        Encodes a JSON object with processed float values to 8 decimal places.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes the encoder with a pre-compiled decimal precision context.

        This context is set to 8 decimal places, which helps in rounding float
        values efficiently to the nearest even decimal. Pre-compiling this precision
        reduces the overhead of creating Decimal objects for each encoding operation.

        Parameters
        ----------
        *args : tuple
            Positional arguments passed to the parent JSONEncoder.
        **kwargs : dict
            Keyword arguments passed to the parent JSONEncoder.
        """
        super().__init__(*args, **kwargs)
        self.quantize_exp = Decimal('0.00000000')  # Pre-compiled for 8-decimal precision


    def _truncate(self, x):
        """
        Truncates a float to 8 decimal places, rounding to the nearest even number.

        This method uses the pre-compiled `quantize_exp` attribute to apply
        precision consistently. The rounding mode `ROUND_HALF_EVEN` is used to
        minimize rounding bias in statistical data.
        
        If the value is NaN or Infinity, it is replaced with None (which serializes as null).

        Parameters
        ----------
        x : float
            The float value to truncate.

        Returns
        -------
        float
            The truncated float value, or the original value if truncation fails.
        """
        
        if np.isnan(x) or np.isinf(x):  # Replace NaN or Infinity with None
            return None
        
        try:
            return float(Decimal(format(x, '.8f')).quantize(
                self.quantize_exp, rounding=ROUND_HALF_EVEN
            ))
        except (DecimalException, ValueError):
            return x  # Return original value if there's an exception


    def _process(self, obj):
        """
        Processes an object by truncating all float values within nested structures.

        This method applies `_truncate` recursively to handle data structures
        such as dictionaries, lists, and numpy arrays. It ensures all float values
        in the structure are consistently truncated to 8 decimal places.

        Parameters
        ----------
        obj : any
            The object to process. This can be a float, list, dictionary, or numpy array.

        Returns
        -------
        any
            The processed object with all float values truncated, maintaining
            the original structure of the input.
        """
        obj_type = type(obj)

        if obj_type in (float, np.float32, np.float64):
            return self._truncate(obj)
        elif obj_type == dict:
            return {k: self._process(v) for k, v in obj.items()}
        elif obj_type in (list, np.ndarray):
            return [self._process(x) for x in obj]
        return obj

    def encode(self, obj):
        """
        Encodes the processed object as a JSON-formatted string.

        This method overrides the `encode` method of JSONEncoder, ensuring that
        all float values in the object are processed for precision before encoding.

        Parameters
        ----------
        obj : any
            The object to encode, which may contain nested structures with float values.

        Returns
        -------
        str
            JSON-encoded string with truncated float values.
        """
        return super().encode(self._process(obj))