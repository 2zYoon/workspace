# message protocol & handler (for both client and server)

from typing import Final
'''
message metadata (4 bytes):
	- [31]		message follows(0) / only-metadata(1) 
	- [30-29]	message type (notify(00) / request(01) / response(10) / ack(11))
	                - notify: can be handled async-ly
	                - request: expect to get response
	                - response: response to something
	                - ack: acknowledgement
	- [28-22]	message type (semantic differs across server/client)
	- [21-11]	Additional custom metadata  (semantic differs across message types)
	- [10-0]	message length
'''

def msg_int_to_meta(num):
	return format(num, "08X")
	
def msg_meta_to_int(meta):
	return int(meta, 16)
	
# (binary) msg -> (follow, mtype, meta, mlen)
def msg_metadata_resolver(msg):
	ret = msg_meta_to_int(msg.decode())
	follow = (ret & (0b1 << 31)) >> 31
	mtype = (ret & (0b111111111 << 22)) >> 22
	meta = (ret & (0b11111111111 << 11)) >> 11
	mlen = (ret & 0b11111111111)
	
	return follow, mtype, meta, mlen
	

# (follow, nrra, mtype, meta, mlen) -> (string) msg
def msg_metadata_generator(follow, mtype, meta, mlen):
	ret = 0
	ret |= int(follow) << 31
	ret |= int(mtype) << 22
	ret |= int(meta) << 11
	ret |= int(mlen)
	
	return msg_int_to_meta(ret)
	
# Metadata constants
META_FOLLOW_MSG:                           Final= 0b0
META_NO_FOLLOW:                            Final= 0b1

META_TYPE_SERVER_REQ_ID_PWD:               Final= 0b010000000
META_TYPE_SERVER_REQ_ID:                   Final= 0b010000001
META_TYPE_SERVER_REQ_PWD:                  Final= 0b010000010

META_TYPE_SERVER_RES_SUCCESSFUL:           Final= 0b100000000
META_TYPE_SERVER_RES_FAILED:               Final= 0b100000001
META_TYPE_SERVER_RES_INVALID:              Final= 0b100000010

META_TYPE_CLIENT_REQ_IDCHECK:              Final= 0b010000000

META_TYPE_CLIENT_RES_ID:                   Final= 0b100000010
META_TYPE_CLIENT_RES_PWD:                  Final= 0b100000011   
META_TYPE_CLIENT_RES_ID_PWD:               Final= 0b100000000 # meta: ID length in msg
META_TYPE_CLIENT_RES_NEED_SIGNUP:          Final= 0b100000001

META_NO_ADD_META:                          Final= 0b0
META_NO_CONTENT:						   Final= 0b0
