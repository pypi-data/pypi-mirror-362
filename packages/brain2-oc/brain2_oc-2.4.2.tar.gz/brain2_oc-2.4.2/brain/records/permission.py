# coding=utf8
""" Brain Permission Records

Handles the individual permission records for users
"""

__author__		= "Chris Nasr"
__version__		= "1.0.0"
__maintainer__	= "Chris Nasr"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2025-03-11"

# Limit exports
__all__ = [ 'Permission' ]

# Ouroboros imports
from body.constants import SECONDS_DAY
from config import config
from define import Tree
import jsonb
from rest_mysql.Record_MySQL import Record

# Python imports
import pathlib

# Local imports
from brain import records
from .user import User

class Permission(Record):
	"""Permission

	Represents a set of read, create, updated, delete permissions on an ID and \
	name in a specific portal

	Extends:
		Record_MySQL.Record
	"""

	_conf = Record.generate_config(
		Tree.from_file('%s/define/permission.json' % pathlib.Path(
			__file__
		).parent.parent.resolve(), {
			'__name__': 'record',
			'__sql__': {
				'auto_primary': False,
				'create': [ '_user', '_portal', 'name', 'id', 'rights' ],
				'db': config.mysql.db('brain'),
				'host': config.brain.mysql('records'),
				'indexes': {
					'i_user_portal': [ '_user', '_portal' ]
				},
				'primary': False,
				'table': 'brain_permission',
				'charset': 'utf8mb4',
				'collate': 'utf8mb4_bin'
			},

			'_user': { '__sql__': { 'binary': True } },
			'_portal': { '__sql__': { 'type': 'char(16)' } },
			'name': { '__sql__': { 'type': 'char(32)' } },
			'id': { '__sql__': { 'binary': True } },
			'rights': { '__sql__': { 'type': 'tinyint(2)' } }
		})
	)
	"""Configuration"""

	_tree_key = 'perms:%s%s'
	"""The template used to generate the tree cache keys"""

	@classmethod
	def config(cls):
		"""Config

		Returns the configuration data associated with the record type

		Returns:
			dict
		"""
		return cls._conf

	@classmethod
	def portal_tree(cls, id_portal: tuple) -> dict:
		"""User Tree

		Returns the tree

		Arguments:
			id_portal (tuple): The ID and portal of the permissions

		Returns:
			dict
		"""

		# If we got a single id
		if isinstance(id_portal, tuple):

			# Try to fetch it from the cache
			sPermissions = records.redis.get(cls._tree_key % id_portal)

			# If it's found
			if sPermissions:

				# If it's -1
				if sPermissions in [ b'-1', '-1' ]:
					return None

				# Decode and return the data
				return jsonb.decode(sPermissions)

			# Else, permissions not found in cache, fetch and return them from
			#	the db
			else:
				return cls.portal_tree_reset(id_portal)

		# Else, we got multiple IDs
		else:

			# Fetch multiple keys
			lPermissions = records.redis.mget([
				cls._tree_key % t for t in id_portal
			])

			# Go through each one
			for i, t in enumerate(id_portal):

				# If we have a record
				if lPermissions[i]:

					# If it's -1
					if lPermissions[i] in [ b'-1', '-1' ]:
						lPermissions[i] = None

					# Else, decode it
					else:
						lPermissions[i] = jsonb.decode(lPermissions[i])

				else:

					# Fetch the records from the DB
					lPermissions[i] = cls.portal_tree_reset(t)

					# Store it in the cache
					records.redis.set(
						cls._tree_key % t,
						jsonb.encode(lPermissions[i])
					)

			# Return the permissions
			return lPermissions

	@classmethod
	def portal_tree_clear(cls, id_portal: list | tuple):
		"""Portal Tree Clear

		Removes permissions from the cache by ID

		Arguments:
			id_portal (tuple|tuple[]): One or more tuples with the ID of the \
			user and the portal
		"""

		# If we got one id, delete the one key
		if isinstance(id_portal, tuple):
			records.redis.delete(cls._tree_key % id_portal)

		# Else, delete multiple keys if we didn't just get an empty list
		elif id_portal:
			records.redis.delete(*[ cls._tree_key % t for t in id_portal ])

	@classmethod
	def portal_tree_reset(cls, id_portal: tuple) -> dict:
		"""User Tree Rest

		Resets the user's portal tree in the cache and returns it for anyone \
		who needs it

		Arguments:
			user (tuple): The ID and portal of the permissions

		Returns:
			dict
		"""

		# Fetch the records from the DB
		lPermissions = cls.filter({
			'_user': id_portal[0],
			'_portal': id_portal[1]
		}, raw = [ 'name', 'id', 'rights' ] )

		# If there's none
		if not lPermissions:

			# Check if the user even exists, if not,
			if not User.exists(id_portal[0]):

				# Store it for an hour to avoid bad actors
				records.redis.setex(
					cls._tree_key % id_portal, '-1', SECONDS_DAY
				)

				# Return nothing
				return None

		# Init the tree
		dTree = {}

		# Loop through the records to generate the tree
		for d in lPermissions:

			# If the name exists, add to it
			if d['name'] in dTree:
				dTree[d['name']][d['id']] = d['rights']

			# Else, create a new dict for the name
			else:
				dTree[d['name']] = { d['id']: d['rights'] }

		# Store it in the cache
		records.redis.set(
			cls._tree_key % id_portal,
			jsonb.encode(dTree)
		)

		# Return the tree
		return dTree