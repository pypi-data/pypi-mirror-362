# coding=utf8
""" Install

Method to install the necessary brain tables
"""

__author__		= "Chris Nasr"
__copyright__	= "Ouroboros Coding Inc."
__version__		= "1.0.0"
__email__		= "chris@ouroboroscoding.com"
__created__		= "2023-07-12"

# Ouroboros imports
from body.regex import EMAIL_ADDRESS
from config import config
from upgrade_oc import set_latest
from rest_mysql import Record_MySQL

# Python imports
from getpass import getpass
from os.path import abspath, expanduser
from pathlib import Path

# Module imports
from brain.helpers import access
from brain.records import key, permission, user

def create_admin() -> int:
	"""Create Admin

	Prompts the user to enter an email and password to create an administrator

	Returns:
		int
	"""

	# Init the variables
	sEmail = None
	sPasswd = None
	sFirst = None

	# Start
	print('Please enter details to give administrator access')

	# Loop until we get it working
	while True:

		# While we don't have an email
		while not sEmail:

			# Get the email address
			sInput = input('E-mail address: ').strip()

			# If it's not valid
			if not EMAIL_ADDRESS.match(sInput):
				print('Not a valid email address: %s' % sInput)
				continue

			# If the user already exists
			if user.User.filter(
				{ 'email': sInput },
				raw = '_id',
				limit = 1
			):
				print('User exists.')
				return

			# Store the email
			sEmail = sInput

		# While we don't have a password
		while not sPasswd:

			# Get the password
			sInput = getpass('Password: ').strip()

			# If it's not valid
			if not user.User.password_strength(sInput):
				print('Password is not strong enough')
				continue

			# Store the password after hashing it
			sPasswd = user.User.password_hash(sInput)

		# While we don't have a first name
		while not sFirst:

			# Get the name
			sInput = input('First name: ').strip()

			# If nothing was entered
			if not sInput:
				continue

			# Store the first name
			sFirst = sInput

		# Get the last name
		sLast = input('Last name: ').strip()

		# Create the user instance
		try:
			oUser = user.User({
				'email': sEmail,
				'passwd': sPasswd,
				'locale': config.brain.user_default_locale('en-US'),
				'first_name': sFirst,
				'last_name': sLast
			})
		except ValueError as e:
			print(e.args)
			continue

		# Create the user in the database
		sUserId = oUser.create(
			changes = { 'user': access.SYSTEM_USER_ID }
		)

		# Notify
		print('User created')

		# Add admin permissions
		permission.Permission.create_many([
			permission.Permission({
				'_user': sUserId,
				'_portal': '',
				'name': 'brain_user',
				'id': access.RIGHTS_ALL_ID,
				'rights': access.C | access.R | access.U
			}),
			permission.Permission({
				'_user': sUserId,
				'_portal': '',
				'name': 'brain_permission',
				'id': access.RIGHTS_ALL_ID,
				'rights': access.R | access.U
			})
		])

		# Notify
		print('Permissions added')

		# OK
		return

def run() -> int:
	"""Run

	Entry point into the install process. Will install required files, tables, \
	records, etc. for the service

	Returns:
		int
	"""

	# Add the global prepend
	Record_MySQL.db_prepend(config.mysql.prepend(''))

	# Add the primary mysql DB
	Record_MySQL.add_host(
		'brain',
		config.mysql.hosts[config.brain.mysql('primary')]({
			'host': 'localhost',
			'port': 3306,
			'charset': 'utf8mb4',
			'user': 'root',
			'passwd': ''
		})
	)

	# Notify
	print('Installing tables')

	# Install tables
	key.Key.table_create()
	permission.Permission.table_create()
	user.User.table_create()

	# Notify
	print('Setting lastest version')

	# Get the path to the data folder
	sData = config.brain.data('./.data')
	if '~' in sData:
		sData = expanduser(sData)
	sData = abspath(sData)

	# Store the last known upgrade version
	set_latest(
		sData,
		Path(__file__).parent.resolve()
	)

	# Create the admin user
	create_admin()

	# Notify
	print('Done')

	# Return OK
	return 0