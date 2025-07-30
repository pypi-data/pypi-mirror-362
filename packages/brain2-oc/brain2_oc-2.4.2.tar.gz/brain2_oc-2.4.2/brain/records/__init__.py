# coding=utf8
""" Records

Handles shared records connections
"""

__author__		= "Chris Nasr"
__version__		= "1.0.0"
__maintainer__	= "Chris Nasr"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2025-03-11"

# Ouroboros imports
from define import Parent

# Python imports
import pathlib

redis = None
"""Redis records connection"""

Verify = Parent.from_file('%s/define/verify.json' % \
		pathlib.Path(__file__).parent.parent.resolve()
)
"""Used to validate verify calls from the outside"""