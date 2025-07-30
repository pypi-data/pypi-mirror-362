# coding=utf8
""" Upgrade 1.0.1 to 1.1.0

Handles taking the existing 1.0.1 data and converting it to a usable format in
1.1.0
"""
__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-07-16"

# Pip imports
from rest_mysql import Record_MySQL

# Local imports
from brain.records import Permissions

def run():
	"""Run

	Main entry into the script, called by the upgrade module

	Returns:
		bool
	"""

	# Notify the user
	print('Running 1.0 to 1.1 Upgrade script')

	# Get the structure for the table
	dStruct = Permissions.struct()

	# Altering the `permissions` table to add the `portal` field and turn
	#	`_user` into `user`, add a unique index using both, and then drop the
	#	primary key
	Record_MySQL.Commands.execute(
		dStruct['host'],
		"ALTER TABLE `%(db)s`.`%(table)s` " \
		"ADD COLUMN `_id` CHAR(36) NOT NULL DEFAULT UUID() FIRST, " \
		"CHANGE COLUMN `_user` `user` CHAR(36) NOT NULL AFTER `_updated`, " \
		"ADD COLUMN `portal` CHAR(16) NOT NULL DEFAULT '' AFTER `user`, " \
		"ADD UNIQUE INDEX `u_user_portal` (`user` ASC, `portal` ASC), " \
		"DROP PRIMARY KEY, " \
		"ADD PRIMARY KEY (`_id`)" % dStruct
	)

	# Now that we have new IDs, remove the default value cause it breaks MySQL
	#	workbench and that's a pain
	Record_MySQL.Commands.execute(
		dStruct['host'],
		"ALTER TABLE `%(db)s`.`%(table)s` " \
		"CHANGE COLUMN `_id` `_id` char(36) NOT NULL" % dStruct
	)

	# Altering the changes table so that it matches the primary one
	Record_MySQL.Commands.execute(
		dStruct['host'],
		"ALTER TABLE `%(db)s`.`%(table)s_changes` " \
		"CHANGE COLUMN `_user` `_id` CHAR(36) NOT NULL, " \
		"DROP INDEX `_user`, " \
		"ADD INDEX `_id` (`_id` ASC)" % dStruct
	)

	# Find all the _changes records
	lRecords = Record_MySQL.Commands.select(
		dStruct['host'],
		"SELECT " \
		" `pc`.`_id` as `pc_id`, " \
		" `p`.`_id` as `p_id` " \
		"FROM `%(db)s`.`%(table)s_changes` as `pc` " \
		"JOIN `%(db)s`.`%(table)s` as `p` " \
		" ON `pc`.`_id` = `p`.`user`" % dStruct,
		Record_MySQL.ESelect.ALL
	)

	# Go through each one
	for d in lRecords:

		# Update the new `_id` field to match the one in permissions
		Record_MySQL.Commands.execute(
			dStruct['host'],
			"UPDATE `%(db)s`.`%(table)s_changes` " \
			"SET `_id` = '%(new)s' " \
			"WHERE `_id` = '%(old)s'" % {
				'db': dStruct['db'],
				'table': dStruct['table'],
				'old': d['pc_id'],
				'new': d['p_id']
			}
		)

	# Notify the user
	print('Finished')

	# Return OK
	return True