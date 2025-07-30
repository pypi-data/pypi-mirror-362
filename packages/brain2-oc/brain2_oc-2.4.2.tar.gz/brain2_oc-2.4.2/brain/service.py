# coding=utf8
""" Brain Service

Handles all Authorization / Login requests
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__email__		= "chris@ouroboroscoding.com"
__created__		= "2022-08-26"

# Ouroboros imports
from body import create, Error, Response, ResponseException, Service
from body.external import request as body_request
from body.regex import EMAIL_ADDRESS
from config import config
from define import Hash
from jobject import jobject
import memory
from nredis import nr
from rest_mysql.Record_MySQL import DuplicateException
from strings import random
from tools import clone, combine, evaluate, get_client_ip, merge, without

# Python imports
import re
import requests
from sys import stderr
from typing import List, Literal

# Pip imports
from googleapiclient.discovery import build as gapi_build
from oauthlib.oauth2.rfc6749.errors import InvalidGrantError

# Records
from brain import records
from brain.records.key import Key
from brain.records.permission import Permission
from brain.records.user import password_validate, User

# Errors and Helpers
from brain import errors
from brain.helpers import access, users

# Constants
_VERBOSE = False

# Regular expressions
_URL = re.compile(r'^https?:\/\/.*?\{key\}.*?$')

class Brain(Service):
	"""Brain Service class

	Service for authorization, sign in, sign up, permissions etc.

	### Rights
	In the case of all things RIGHTS, when dealing with a number (js) or
	int (py), it symbolises the first 4 bits

	```0x01``` (C)reate\\
	```0x02``` (R)ead\\
	```0x04``` (U)pdate\\
	```0x08``` (D)elete

	So if you wanted to give full access, it would be `15`.\\
	```c | r | u | d = 15```

	Only read access? ```2```

	Only create access? ```1```

	User can read and update records, but never create or delete any\\
	```r | u = 6```

	#### python rights
	In python these bits can be found in the `brain.rights` module

	```python
	# Import individually
	from brain.rights import ALL, CREATE, READ, UPDATE, DELETE
	```

	```python
	# Import the entire rights module
	from brain import rights

	# If the user can create
	-if some_rights & rights.CREATE:-
	  # do some creating
	```

	#### javascript rights

	In JavaScript / React these bits can be found in the `@ouroboros/brain`
	module

	```javascript
	import { RIGHTS } from '@ouroboros/brain';
	if(some_rights & RIGHTS.CREATE) {
	  // do some creating
	}
	```

	### RIGHTS_ALL_ID
	When setting a right that is global, i.e. across all possible IDs, you need
	an ID that is both valid, and impossible, for this we have, RIGHTS_ALL_ID

	#### RIGHTS_ALL_ID in python
	In python RIGHTS_ALL_ID can be found in the `brain.rights` module

	```python
	# Import individually
	from brain.rights import RIGHTS_ALL_ID
	```

	```python
	# Import the entire rights module
	from brain import rights

	# Set global 'my_service_permission' to create, read, update and delete
	permissions = {
	  'my_service_permission': {
	    rights.RIGHTS_ALL_ID = rights.ALL
	  }
	}
	```

	#### RIGHTS_ALL_ID in javascript
	In javascript RIGHTS_ALL_ID can be found in the `@ouroboros/brain` module

	```javascript
	import { RIGHTS_ALL_ID, RIGHTS } from '@ouroboros/brain';

	// Set global 'my_service_permission' just to create and to delete
	const permissions = {
	  'my_service_permission': {
	    RIGHTS_ALL_ID: RIGHTS.CREATE | RIGHTS.DELETE
	  }
	};
	```

	docs file:
		rest

	docs body:
		brain
	"""

	_rights = Hash({
		'__hash__': {
			'__type__': 'string',
			'__regex__': r'[a-z_]{1,32}'
		},
		'__type__': {
			'__hash__': {
				'__type__': 'string',
				'__regex__': r'^(?:[a-f0-9]{8}[a-f0-9]{4}[a-f0-9]{4}[a-f0-9]{4}[a-f0-9]{12}|\*)$'
			},
			'__type__': 'uint',
			'__minimum__': 1,
			'__maximum__': 15
		}
	})

	def __init__(self, google_flow):
		"""Constructor

		Initialises the instance

		Arguments:
			google_flow (google_auth_oauthlib.flow): The google auth flow

		Returns:
			Brain
		"""

		# Call the parent constructor
		super().__init__()

		# Store the google flow
		self._google_flow = google_flow

	def _create_key(self, user, type_):
		"""Create Key

		Creates a key used for verification of the user

		Arguments:
			user (str): The ID of the user
			type_ (str): The type of key to make

		Returns:
			str
		"""

		# Create an instance
		oKey = Key({
			'_id': random(32, ['0x']),
			'user': user,
			'type': type_
		})

		# Loop until we resolve the issue
		while True:
			try:

				# Create the key record
				oKey.create()

				# Return the key
				return oKey['_id']

			# If we got a duplicate key error
			except DuplicateException as e:

				# If the primary key is the duplicate
				if 'PRIMARY' in e.args[1]:

					# Generate a new key and try again
					oKey['_id'] = random(32, ['0x'])
					continue

				# Else, the type has already been used for the user
				else:

					# Find and return the existing key
					return Key.filter({
						'user': user,
						'type': type_
					}, raw = [ '_id' ], limit = 1)['_id']

	@classmethod
	def _internal_or_verify(cls,
		req: jobject,
		permission: dict | List[dict]
	) -> Literal[0] | Literal[1]:
		"""Internal or Verify

		Does the same thing as the access method of the same name, but without \
		the round trip of talking to ourself

		Arguments:
			request (request): The bottle request for the headers
			session (memory._Memory): The session object to check
			permission (dict | dict[]): A dict with 'name', 'right' and \
				optional 'id', or a list of those dicts

		Raises:
			body.ResponseException

		Returns:
			access.INTERNAL | access.VERIFY
		"""

		# If we have an internal key
		if 'meta' in req and 'Authorize-Internal' in req.meta:

			# Run the internal check
			access.internal(req)

			# Return the system user ID
			return access.SYSTEM_USER_ID

		# Else
		else:

			# Make sure the user has the proper permission to do this
			cls._verify(
				(req.session.user._id, req.session.portal),
				permission
			)

			# Return the session user ID
			return req.session.user._id

	def _recaptcha_v2(self, response: str, ip: str) -> dict:
		"""ReCaptcha V2

		Verifies a google recaptcha v2 response

		Arguments:
			response (str): The response delivered by the UI
			ip (str): The IP of the client that generated the response

		Returns:
			dict
		"""

		# If the secret is missing
		if 'secret' not in self._conf['recaptcha']:
			raise ResponseException(error = (
				errors.BAD_CONFIG, [ 'recaptcha.secret', 'missing ']
			))

		# Generate the URL
		sURL = 'https://www.google.com/recaptcha/api/siteverify' \
				'?secret=%s' \
				'&response=%s' \
				'&remoteip=%s' % (
			self._conf['recaptcha']['secret'],
			response,
			ip
		)

		# Run the request
		oResponse = requests.get(sURL)

		# Return the result
		return oResponse.json()

	def _recaptcha_v3(self, token: str, action: str) -> dict:
		"""ReCaptcha Assessment

		ReCaptcha V3, create an assessment to analyze the risk of a UI action

		Arguments:
			token: The generated token obtained from the client
			action: Action name corresponding to the token

		Returns:
			dict
		"""

		# Check the minimum config
		try:
			evaluate(
				self._conf['recaptcha'],
				[ 'api_key', 'key', 'project' ]
			)
		except ValueError as e:
			return ResponseException(error = (
				errors.BAD_CONFIG,
				[ [ 'recaptcha.%s' % f, 'missing' ] for f in e.args ]
			))

		# Generate the URL and JSON body
		sURL = 'https://recaptchaenterprise.googleapis.com' \
				'/v1/projects/%s/assessments?key=%s' % (
			self._conf['recaptcha']['project'],
			self._conf['recaptcha']['api_key']
		)

		# Run the request using the API
		oResponse = requests.post(sURL, json = {
			'event': {
				'token': token,
				'expectedAction': action,
				'siteKey': self._conf['recaptcha']['key']
			}
		})

		# Pull out the data
		dData = oResponse.json()

		# If there's an error
		if 'error' in dData:
			return {
				'result': False,
				'reason': f"({dData['error']['code']}) {dData['error']['message']}"
			}

		# If the token is not valid
		if not dData['tokenProperties']['valid']:
			return {
				'result': False,
				'reason': dData['tokenProperties']['invalidReason']
			}

		# Check if the expected action was executed.
		if dData['tokenProperties']['action'] != action:
			return {
				'result': False,
				'reason': 'invalid action'
			}

		# If the score is below 0.2, deny it
		elif dData['riskAnalysis']['score'] < 0.2:
			return {
				'result': False,
				'reason': [ 'high risk user', dData['riskAnalysis']['reasons'] ]
			}

		# Else, return ok
		return { 'result': True }

	@classmethod
	def _verify(cls,
		_id: tuple,
		permission: dict | List[dict]
	) -> bool:
		"""Verify

		Checks the user currently in the session has access to the requested \
		permission. If multiple permissions are sent, it is assumed the user \
		only has to match one of them to return success.

		Arguments:
			_id (tuple): The user ID and portal of the permissions
			permission (dict | dict[]): A dict with 'name', 'right' and \
				optional 'id', or a list of those dicts

		Returns:
			bool
		"""

		# Find the permissions
		dPerms = Permission.portal_tree(_id)

		# If there's no such permissions
		if not dPerms:
			raise ResponseException(
				error = (errors.BAD_PORTAL, _id[1])
			)

		# If we only have one permission
		if isinstance(permission, dict):
			permission = [ permission ]

		# Step through each permission
		for i, d in enumerate(permission):

			# If it doesn't exist
			if _VERBOSE: print('checking %s is in perms' % d['name'])
			if d['name'] not in dPerms:
				if _VERBOSE: print('it is not')
				continue

			# If no ID was passed, use the ALL one
			if 'id' not in d:
				d['id'] = [ access.RIGHTS_ALL_ID ]

			# If it's a string, turn it into a list with ALL added
			elif isinstance(d['id'], str):
				d['id'] = [ d['id'], access.RIGHTS_ALL_ID ]

			# Else, we have a list, add the ALL to it
			else:
				d['id'].append(access.RIGHTS_ALL_ID)

			# Step through each ID
			for sID in d['id']:

				# If it exists in the name
				if _VERBOSE: print('checking %s is in perms[%s]' % (sID, d['name']))
				if sID in dPerms[d['name']]:
					if _VERBOSE: print('it is')

					# If one right was requested
					if isinstance(d['right'], int):

						# If the permission contains the requested right
						if _VERBOSE: print('checking %i is in perms[%s][%s]' % (d['right'], d['name'], sID))
						if dPerms[d['name']][sID] & d['right']:

							# The user has the necessary permissions
							if _VERBOSE: print('success: verified!')
							return True

					# Else, if it's a list of rights
					elif isinstance(d['right'], list):

						# Go through each one
						for i in d['right']:

							# If it passes
							if _VERBOSE: print('checking %i is in perms[%s][%s]' % (i, d['name'], sID))
							if dPerms[d['name']][sID] & i:

								# The user has the necessary permissions
								if _VERBOSE: print('success: verified!')
								return True

					# Else, invalid right data
					else:
						raise ResponseException(error=(
							errors.DATA_FIELDS,
							[ [ 'right', 'invalid, must be int or int[]' ] ]
					))

		# Never found a valid permission
		if _VERBOSE: print('error: unverified!')
		return False

	def google_auth_create(self, req: jobject) -> Response:
		"""Google Auth create

		Handles converting the response from Google into an email and then
		either creating the account for the user or signing them in.

		In order to use Google Auth create, the google flow instance must be
		created, which requires 2 items and an optional 3rd in the
		`config.brain` section.

		```json
		{
		  "brain": {
		    "google": {
		      "client_secret": "../client_secret.json",
		      "redirect": "https://mydomain.com/google/auth",
		      "locales": { "en": "en-CA", "fr": "fr-CA" }
		    }
		  }
		}
		```

		The first required item is `client_secret` which should point to a file
		with the client_secret.json file Google provided for you.

		The second required item is `redirect` which has to match the redirect
		given to Google for after the user grants us permission.

		The third optional item is `locales`, an object to match google's
		[a-z]{2} format to our [a-z]{2}-[A-Z]{2} format when creating a new
		users. If no locales section is found, it defaults to
		`config.brain.user_default_locale`.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			POST google/auth

		Data:
			redirect, str, no, The redirect url after authenticating
			url, str, no, The url to send the user by email to finish setup

		Response:
			session, string, The key to access the session created
			user, object, The user data currently in the session
			portal, string, The portal the user is signed into

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1102, DB_CREATE_FAILED, Failed to create the user record
			1202, BAD_PORTAL, OAuth worked, but the portal is invalid
			1204, BAD_OAUTH, Google OAuth failed
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'redirect', 'url' ])

		# Make sure the URL is valid
		if not _URL.match(req.data.url):
			return Error(
				errors.DATA_FIELDS,
				[ [ 'url', 'invalid url or missing "{key}"' ] ]
			)

		# If the portal was not passed
		if 'portal' not in req.data:
			req.data.portal = ''

		# Pass the requested URL to the flow so google can confirm
		try:
			self._google_flow.fetch_token(
				authorization_response = req.data.redirect
			)
		except InvalidGrantError as e:
			return Error(errors.BAD_OAUTH, e.args)

		# Use the credentials to fetch the user's info
		UserInfoService = gapi_build(
			'oauth2',
			'v2',
			credentials = self._google_flow.credentials
		)
		dInfo = UserInfoService.userinfo().get().execute()

		# Look for the user
		oUser = User.filter({
			'email': dInfo['email']
		}, limit = 1)

		# If the user exists
		if oUser:

			# Check if the user has permissions in the given portal
			dPerms = Permission.portal_tree(
				( oUser['_id'], req.data.portal )
			)

			# If we don't have permissions for the given portal
			if not dPerms:
				return Error(errors.BAD_PORTAL, req.data.portal)

			# Set user ID
			sID = oUser['_id']

		# Else, no such user
		else:

			# Do we have a locale convert table, and is the locale in it?
			if 'locales' in self._conf['google'] and \
				dInfo['locale'] in self._conf['google']['locales']:

				# Use the table to get an acceptable locale
				sLocale = self._conf['google']['locales'][dInfo['locale']]
			else:

				# Just use the default locale
				sLocale = self._conf['user_default_locale']

			# Validate by creating a Record instance
			try:
				oUser = User({
					'email': dInfo['email'],
					'passwd': users.EMPTY_PASS,
					'locale': sLocale,
					'first_name': dInfo['given_name'],
					'last_name': dInfo['family_name'],
					'verified': dInfo['verified_email']
				})
			except ValueError as e:
				return Error(errors.DATA_FIELDS, e.args[0])

			# Create the record
			sID = oUser.create(changes = { 'user': users.SYSTEM_USER_ID })
			if not sID:
				return Error(errors.DB_CREATE_FAILED, 'user')

			# Notify if enabled
			self._conf['notify'] and self._notify('signup', sID, {
				'portal': req.data.portal,
				'user': without(oUser.record(), 'passwd')
			})

			# If the email is verified
			if oUser['verified']:

				# Notify if enabled
				self._conf['notify'] and self._notify('setup', sID, {
					'portal': req.data.portal,
					'user': without(oUser.record())
				})

			# Else, if it's not verified
			else:

				# Create key for setup validation
				sSetupKey = self._create_key(sID, 'setup')

				# Email the user the setup link
				oResponse = create(
					'mouth',
					'email',
					access.generate_key({ 'data': {
						'template': {
							'name': 'setup_user',
							'locale': sLocale,
							'variables': {
								'key': sSetupKey,
								'url': req.data.url.replace(
									'{key}',
									sSetupKey
								)
							},
						},
						'to': req.data.email
					}})
				)
				if oResponse.error:
					Key.delete_get(sSetupKey)
					return oResponse

		# Create a new session
		oSesh = memory.create(self._conf['portals'][req.data.portal]['ttl'])

		# Store the user ID and portal in th session
		oSesh['user'] = { '_id': sID }
		oSesh['portal'] = req.data.portal

		# Save the session
		oSesh.save()

		# Notify if enabled
		self._conf['notify'] and self._notify('signin', sID, {
			'portal': req.data.portal,
			'user': without(oUser.record(), 'passwd')
		})

		# Return the session ID, primary user data, and portal name
		return Response({
			'session': oSesh.key(),
			'user': oSesh['user'],
			'portal': oSesh['portal']
		})

	def passwd_verify_create(self, req: jobject) -> Response:
		"""Password Verify create

		Takes a password and verifies if it matches the currently signed in
		user's password.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			POST passwd/verify

		Data:
			passwd, string, no, The password to verify against the currently signed in user

		Data Example:
			{ "passwd": "somepasswordstring" }

		Response:
			Returns `true` on success, else an error code

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1100, DB_NO_RECORD, Couldn't find the signed in user
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'passwd' ])

		# Get the user associated with the session
		oUser = User.get(req.session.user._id)
		if not oUser:
			return Error(
				errors.DB_NO_RECORD,
				[ req.session.user._id, 'user' ]
			)

		# Check the password and return the result
		return Response(
			oUser.password_validate(req.data.passwd)
		)

	def permissions_add_create(self, req: jobject) -> Response:
		"""Permissions Add create

		Addes a specific permission type to existing permissions. When
		generating permission names, be careful not to exceed 32 characters.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			POST permissions/add

		Data:
			user, string, no, The ID of the user
			rights, object, no, An object representing rights, the keys of which represent the names of rights
			rights[key], object, no, The rights per ID under each name, { [string]: number }
			portal, string, yes, Optional, defaults to an empty string

		Data Example:
		{
		  "user": "18f85e33036d11f08878ea3e7aa7d94a",
		  "portal": "my_app",
		  "rights": {
		    "my_service_permission": {
		      "012345679abc4defa0123456789abcde": 15
		    },
		    "my_other_service_permission": {
		      "012345679abc4defa0123456789abcde": 2
		    }
		  }
		}

		Response:
			Returns `true` on success, else an error code

		Error:
			1000, RIGHTS, User doesn't have the rights to make the request
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1100, DB_NO_RECORD, Failed to find the user
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'user', 'rights' ])

		# If the portal wasn't passed
		if 'portal' not in req.data:
			req.data.portal = ''

		# Check internal or verify
		self._internal_or_verify(
			req, { 'name': 'brain_permission', 'right': access.UPDATE }
		)

		# If the user doesn't exist
		if not User.exists(req.data.user):
			return Error(
				errors.DB_NO_RECORD, [ req.data.user, 'user' ]
			)

		# Init the list of new permissions
		lPermissions = []

		# Step through the names of the rights
		for sName, dUUIDs in req.data.rights.items():

			# Step through the IDs and rights
			for sID, iRights in dUUIDs.items():

				# Add the permission
				try:
					lPermissions.append(
						Permission({
							'_user': req.data.user,
							'_portal': req.data.portal,
							'name': sName,
							'id': sID,
							'rights': iRights
						})
					)
				except ValueError as e:
					return Error(errors.DATA_FIELDS, e.args[0])

		# If we have any records, create them
		if lPermissions:
			Permission.create_many(lPermissions)

		# Return OK
		return Response(True)

	def permissions_by_id_delete(self, req: jobject) -> Response:
		""" Permissions By Id delete

		Deletes all permissions associated with a specific ID in a portal,
		useful when a record gets deleted / archived and all permissions
		associated should be removed. Clears the permission cache of all
		associated users.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Raises:
			ResponseException

		Returns:
			Response

		Noun:
			DELETE permissions/by/id

		Data:
			id, string | string[], no, The ID(s) of the permissions to delete
			portal, string, yes, The optional portal to filter by

		Data Example:
		{
		  "id": [ "acf629ea038b11f08878ea3e7aa7d94a",
		    "b2df3ae2038b11f08878ea3e7aa7d94a" ],
		  "portal": "my_app"
		}

		Response:
			Returns `true` on success, else an error code

		Error:
			1000, RIGHTS, User has no rights to delete the avatar
			1001, DATA_FIELDS, See [DATA_FIELD errors](../README.md#data_field-1001-errors)
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'id' ])

		# Check internal or verify
		self._internal_or_verify(
			req, { 'name': 'brain_permission', 'right': access.UPDATE }
		)

		# If the portal is not set
		if 'portal' not in req.data:
			req.data.portal = ''

		# First, fetch the list of users associated with those IDs
		lUserIDs = Permission.filter({
			'id': req.data.id,
			'_portal': req.data.portal
		}, raw = '_user', distinct = True)

		# If we got nothing, do nothing
		if not lUserIDs:
			return Response(True)

		# Delete the associated permissions
		Permission.delete_get(filter = {
			'_portal': req.data.portal,
			'id': req.data.id
		})

		# Clear the permission cache for all associated users
		Permission.portal_tree_clear([
			( s, req.data.portal ) for s in lUserIDs
		])

		# Return OK
		return Response(True)

	def permissions_by_name_delete(self, req: jobject) -> Response:
		""" Permissions By Name delete

		Deletes all permissions associated with a specific name in a portal.
		Clears the permission cache of all associated users.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Raises:
			ResponseException

		Returns:
			Response

		Noun:
			DELETE permissions/by/name

		Data:
			name, string | string[], no, The name(s) of the permissions to delete
			portal, string, yes, Optional, defaults to an empty string

		Data Example:
		{
		  "name": "my_service_permission",
		  "portal": "my_app"
		}

		Response:
			Returns `true` on success, else an error code

		Error:
			1000, RIGHTS, User has no rights to delete the avatar
			1001, DATA_FIELDS, See [DATA_FIELD errors](../README.md#data_field-1001-errors)
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'id' ])

		# Check internal or verify
		self._internal_or_verify(
			req, { 'name': 'brain_permission', 'right': access.UPDATE }
		)

		# Init the filter with the name
		dFilter = { 'name': req.data.name }

		# If the portal is set
		if 'portal' in req.data:
			dFilter['_portal'] = req.data.portal

		# First, fetch the list of users associated with those IDs
		lUserIDs = Permission.filter(dFilter, raw = '_user', distinct = True)

		# If we got nothing, do nothing
		if not lUserIDs:
			return Response(True)

		# Delete the associated permissions
		Permission.delete_get(filter = {
			'_portal': req.data.portal,
			'name': req.data.name
		})

		# Clear the permission cache for all associated users
		Permission.portal_tree_clear([
			(s, req.data.portal) for s in lUserIDs
		])

		# Return OK
		return Response(True)

	def permissions_read(self, req: jobject) -> Response:
		"""Permissions read

		Returns all permissions associated with a user, or with a single portal
		associated with a user.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			GET permissions

		Data:
			user, string, no, The ID of the user
			portal, string, yes, The specific portal to return if set

		Data Example:
		{
		  "user": "18f85e33036d11f08878ea3e7aa7d94a",
		  "portal": "my_app"
		}

		Response:
			Returns a single tree if portal is set, else a list of trees

		Error:
			1000, RIGHTS, User doesn't have the rights to make the request
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'user' ])

		# Check internal or verify
		self._internal_or_verify(
			req, { 'name': 'brain_permission', 'right': access.READ }
		)

		# If we have a portal
		if 'portal' in req.data:

			# Fetch it from the cache and return it
			return Response(
				Permission.portal_tree((req.data.user, req.data.portal))
			)

		# Else, get the list of portals from the config and use that to fetch
		#	the data from the cache
		lPermissions = Permission.portal_tree([
			(req.data.user, s) for s in self._conf['portals'].keys()
		])

		# Store the trees by portal name and return them
		return Response({
			sKey: lPermissions[i] \
			for i, sKey in enumerate(self._conf['portals'].keys()) \
			if lPermissions[i]
		})

	def permissions_update(self, req: jobject) -> Response:
		"""Permissions update

		Updates the permissions for a single user and portal. For the global
		ID '012345679abc4defa0123456789abcde', you can use
		[RIGHTS_ALL_ID](#rights_all_id). And use the constants to calculate
		[rights](#rights). When generating permission names, be careful not to
		exceed 32 characters.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			PUT permissions

		Data:
			user, string, no, The ID of the user
			rights, object, no, An object representing rights, the keys of which represent the names of rights
			rights[name], object, no, The rights per ID under each name, { [string]: number }
			portal, string, yes, Optional, defaults to an empty string

		Data Example:
		{
		  "user": "18f85e33036d11f08878ea3e7aa7d94a",
		  "portal": "my_app",
		  "rights": {
		    "my_service_permission": {
		      "012345679abc4defa0123456789abcde": 15
		    },
		    "my_other_service_permission": {
		      "012345679abc4defa0123456789abcde": 2
		    },
		    "blahblah": {
		      "012345679abc4defa0123456789abcde":
		    }
		  }
		}

		Response:
			Returns `true` on success, else an error code

		Error:
			1000, RIGHTS, User doesn't have the rights to make the request
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1100, DB_NO_RECORD, Failed to find the user

		Example:
			```javascript
			import brain, { RIGHTS_ALL_ID, RIGHTS } from '@ouroboros/brain';

			brain.update(
			  'permissions', {
			    user: '18f85e33036d11f08878ea3e7aa7d94a',
			    portal: 'my_app',
			    rights: {
			      my_service_permission: { RIGHTS_ALL_ID: RIGHTS.ALL },
			      my_other_service_permission: { RIGHTS_ALL_ID: RIGHTS.READ }
			      blahblah: { RIGHTS_ALL_ID: RIGHTS.CREATE | RIGHTS.DELETE }
			    }
			  }
			).then(data => {}, error => {});
			```
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'user', 'rights' ])

		# If the portal wasn't passed
		if 'portal' not in req.data:
			req.data.portal = ''

		# Check internal or verify
		self._internal_or_verify(
			req, { 'name': 'brain_permission', 'right': access.UPDATE }
		)

		# If the user doesn't exist
		if not User.exists(req.data.user):
			return Error(
				errors.DB_NO_RECORD, [ req.data.user, 'user' ]
			)

		# Find the permissions
		dPerms = Permission.portal_tree(
			(req.data.user, req.data.portal)
		)

		# If they exist
		if dPerms:

			# If a merge was requested
			if 'merge' in req.data and req.data.merge:

				# Generate the new merged permissions
				req.data.rights = combine(dPerms, req.data.rights)

			# We need to delete old records
			bDelete = True

		# Else, nothing to delete or combine
		else:
			bDelete = False

		# Init the list of new permission records
		lPermissions = []

		# Step through each of the rights
		for sName, dUUIDs in req.data.rights.items():

			# If it's empty
			if not dUUIDs:
				continue

			# Step through each of the IDs
			for sID, iRights in dUUIDs.items():

				# If there's no rights
				if not iRights:
					continue

				# Add the permission
				try:
					lPermissions.append(
						Permission({
							'_user': req.data.user,
							'_portal': req.data.portal,
							'name': sName,
							'id': sID,
							'rights': iRights
						})
					)
				except ValueError as e:
					return Error(errors.DATA_FIELDS, e.args[0])

		# If we need to delete
		if bDelete:
			Permission.delete_get(filter = {
				'_user': req.data.user,
				'_portal': req.data.portal
			})

		# If we have permissions, create them
		if lPermissions:
			Permission.create_many(lPermissions)

		# Clear the cache
		Permission.portal_tree_clear(( req.data.user, req.data.portal ))

		# Return OK
		return Response(True)

	def reset(self):
		"""Reset

		Called to reset the config and connections

		Returns:
			Brain
		"""

		# Get config
		self._conf = config.brain({
			'google': False,
			'internal': {
				'salt': ''
			},
			'notify': False,
			'portals': {
				'': {
					'rights': {},
					'ttl': 86400
				}
			},
			'redis': 'records',
			'recaptcha': {
				'version': 'v3'
			},
			'user_default_locale': 'en-US'
		})

		# If notify is not Falsy and it's not a dict
		if self._conf['notify'] and not isinstance(self._conf['notify'], dict):

			# Raise an error with an explanation
			raise ValueError(
				'brain.notify', 'must be false or an Object'
			)

		# Go through each portal and make sure we have rights and a session TTL
		for p in self._conf['portals']:
			if 'rights' not in self._conf['portals'][p]:
				self._conf['portals'][p]['rights'] = { }
			else:
				if not self._rights.valid(self._conf['portals'][p]['rights']):
					raise Exception(
						'config.portals.%s.rights' % p,
						self._rights.validation_failures
					)
			if 'ttl' not in self._conf['portals'][p]:
				self._conf['portals'][p]['ttl'] = 0

		# If the salt is set and invalid
		if self._conf['internal']['salt'] and \
			len(self._conf['internal']['salt']) % 16 != 0:

			# Raise an error with an explanation
			raise ValueError(
				'brain.internal.salt',
				'must be a string with a length that is multiples of 16 ' \
					'characters'
			)

		# Create a connection to Redis for the records
		records.redis = nr(self._conf['redis'])

		# Return self for chaining
		return self

	def search_read(self, req: jobject) -> Response:
		"""Search

		Looks up users by search / query

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			GET search

		Data:
			filter, object, no, The filter to apply on the search, see Record_MySQL.Record.search()
			fields, string[], yes, The list of fields to return for each record found

		Data Example:
		{
		  "filter": {
		    "first_name": { "type": "asterisk", "value": "Chri*" },
		    "last_name": { "type": "end", "value": "Nasr" }
		  },
		  "fields": [ "_id", "email", "first_name", "last_name" ]
		}

		Response:
			Returns the list of user records found

		Error:
			1000, RIGHTS, User doesn't have the rights to make the request
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
		"""

		# Check permissions
		self._verify(
			(req.session.user._id, req.session['portal']),
			{ 'name': 'brain_user', 'right': access.READ }
		)

		# Check minimum fields
		self.check_data(req.data, [ 'filter' ])

		# If the filter isn't a dict
		if not isinstance(req.data.filter, dict):
			return Error(
				errors.DATA_FIELDS, [ [ 'filter', 'must be an object' ] ]
			)

		# If fields is passed, and is not a list
		if 'fields' in req.data and \
			not isinstance(req.data.fields, list):

			# Return an error
			return Error(
				errors.DATA_FIELDS, [ [ 'fields', 'must be a list' ] ]
			)

		# Search based on the req.data passed
		lRecords = [
			d['_id'] \
			for d in User.search(req.data.filter, raw = [ '_id' ])
		]

		# If we got something, fetch the records from the cache
		if lRecords:
			lRecords = User.cache(
				lRecords,
				raw = ('fields' in req.data and req.data.fields or True)
			)

		# Remove the passwd
		for d in lRecords:
			del d['passwd']

		# Return the results
		return Response(lRecords)

	def session_read(self, req: jobject) -> Response:
		"""Session

		Returns the ID of the user, and the portal current signed in

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			GET session

		Response:
			user._id, string, The user's ID
			portal, string, The portal the user is signed into

		Response Example:
			{
			  "user": { "_id": "18f85e33036d11f08878ea3e7aa7d94a" },
			  "portal": "my_app"
			}
		"""
		return Response({
			'user' : {
				'_id': req.session.user._id
			},
			'portal': req.session.portal
		})

	def signin_create(self, req: jobject) -> Response:
		"""Signin

		Signs a user into the system

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Result

		Noun:
			POST signin

		Data:
			email, string, no, The e-mail address of the user
			passwd, string, no, The password of the user

		Data Example:
			{
			  "email": "me@mydomain.com",
			  "passwd": "********"
			}

		Response:
			session, string, The key of the signed in session
			user, object, The user data stored in the session
			portal, string, The portal the user signed into

		Response Example:
			{
			  "session": "sesh:1daf1317c424409893927640aafac2f5",
			  "user": { "_id": "18f85e33036d11f08878ea3e7aa7d94a" },
			  "portal": "my_app"
			}

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1200, SIGNIN_FAILED, E-mail address OR password is invalid
			1202, BAD_PORTAL, User has no access to the given portal
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'email', 'passwd' ])

		# Look for the user by email
		oUser = User.filter({ 'email': req.data.email }, limit = 1)
		if not oUser:
			return Error(errors.SIGNIN_FAILED)

		# If it's the system user, reject it
		if oUser['_id'] == users.SYSTEM_USER_ID:
			return Error(errors.SIGNIN_FAILED)

		# Validate the password
		if not oUser.password_validate(req.data.passwd):
			return Error(errors.SIGNIN_FAILED)

		# Check if the user has permissions in the given portal
		sPortal = 'portal' in req.data and \
					req.data.portal or \
					''
		dPerms = Permission.portal_tree((oUser['_id'], sPortal))

		# If we don't have permissions for the given portal
		if dPerms is None:
			return Error(errors.BAD_PORTAL, sPortal)

		# Create a new session
		oSesh = memory.create(self._conf['portals'][sPortal]['ttl'])

		# Store the user ID and portal in the session
		oSesh['user'] = { '_id': oUser['_id'] }
		oSesh['portal'] = sPortal

		# Save the session
		oSesh.save()

		# Notify if enabled
		self._conf['notify'] and self._notify('signin', oUser['_id'], {
			'portal': sPortal
		})

		# Return the session ID, primary user data, and portal name
		return Response({
			'session': oSesh.key(),
			'user': oSesh['user'],
			'portal': oSesh['portal']
		})

	def signin_internal_create(self, req: jobject) -> Response:
		"""Signin Internal create

		Signs in a user by email or ID, not callable from the outside world, can
		only be called with an internal key. Useful for services that need to
		sign a user in based on some 3rd party identification but who don't want
		to bypass or recreate the entire signin process.

		Arguments:
			req (jobject): The request details, which can include 'data', \
				'environment', and 'session'

		Raises:
			ResponseException

		Returns:
			Response

		Noun:
			POST signin/internal

		Data:
			_id, string, yes, The ID of the user to sign in, must be set if `email` not set
			email, string, yes, The e-mail address of the user, must be set if `_id` not set
			portal, string, yes, The portal to sign in to, defaults to an empty string

		Data Example:
			{
			  "email": "me@mydomain.com"
			}

		Response:
			session, string, The key of the signed in session
			user, object, The user data stored in the session
			portal, string, The portal the user signed into

		Response Example:
			{
			  "session": "sesh:1daf1317c424409893927640aafac2f5",
			  "user": { "_id": "18f85e33036d11f08878ea3e7aa7d94a" },
			  "portal": "my_app"
			}

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1200, SIGNIN_FAILED, E-mail address OR password is invalid
			1202, BAD_PORTAL, User has no access to the given portal
		"""

		# Verify this is an internal call
		access.internal(req)

		# If we have an ID
		if '_id' in req.data:

			# Look for the user by ID
			oUser = User.get(req.data._id)

		# Else, if we have an email
		elif 'email' in req.data:

			# Look for the user by email
			oUser = User.filter({ 'email': req.data.email }, limit = 1)

		# Else, invalid
		else:
			return Error(errors.DATA_FIELDS, [ [ '_id', 'missing' ] ])

		# If no user was found, or it's the system user
		if not oUser or oUser['_id'] == users.SYSTEM_USER_ID:
			return Error(errors.SIGNIN_FAILED)

		# Check if the user has permissions in the given portal
		sPortal = 'portal' in req.data and \
					req.data.portal or \
					''
		dPerms = Permission.portal_tree((oUser['_id'], sPortal))

		# If we don't have permissions for the given portal
		if dPerms is None:
			return Error(errors.BAD_PORTAL, sPortal)

		# Create a new session
		oSesh = memory.create(self._conf['portals'][sPortal]['ttl'])

		# Store the user ID and portal in the session
		oSesh['user'] = { '_id': oUser['_id'] }
		oSesh['portal'] = sPortal

		# Save the session
		oSesh.save()

		# Notify if enabled
		self._conf['notify'] and self._notify('signin', oUser['_id'], {
			'portal': sPortal
		})

		# Return the session ID, primary user data, and portal name
		return Response({
			'session': oSesh.key(),
			'user': oSesh['user'],
			'portal': oSesh['portal']
		})

	def signin_to_create(self, req: jobject) -> Response:
		"""Signin To

		Gets a new session for a different portal using the credentials of
		the user already signed in

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			POST signin/to

		Data:
			email, string, no, The e-mail address of the user
			passwd, string, no, The password of the user
			portal, string, yes, Optional, defaults to an empty string

		Data Example:
			{ "portal": "my_other_app" }

		Response:
			session, string, The key of the signed in session
			portal, string, The portal the user signed into

		Response Example:
			{
			  "session": "sesh:8baf1317c424409893927640aafac2f5",
			  "portal": "my_other_app"
			}

		Error:
			1202, BAD_PORTAL, User has no access to the given portal
		"""

		# Store the user ID (and immediately validate we have a session)
		sUserID = req.session.user._id

		# Check if the user has permissions in the given portal
		sPortal = 'portal' in req.data and \
					req.data.portal or \
					''
		dPerms = Permission.portal_tree((sUserID, sPortal))

		# If we don't have permissions for the given portal
		if dPerms is None:
			return Error(errors.BAD_PORTAL, sPortal)

		# Create a new session
		oSesh = memory.create(self._conf['portals'][sPortal]['ttl'])

		# Store the user ID and portal in th session
		oSesh['user'] = { '_id': sUserID }
		oSesh['portal'] = sPortal

		# Save the session
		oSesh.save()

		# Check if signin is specifically enabled
		self._conf['notify'] and self._notify('signin', sUserID, {
			'portal': sPortal
		})

		# Return the session ID and portal name
		return Response({
			'session': oSesh.key(),
			'portal': oSesh['portal']
		})

	def signout_create(self, req: jobject) -> Response:
		"""Signout create

		Called to sign out a user and destroy their session

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			POST signout

		Response:
			Returns `true`
		"""

		# Close the session so it can no longer be found/used
		if 'session' in req and req.session:
			req.session.close()

		# Return OK
		return Response(True)

	def signup_create(self, req: jobject) -> Response:
		"""Signup create

		Creates a new account for the email given. Uses the default
		permissions based on the
		-[portal](https://github.com/ouroboroscoding/brain2/blob/main/README.md#brainportals)-
		passed.

		Requires a `passwd` passed if it turns out the e-mail provided is
		already signed up with another portal.

		Absolutely requires g-recaptcha-response, which itself requires
		`config.brain.recaptcha` to be setup.

		ReCaptcha version 3
		```json
		  "brain": {
		    "recaptcha": {
		      "version": "v3",
		      "api_key": "yourgoogleapikey",
		      "key": "yourgooglekey",
		      "project": "mydomain-1234567890123"
		    }
		  }
		```

		ReCaptcha version 2
		```json
		  "brain": {
		    "recaptcha": {
		      "version": "v2",
		      "secret": "secretkey_fromgoogle"
		    }
		  }
		```

		If you need to create a user without captcha see [User create](#user-create).

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			POST signup

		Data:
			email, string, no, The e-mail address for the new user
			locale, string, yes, The locale of the user, en-US, en-CA, fr-CA, etc. Defaults to config.brain.user_default_locale
			g-recaptcha-response, mixed, no, The google recaptcha data from the client side, depedant on the recaptcha version
			url, string, no, The URL to email the user to finish setup. Requires the string "{key}" inside as a placeholder for the actual setup key
			passwd, string, yes, A password is necessary if the user already has an account, but not to the specific portal being requested
			portal, string, yes, The portal to sign up for, defaults to an empty string

		Response:
			Returns the ID if a new user is created, else `true` for new portal

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1101, DB_DUPLICATE, User already has access to the portal
			1205, BAD_CONFIG, Portal doesn't exist in config
		"""

		# Get the passed portal or use the default empty string
		sPortal = 'portal' in req.data and \
					req.data.pop('portal') or \
					''

		# If there's no section in the config
		if sPortal not in self._conf['portals']:
			return Error(errors.BAD_CONFIG, 'portals.%s' % sPortal)

		# Check minimum fields
		self.check_data(req.data, [ 'email', 'g-recaptcha-response', 'url' ])

		# If we're doing v3
		if self._conf['recaptcha']['version'] == 'v3':

			# Run the assessment
			dRes = self._recaptcha_v3(
				req.data.pop('g-recaptcha-response'),
				'signup'
			)

			# If the assessment failed
			if not dRes['result']:
				return Error(
					errors.DATA_FIELDS,
					[ [ 'record.g-recaptcha-response', dRes['reason'] ] ]
				)

		# Else, if we're doing v2
		elif self._conf['recaptcha']['version'] == 'v2':

			# Check the captcha (pop off the field from req.data)
			dRes = self._recaptcha_v2(
				req.data.pop('g-recaptcha-response'),
				get_client_ip(req.environment)
			)

			# If the captcha failed, return the errors
			if not dRes['success']:
				return Error(
					errors.DATA_FIELDS,
					[ [ 'g-recaptcha-response', dRes['error-codes'] ] ]
				)

		# Else
		else:
			return Error(
				errors.BAD_CONFIG, [ 'recaptcha.version', 'must be v2 or v3' ]
			)

		# Make sure the URL is valid
		if not _URL.match(req.data.url):
			return Error(
				errors.DATA_FIELDS,
				[ [ 'url', 'invalid url or missing "{key}"' ] ]
			)

		# Pop off the URL
		sURL = req.data.pop('url')

		# Strip leading and trailing spaces on the email
		req.data.email = req.data.email.strip()

		# Make sure the email is valid structurally
		if not EMAIL_ADDRESS.match(req.data.email):
			return Error(
				errors.DATA_FIELDS, [ [ 'email', 'invalid' ] ]
			)

		# Check if a user with that email already exists
		dUser = User.filter({
			'email': req.data.email
		}, raw = [ '_id', 'passwd' ], limit = 1)

		# Flag to send setup email
		bSetup = False

		# If the user already exists
		if dUser:

			# Check for existing permissions on that given portal
			dPerms = Permission.portal_tree(( dUser['_id'], sPortal ))

			# If the user already has an account with the portal
			if dPerms:
				return Error(
					errors.DB_DUPLICATE, [ req.data.email , 'user' ]
				)

			# If we need a password
			if 'passwd' not in req.data:
				return Error(errors.DATA_FIELDS, [ [ 'passwd', 'missing' ] ])

			# If it's invalid
			if not password_validate(dUser['passwd'], req.data.passwd):
				return Error(errors.SIGNIN_FAILED)

			# Set the user ID
			sUserID = dUser['_id']

		# Else, this is a new user
		else:

			# Add the blank password
			req.data.passwd = users.EMPTY_PASS

			# Add defaults
			if 'locale' not in req.data:
				req.data.locale = self._conf['user_default_locale']

			# Validate by creating a Record instance
			try:
				oUser = User(req.data)
			except ValueError as e:
				return Error(errors.DATA_FIELDS, e.args[0])

			# Create the record
			sUserID = oUser.create(changes = { 'user': users.SYSTEM_USER_ID })

			# Notify if enabled
			self._conf['notify'] and self._notify('signup', sUserID, {
				'portal': sPortal,
				'user': without(oUser.record(), 'passwd')
			})

			# Send the setup email
			bSetup = True

		# If the record was created (or already existed)
		if sUserID:

			# If we have any rights for the portal
			if self._conf['portals'][sPortal]['rights']:
				dRights = self._conf['portals'][sPortal]['rights']

				# Init the list of permissions
				lPermissions = []

				# Step through the names
				for sName, dUUIDs in dRights.items():

					# Step through the IDs and rights
					for sIdent, iRights in dUUIDs.items():

						# Add the permission
						try:
							lPermissions.append(
								Permission({
									'_user': sUserID,
									'_portal': sPortal,
									'name': sName,
									'id': sIdent,
									'rights': iRights
								})
							)
						except ValueError as e:
							oUser.delete(changes = {
								'user': users.SYSTEM_USER_ID
							})
							return Error(
								errors.BAD_CONFIG,
								[ 'portals.%s.rights' % sPortal, e.args[0] ]
							)

				# Create the permissions if we have any
				if lPermissions:
					Permission.create_many(lPermissions)

		# If we need to send the setup email for a new user
		if bSetup:

			# Create key for setup validation
			sSetupKey = self._create_key(sUserID, 'setup')

			# Email the user the setup link
			oResponse = create(
				'mouth',
				'email',
				access.generate_key({ 'data': {
					'template': {
						'name': 'setup_user',
						'locale': oUser['locale'],
						'portal': sPortal,
						'variables': {
							'key': sSetupKey,
							'url': sURL.replace('{key}', sSetupKey)
						},
					},
					'to': req.data.email
				}})
			)
			if oResponse.error:
				Key.delete_get(sSetupKey)
				return oResponse

			# Return the user ID
			return Response(sUserID)

		# Else, just send True
		else:
			return Response(True)

	def user_create(self, req: jobject) -> Response:
		"""User create

		Creates a new user. The `url` is required, and must explicitly be set
		to `false` to not have an email go to the user. If an e-mail is not
		sent, it is up to you to notify the user somehow of their account and
		have them finish the setup process.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			POST user

		Data:
			email, string, no, The email of the user to create
			url, string | false, no, The URL to email to the user to finish setup, if `false`, no e-mail is sent, if a string "{key}" is required as a placeholder for the actual setup key
			locale, string, yes, The locale of the user, en-US, en-CA, fr-CA, etc. Defaults to config.brain.user_default_locale
			first_name, string, yes, The name of the user
			last_name, string, yes, The surname of the user
			title, string, yes, The title of the user, Mr, Mrs, Dr, etc
			suffix, string, yes, The suffix of the user, PhD, RN, Esquire, etc
			phone_number, string, yes, The phone number of the user
			phone_ext, string, yes, The phone number extension
			verified, bool, yes, Is the user already verified?

		Data Example:
			{
			  "email": "me@mydomain.com",
			  "locale": "en-US",
			  "first_name": "Bob",
			  "last_name": "Smith",
			  "title": "Mr.",
			  "portal": "my_app"
			  "url": "https://mydomain.com/setup/{key}"
			}

		Response:
			The ID of the new user

		Error:
			1000, RIGHTS, User doesn't have the rights to make the request
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1101, DB_DUPLICATE, A user with the given email address already exists
		"""

		# Check internal or verify
		sSessionUser = self._internal_or_verify(
			req, { 'name': 'brain_user', 'right': access.CREATE }
		)

		# Check minimum fields
		self.check_data(req.data, [ 'email', 'url' ])

		# Pop off the URL
		sURL = req.data.pop('url')

		# If we have a url
		if sURL:

			# Make sure the URL is valid
			if not _URL.match(sURL):
				return Error(
					errors.DATA_FIELDS,
					[ [ 'url', 'invalid url or missing "{key}"' ] ]
				)

		# If the verified flag is not set
		if 'verified' not in req.data:
			req.data.verified = False

		# Get the passed portal or use the default empty string
		sPortal = 'portal' in req.data and \
					req.data.pop('portal') or \
					''

		# Strip leading and trailing spaces on the email
		req.data.email = req.data.email.strip()

		# Make sure the email is valid structurally
		if not EMAIL_ADDRESS.match(req.data.email):
			return Error(
				errors.DATA_FIELDS, [ [ 'email', 'invalid' ] ]
			)

		# Check if a user with that email already exists
		sExistingUserID = User.filter({
			'email': req.data.email
		}, raw = '_id', limit = 1)
		if sExistingUserID:
			return Error(
				errors.DB_DUPLICATE, [ req.data.email, 'user', sExistingUserID ]
			)

		# Add the blank password
		req.data.passwd = users.EMPTY_PASS

		# Add defaults
		if 'locale' not in req.data:
			req.data.locale = self._conf['user_default_locale']

		# Validate by creating a Record instance
		try:
			oUser = User(req.data)
		except ValueError as e:
			return Error(errors.DATA_FIELDS, e.args[0])

		# Create the record
		sID = oUser.create(changes = { 'user': sSessionUser })

		# If the record was created and we have a URL
		if sID and sURL:

			# Create key for setup validation
			sSetupKey = self._create_key(oUser['_id'], 'setup')

			# Email the user the setup link
			oResponse = create(
				'mouth',
				'email',
				access.generate_key({ 'data': {
					'template': {
						'name': 'setup_user',
						'locale': oUser['locale'],
						'variables': {
							'key': sSetupKey,
							'url': sURL.replace('{key}', sSetupKey)
						}
					},
					'to': req.data.email
				}})
			)
			if oResponse.error:
				Key.delete_get(sSetupKey)
				return oResponse

		# Return the result
		return Response(sID)

	def user_exists_read(self, req: jobject) -> Response:
		"""User Exists read

		Requires one of `_id` or `email` in order to look up if the user exists.

		Arguments:
			req (jobject): The request details, which can include 'data', \
				'environment', and 'session'

		Raises:
			ResponseException

		Returns:
			Response

		Noun:
			GET user/exists

		Data:
			_id, string, yes, The possible ID of the user to verify
			email, string, yes, The possible email address of a user to verify

		Response:
			Returns the `_id` of the record if found, else `False`.

		Error:
			1000, RIGHTS, User doesn't have the rights to make the request
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
		"""

		# If an ID was passed
		if '_id' in req.data:

			# Does the user exist?
			return Response(
				User.exists(req.data._id)
			)

		# If the email was passed
		elif 'email' in req.data:

			# Does the user exist
			return Response(
				User.filter(
					{ 'email': req.data.email },
					raw = '_id',
					limit = 1
				) or False
			)

		# Missing data
		else:
			return Error(errors.DATA_FIELDS, [ [ 'email', 'missing' ] ])

	def user_read(self, req: jobject) -> Response:
		"""User Read

		Fetches an existing user and returns their data.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			GET user

		Data:
			_id, string, yes, The ID of the user to get, else use the signed in user
			portal, string, yes, Used to get the permissions associated to the user that will be returned

		Data Example:
			{ "_id": "18f85e33036d11f08878ea3e7aa7d94a" }

		Response:
			Returns an object with the user details and permissions

		Error:
			1000, RIGHTS, User doesn't have the rights to make the request
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1100, DB_NO_RECORD, User is not found by ID
		"""

		# If there's an ID, check permissions
		if 'data' in req and '_id' in req.data:
			self._verify(
				(req.session.user._id, req.session['portal']),
				{ 'name': 'brain_user', 'right': access.READ }
			)

			# If no portal was passed
			if 'portal' not in req.data:
				req.data.portal = ''

		# Else, assume the signed in user's Record
		else:
			req.data = {
				'_id': req.session.user._id,
				'portal': req.session['portal']
			}

		# Fetch it from the cache
		dUser = User.cache(req.data._id, raw = True)

		# If it doesn't exist
		if not dUser:
			return Error(
				errors.DB_NO_RECORD, [ req.data._id, 'user' ]
			)

		# Remove the passwd
		del dUser['passwd']

		# Fetch the permissions and add them to the user
		dUser['permissions'] = Permission.portal_tree(
			(req.data._id, req.data.portal)
		)

		# Return the user data
		return Response(dUser)

	def user_update(self, req: jobject) -> Response:
		"""User Update

		Updates an existing user. Only requires sending of data that is
		changing.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			PUT user

		Data:
			_id, string, yes, The ID of the user to update, else we use the signed in user
			locale, string, yes, The locale of the user, en-US, en-CA, fr-CA, etc
			first_name, string, yes, The name of the user
			last_name, string, yes, The surname of the user
			title, string, yes, The title of the user, Mr, Mrs, Dr, etc
			suffix, string, yes, The suffix of the user, PhD, RN, Esquire, etc
			phone_number, string, yes, The phone number of the user
			phone_ext, string, yes, The phone number extension

		Data Example:
			{
			  "_id": "18f85e33036d11f08878ea3e7aa7d94a",
			  "suffix": "Esq."
			}

		Response:
			Returns `true` on success, else an error code

		Error:
			1000, RIGHTS, User doesn't have the rights to make the request
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1100, DB_NO_RECORD, User not found
			1104, DB_UPDATE_FAILED, Email hasn't changed, or the DB failed somehow
		"""

		# If there's an ID, check permissions
		if '_id' in req.data and \
			req.data._id != req.session.user._id:

			# If the ID isn't set
			if not req.data._id:
				return Error(
					errors.DATA_FIELDS, [ [ '_id', 'missing' ] ]
				)

			# Make sure the user has the proper permission to do this
			self._verify(
				(req.session.user._id, req.session['portal']),
				{ 'name': 'brain_user', 'right': access.UPDATE }
			)

		# Else, assume the signed in user's Record
		else:
			req.data._id = req.session.user._id

			# If there's an email, strip it out
			if 'email' in req.data:
				del req.data.email

		# Fetch it from the cache
		oUser = User.cache(req.data._id)

		# If the user isn't found
		if not oUser:
			return Error(
				errors.DB_NO_RECORD, [ req.data._id, 'user' ]
			)

		# Remove fields that can't be changed
		for k in [ '_id', '_created', '_updated', 'email', 'passwd' ]:
			try: del req.data[k]
			except KeyError: pass

		# Step through each field passed and update/validate it
		lErrors = []
		for f in req.data:
			try: oUser[f] = req.data[f]
			except ValueError as e: lErrors.extend(e.args[0])

		# If there was any errors
		if lErrors:
			return Error(errors.DATA_FIELDS, lErrors)

		# Update the record
		if not oUser.save(changes = { 'user': req.session.user._id }):
			return Error(errors.DB_UPDATE_FAILED, [ oUser['_id'], 'user' ])

		# If it was updated, clear the cache
		User.clear(oUser['_id'])

		# Return OK
		return Response(True)

	def user_email_update(self, req: jobject) -> Response:
		"""User Email update

		Changes the email for the current signed in user. A user changing their
		email triggers a re-verification process by sending them an email. This
		Requires sending the `url` param with a "{key}" string inside it

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			PUT user/email

		Data:
			email, string, no, The new email to set for the user
			email_passwd, string, no, The current password of the user to verify they are who they say they are
			url, string, no, The URL to send to the user by email to verify the change

		Data Example:
			{
			  "email": "me@mydomain.com",
			  "email_passwd": "********",
			  "url": "https://mydomain.com/verify/{key}"
			}

		Response:
			Returns `true` on success, else an error code

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1100, DB_NO_RECORD, User not found
			1101, DB_DUPLICATE, A user with the given email address already exists
			1104, DB_UPDATE_FAILED, Email hasn't changed, or the DB failed somehow
			1200, SIGNIN_FAILED, `email_passwd` is invalid for the user
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'email', 'email_passwd', 'url' ])

		# Make sure the URL is valid
		if not _URL.match(req.data.url):
			return Error(
				errors.DATA_FIELDS,
				[ [ 'url', 'invalid url or missing "{key}"' ] ]
			)

		# Find the user
		oUser = User.get(req.session.user._id)
		if not oUser:
			return Error(
				errors.DB_NO_RECORD,
				[ req.session.user._id, 'user' ]
			)

		# Validate the password
		if not oUser.password_validate(req.data.email_passwd):
			return Error(errors.SIGNIN_FAILED)

		# Strip leading and trailing spaces on email
		req.data.email = req.data.email.strip()

		# If the email hasn't changed
		if oUser['email'] == req.data.email:
			return Error(
				errors.DB_UPDATE_FAILED, [ req.session.user._id, 'user' ]
			)

		# Make sure the email is valid structurally
		if not EMAIL_ADDRESS.match(req.data.email):
			return Error(
				errors.DATA_FIELDS, [ [ 'email', 'invalid' ] ]
			)

		# Look for someone else with that email
		dUser = User.filter({ 'email': req.data.email }, raw = [ '_id' ])
		if dUser:
			return Error(
				errors.DB_DUPLICATE, [ req.data.email, 'user' ]
			)

		# Update the email and verified fields
		try:
			oUser['email'] = req.data.email
			oUser['verified'] = False
		except ValueError as e:
			return Error(errors.DATA_FIELDS, e.args[0])

		# Generate a new key
		sKey = self._create_key(oUser['_id'], 'verify')

		# Update the user
		if not oUser.save(changes = { 'user': req.session.user._id }):
			return Error(
				errors.DB_UPDATE_FAILED, [ req.session.user._id, 'user' ]
			)

		# Clear the cache
		User.clear(oUser['_id'])

		# Create key
		sKey = self._create_key(oUser['_id'], 'verify')

		# Verification template variables
		dTpl = {
			'key': sKey,
			'url': req.data.url.replace('{key}', sKey)
		}

		# Email the user the key
		oResponse = create(
			'mouth',
			'email',
			access.generate_key({ 'data': {
				'template': {
					'name': 'verify_email',
					'locale': oUser['locale'],
					'variables': dTpl
				},
				'to': req.data.email,
			}})
		)
		if oResponse.error:
			Key.delete_get(sKey)
			return oResponse

		# Return OK
		return Response(True)

	def user_email_verify_update(self, req: jobject) -> Response:
		"""User Email Verify update

		Marks the user/email as verified.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			PUT user/email/verify

		Data:
			key, string, no, The key used to identify the user

		Data Example:
			{ "key": "randomstringkeypassedbyurl" }

		Response:
			Returns `true` on success, else an error code

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1100, DB_NO_RECORD, User not found
			1104, DB_UPDATE_FAILED, Email hasn't changed, or the DB failed somehow
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'key' ])

		# Look for the key
		oKey = Key.get(req.data.key)
		if not oKey:
			return Error(
				errors.DB_NO_RECORD, [ req.data.key, 'key' ]
			)

		# Find the user associated with they key
		oUser = User.get(oKey['user'])
		if not oUser:
			return Error(
				errors.DB_NO_RECORD, [ oKey['user'], 'user' ]
			)

		# Mark the user as verified and save
		oUser['verified'] = True
		if not oUser.save(changes = { 'user': oKey['user'] }):
			return Error(errors.DB_UPDATE_FAILED, [ oUser['_id'], 'user' ])

		# Clear the cache
		User.clear(oKey['user'])

		# Delete the key
		oKey.delete()

		# Return OK
		return Response(True)

	def user_names_read(self, req: jobject) -> Response:
		"""User Names read

		Returns a list or dict of IDs to names of users.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			GET user/names

		Data:
			_id, string | string[], no, The ID(s) of the user(s)
			type, 'object' | 'array', yes, The format to return, defaults to 'object'

		Response:
			Returns an object with the key being the ID and the value being
			another object of first_name and last_name. or an array of objects
			with keys _id first_name last_name.

		Response Example:
			{
			  "18f85e33036d11f08878ea3e7aa7d94a": {
			    "first_name": "Bob", "last_name": "Smith"
			  },
			  "0905dba5042e11f0b65524a3c6f47776": {
			    "first_name": "John", "last_name": "Baker"
			  },
			  "0c9096eb042e11f0b65524a3c6f47776": {
			    "first_name": "Frank", "last_name": "Candlestickmaker"
			  }
			}

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
		"""

		# Check minimum fields
		self.check_data(req.data, [ '_id' ])

		# If the type is missing
		if 'type' not in req.data or not req.data.type:
			req.data.type = 'object'

		# Else, if the type is invalid
		elif req.data.type not in [ 'array', 'object' ]:
			return Error(
				errors.DATA_FIELDS, [ [ 'type', 'invalid' ] ]
			)

		# If we only got one ID
		if isinstance(req.data._id, str):
			req.data._id = [ req.data._id ]

		# If the list is empty
		if not req.data._id:
			return Error(
				errors.DATA_FIELDS, [ [ '_id', 'empty' ] ]
			)

		# If the client requested an array, return a list
		if req.data.type == 'array':
			return Response(
				User.get(
					req.data._id,
					raw = [ '_id', 'first_name', 'last_name' ],
					orderby = [ 'first_name', 'last_name' ]
				)
			)

		# Else, they requested an object, so return a dict
		else:
			return Response({
				d['_id']: {
					'first_name': d['first_name'],
					'last_name': d['last_name']
				} \
				for d in User.get(
					req.data._id,
					raw = [ '_id', 'first_name', 'last_name' ]
				)
			})

	def _notify(self,
		_type: Literal[ 'setup', 'signin', 'signup' ],
		_id: dict,
		additional: dict = {}
	):
		"""Notify

		Handles sending out requests if anyone is subscribed to specific notify
		types. Make sure to check self._conf['notify'] is not Falsy before calling
		this method, as it assumes it is a dict.

		Arguments:
			_type ('setup' | 'signin' | 'signup'): The type of notify call
			_id (str): The ID of the user associated with the notify call
			additional (dict): Additional, optional, information to send with
				the notify call
		"""

		# Wrap the whole thing in a try / except block so that bad config
		#	data doesn't crash the service
		try:

			# If we don't have the section, return
			if _type not in self._conf['notify']:
				return

			# Step through the list
			for d in self._conf['notify'][_type]:

				# Call the request based on the data
				body_request(
					d['service'],
					d['action'],
					d['path'],
					access.generate_key({ 'data': {
						'user_id': _id,
						'additional': additional
					} })
				)

		# Except all exceptions, print, and do nothing
		except Exception as e:
			print(e, file = stderr)
			print(e.args, file = stderr)
			return

	def user_passwd_update(self, req: jobject) -> Response:
		"""User Password update

		Changes the password for the current signed in user.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			PUT user/passwd

		Data:
			new_passwd, string, no, The new password to set
			_id, string, yes, The ID of the user, else the signed in user
			passwd, string, yes, The user of the password to verify themselves, optional only if `_id` is passed

		Data Example:
			{
			  "new_passwd": "**********",
			  "passwd": "********"
			}

		Response:
			Returns `true` on success, else an error code

		Error:
			1000, RIGHTS, User doesn't have the rights to make the request
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1104, DB_UPDATE_FAILED, Email hasn't changed, or the DB failed somehow
			1201, PASSWORD_STRENGTH, The password isn't strong enough
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'new_passwd' ])

		# If the id is passed
		if '_id' in req.data and req.data._id is not None:

			# If it doesn't match the logged in user, check permissions
			if req.data._id != req.session.user._id:
				self._verify(
					(req.session.user._id, req.session['portal']),
					{ 'name': 'brain_user', 'right': access.UPDATE }
				)

		# Else, use the user from the session
		else:

			# If the old password is missing
			if 'passwd' not in req.data:
				return Error(
					errors.DATA_FIELDS, [ [ 'passwd', 'missing' ] ]
				)

			# Store the session as the user ID
			req.data._id = req.session.user._id

		# Find the user
		oUser = User.get(req.data._id)
		if not oUser:
			return Error(
				errors.DB_NO_RECORD, [ req.data._id, 'user' ]
			)

		# If we have an old password
		if 'passwd' in req.data:

			# Validate it
			if not oUser.password_validate(req.data.passwd):
				return Error(
					errors.DATA_FIELDS, [ [ 'passwd', 'invalid' ] ]
				)

		# Make sure the new password is strong enough
		if not User.password_strength(req.data.new_passwd):
			return Error(errors.PASSWORD_STRENGTH)

		# Set the new password and save
		oUser['passwd'] = User.password_hash(req.data.new_passwd)
		if not oUser.save(changes = { 'user': req.session.user._id }):
			return Error(errors.DB_UPDATE_FAILED, [ req.data._id, 'user' ])

		# Return OK
		return Response(True)

	def user_passwd_forgot_create(self, req: jobject) -> Response:
		"""User Password Forgot create

		Creates the key that will be used to allow a user to change their
		password if they forgot it. Requires `url` contain the "{key}" string
		as a plaeholder for the actual forgot password key.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			POST user/passwd/forgot

		Data:
			email, string, no, The email of the user to find
			url, string, no, The URL to email the user to change their password

		Data Example:
			{
			  "email": "me@mydomain.com",
			  "url": "https://mydomain.com/forgot/{key}"
			}

		Response:
			Returns a bool

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'email', 'url' ])

		# Make sure the URL is valid
		if not _URL.match(req.data.url):
			return Error(
				errors.DATA_FIELDS,
				[ [ 'url', 'invalid url or missing "{key}"' ] ]
			)

		# Look for the user by email
		dUser = User.filter(
			{'email': req.data.email},
			raw = ['_id', 'locale'],
			limit = 1
		)
		if not dUser:
			return Response(False)

		# Generate a key
		sKey = self._create_key(dUser['_id'], 'forgot')

		# Forgot email template variables
		dTpl = {
			'key': sKey,
			'url': req.data.url.replace('{key}', sKey)
		}

		# Email the user the key
		oResponse = create(
			'mouth',
			'email',
			access.generate_key({ 'data': {
				'template': {
					'name': 'forgot_password',
					'locale': dUser['locale'],
					'variables': dTpl
				},
				'to': req.data.email,
			}})
		)
		if oResponse.error:
			Key.delete_get(sKey)
			return oResponse

		# Return OK
		return Response(True)

	def user_passwd_forgot_update(self, req: jobject) -> Response:
		"""User Password Forgot update

		Validates the key and changes the password to the given value.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			PUT user/passwd/forgot

		Data:
			passwd, string, no, The new password to set for the user
			key, string, no, The key used to verify the user

		Data Example:
			{
			  "passwd": "**********",
			  "key": "randomstringkeypassedbyurl"
			}

		Response:
			Returns `true` on success, else an error code

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1100, DB_NO_RECORD, User not found
			1104, DB_UPDATE_FAILED, Email hasn't changed, or the DB failed somehow
			1201, PASSWORD_STRENGTH, The password isn't strong enough
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'passwd', 'key' ])

		# Look up the key
		oKey = Key.get(req.data.key)
		if not oKey:
			return Error(
				errors.DB_NO_RECORD, [ req.data.key, 'key' ]
			)

		# Make sure the new password is strong enough
		if not User.password_strength(req.data.passwd):
			return Error(errors.PASSWORD_STRENGTH)

		# Find the User
		oUser = User.get(oKey['user'])
		if not oUser:
			return Error(
				errors.DB_NO_RECORD, [ oKey['user'], 'user' ]
			)

		# Store the new password, mark verified, and update
		oUser['passwd'] = User.password_hash(req.data.passwd)
		oUser['verified'] = True
		if not oUser.save(changes=False):
			return Error(errors.DB_UPDATE_FAILED, [ oKey['user'], 'user' ])

		# Delete the key
		oKey.delete()

		# Return OK
		return Response(True)

	def user_portal_create(self, req: jobject) -> Response:
		"""User Portal create

		Adds the portal's base permissions to the given user's account. Can also
		pass `rights` for additional rights to merged onto the base rights and
		added to the user.

		Arguments:
			req (jobject): The request details, which can include 'data', \
				'environment', and 'session'

		Raises:
			ResponseException

		Returns:
			Response

		Noun:
			POST user/portal

		Data:
			_id, string, no, The ID of the user
			portal, string, no, The name of the portal to add,
			rights, object, yes, Additional rights to add to the portal permissions

		Data Example:
			{
			  "_id": "",
			  "portal": "my_app",
			  "rights": {
			    "my_service_permission": {
			      "*": 15
				}
			  }
			}

		Response:
			Returns `True` on success, else an error code

		Error:
			1000, RIGHTS, User has no rights to make the request
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1102, DB_CREATE_FAILED, Failed to create the user record
		"""

		# Check minimum fields
		self.check_data(req.data, [ '_id', 'portal' ])

		# Check internal or verify
		self._internal_or_verify(
			req, { 'name': 'brain_permission', 'right': access.UPDATE }
		)

		# If there's no such portal
		if req.data.portal not in self._conf['portals']:
			return Error(errors.DATA_FIELDS, [ [ 'portal', 'invalid' ] ])

		# Check for existing permissions on that given portal
		dPerms = Permission.portal_tree(( req.data._id, req.data.portal ))

		# If the user already has an account with the portal
		if dPerms:
			return Error(
				errors.DB_DUPLICATE,
				[ (req.data._id, req.data.portal ), 'permission' ]
			)

		# Start with the rights from the config
		dRights = clone(self._conf['portals'][req.data.portal]['rights'])

		# If we have additional
		if 'rights' in req.data:

			# If they're not valid
			if not self._rights.valid(req.data.rights):
				return Error(
					errors.DATA_FIELDS,
					[ [ 'rights.%s' % l[0], l[1] ] \
						for l in self._rights.validation_failures ]
				)

			# Else merge them onto the base
			merge(dRights, req.data.rights)

		# If we have any rights for the portal
		if dRights:

			# Init the list of permissions
			lPermissions = []

			# Step through the names
			for sName, dUUIDs in dRights.items():

				# Step through the IDs and rights
				for sIdent, iRights in dUUIDs.items():

					# If the ident is "*", replace it
					if sIdent == '*':
						sIdent = access.RIGHTS_ALL_ID

					# Add the permission
					try:
						lPermissions.append(
							Permission({
								'_user': req.data._id,
								'_portal': req.data.portal,
								'name': sName,
								'id': sIdent,
								'rights': iRights
							})
						)
					except ValueError as e:
						return Error(
							errors.BAD_CONFIG,
							[ 'portals.%s.rights' % req.data.portal, e.args[0] ]
						)

			# Create the permissions if we have any
			if lPermissions:
				if Permission.create_many(lPermissions) != len(lPermissions):
					return Error(errors.DB_CREATE_FAILED, 'permission')

			# Clear the cache
			Permission.portal_tree_clear(( req.data._id, req.data.portal ))

		# Return OK
		return Response(True)

	def user_setup_key_read(self, req: jobject) -> Response:
		"""User Setup Key read

		Generates a usable setup key for a user. Only accessible internally.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			GET user/setup/key

		Data:
			_id, string, no, The ID of the user to generate a key for

		Response:
			Returns the new key (string), or an error code

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1203, INTERNAL_KEY, Failed verification
		"""

		# Verify the internal key
		access.internal(req)

		# Check minimum fields
		self.check_data(req.data, [ '_id' ])

		# Create key for setup validation and return it
		return Response(
			self._create_key(req.data._id, 'setup')
		)

	def user_setup_read(self, req: jobject) -> Response:
		"""User Setup read

		Validates the key exists and returns the user's info.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			GET user/setup

		Data:
			key, string, no, The setup key used to identify the user

		Response:
			Returns an object with the user details, else an error code

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1100, DB_NO_RECORD, Key or user not found
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'key' ])

		# Look up the key
		dKey = Key.get(req.data.key, raw=True)
		if not dKey:
			return Error(
				errors.DB_NO_RECORD, [ req.data.key, 'key' ]
			)

		# Get the user
		dUser = User.get(dKey['user'], raw=True)
		if not dUser:
			return Error(
				errors.DB_NO_RECORD, [ dKey['user'], 'user' ]
			)

		# Delete unnecessary fields
		for k in [ '_id', '_created', '_updated', 'passwd', 'verified' ]:
			del dUser[k]

		# Return the user
		return Response(dUser)

	def user_setup_send_create(self, req: jobject) -> Response:
		"""User Setup Send create

		Used to re-send the setup email message to a user in case they never
		got it. Requires `url` contain the "{key}" string as a placeholder for
		the actualy setup key.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			POST user/setup/send

		Data:
			_id, string, no, The ID of the user
			url, string, no, The URL to email the user to complete the setup

		Response:
			Returns `true` on success, else an error code

		Error:
			1000, RIGHTS, User doesn't have the rights to make the request
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1002, body.ALREADY_DONE, User is already setup
			1100, DB_NO_RECORD, User is not found by ID
		"""

		# Check internal or verify
		self._internal_or_verify(req,
			{ 'name': 'brain_user', 'right': [ access.CREATE, access.UPDATE ] }
		)

		# Check minimum fields
		self.check_data(req.data, [ '_id', 'url' ])

		# Make sure the URL is valid
		if not _URL.match(req.data.url):
			return Error(
				errors.DATA_FIELDS,
				[ [ 'url', 'invalid url or missing "{key}"' ] ]
			)

		# Pop off the URL
		sURL = req.data.pop('url')

		# Find the user
		dUser = User.get(req.data._id, raw = True)
		if not dUser:
			return Error(
				errors.DB_NO_RECORD, [ req.data._id, 'user' ]
			)

		# If the user is already setup
		if dUser['passwd'] != users.EMPTY_PASS:
			return Error(errors.ALREADY_DONE)

		# Create key for setup validation
		sSetupKey = self._create_key(dUser['_id'], 'setup')

		# Email the user the setup link
		oResponse = create(
			'mouth',
			'email',
			access.generate_key({ 'data': {
				'template': {
					'name': 'setup_user',
					'locale': dUser['locale'],
					'variables': {
						'key': sSetupKey,
						'url': sURL.replace('{key}', sSetupKey)
					},
				},
				'to': dUser['email']
			}})
		)
		if oResponse.error:
			Key.delete_get(sSetupKey)
			return oResponse

		# Return OK
		return Response(True)

	def user_setup_update(self, req: jobject) -> Response:
		"""User Setup update

		Finishes setting up the account for the user by setting their password
		and verified fields.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			PUT user/setup

		Data:
			key, string, no, The setup key used to identify the user
			passwd, string, no, The password to set for the user
			portal, string, yes, The portal the user will be signed into after setup
			locale, string, yes, The locale of the user, en-US, en-CA, fr-CA, etc
			first_name, string, yes, The name of the user
			last_name, string, yes, The surname of the user
			title, string, yes, The title of the user, Mr, Mrs, Dr, etc
			suffix, string, yes, The suffix of the user, PhD, RN, Esquire, etc
			phone_number, string, yes, The phone number of the user
			phone_ext, string, yes, The phone number extension

		Data Example:
			{
			  "key": "randomstringkeypassedbyurl",
			  "passwd": "********",
			  "portal": "my_app",
			  "locale": "en-CA",
			  "first_name": "Bob",
			  "last_name": "Smith"
			}

		Response:
			Returns the new session key (string) on success, else an error code

		Response Example:
			"sesh:6aaf1417c424409893927640aafac2f5"

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1100, DB_NO_RECORD, User not found
			1104, DB_UPDATE_FAILED, Email hasn't changed, or the DB failed somehow
			1201, PASSWORD_STRENGTH, The password is not strong enough
		"""

		# Check minimum fields
		self.check_data(req.data, [ 'passwd', 'key' ])

		# Look up the key
		oKey = Key.get(req.data.key)
		if not oKey:
			return Error(
				errors.DB_NO_RECORD, (req.data.key, 'key')
			)
		req.data.pop('key')

		# If there's a portal
		sPortal = 'portal' in req.data and req.data.pop('portal') or ''

		# Find the user
		oUser = User.get(oKey['user'])
		if not oUser:
			return Error(
				errors.DB_NO_RECORD, [ oKey['user'], 'user' ]
			)

		# Make sure the new password is strong enough
		if not User.password_strength(req.data.passwd):
			return Error(errors.PASSWORD_STRENGTH)

		# Pop off the password
		sPassword = req.data.pop('passwd')

		# Go through the remaining fields and attempt to update
		lErrors = []
		for k in req.data:
			try: oUser[k] = req.data[k]
			except ValueError as e: lErrors.extend(e.args[0])
		if lErrors:
			return Error(errors.DATA_FIELDS, lErrors)

		# Set the new password, mark as verified, and save
		oUser['passwd'] = User.password_hash(sPassword)
		oUser['verified'] = True
		if not oUser.save(changes = { 'user': oKey['user'] }):
			return Error(errors.DB_UPDATE_FAILED, [ oKey['user'], 'user' ])

		# Delete the key
		oKey.delete()

		# Notify if enabled
		self._conf['notify'] and self._notify('setup', oUser['_id'], {
			'portal': sPortal,
			'user': without(oUser.record(), 'passwd')
		})

		# Create a new session
		oSesh = memory.create(self._conf['portals'][sPortal]['ttl'])

		# Store the user ID and portal in the session
		oSesh['user'] = {'_id': oUser['_id']}
		oSesh['portal'] = sPortal

		# Save the session
		oSesh.save()

		# Notify if enabled
		self._conf['notify'] and self._notify('signin', oUser['_id'], {
			'portal': sPortal
		})

		# Return the session ID
		return Response(oSesh.key())

	def users_by_email_read(self, req: jobject) -> Response:
		"""Users By E-Mail read

		Finds a user given their unique email address

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			GET users/by/email

		Data:
			email, string | string[], no, The email(s) to look up
			fields, array, yes, The list of user fields to return, defaults to [ '_id', 'email', 'first_name', 'last_name' ]
			order, string[], yes, The order to return the users in, defaults to [ 'first_name', 'last_name' ]

		Data Example:
			{
			  "email": [ "me@mydomain.com", "johnnieb@gmail.com" ],
			  "fields": [ "first_name", "last_name" ],
			  "order": [ "last_name", "first_name" ]
			}

		Response Example:
			[
			  { "first_name": "John", "last_name": "Baker" },
			  { "first_name": "Bob", "last_name": "Smith" }
			]

		Error:
			1000, RIGHTS, User doesn't have the rights to make the request
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
		"""

		# Check internal or verify
		self._internal_or_verify(
			req, { 'name': 'brain_user', 'right': access.READ }
		)

		# Check minimum fields
		self.check_data(req.data, [ 'email' ])

		# If the fields are passed
		if 'fields' in req.data:

			# If it's not a list
			if not isinstance(req.data.fields, list):
				return Error(
					errors.DATA_FIELDS,
					[ [ 'fields', 'must be an array' ] ]
				)

		# Else, set default fields
		else:
			req.data.fields = [ '_id', 'email', 'first_name', 'last_name' ]

		# If the order is passed
		if 'order' in req.data:

			# If it's not a list
			if not isinstance(req.data.order, list):
				return Error(
					errors.DATA_FIELDS, [ [ 'order', 'must be an array' ] ]
				)

		# Else, set default fields
		else:
			req.data.order = [ 'first_name', 'last_name' ]

		# If we only got one email
		mLimit = isinstance(req.data.email, str) and 1 or None

		# Get the user IDs of the sent emails
		lUserIDs = User.filter(
			{ 'email': req.data.email },
			raw = '_id',
			orderby = req.data.order,
			limit = mLimit
		)

		# Find and return the user(s) from the cache
		return Response(
			User.cache(lUserIDs, raw = req.data.fields)
		)

	def users_by_permission_id_read(self, req: jobject) -> Response:
		""" Users By Permission ID read

		Given a specific permission ID, return the IDs of all users who have
		that permission ID set. Optionally a name can be sent to narrow down
		the search if an ID is used across multiple names.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Raises:
			ResponseException

		Returns:
			Response

		Noun:
			GET users/by/permission/id

		Data:
			id, string, no, The ID of the permission to get
			name, string, yes, The optional name to also match against

		Response:
			Returns an array of unique user IDs

		Error:
			1000, RIGHTS, User has no rights to delete the avatar
			1001, DATA_FIELDS, See [DATA_FIELD errors](../README.md#data_field-1001-errors)

		Example:
			This is a internal key only request, it can not be called from the web
		"""

		# Make sure an internal key was passed
		access.internal(req)

		# Check minimum fields
		self.check_data(req.data, [ 'id' ])

		# Init the filter with the ID
		dFilter = { 'id': req.data.id }

		# If have a name as well
		if 'name' in req.data:
			dFilter['name'] = req.data.name

		# Fetch the unique list of user IDs and return it
		return Response(
			Permission.filter(
				dFilter,
				raw = '_user',
				distinct = True
			)
		)

	def users_by_permission_name_read(self, req: jobject) -> Response:
		""" Users By Permission Name read

		Given a specific permission name, return the IDs of all users who have
		that permission name set

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Raises:
			ResponseException

		Returns:
			Response

		Noun:
			GET users/by/permission/name

		Data:
			name, string, no, The name to match against

		Response:
			Returns an array of unique user IDs

		Error:
			1000, RIGHTS, User has no rights to delete the avatar
			1001, DATA_FIELDS, See [DATA_FIELD errors](../README.md#data_field-1001-errors)

		Example:
			This is a internal key only request, it can not be called from the web
		"""

		# Make sure an internal key was passed
		access.internal(req)

		# Check minimum fields
		self.check_data(req.data, [ 'name' ])

		# Fetch the unique list of user IDs and return it
		return Response(
			Permission.filter(
				{ 'name': req.data.name },
				raw = '_user',
				distinct = True
			)
		)

	def users_by_id_read(self, req: jobject) -> Response:
		"""Users By ID read

		Finds all users with the given ID(s). Returns `null` for invalid IDs.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			GET users/by/id

		Data:
			_id, string | string[], no, The user ID(s) to look up
			fields, array, yes, The list of user fields to return, defaults to [ '_id', 'email', 'first_name', 'last_name' ]

		Data Example:
			{
			  "_id": [
			    "18f85e33036d11f08878ea3e7aa7d94a",
			    "0905dba5042e11f0b65524a3c6f47776"
			  ],
			  "fields": [ "email", "first_name", "last_name" ]
			}

		Response Example:
			[ {
			  "email": "me@mydomain.com",
			  "first_name": "Bob",
			  "last_name": "Smith"
			}, {
			  "email": "johnnieb@gmail.com",
			  "first_name": "John",
			  "last_name": "Baker"
			} ]

		Error:
			1000, RIGHTS, User doesn't have the rights to make the request
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
		"""

		# Check internal or verify
		self._internal_or_verify(
			req, { 'name': 'brain_user', 'right': access.READ }
		)

		# Check minimum fields
		self.check_data(req.data, [ '_id' ])

		# If the fields are passed
		if 'fields' in req.data:

			# If it's not a list
			if not isinstance(req.data.fields, list):
				return Error(
					errors.DATA_FIELDS,
					[ [ 'fields', 'must be an array' ] ]
				)

		# Else, set default fields
		else:
			req.data.fields = [ '_id', 'email', 'first_name', 'last_name' ]

		# Fetch the users from the cache and return
		return Response(
			User.cache(
				req.data._id,
				raw = req.data.fields
			)
		)

	def verify_read(self, req: jobject) -> Response:
		"""Verify read

		Checks the user currently in the session has access to the requested
		permission.

		Arguments:
			req (jobject): The request details, which can include 'data',
				'environment', and 'session'

		Returns:
			Services.Response

		Noun:
			GET verify

		Data Example:
			[{
			  name: 'brain_user',
			  right: 1
			}, {
			  name: 'brain_permission',
			  right: 4
			}]

		Response:
			Returns `true` on verification, else `false`

		Error:
			1001, DATA_FIELDS, Data sent to the request is missing or invalid
			1202, BAD_PORTAL, User has no access to the portal
		"""

		# Init possible errors
		lErrors = []

		# If it's a dict
		if isinstance(req.data, dict):

			# If not valid
			if not records.Verify.valid(req.data):

				# Return the validation errors
				return Error(
					errors.DATA_FIELDS, records.Verify.validation_failures
				)

		# Else, if it's a list
		elif isinstance(req.data, list):

			# Init errors list
			lErrors = []

			# Step through each permission
			for i, d in enumerate(req.data):

				# If not valid
				if not records.Verify.valid(d, level = [ '[%d]' % i ]):

					# Extend the errors with the validation errors
					lErrors.extend(records.Verify.validation_failures)

			# If there's errors, return them
			if lErrors:
				return Error(errors.DATA_FIELDS, lErrors)

		# Verify and return the result
		return Response(
			self._verify(
				(req.session.user._id, req.session.portal),
				req.data
			)
		)