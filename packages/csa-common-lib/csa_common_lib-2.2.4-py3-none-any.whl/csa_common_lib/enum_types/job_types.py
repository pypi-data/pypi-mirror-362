from enum import Enum


class JobType(Enum):
    """Enumeration of prediction task types.
    
    This enumeration provides a list of task types for different
    prediction job modes. Each task type is represented by a tuple,
    containing a numerical identifier and a string label.

    Attributes
    ----------
    SINGLE : tuple
        Represents a single prediction task type with an identifier of 0.
    MULTI_Y : tuple
        Represents a multi-y prediction task type with an identifier of 1.
    MULTI_THETA : tuple
        Represents a multi-theta prediction task type with an identifier of 2.
    """    
    
    SINGLE = (0, 'single')
    MULTI_Y = (1, 'multi_y')
    MULTI_THETA = (2, 'multi_theta')
    
    
    def __str__(self):
        """Returns the string representation of the task type."""
        return self.value[1]

    def __float__(self):
        """Returns the numerical identifier of the task type as a float."""
        return float(self.value[0])

    def __int__(self):
        """Returns the numerical identifier of the task type as an integer."""
        return self.value[0]