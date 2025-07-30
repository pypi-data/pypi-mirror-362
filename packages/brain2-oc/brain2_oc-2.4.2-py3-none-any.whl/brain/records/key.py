# coding=utf8
""" Brain Key Records

Handles the key table for verification / forgot password / etc unique keys
"""

__author__		= "Chris Nasr"
__version__		= "1.0.0"
__maintainer__	= "Chris Nasr"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2025-03-11"

# Limit exports
__all__ = [ 'Key' ]

# Ouroboros imports
from config import config
from define import Tree
from rest_mysql.Record_MySQL import Record

# Python imports
import pathlib

class Key(Record):
	"""Key

	Represents a key for email verification, forgotten password, etc.

	Extends:
		Record_MySQL.Record
	"""

	_conf = Record.generate_config(
		Tree.from_file('%s/define/key.json' % pathlib.Path(
			__file__
		).parent.parent.resolve(), {
			'__name__': 'record',
			'__sql__': {
				'auto_primary': False,
				'create': [ '_created', '_updated', 'user', 'type' ],
				'db': config.mysql.db('brain'),
				'host': config.brain.mysql('records'),
				'indexes': {
					'ui_user_type': { 'unique': [ 'user', 'type' ] }
				},
				'table': 'brain_key',
				'charset': 'utf8mb4',
				'collate': 'utf8mb4_bin'
			},

			'_id': { '__sql__': { 'type': 'char(32)' } },
			'_created': { '__sql__': {
				'opts': 'default CURRENT_TIMESTAMP'
			} },
			'_updated': { '__sql__': {
				'opts': 'default CURRENT_TIMESTAMP on update CURRENT_TIMESTAMP'
			} },
			'user': { '__sql__': { 'binary': True } }
		})
	)
	"""Configuration"""

	@classmethod
	def config(cls):
		"""Config

		Returns the configuration data associated with the record type

		Returns:
			dict
		"""
		return cls._conf