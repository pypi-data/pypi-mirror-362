from enum import Enum

class LambdaStatus(Enum):
    """Enumeration of AWS Lambda status codes and their associated messages.

    Attributes
    ----------
    INITIALIZED : tuple
        Status code and message for inputs initialized in the database.
    PENDING : tuple
        Status code and message for inputs awaiting processing.
    PROCESSING : tuple
        Status code and message for a job currently being processed.
    COMPLETED : tuple
        Status code and message for a completed prediction task.
    """

    # Post-job
    INITIALIZED = (0, 'initialized') # Inputs initialized in the database
    PENDING = (1, 'pending') # Inputs are waiting to be processed

    # Process Job    
    PROCESSING = (10, 'processing') # Currently processing the job
    COMPLETED = (11, 'completed') # Prediction task has been completed


    @classmethod
    def status_by_code(cls, code):
        """Retrieve the full enum object based on the code.

        Parameters
        ----------
        code : int
            The status code to search for.

        Returns
        -------
        tuple or None
            The corresponding status tuple (code, message) if found,
            otherwise `None`.
        """
        
        
        for status in cls:
            if status.value[0] == code:
                return status.value
        return None  