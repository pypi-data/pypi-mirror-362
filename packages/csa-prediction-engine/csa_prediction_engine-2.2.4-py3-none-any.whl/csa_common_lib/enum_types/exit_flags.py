from enum import Enum

# http return codes
# from http import HTTPStatus

class AccessIDStatus(Enum):
    """Enumeration of Access ID Status flags.

    Parameters
    ----------
    Enum : AccessIDStatus
        Access ID status codes
    """    
    VALID = (0, 'Access ID verified.')
    EXPIRED = (1, 'Access ID expired.')
    INVALID = (2, 'Invalid Access ID or Key.')
    
    def __str__(self):
        return self.value[1]
        
    def __float__(self):
        return float(self.value[0])
    
    def __int__(self):
        return self.value[0]
    
    
class UserTokenStatus(Enum):
    """Enumeration of user Token Status flags.

    Parameters
    ----------
    Enum : UserTokenStatus
        User token status codes
    """    
    VALID = (0, 'Token verified.')
    INVALID = (1, 'Invalid token.')
    EXPIRED_ACCESS = (2, 'Expired token.')
    MAX_TOKEN = (3, 'Invalid token: Maximum number of tokens reached.')
    NON_EXISTENT = (4, 'Token does not exist.')

    def __str__(self):
        return self.value[1]
        
    def __float__(self):
        return float(self.value[0])
    
    def __int__(self):
        return self.value[0]