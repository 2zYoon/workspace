# Common utils
# imported by (almost) everyone (so do not implement sensitive things here)

import sys
import re
import hashlib


# Performs string validation (for name, id, pwd, etc.)
# - ASCII 
# - Printable
# - Only with alphabet, digit, and underscore
#
# @s:	string to check
# returns 0 if it is valid, otherwise non-zero value.
def check_string(s):
	if not (s.isascii() and s.isprintable()):
		return 1
	
	p = re.compile("[a-zA-Z0-9_]*")
	return 0 if len(p.match(s).group()) == len(s) else 2
		
		
# performs hashing (for pwd, etc.)
#
# @msg: string to hash
# returns hashed value (hex)
def hashing(msg):
	m = hashlib.sha256(msg.encode()).hexdigest()
	return str(m)
