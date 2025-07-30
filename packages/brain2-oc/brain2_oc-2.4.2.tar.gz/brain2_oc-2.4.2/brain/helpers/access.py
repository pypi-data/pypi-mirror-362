# coding=utf8
""" Access

Shared methods for verifying access
"""

__author__ = "Chris Nasr"
__copyright__ = "Ouroboros Coding Inc"
__version__ = "1.0.0"
__email__ = "chris@ouroboroscoding.com"
__created__ = "2022-08-29"

# Limit exports
__all__ = [
	'generate_key', 'internal', 'internal_or_verify', 'SYSTEM_USER_ID' 'verify'
]

# Ouroboros imports
import body
from config import config
import jobject
from memory import _Memory
from nredis import nr
from strings import random

# Python imports
from hashlib import sha1
from time import time
from typing import List, MutableMapping
from sys import stderr

# Package imports
from brain import errors, rights

# Constants
INTERNAL = 1
VERIFY = 2

ALL = rights.ALL
A = ALL
"""Allowed to CRUD"""

CREATE = rights.CREATE
C = CREATE
"""Allowed to create records"""

DELETE = rights.DELETE
D = DELETE
"""Allowed to delete records"""

READ = rights.READ
R = READ
"""Allowed to read records"""

UPDATE = rights.UPDATE
U = UPDATE
"""Allowed to update records"""

SYSTEM_USER_ID = '00000000000000000000000000000000'
"""System User ID"""

RIGHTS_ALL_ID = '012345679abc4defa0123456789abcde'
"""Used to represent rights across the entire system"""

_internal = config.brain.internal({
	'redis': 'session',
	'salt': '',
	'ttl': 5
})
"""Internal Configuration"""

_redis_conn = nr(_internal['redis'])
"""Redis Connection"""

# Encode the salt to utf-8
_internal['salt'] = _internal['salt'].encode('utf-8')

# Don't allow 0 for ttl, and give a warning if anyone tries
if _internal['ttl'] <= 0:
	print(
		'brain.internal.ttl can NOT be less than 0 (zero). Setting to 5 ' \
		'(seconds)',
		file=stderr
	)
	_internal['ttl'] = 5

def generate_key(req: MutableMapping) -> MutableMapping:
	"""Generate Key

	Used as a wrapper to generates a key and add it to the passed req which it
	then returns.

	Arguments:
		req (MutableMapping): The dict or jobject being sent with the request.

	Returns:
		The same req object passed to it
	"""

	# Pull in the global internal config
	global _internal

	# Generate a unique ID
	sID = str(random(32, [ 'aZ', '10', '!*' ]))

	# Get the current timestamp as a string
	sTime = str(int(time()))

	# Generate a sha1 from the salt and parts of the time
	sSHA1 = sha1(
		sTime[3:].encode('utf-8') +
		_internal['salt'] +
		sTime[:3].encode('utf-8')
	).hexdigest()

	# Store the key
	if not _redis_conn.set(name = sID, value = sSHA1, ex = _internal['ttl']):
		return False

	# Add the meta
	try:
		req['meta']['Authorize-Internal'] = '%s~%s' % ( sID, sTime )
	except KeyError:
		req['meta'] = { 'Authorize-Internal': '%s~%s' % ( sID, sTime ) }

	# Return the req
	return req

def internal(req: jobject):
	"""Internal

	Checks for an internal key and throws an exception if it's missing or
	invalid

	Arguments:
		req (jobject): The req object passed to the request

	Raises:
		ResponseException

	Returns:
		None
	"""

	# Pull in the global internal config
	global _internal

	# Get the current time stamp as soon as possible
	iNow = int(time())

	# Use bottle from inside body.rest to get the text ID and time using the
	#	Authorize-Internal header
	try:
		sID, sTime = req.meta['Authorize-Internal'].split('~')
	except KeyError:
		raise body.ResponseException(error = (
			errors.INTERNAL_KEY, 'missing'
		))

	# Fetch the key from redis
	sKey = _redis_conn.get(sID).decode()
	if sKey is None:
		raise body.ResponseException(error = (
			errors.INTERNAL_KEY, 'no key'
		))

	# If the time is not close enough, the rest is irrelevant
	if int(sTime) - iNow > _internal['ttl']:

		# Raise an exception
		raise body.ResponseException(error = (
			errors.INTERNAL_KEY, 'expired'
		))

	# Generate a sha1 from the salt, parts of the text, and the time
	sSHA1 = sha1(
		sTime[3:].encode('utf-8') +
		_internal['salt'] +
		sTime[:3].encode('utf-8')
	).hexdigest()

	# If they aren't equal
	if sSHA1 != sKey:
		raise body.ResponseException(error = (
			errors.INTERNAL_KEY, 'invalid'
		))

	# Delete the key
	_redis_conn.delete(sID)

	# Return OK
	return True

def internal_or_verify(
	req: jobject,
	permission: dict | List[dict]
) -> str:
	""" Internal or Verify

	Checks for an internal key, if it wasn't sent, does a verify check.

	Returns the UUID of the user requesting access via the session, else the \
	SYSTEM_USER_ID when the request is made internally

	Arguments:
		req (jobject): The current request object sent to the request
		permission (dict | dict[]): A dict with 'name', 'right' and optional \
			'id', or a list of those dicts

	Raises:
		ResponseException

	Returns:
		string
	"""

	# If we have an internal key
	if 'meta' in req and 'Authorize-Internal' in req.meta:

		# Run the internal check
		internal(req)

		# Return that the request passed the internal check
		return SYSTEM_USER_ID

	# Else
	else:

		# Make sure the user has the proper permission to do this
		verify(req.session, permission)

		# Return that the request passed the verify check
		return req.session.user._id

def verify(
	session: _Memory,
	permission: dict | List[dict],
	_return: bool = False
) -> True:
	"""Verify

	Checks's if the currently signed in user has the requested right on the
	given permission. If the user has rights, True is returned, else an
	exception of ResponseException is raised

	Arguments:
		session (memory._Memory): The current session
		permission (dict | dict[]): A dict with 'name', 'right' and optional \
			'id', or a list of those dicts
		_return (bool): Optional, set to True to return instead of raising

	Raises:
		ResponseException

	Returns:
		bool
	"""

	# Check with the authorization service
	oResponse = body.read('brain', 'verify', {
		'data': permission,
		'session': session
	})

	# If the response failed
	if oResponse.error:
		raise body.ResponseException(oResponse)

	# If the check failed, raise an exception
	if not oResponse.data:
		if _return: return False
		raise body.ResponseException(error = body.errors.RIGHTS)

	# Return OK
	return True