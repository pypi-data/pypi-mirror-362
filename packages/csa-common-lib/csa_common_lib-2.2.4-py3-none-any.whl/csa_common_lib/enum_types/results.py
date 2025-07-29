from enum import Enum

# 'weights': weights,
#         'relevance': r,
#         'similarity': simlr_x,
#         'info_x': info_x,
#         'info_theta': info_theta,
#         'include': include,
#         'lambda_sq': verify_row_vector(lambda_sq),
#         'n': verify_row_vector(n),
#         'phi': verify_row_vector(phi),
#         'r_star': verify_row_vector(r_star),
#         'r_star_percent': verify_row_vector(r_star_percent/100),
#         'most_eval': repmat(np.array([most_eval]), 1, r_star.size)

class PSRResult(Enum):
    """Enumeration of PSR library result types.

    Parameters
    ----------
    Enum : PSR Result Types
        Partial Sample Regression result types.
    """    
    YHAT = (0, 'y_hat')
    FIT = (1, 'fit')
    WEIGHTS = (2, 'weights')
    RELEVANCE = (3, 'relevance')
    SIMILARITY = (4, 'similarity')
    INFO_X = (5, 'info_X')
    INFO_THETA = (6, 'info_theta')
    INCLUDE = (7, 'include')
    LAMBDA_SQ = (8, 'lambda_sq')
    N = (9, 'n')
    PHI = (10, 'phi')
    R_STAR = (11, 'r_star')
    R_STAR_PERCENT = (12, 'r_star_percent')
    ALL = (13, 'all')
    
    def __str__(self):
        return self.value[1]
        
    def __float__(self):
        return float(self.value[0])
    
    def __int__(self):
        return self.value[0]
    