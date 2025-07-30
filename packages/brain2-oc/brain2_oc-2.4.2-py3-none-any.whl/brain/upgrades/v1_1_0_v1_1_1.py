# coding=utf8
""" Upgrade 1.1.0 to 1.1.1

Handles taking the existing 1.1.0 data and converting it to a usable format in
1.1.1
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-07-28"

# Ouroboros imports
from body import constants
import jsonb

# Pip imports
from rest_mysql import Record_MySQL

# Local imports
from brain.helpers.access import RIGHTS_ALL_ID
from brain.records import Permissions

def run():
	"""Run

	Main entry into the script, called by the upgrade module

	Returns:
		bool
	"""

	# Notify the user
	print('Running 1.1 to 1.1.1 Upgrade script')

	# Get the structure for the table
	dStruct = Permissions.struct()

	# Find all the permissions records
	lRecords = Record_MySQL.Commands.select(
		dStruct['host'],
		"SELECT `_id`, `rights` " \
		"FROM `%(db)s`.`%(table)s` " % dStruct,
		Record_MySQL.ESelect.ALL
	)

	# Go through each one
	for d in lRecords:

		# Convert the rights
		dRights = jsonb.decode(d['rights'])

		# Go through each one and turn the single value into a dict of mode =>
		#	value
		for k in dRights:
			dRights[k] = { RIGHTS_ALL_ID: dRights[k] }

		# Save the new record
		Record_MySQL.Commands.execute(
			dStruct['host'],
			"UPDATE `%(db)s`.`%(table)s` " \
			"SET `rights` = '%(rights)s' " \
			"WHERE `_id` = '%(id)s'" % {
				'db': dStruct['db'],
				'table': dStruct['table'],
				'rights': Record_MySQL.Commands.escape(
					dStruct['host'],
					jsonb.encode(dRights)
				),
				'id': d['_id']
			}
		)

	# Notify the user
	print('Finished')

	# Return OK
	return True