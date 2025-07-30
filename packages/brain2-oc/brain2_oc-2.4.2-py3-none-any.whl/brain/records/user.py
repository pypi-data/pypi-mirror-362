# coding=utf8
""" Brain User Records

Handles the user table
"""

__author__		= "Chris Nasr"
__version__		= "1.0.0"
__maintainer__	= "Chris Nasr"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2025-03-11"

# Limit exports
__all__ = [ 'User' ]

# Ouroboros imports
from body.constants import SECONDS_DAY
from config import config
from define import Tree
import jsonb
from rest_mysql.Record_MySQL import Commands, ESelect, Record
from strings import random

# Python imports
from hashlib import sha1
import pathlib
import re

# Local imports
from brain import records

# Constants
SECONDS_30_DAYS = SECONDS_DAY * 30

def password_validate(hash, passwd):
	"""Password Validate

	Validates the given password against the current instance

	Arguments:
		hash (str): The hashed password to compare against
		passwd (str): The password to validate

	Returns:
		bool
	"""

	# Split the password
	sSalt = hash[:20] + hash[60:]
	sHash = hash[20:60]

	# Return OK if the re-hashed password matches
	return sHash == sha1(
		sSalt.encode('utf-8') + passwd.encode('utf-8')
	).hexdigest()

class User(Record):
	"""User

	Represents a single user

	Extends:
		Record_MySQL.Record
	"""

	_conf = Record.generate_config(
		Tree.from_file('%s/define/user.json' % pathlib.Path(
			__file__
		).parent.parent.resolve(), {
			'__name__': 'record',
			'__sql__': {
				'auto_primary': True,
				'changes': [ 'user' ],
				'create': [
					'_created', '_updated', 'email', 'passwd', 'locale',
					'first_name', 'last_name', 'title', 'suffix',
					'phone_number', 'phone_ext', 'verified'
				],
				'db': config.mysql.db('brain'),
				'host': config.brain.mysql('records'),
				'indexes': {
					'ui_email': { 'unique': [ 'email' ] }
				},
				'table': 'brain_user',
				'charset': 'utf8mb4',
				'collate': 'utf8mb4_unicode_ci'
			},

			'_id': { '__sql__': { 'binary': True } },
			'_created': { '__sql__': {
				'opts': 'default CURRENT_TIMESTAMP'
			} },
			'_updated': { '__sql__': {
				'opts': 'default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP'
			} },
			'passwd': { '__sql__': { 'type': 'char(72)' } },
			'locale': { '__sql__': { 'type': 'char(5)' } },
			'phone_number': { '__sql__': { 'type': 'varchar(31)' } },
			'verified': { '__sql__': { 'opts': 'default 0' } }
		})
	)
	"""Configuration"""

	@classmethod
	def cache(cls, _id, raw = False, custom = {}):
		"""Cache

		Fetches the Users from the cache and returns them

		Arguments:
			_id (str|str[]): The ID(s) to fetch
			raw (bool): Return raw records or Users
			custom (dict): Custom Host and DB info
				'host' the name of the host to get/set data on
				'append' optional postfix for dynamic DBs

		Returns:
			User|User[]|dict|dict[]
		"""

		# If we got a single ID
		if isinstance(_id, str):

			# Fetch a single key
			sUser = records.redis.get(_id)

			# If we have a record
			if sUser:

				# If it's there just to avoid DB hits
				if sUser in [b'-1', '-1']:
					return None

				# Decode it
				dUser = jsonb.decode(sUser)

			else:

				# Fetch the record from the DB
				dUser = cls.get(_id, raw = True, custom = custom)

			# If we don't have a record
			if not dUser:

				# Store in the cache temporarily to avoid bad actors and return
				#	null
				records.redis.setex(_id, SECONDS_DAY, '-1')
				return None

			# Store it in the cache for 30 days
			records.redis.setex(_id, SECONDS_30_DAYS, jsonb.encode(dUser))

			# Return the raw data or an instance
			return raw and dUser or cls(dUser)

		# Else, fetch multiple
		else:

			# Fetch multiple keys
			lUsers = records.redis.mget(list(_id))

			# Go through each one
			for i, s in enumerate(_id):

				# If we have a record
				if lUsers[i]:

					# If it's there just to avoid DB hits, mark it as null
					if lUsers[i] in [b'-1', '-1']:
						lUsers[i] = None

					# Else, decode it
					else:
						lUsers[i] = jsonb.decode(lUsers[i])

				# If we don't have a record in the cache
				else:

					# Fetch the record from the DB
					lUsers[i] = cls.get(s, raw = True, custom = custom)

					# If we don't have a record
					if not lUsers[i]:

						# Store in the cache temporarily to avoid bad actors
						records.redis.setex(s, SECONDS_DAY, '-1')

					# Else, store it in the cache for 30 days
					else:
						records.redis.setex(s, SECONDS_30_DAYS, jsonb.encode(lUsers[i]))

			# If we want raw
			if raw:
				return lUsers

			# Return instances
			return [ d and cls(d) or None for d in lUsers ]

	@classmethod
	def clear(cls, _id):
		"""Clear

		Removes a user from the cache

		Arguments:
			_id (str): The ID of the user to remove

		Returns:
			None
		"""

		# Delete the key in Redis
		records.redis.delete(_id)

	@classmethod
	def config(cls):
		"""Config

		Returns the configuration data associated with the record type

		Returns:
			dict
		"""
		return cls._conf

	@staticmethod
	def password_hash(passwd):
		"""Password Hash

		Returns a hashed password with a unique salt

		Arguments:
			passwd (str): The password to hash

		Returns:
			str
		"""

		# Generate the salt
		sSalt = random(32, ['0x'])

		# Generate the hash
		sHash = sha1(sSalt.encode('utf-8') + passwd.encode('utf-8')).hexdigest()

		# Combine the salt and hash and return the new value
		return sSalt[:20] + sHash + sSalt[20:]

	@classmethod
	def password_strength(cls, passwd):
		"""Password Strength

		Returns true if a password is secure enough

		Arguments:
			passwd (str): The password to check

		Returns:
			bool
		"""

		# If we don't have enough or the right chars
		if 8 > len(passwd) or \
			re.search('[A-Z]+', passwd) == None or \
			re.search('[a-z]+', passwd) == None or \
			re.search('[0-9]+', passwd) == None:

			# Invalid password
			return False

		# Return OK
		return True

	def password_validate(self, passwd):
		"""Password Validate

		Validates the given password against the current instance

		Arguments:
			passwd (str): The password to validate

		Returns:
			bool
		"""

		# Call the base method using the records `passwd` field
		return password_validate(
			self.field_get('passwd'),
			passwd
		)

	@classmethod
	def simple_search(cls, query, custom={}):
		"""Simple Search

		Looks for query in multiple fields

		Arguments:
			query (str): The query to search for
			custom (dict): Custom Host and DB info
				'host' the name of the host to get/set data on
				'append' optional postfix for dynamic DBs

		Returns:
			str[]
		"""

		# Get the structure
		dStruct = cls.struct(custom)

		# Generate the SQL
		sSQL = "SELECT HEX(`_id`) as `_id`\n" \
				"FROM `%(db)s`.`%(table)s`\n" \
				"WHERE `first_name` LIKE '%%%(query)s%%'\n" \
				"OR `last_name` LIKE '%%%(query)s%%'\n" \
				"OR CONCAT(`first_name`, ' ', `last_name`) LIKE '%%%(query)s%%'\n" \
				"OR `email` LIKE '%%%(query)s%%'\n" \
				"OR `phone_number` LIKE '%%%(query)s%%'" % {
			'db': dStruct['db'],
			'table': dStruct['table'],
			'query': Commands.escape(dStruct['host'], query)
		}

		# Run the search and return the result
		return Commands.select(
			dStruct['host'],
			sSQL,
			ESelect.COLUMN
		)