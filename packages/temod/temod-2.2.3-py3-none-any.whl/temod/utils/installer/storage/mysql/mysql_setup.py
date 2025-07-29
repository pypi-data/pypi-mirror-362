from temod.utis.installer.common import *
import mysql.connector
import sys





class MysqlInstaller(object):
	"""docstring for MysqlInstaller"""
	def __init__(self):
		super(MysqlInstaller, self).__init__()
		
	def search_existing_database(self, credentials):
		try:
			connexion = mysql.connector.connect(**credentials)
		except:
			LOGGER.error("Can't connect to the specified database using these credentials. Verify the credentials and the existence of the database.")
			LOGGER.error(traceback.format_exc())
			sys.exit(1)

		cursor = connexion.cursor()
		cursor.execute('show tables;')

		try:
			return len(cursor.fetchall()) > 0
		except:
			raise
		finally:
			cursor.close()
			connexion.close()


	def confirm_database_overwrite(self):
		print(); print_decorated_title("! DANGER"); print()
		LOGGER.info("The specified database already exists and is not empty. This installation script will erase all the database content and overwrite it with a clean one.")
		rpsn = input("Continue the installation (y/*) ?").lower()
		return rpsn == "y"


	def setup(self, args):

		credentials = get_mysql_credentials(no_confirm=args.accept_all)

		already_created = search_existing_database(credentials)
		if already_created and not args.accept_all:
			if not confirm_database_overwrite():
				LOGGER.warning("If you which to just update the app, run the script install/update.py")
				return False

		return True
