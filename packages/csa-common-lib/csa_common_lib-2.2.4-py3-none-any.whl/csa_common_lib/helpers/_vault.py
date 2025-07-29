from csa_local_compute.classes._vault_metadata import VaultMetadata
from csa_common_lib.classes.prediction_options import PredictionOptions


def validate_vault_npz_data(y, X, theta, yhat_details, 
                            Metadata: VaultMetadata, Options: PredictionOptions = None) -> bool:
    """
    Validates the formatting of input data before saving to a .npz file.
    Ensures that all data arrays and metadata are consistent and correctly formatted.

    Parameters
    ----------
    y : ndarray
        Array of dependent variable data.
    X : ndarray
        Matrix of independent variables data.
    theta : ndarray
        Matrix of experimental conditions or circumstances.
    yhat_details : dict
        Result data generated from a prediction.
    Metadata : VaultMetadata
        Custom object for storing supporting experiment data, such as labels 
        and additional metadata information.
    Options : PredictionOptions, optional
        Custom object for storing optional prediction parameters.
        Also accepts MaxFitOptions and GridOptions 
        (inherits from PredictionOptions), defaults to None.

    Raises
    ------
    ValueError
        If any of the data or metadata formats are inconsistent or incorrect.

    Returns
    -------
    bool
        True if all data and metadata are formatted correctly.
    """

    # Check that Metadata attributes are lists
    if not isinstance(Metadata.Xcol_labels, list):
        raise ValueError(
            f"Metadata.Xcol_labels needs to be of type list. It is of type: {type(Metadata.Xcol_labels)}"
        )
    if not isinstance(Metadata.Xrow_labels, list):
        raise ValueError(
            f"Metadata.Xrow_labels needs to be of type list. It is of type: {type(Metadata.Xrow_labels)}"
        )
    if not isinstance(Metadata.outcome_labels, list):
        raise ValueError(
            f"Metadata.outcome_labels needs to be of type list. It is of type: {type(Metadata.outcome_labels)}"
        )

    # Check that column dimensions match across data
    if len(theta) > 0:
        if len(theta[0]) != len(Metadata.Xcol_labels):
            raise ValueError("The number of variables in theta does not match Metadata.Xcol_labels.")
        if len(Metadata.outcome_labels) != len(theta):
            raise ValueError("Metadata.outcome_labels does not match the length of theta.")

    if len(Metadata.Xrow_labels) != len(X):
        raise ValueError("Metadata.Xrow_labels does not match the number of rows in the X matrix.")
    if len(Metadata.Xrow_labels) != len(y):
        raise ValueError("Metadata.Xrow_labels does not match the number of observations in y (inputs).")
    if len(theta) < 1:
        raise ValueError("Theta is empty. Please supply experimental conditions.")
    if len(y) != len(X):
        raise ValueError("Mismatch in the number of observations between X and y (inputs).")

    # If no formatting errors are detected, return True
    return True


def _extract_ids(id_dict:dict):
    """Processes a dictionary of ids and validates that none are empty along the way.
    Prompts user if an id is missing.  

    Args:
        id_dict (dict): Dictionary of key value pairs where the value is the db id

    Returns:
        id_list list[int]: Array of ids extracted from the dictionary
    """

    keys = id_dict.keys()

    no_id = []
    id_list = []

    for key in keys:
        id = id_dict[key]

        if id == None or not isinstance(id, int):
            no_id.append(key)
        else:
            id_list.append(id)

    if len(no_id) > 0:
        proceed_flag = _prompt_user_for_missing_ids(no_id=no_id)
        if proceed_flag == False:
            print("Subset selection ended. ")
            return 
    
    return id_list


def _prompt_user_for_missing_ids(no_id):
    """
    Prompt the user to decide whether to continue with the upload when some player IDs are missing.

    Args:
        no_id (list): List of player IDs that are missing.

    Returns:
        bool: True if the user wants to continue, False otherwise.
    """

    # Warn the user about the missing IDs
    print(f"Warning: {len(no_id)} player(s) will be excluded due to missing IDs.")

    # Ask if they want to see the players who will be excluded
    show_missing = input("Do you want to see the players who will not be included? (y/n): ").strip().lower()
    if show_missing == 'y':
        print("The following players will be excluded:")
        for player_id in no_id:
            print(player_id)

    # Ask if they want to continue with the upload
    proceed = input("Do you want to continue with the upload? (y/n): ").strip().lower()
    if proceed == 'y':
        return True
    else:
        return False
    