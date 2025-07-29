import inspect


def class_obj_to_dict(obj):
    """
    Converts a class object into a dictionary containing its attributes and 
    respective values.

    Parameters
    ----------
    obj : object
        An instance of any class type.

    Returns
    -------
    dict
        A dictionary containing the attributes and their values of the class 
        object. If the object has a `__dict__` attribute, it directly returns 
        `obj.__dict__`. Otherwise, it inspects the object's attributes and 
        returns a dictionary of attribute names and values, excluding private 
        or protected attributes (those starting with an underscore).
    """
    
    
    if hasattr(obj, '__dict__'):
        # If the object has a __dict__ attribute, return it directly.
        return obj.__dict__
    else:
        # Get non-routine attributes, excluding private/protected attributes.
        attributes = inspect.getmembers(obj, lambda a: not(inspect.isroutine(a)))
        return {name: value for name, value in attributes if not name.startswith('_')}


def is_obj_userdefined_class(obj):
    """
    Checks if the given object is an instance of a user-defined class.

    Parameters
    ----------
    obj : object
        An instance of any class type.

    Returns
    -------
    bool
        True if the object is an instance of a user-defined class, 
        False otherwise.
    """
    
    
    obj_type = type(obj)

    # Check if the object is a class and not from the built-in module.
    return inspect.isclass(obj_type) and obj_type.__module__ != 'builtins'