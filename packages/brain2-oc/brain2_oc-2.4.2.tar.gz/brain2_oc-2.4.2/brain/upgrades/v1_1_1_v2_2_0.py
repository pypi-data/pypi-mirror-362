# coding=utf8
""" Upgrade 1.1.1 to 2.2.0

Handles taking the existing 1.1.1 data and converting it to a usable format in
2.2.0
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2025-02-25"

# Ouroboros imports
import jsonb

# Pip imports
from rest_mysql.Record_MySQL import Commands, ESelect

# Local imports
from brain.records import Permission

def run():
	"""Run

	Main entry into the script, called by the upgrade module

	Returns:
		bool
	"""

	# Notify the user
	print('Running 1.1.1 to 2.2.0 Upgrade script')

	# Create the permission table
	Permission.table_create()

	# Get the permission struct, just for the host
	dStruct = Permission.struct()

	# Loop until we have no more permissions
	while True:

		# Fetch a single permission
		dRow = Commands.select(
			dStruct['host'],
			'SELECT * FROM `%(db)s`.`brain_permissions` LIMIT 1' % dStruct,
			ESelect.ROW
		)

		# If we got nothing, we're done
		if not dRow:
			break

		# Convert the rights from json
		dRow['rights'] = jsonb.decode(dRow['rights'])

		# Init the list of new records
		lRecords = []

		# Step through each right
		for sName, dUUIDs in dRow['rights'].items():

			# Step through the UUIDs
			for sID, iRights in dUUIDs.items():

				# Add a record
				lRecords.append(
					Permission({
						'_user': dRow['user'],
						'_portal': dRow['portal'],
						'name': sName,
						'id': sID,
						'rights': iRights
					})
				)

		# If we have any
		if lRecords:

			# Create them all
			if not Permission.create_many(lRecords):
				return False

		# Delete the original permissions record
		dStruct['_id'] = dRow['_id']
		Commands.execute(
			dStruct['host'],
			"DELETE FROM `%(db)s`.`brain_permissions` " \
			"WHERE `_id` = '%(_id)s'" % dStruct
		)

	# Return OK
	return True