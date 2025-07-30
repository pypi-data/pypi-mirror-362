# coding=utf8
""" Errors

Brain error codes
"""

__author__ = "Chris Nasr"
__copyright__ = "Ouroboros Coding Inc"
__version__ = "1.0.0"
__email__ = "chris@ouroboroscoding.com"
__created__ = "2023-01-16"

# Import all body errors as local errors
from body.errors import *

SIGNIN_FAILED = 1200
"""Sign In Failed"""

PASSWORD_STRENGTH = 1201
"""Password not strong enough"""

BAD_PORTAL = 1202
"""Portal doesn't exist, or the user doesn't have permissions for it"""

INTERNAL_KEY = 1203
"""Internal key failed to validate"""

BAD_OAUTH = 1204
"""Something failed in the OAuth process"""

BAD_CONFIG = 1205
"""Something is missing from the configuration"""

__all__ = [ n for n,v in globals().items() if isinstance(v, int) ]
""" Export all the constants"""