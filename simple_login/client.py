import sys
import socket
import threading

from msg import *
from common import *


def signup(csock):
    print("[INFO] Welcome")
    print("[INFO] Please sign up to enjoy")
    meta = msg_metadata_generator(META_NO_FOLLOW,
                                  META_TYPE_CLIENT_RES_NEED_SIGNUP,
                                  META_NO_ADD_META,
                                  META_NO_CONTENT)
    
    csock.sendall(meta.encode())
    
    try:
        _id = input("ID: ")
    except:
        print("[INFO] signup canceled. existing...")
        return
    
    meta = msg_metadata_generator(META_FOLLOW_MSG,
                                  META_TYPE_CLIENT_REQ_IDCHECK,
                                  META_NO_ADD_META,
                                  len(_id))
                                  
    msg = meta + _id
    csock.sendall(msg.encode())

    meta1 = msg_metadata_resolver(csock.recv(8))
    if meta1[1] == META_TYPE_SERVER_RES_FAILED:
        print("[ERROR] ID already exists, exiting...")
        return
    elif meta1[1] == META_TYPE_SERVER_RES_INVALID:
        print("[ERROR] Invalid ID format (> 4 characters with alphabet, digit or underscore(_))")
        return  
    elif meta1[1] != META_TYPE_SERVER_REQ_PWD:
        print("[ERROR] unexpected msg, exiting...")

    try:
        pwd = input("PWD: ")
    except:
        print("[INFO] signup canceled. existing...")
        return
    
    meta2 = msg_metadata_generator(META_FOLLOW_MSG,
                                  META_TYPE_CLIENT_RES_PWD,
                                  META_NO_ADD_META,
                                  len(hashing(pwd)))
    
    msg = meta2 + hashing(pwd)
    csock.sendall(msg.encode())

    meta3 = msg_metadata_resolver(csock.recv(8))
    if meta3[1] == META_TYPE_SERVER_RES_SUCCESSFUL:
        print("[INFO] account was succefully created, exiting...")
    else:
        print("[ERROR] sign up was failed, exiting...")
    return


    

def login(csock):
    print("[INFO] Please sign in to server")
    try:
        _id = input("ID: ")
        pwd = input("Password: ")
    except:
        print()
        return -1
    
    idlen = len(_id)
    totallen = len(_id) + len(hashing(pwd))
    print("[INFO] Please wait...")
    
    meta = msg_metadata_generator(META_FOLLOW_MSG,
                                  META_TYPE_CLIENT_RES_ID_PWD,
                                  idlen, totallen)
    
    msg = meta + _id + hashing(pwd)
    csock.sendall(msg.encode())
    
    # waits login result
    res = msg_metadata_resolver(csock.recv(8))
    if res[1] == META_TYPE_SERVER_RES_SUCCESSFUL:
        print("[INFO] login ")
    elif res[1] == META_TYPE_SERVER_RES_FAILED:
        print("[ERROR] login error, please check ID or password.")
        return -1
    
    return 1
    


def main_handle(csock, cmd):
    # local status
    LOGGED_IN = 0

    while (1):
        try:
            dat = csock.recv(8)
            if not dat:
                csock.close()
                return
            meta = msg_metadata_resolver(dat)
            
            # only metadata
            if meta[0] == 1:
                # server requests ID and pwd
                if meta[1] == META_TYPE_SERVER_REQ_ID_PWD:
                    if cmd == "signup":
                        signup(csock)
                        break;
                    
                    if not LOGGED_IN:
                        LOGGED_IN = login(csock)
                        if (LOGGED_IN == -1):
                            break
                continue
                
            # message with contents
            else:
                # read more
                msg = csock.recv(meta[3]).decode()
                print(msg)
        
        except KeyboardInterrupt:
            csock.close()
            return
    
    csock.close()
    return

def main(args):

    csock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    csock.connect(('127.0.0.1', 12733))

    th = threading.Thread(target=main_handle, args=(csock, args[1] if len(args) >= 2 else None))
    th.daemon = True
    th.start()
    th.join()


if __name__ == "__main__":
	main(sys.argv)
