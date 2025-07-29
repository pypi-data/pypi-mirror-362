# Standard library imports
import os

# Third-party imports
import numpy as np

# Local application imports
from csa_common_lib.helpers._conversions import convert_to_float32
from csa_common_lib.toolbox.classes.utilities import (
    class_obj_to_dict,
    is_obj_userdefined_class
)


def load_npz(file_path: str) -> dict:
    """
    Loads a `.npz` file and returns its contents as a dictionary.

    Parameters
    ----------
    file_path : str
        Path to the `.npz` file.

    Returns
    -------
    dict
        A dictionary containing the key-value pairs from the `.npz` file.
        If the file does not exist or an error occurs during loading, 
        an empty dictionary is returned.
    """
    
    if os.path.exists(file_path):
        # Try loading the .npz file into a dictionary.
        try:
            with np.load(os.path.normpath(file_path), allow_pickle=True) as npz_file:
                obj = {}
                for key in npz_file.files:
                    # Convert numpy arrays to lists.
                    obj[key] = npz_file[key].tolist() if isinstance(npz_file[key], np.ndarray) else npz_file[key]
                return obj
        except Exception as e:
            print(f"Failed to load .npz file: {e}")
            return {}
    else:
        print(f"Invalid file path: {file_path}")
        return {}


def save_to_npz(filename: str = None, single_precision: bool = False, **data) -> str:
    """
    Saves the given data to a compressed `.npz` file.

    Parameters
    ----------
    filename : str, optional
        The name of the file to save the data in. If not provided, defaults to None.
    single_precision : bool, optional
        If True, converts numerical data to `float32` before saving. Default is False.
    **data : dict
        Additional data to save, passed as keyword arguments. The names of the 
        variables are preserved as keys in the `.npz` file.

    Returns
    -------
    str
        The name of the saved file.

    Raises
    ------
    ValueError
        If `filename` is not provided.
    """
    
    if not filename:
        raise ValueError("Filename must be provided to save the data.")

    # Ensure the filename ends with '.npz'
    if not filename.endswith(".npz"):
        filename += ".npz"

    # Convert user-defined class instances to dictionaries.
    for key, value in data.items():
        if is_obj_userdefined_class(value):
            data[key] = class_obj_to_dict(value)

    # Convert all data to float32 before saving, if requested.
    if single_precision:
        data = {k: convert_to_float32(v) for k, v in data.items()}

    # Save the data into a compressed `.npz` file.
    np.savez_compressed(filename, **data)

    return filename