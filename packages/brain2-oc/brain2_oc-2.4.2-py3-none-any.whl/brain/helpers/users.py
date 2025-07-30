# coding=utf8
""" Users

Shared methods for accessing user info
"""

__author__ = "Chris Nasr"
__copyright__ = "Ouroboros Coding Inc"
__version__ = "1.0.0"
__email__ = "chris@ouroboroscoding.com"
__created__ = "2022-08-29"

# Limit exports
__all__ = [ 'details', 'EMPTY_PASS', 'exists', 'permissions', 'SYSTEM_USER_ID' ]

# Ouroboros modules
from body import read, ResponseException
import undefined

# Python imports
from typing import List, Literal

# Pip imports
from brain.helpers.access import generate_key, SYSTEM_USER_ID

EMPTY_PASS = '000000000000000000000000000000000000' \
			 '000000000000000000000000000000000000'
"""Default password value"""

def details(
	_id: str | List[str],
	fields: List[str] = undefined,
	order: List[str] = undefined,
	as_dict: Literal[False] | str = '_id'
) -> dict | list:
	"""Details

	Fetches user info from IDs and returns a single object if a single ID is \
	passed, else returns a dict with each key representing the ID, with the \
	value being the rest of the user details requested via fields. Setting \
	`as_dict` to False, allows for returning a normal list which will be \
	sorted by `order`

	Arguments:
		_id (str|str[]) The ID(s) to fetch info for
		fields (str[]): The list of fields to return
		order (str[]): The list of fields to order by
		as_dict (False | str): Optional, if false, returns a list, if set, must
						be a field that's passed

	Returns:
		dict | list
	"""

	# Init the data by adding the ID(s)
	dData = { '_id': _id }

	# If we want specific fields
	if fields:
		dData['fields'] = fields

	# If we want a specific order
	if order:
		dData['order'] = order

	# Make the read using an internal key
	oResponse = read('brain', 'users/by/id', generate_key({
		'data': dData
	}))

	# If there's an error
	if oResponse.error:

		# Raise it
		raise ResponseException(oResponse)

	# If we got a single dictionary, or want the original unaltered list
	if not as_dict or isinstance(oResponse.data, dict):
		return oResponse.data

	# Convert the data into a dictionary
	dUsers = {}
	for d in oResponse.data:

		# Pop off the field used as a key
		sKey = d.pop(as_dict)

		# Store the rest by the key
		dUsers[sKey] = d

	# Return the users
	return dUsers

def exists(
	_id: str | List[str]
) -> bool:
	"""Exists

	Returns true if all User IDs passed exist in the system

	Arguments:
		_id (str | str[]): One or more IDs to check

	Returns:
		bool
	"""

	# Init the data by adding the ID(s)
	dData = { '_id': _id, 'fields': ['_id'] }

	# Make the read using an internal key
	oResponse = read('brain', 'users/by/id', generate_key({
		'data': dData
	}))

	# If there's an error
	if oResponse.error:

		# Throw it
		raise ResponseException(oResponse)

	# If we got a string
	if isinstance(_id, str):

		# Set the return based on whether we got anything or not
		bRet = oResponse.data and True or False

	# Else, we got a list
	else:

		# Set the return based on if the counts match
		bRet = len(_id) == len(oResponse.data)

	# Return
	return bRet

def permissions(
	user: str,
	portal: str = undefined
) -> dict:
	"""Permissions

	Returns the list of all permissions for the user by portal, or only the
	permissions for one specific portal

	Arguments:
		user (str): The ID of the user to fetch permissions for
		portal (str): Optional, the specific set of permissions to return

	Returns:
		dict | None
	"""

	# Init the data by adding the ID
	dData = { 'user': user }

	# If we have a portal
	if portal is not undefined:
		dData['portal'] = portal

	# Make the read using an internal key
	oResponse = read('brain', 'permissions', generate_key({
		'data': dData
	}))

	# If there's an error, raise it
	if oResponse.error:
		raise ResponseException(oResponse)

	# Return the permissions
	return oResponse.data