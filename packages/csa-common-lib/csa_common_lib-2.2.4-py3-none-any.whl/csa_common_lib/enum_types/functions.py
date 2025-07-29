from enum import Enum


class PSRFunction(Enum):
    """Enumeration of PSR library function types.

    Parameters
    ----------
    Enum : PSR Function Types
        Partial Sample Regression function types.
    """    
    PSR = (0, 'psr')
    MAXFIT = (1, 'maxfit')
    GRID = (2, 'grid')
    GRID_SINGULARITY = (3, 'grid_singularity')
    PSR_BINARY = (4, 'psr_binary')
    MAXFIT_BINARY= (5, 'maxfit_binary')
    GRID_BINARY = (6, 'grid_binary')
    GRID_SINGULARITY_BINARY = (7, 'grid_singularity_binary')
    
    
    def __str__(self):
        return self.value[1]
        
    def __float__(self):
        return float(self.value[0])
    
    def __int__(self):
        return self.value[0]