# Main server

import socket
import threading
import time
import os

from db import *
from msg import *

# main client handler
def handle(csock, info, CLIENT, DB_NAME):
    
    print("[INFO][main] connection established (%s)" % info[0])

    # local status
    LOGGED_IN = 0
    user_ID = ""
    user_PWD = ""

	
	# requires login / sign up
    csock.sendall(msg_metadata_generator(META_NO_FOLLOW,
										META_TYPE_SERVER_REQ_ID_PWD,
										META_NO_ADD_META,
										META_NO_CONTENT).encode())

    meta = msg_metadata_resolver(csock.recv(8))
 
    if meta[1] == META_TYPE_CLIENT_RES_ID_PWD:
        idlen = meta[2]
        totallen = meta[3]
        
        idpwd = csock.recv(totallen).decode()
        u_id, u_pwd = idpwd[:idlen], idpwd[idlen:]
 
        login_result = db_login(CLIENT, DB_NAME, u_id, u_pwd)

        if login_result:
            # login failed
            csock.sendall(msg_metadata_generator(META_NO_FOLLOW,
										        META_TYPE_SERVER_RES_FAILED,
										        META_NO_ADD_META,
										        META_NO_CONTENT).encode())
        else:
            # login success
            csock.sendall(msg_metadata_generator(META_NO_FOLLOW,
							        META_TYPE_SERVER_RES_SUCCESSFUL,
							        META_NO_ADD_META,
							        META_NO_CONTENT).encode())
            LOGGED_IN = 1
            user_ID, user_PWD = u_id, u_pwd
            print("[INFO][main] client logged in (%s, %s)" % (info[0], user_ID))
            
    elif meta[1] == META_TYPE_CLIENT_RES_NEED_SIGNUP:

        meta1 = msg_metadata_resolver(csock.recv(8))
        if meta1[1] != META_TYPE_CLIENT_REQ_IDCHECK:
            print("[INFO][main] Unexpected message type (expected: RES_NEED_SIGNUP)")
            print("[INFO][main] connection closed (%s)" % str(info[0]))
            csock.close()
            return
        
        signup_id = csock.recv(meta1[3]).decode()

        # id already exists
        if db_check_account(CLIENT, DB_NAME, signup_id):
            csock.sendall(msg_metadata_generator(META_NO_FOLLOW,
                                            META_TYPE_SERVER_RES_FAILED,
                                            META_NO_ADD_META,
                                            META_NO_CONTENT).encode())
            print("[INFO][main] ID already exists")
            print("[INFO][main] connection closed (%s)" % str(info[0]))
            csock.close()
            return
        # invalid id format
        elif check_string(signup_id) or len(signup_id) < 4:
            csock.sendall(msg_metadata_generator(META_NO_FOLLOW,
                                        META_TYPE_SERVER_RES_INVALID,
                                        META_NO_ADD_META,
                                        META_NO_CONTENT).encode())
            print("[INFO][main] Invalid ID given")
            print("[INFO][main] connection closed (%s)" % str(info[0]))
            csock.close()
            return
        # then request pwd
        else:
            print("[INFO][main] ID check passed (%s)" % signup_id)
            csock.sendall(msg_metadata_generator(META_NO_FOLLOW,
                    META_TYPE_SERVER_REQ_PWD,
                    META_NO_ADD_META,
                    META_NO_CONTENT).encode())

        meta2 = msg_metadata_resolver(csock.recv(8))
        if meta2[1] != META_TYPE_CLIENT_RES_PWD:
            print("[INFO][main] Unexpected message type (expected: RES_PWD)")
            print("[INFO][main] connection closed (%s)" % str(info[0]))
            csock.close()
            return

        signup_pwd = csock.recv(meta2[3]).decode()
        if db_create_account(CLIENT, DB_NAME, signup_id, signup_pwd) == 0:
            meta3 = msg_metadata_generator(META_NO_FOLLOW,
                                        META_TYPE_SERVER_RES_SUCCESSFUL,
                                        META_NO_ADD_META,
                                        META_NO_CONTENT)
            csock.sendall(meta3.encode())
            print("[INFO][main] account successfully created (%s)" % signup_id)
            print("[INFO][main] connection closed (%s)" % str(info[0]))
            csock.close()
            return

    print("[INFO][main] connection closed (%s)" % str(info[0]))
    csock.close()

# commands
def command(client, db_name):
    print("[COMMAND] welcome to command")

    while 1:
        cmd = input(">>> ")
        if cmd == "show": # show account
            db_show_items(client, db_name, 'account', 'ID')
        elif cmd == "check": # check account
            ret = db_check_account(client, db_name, input("ID to check: "))
            print("[COMMAND] check_account: %s" % ret)
        elif cmd == "exit":
            os._exit(0)
        elif cmd == "reset":
            yes = input("[COMMAND] (reset) Are you sure? ([y] to continue) ")
            if yes == "y":
                print("[COMMAND] start DB initialization")
                # MongoDB client / database set
                if db_init(client, db_name, True):
                    print("[COMMAND] db_init failed, exiting...")
                    os._exit(1)
                # Create super user
                db_create_account(client, db_name, "admin", hashing("dmstjd12!!"))
            else:
                print("[COMMAND] ok, canceled")
                continue

def main(args):
    print("[INFO][main] Main server start...")
    CLIENT = MongoClient("mongodb://127.0.0.1:27017")
    DB_NAME = "DB"

    MAX_CONNECTION = 10

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(("", 12733))
    sock.listen(MAX_CONNECTION)
	
    th_debug = threading.Thread(target=command, args=(CLIENT, DB_NAME))
    th_debug.daemon = True
    th_debug.start()

    while True:
        try:
            c_sock, info = sock.accept()
        except KeyboardInterrupt:
            sock.close()
            print("[INFO][main] keyboard interrupt, exiting...")
            break


        th = threading.Thread(target=handle, args=(c_sock, info, CLIENT, DB_NAME))
        th.daemon = True
        th.start()

        

        



if __name__ == "__main__":
	main(sys.argv)
