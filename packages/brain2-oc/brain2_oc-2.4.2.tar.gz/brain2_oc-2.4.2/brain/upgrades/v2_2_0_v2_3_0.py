# coding=utf8
""" Upgrade 2.2.0 to 2.3.0

Handles taking the existing 2.2.0 data and converting it to a usable format in
2.3.0
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2025-03-11"

# Ouroboros imports
from config import config
import jsonb
from strings import uuid_strip_dashes

# Python imports
from os.path import abspath, expanduser, exists

# Pip imports
from rest_mysql.Record_MySQL import Commands, DuplicateException, ESelect

# Local imports
from brain.records import key, permission, user

def run():
	"""Run

	Main entry into the script, called by the upgrade module

	Returns:
		bool
	"""

	# Get Brain data folder
	sDataPath = config.brain.data('./.brain')
	if '~' in sDataPath:
		sDataPath = expanduser(sDataPath)
	sDataPath = abspath(sDataPath)

	# Generate the name of the keys backup file
	sKeysFile = '%s/brain_v2_2_keys.json' % sDataPath

	# If the backup file already exists
	if exists(sKeysFile):

		# Load it
		lRecords = jsonb.load(sKeysFile)

	# Else, no backup yet
	else:

		# Get the keys struct
		dStruct = key.Key.struct()

		# Pull out all the records from the key table
		lRecords = Commands.select(
			dStruct['host'],
			'SELECT `_id`, ' \
				'UNIX_TIMESTAMP(`_created`) as `_created`, ' \
				'UNIX_TIMESTAMP(`_updated`) as `_updated`, ' \
				'`user`, `type` ' \
			'FROM `%(db)s`.`%(table)s` ORDER BY `_created`' % dStruct,
			ESelect.ALL
		)

		# Store them to a local file
		jsonb.store(lRecords, sKeysFile)

		# Drop the table
		key.Key.table_drop()

		# Recreate the table
		key.Key.table_create()

	# Go through each record, convert the values, and add them
	for d in lRecords:
		try:
			d['_id'] = uuid_strip_dashes(d['_id'])
			d['user'] = uuid_strip_dashes(d['user'])
			key.Key.create_now(d)
		except DuplicateException as e:
			print(e.args)

	# Generate the name of the permissions backup file
	sPermissionsFile = '%s/brain_v2_2_permissions.json' % sDataPath

	# If the backup file already exists
	if exists(sPermissionsFile):

		# Load it
		lRecords = jsonb.load(sPermissionsFile)

	# Else, no backup yet
	else:

		# Get the permissions struct
		dStruct = permission.Permission.struct()

		# Pull out all the records from the permission table
		lRecords = Commands.select(
			dStruct['host'],
			'SELECT * FROM `%(db)s`.`%(table)s`' % dStruct,
			ESelect.ALL
		)

		# Store them to a local file
		jsonb.store(lRecords, sPermissionsFile)

		# Drop the table
		permission.Permission.table_drop()

		# Recreate the table
		permission.Permission.table_create()

	# Go through each record, convert the values, and add them
	for d in lRecords:
		try:
			d['_user'] = uuid_strip_dashes(d['_user'])
			d['id'] = uuid_strip_dashes(d['id'])
			permission.Permission.create_now(d)
		except DuplicateException as e:
			print(e.args)

	# Get the users struct
	dStruct = user.User.struct()

	# Generate the name of the users backup file
	sUserChangesFile = '%s/brain_v2_2_user_changes.json' % sDataPath

	# If the backup file already exists
	if exists(sUserChangesFile):

		# Load it
		lChangeRecords = jsonb.load(sUserChangesFile)

	# Else, no backups yet
	else:

		# Pull out all the records from the user changes table
		lChangeRecords = Commands.select(
			dStruct['host'],
			'SELECT `_id`, UNIX_TIMESTAMP(`created`) as `created`, `items` ' \
			'FROM `%(db)s`.`%(table)s_changes` ORDER BY `created`' % dStruct,
			ESelect.ALL
		)

		# Store them to a local file
		jsonb.store(lChangeRecords, sUserChangesFile)

	# Generate the name of the users backup file
	sUsersFile = '%s/brain_v2_2_users.json' % sDataPath

	# If the backup file already exists
	if exists(sUsersFile):

		# Load it
		lRecords = jsonb.load(sUsersFile)

	# Else, no backup yet
	else:

		# Pull out all the records from the user table
		lRecords = Commands.select(
			dStruct['host'],
			'SELECT `_id`, ' \
				'UNIX_TIMESTAMP(`_created`) as `_created`, ' \
				'UNIX_TIMESTAMP(`_updated`) as `_updated`, ' \
				'`email`, `passwd`, `locale`, `first_name`, `last_name`, ' \
				'`title`, `suffix`, `phone_number`, `phone_ext`, `verified` ' \
			'FROM `%(db)s`.`%(table)s` ORDER BY `_created`' % dStruct,
			ESelect.ALL
		)

		# Store them to a local file
		jsonb.store(lRecords, sUsersFile)

		# Drop the table
		user.User.table_drop()

		# Recreate the table
		user.User.table_create()

	# Go through each record, convert the values, and add them
	for d in lRecords:
		try:
			d['_id'] = uuid_strip_dashes(d['_id'])
			d['verified'] = d['verified'] and True or False
			user.User.create_now(d, changes = False)
		except DuplicateException as e:
			print(e.args)

	# Go through each changes record, convert the values, and add them
	for d in lChangeRecords:
		dStruct['_id'] = uuid_strip_dashes(d['_id'])
		dStruct['created'] = d['created']
		dStruct['items'] = Commands.escape(dStruct['host'], d['items'])
		sSQL = "INSERT INTO `%(db)s`.`%(table)s_changes` " \
					"(`_id`, `created`, `items`) " \
				"VALUES (UNHEX('%(_id)s'), FROM_UNIXTIME(%(created)s), " \
					"'%(items)s')" % dStruct
		Commands.execute(dStruct['host'], sSQL)

	# Return OK
	return True