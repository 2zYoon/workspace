# For initialization. Called only once

from db import *

def main(args):
	print("[INFO][main] start initialization")
	# MongoDB client / database set
	CLIENT = MongoClient("mongodb://127.0.0.1:27017")
	DB_NAME = "DB"
	
	if db_init(CLIENT, DB_NAME, True):
		sys.exit("[ERROR][db_init] failed, exiting...")
	
	# Create super user, not a mongoDB admin
	db_create_account(CLIENT, DB_NAME, "admin", "dmstjd12!!")
	

if __name__ == "__main__":
	main(sys.argv)
	
