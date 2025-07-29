

# Helper function to flatten nested lists
def flatten_nested_list(nested_list):
    """Flattens a single-level nested list if it contains only one 
    nested list element.

    Parameters
    ----------
    nested_list : list
        A list that may contain a nested list with a single element (node).

    Returns
    -------
    list or any
        The first element of the nested list if `nested_list` contains
        a single nested list; otherwise, returns `nested_list` as is.

    Examples
    --------
    >>> flatten_nested_list([[5]])
    5
    >>> flatten_nested_list([5])
    [5]
    >>> flatten_nested_list([[5, 6]])
    [[5, 6]]
    """
    
    if (
        isinstance(nested_list, list) 
        and len(nested_list) == 1 
        and isinstance(nested_list[0], list)
    ):
        # Return the first element of the nested list
        return nested_list[0][0]
    
    # Return the element as is if not nested
    return nested_list  
