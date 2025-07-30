# coding=utf8
""" Permissions

Brain permission codes
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc"
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-09-18"

ALL = 0xF
"""Allowed to CRUD"""

CREATE = 0x1
"""Allowed to create records"""

DELETE = 0x8
"""Allowed to delete records"""

READ = 0x2
"""Allowed to read records"""

UPDATE = 0x4
"""Allowed to update records"""

RIGHTS_ALL_ID = '012345679abc4defa0123456789abcde'
"""Used to represent rights across the entire system"""