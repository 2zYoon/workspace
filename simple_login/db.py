# Basic DB operations (only for internal use)

from pymongo import MongoClient
from common import *


# check if login info is valid
#
# @client: 	MongoDB client 
# @db_name:	database name
# @_id:		user ID
# @pwd:		user password
# returns 0 if successful, otherwise non-zero
def db_login(client, db_name, _id, hashed_pwd):
	accounts = client[db_name]['account']
	
	dat = accounts.find_one({"ID": _id})
	if not dat:
		return 1 # given ID doesn't exist
	
	return 0 if hashed_pwd == dat['pwd'] else 2


# check if login info is valid (for internal)
#
# @client: 	MongoDB client 
# @db_name:	database name
# @_id:		user ID
# @pwd:		user password
# returns 0 if successful, otherwise non-zero
def db_login_internal(client, db_name, _id, pwd):
	accounts = client[db_name]['account']
	
	dat = accounts.find_one({"ID": _id})
	if not dat:
		return 1 # given ID doesn't exist
	
	return 0 if hashing(pwd) == dat['pwd'] else 2
	

# Shows items in a given collection
# 
# @client:  	MongoDB client 
# @db_name:		database name
# @col_name:	collection name
# @field:		only prints value in a specific field
def db_show_items(client, db_name, col_name, field=None):
	for i in client[db_name][col_name].find():
		if field:
			print(i[field])
		else:
			print(i)


# Check existence of account
#
# @client:  MongoDB client 
# @db_name:	database name
# @_id:		account ID
# returns 1 if exists, otherwise 0.
def db_check_account(client, db_name, _id):
	res = client[db_name]['account'].find_one({"ID": _id})
	return res


# Create account (must be called after db_init())
#
# @client:  MongoDB client 
# @db_name:	database name
# @_id:		account ID
# @pwd:		account password (hashed)
# returns 0 if successful, non-zero otherwise.
# failure rarely happens because it assumes these are already checked.
def db_create_account(client, db_name, _id, pwd):
	if (check_string(_id)):
		return 1 # ID format check
	
	if db_check_account(client, db_name, _id):
		return 2 # ID already exists

	acc_col = client[db_name]['account']	
	acc_col.insert_one({"ID": _id, "pwd": pwd})
	return 0
	

# Initialize the database
#
# @client:  MongoDB client 
# @db_name: database name
# @clean:   if DB already exists, remove it before initialize.
#           if False, does nothing returning 1
# returns 0 if successful, non-zero otherwise.
def db_init(client, db_name="DB", clean=False):
	if db_name in client.list_database_names():
		if not clean:
			print("[ERROR][db_init] DB already exists")
			return 1
			
		else:
			print("[INFO][db_init] DB already exists, remove...")
			client.drop_database(db_name)
			
	DB = client[db_name]
	print("[INFO][db_init] DB created")
	
	cols_list = ['account', 'status']
	cols = [DB[i] for i in cols_list]
	print("[INFO][db_init] collection created")
	return 0

