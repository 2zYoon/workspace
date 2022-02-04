from sys import argv
from os.path import exists

TYPE_NAME = 0b1                    # Name of variable, function, keyword, macro, etc.
TYPE_NUMERIC_VALUE = 0b10 	      # Numercic value (int, float, etc.)
TYPE_SPECIAL = 0b100     	      # Special character (including operator)

# Whitespace separates token
# Be cautious of what we are in (string, comment, etc.) 
CHAR_CUT = " \n\t"

# Special characters that cannot be a part of name (so exclude "_")
# Most of them do not combine with other operator, but something does
CHAR_SPECIAL = "$@.*+-/<>(){}[]~|!&^%,;=~"        

# These can precede to some special chracter 
# "precede" means that it can make another semantics combining with following character
# e.g. + can precede because += makes sense, but ; cannot
CHAR_CAN_PRECEDE = "+-*/%^|=&!<>"                 

# These can follow some special character
# Some combination does not make sense 
# but it's ok because we assume and only handle valid program
CHAR_CAN_FOLLOW  = "=<>+-"


# Check if the type is specified
# Only one bit set -> the number is power of 2
def check_type_specified(type_bit):
	return type_bit and not (type_bit & (type_bit - 1))


# Eliminate some strings without modifying semantics 
def eliminator(string):
    # \n after backslash
    ret = string.replace("\\\n", "")
        
    return ret

# Format character check
def check_char(char):
    ret = char[0]
    if ret.isalpha() or ret == "_":
        return ret
    else:
        print("E: Invalid argument (char: \"%s\")" % char)
        exit(-1)

# XOR operation    
def XOR(a, b):
    return a & ~b | ~a & b

# Resolve preprocessor directive for avoiding conflict
# 1. Find ready-defined macros
# 2. Find definition check (e.g., ifdef, ifndef)
def directive_resolver(dlist):
    skiplist = []
    for line in dlist:
        temp = line.split()
        if len(temp) >= 2:
            if temp[0] == "#define" or temp[0] == "#ifdef" or temp[0] == "#ifndef":
                tmp = temp[1]
                if temp[0] == "#define":
                    # macro function?
                    ttmp = ""
                    for i in tmp:
                        if i == "(":
                            break
                        else:
                            ttmp += i
                    skiplist.append(ttmp)  
                else:
                    skiplist.append(tmp)
            if len(temp) >= 3:
                if temp[1] == "defined":
                    skiplist.append(temp[2])
    return set(skiplist)    

# Check preprocessor directives and avoid conflict
# Return True if it is ok to use, False otherwise 
# This is pretty dumb but safe
def skip_check(check, dlist):
    # Check if directives define or check its definition
    for line in dlist:
        temp = line.split()
        
        if len(temp) >= 2:
            if temp[0] == "#define": 
                pass
            elif temp[0] == "#if":
                pass
            elif temp[0] == "#ifdef":
                pass
            elif temp[0] == "#ifndef":
                pass
            else:
                continue
            
            for tok in temp[1:]:
                if check in tok:
                    return False
    
    return True

# Check if we define macro of macro
# e.g.
# #define A B
# #define B 100
def skip_check_second(check, dlist, charr):
    if len(set(check)) != 1:
        return True
        
    if list(set(check)) != charr:
        return True
        
    for line in dlist:
        temp = line.split()
        if len(temp) >= 2:
            if temp[0] == "#define":
                tmp = temp[1]
                ttmp = ""
                for i in tmp:
                    if i == "(":
                        break
                    else:
                        ttmp += i
                   
                if check in ttmp:
                    return False
                       
    return True

# Raise an error for debug
# Do not use in case of invalid program
# This should not be called when use
def ERROR(code=-1):
    print("Internal Error")
    exit(-1)
   

# FOR TEST
# Print list
def print_list(l, linenum=False):
    for i in range(len(l)):
        print(("%d: " % i) if linenum else "", l[i], sep="")

def print_element(l):
    for i in l:
        print(i, end=" ")

def test():
	with open("test2.c", 'r') as f:
	    a = eliminator(f.read())
	    print(a)
	
# END FOR TEST

def main():
    argc = len(argv)
    if argc < 3:
        print("Use: python3 main.py <input> <output> [char(default=e)]")
        exit(-1)
        
    chararg = "e" if argc == 3 else check_char(argv[3])
    code = argv[1]
    
    if not exists(code):
        print("E: No such file (filename: \"%s\")" % code)
        exit(-1)
    
    output = argv[2]
    
    lex = []
    directives = []

    # Decomposing source code
    # Each decomposed token is "separable":
    # - do not change semantics even if we separate by whitespace
    # We do not decompose Preprocessor directive
    # - When we use #define, there should be no conflict
    with open(code, 'r') as f:
        str_code = eliminator(f.read()) + "\n"
        
        in_directive = False            # Are we in preprocessor directive?
        in_multi_comment = False        # Are we in multiline comment?
        in_inline_comment = False       # Are we in inline comment?
        in_char_val = False             # Are we in char?
        in_string_val = False           # Are we in string?
        
        buf = ""                # Buffer
        buf_type = 0            # Type

        for char in str_code:
            # If previous iteration clear the buffer,
            # then flag should be reset
            if buf == "":
                in_directive, \
                in_multi_comment, \
                in_inline_comment, \
                in_char_val, \
                in_string_val = [False] * 5
                
            # Put into buffer
            buf += char
            
            # Is this first character?
            if len(buf) == 1:
                if char.isdigit():
                    buf_type = TYPE_NUMERIC_VALUE
                    
                elif char.isalpha() or char == "_":
                    buf_type = TYPE_NAME
                
                elif char == "\"":
                    in_string_val = True
                    
                elif char == "\'":
                    in_char_val = True
                 
                elif char == "#":
                    in_directive = True
                    
                elif char in CHAR_SPECIAL: 
                    if not char in CHAR_CAN_PRECEDE:
                        lex.append(char)
                        buf = ""
                    else:
                        buf_type = TYPE_SPECIAL
                        
                elif char in CHAR_CUT:
                    buf = ""
                
                continue
                    
            # Is this second character?
            # Comment check
            elif len(buf) == 2:
                if buf == "/*":
                    in_multi_comment = True
                    continue
                elif buf == "//":
                    in_inline_comment = True
                    continue
            
            # Now, it is ensured that len(buf) > 1
                    
            # Is string closed?
            if in_string_val:
                if char == "\"":
                    lex.append(buf)
                    buf = ""
                continue
                
            # Is char closed?  
            if in_char_val:
                if char == "\'":
                    lex.append(buf)
                    buf = ""
                continue
            
            # Is inline comment closed?
            # Do not store in lex, just eliminate
            if in_inline_comment:
                if char == "\n":
                    buf = ""
                continue
            
            # Is multiline comment closed?
            # Do not store in lex, just eliminate
            if in_multi_comment:
                if buf[-2:]== "*/" and len(buf) > 3: # Corner case: "/*/"
                    buf = ""
                continue
            
            
            # Preprocessor directive
            if in_directive:
                if char == "\n":
                    directives.append(buf[:-1])
                    buf = ""
                continue

            # Is current chracter whitespace? 
            if char in CHAR_CUT:
                if buf[:-1] != "":
                    lex.append(buf[:-1])
                    buf = ""
                    continue
            
            # Type conflict: From TYPE_NAME
            # Conflict only when special character (except _) follows
            # Note: In valid program, "'# cannot follow, so do not check
            # e.g. bar*=3 | for(int i = 0; ... | x_12,x_13 | b=5
            #         ^   |    ^               |     ^     |  ^
            if buf_type == TYPE_NAME:
                if char in CHAR_SPECIAL:
                    lex.append(buf[:-1])
                    buf = char
                    
                    # If current character cannot precede other special character,
                    # Put into lex[], too
                    if not char in CHAR_CAN_PRECEDE:
                        lex.append(buf)
                        buf = ""
                    else:
                        buf_type = TYPE_SPECIAL
                continue
            
            # Type conflict: From TYPE_NUMERIC_VALUE
            # In valid program, conflict only when special character (except .) follows
            # Note: C does not support "_" (maybe)
            # Note: Sometimes alphabet can follow 
            #       So do not check alphabet strictly, because we assumes valid program
            # e.g. 0xffef; | 12352352325L*533 | 5.31279--; 
            #            ^ |             ^    |        ^  
            elif buf_type == TYPE_NUMERIC_VALUE:
                if char in CHAR_SPECIAL:
                    # Keep going if decimal point is here
                    if char == ".":
                        continue
                    
                    lex.append(buf[:-1])
                    buf = char
                    
                    # If current character cannot precede other special character,
                    # Put into lex[], too
                    if not char in CHAR_CAN_PRECEDE:
                        lex.append(buf)
                        buf = ""
                    else:
                        buf_type = TYPE_SPECIAL
                continue
            
            # Type conflict: From TYPE_SPECIAL
            # Here, the special character in buffer may be able to precede
            # Do not conflict only when follow-able special character follows
            # e.g. a+=15; | a=*pointer | a<<=15 | a+=_value;
            #         ^   |   ^        |     ^  |    ^
            elif buf_type == TYPE_SPECIAL:
                if char in CHAR_CAN_FOLLOW:
                    # If following char cannot precede, then just put into lex
                    if not char in CHAR_CAN_PRECEDE: 
                        lex.append(buf)
                        buf = ""
                        continue
                    
                    # Precede-able? then continue
                    # e.g. >>=
                    #       ^
                    else:
                        continue
                
                else:
                    lex.append(buf[:-1])
                    buf = char
                    
                    # Followng character check
                    # Note that numeric, string, or char can be here
                    if char.isdigit():
                        buf_type = TYPE_NUMERIC_VALUE
                        
                    elif char.isalpha() or char == "_":
                        buf_type = TYPE_NAME
                    
                    elif char == "\"":
                        in_string_val = True
                        
                    elif char == "\'":
                        in_char_val = True
   
                    continue
                         
                         
    # Count each token and sort
    # Idea: give short name to the token with higher occurrence
    lex_set = set(lex)
    lex_dict = dict()
    
    for token in lex_set:
        lex_dict[token] = lex.count(token)
    
    # Now, token list is sorted in descending order
    sorted_lex = sorted(list(lex_dict.items()), key=lambda x: x[1], reverse=True)

    # New code
    new_code = ""
    
    # macro - value mapper
    mapper = dict()
    skip_list = []
    
    multiplier = 0
    for item in sorted_lex:
        multiplier += 1
        # Avoid macro name conflict        
        # while (chararg * multiplier) in skip_set: # DEPRECATED
        while not skip_check(chararg * multiplier, directives):
            multiplier += 1
        
        if not skip_check_second(item[0], directives, chararg):
            mapper[item[0]] = item[0]
            continue
            
        mapper[item[0]] = chararg * multiplier
        new_code += "#define %s %s\n" % (chararg * multiplier, item[0]) 
    
    
    # Read again
    # Write on new_code if something matches
    # Check the mapping and write instead of putting into lex 
    with open(code, 'r') as f:
        str_code = eliminator(f.read()) + "\n"
        
        in_directive = False            # Are we in preprocessor directive?
        in_multi_comment = False        # Are we in multiline comment?
        in_inline_comment = False       # Are we in inline comment?
        in_char_val = False             # Are we in char?
        in_string_val = False           # Are we in string?
        
        buf = ""                # Buffer
        buf_type = 0            # Type

        for char in str_code:
            # If previous iteration clear the buffer,
            # then flag should be reset
            if buf == "":
                in_directive, \
                in_multi_comment, \
                in_inline_comment, \
                in_char_val, \
                in_string_val = [False] * 5
                
            # Put into buffer
            buf += char
            
            # Is this first character?
            if len(buf) == 1:
                if char.isdigit():
                    buf_type = TYPE_NUMERIC_VALUE
                    
                elif char.isalpha() or char == "_":
                    buf_type = TYPE_NAME
                
                elif char == "\"":
                    in_string_val = True
                    
                elif char == "\'":
                    in_char_val = True
                 
                elif char == "#":
                    in_directive = True
                    
                elif char in CHAR_SPECIAL: 
                    if not char in CHAR_CAN_PRECEDE:
                        new_code += "%s " % mapper[char]
                        buf = ""
                    else:
                        buf_type = TYPE_SPECIAL
                        
                elif char in CHAR_CUT:
                    if char == "\n":
                        new_code += char
                    buf = ""
                
                continue
              
            # Is this second character?
            # Comment check
            elif len(buf) == 2:
                if buf == "/*":
                    in_multi_comment = True
                    continue
                elif buf == "//":
                    in_inline_comment = True
                    continue
            
            # Now, it is ensured that len(buf) > 1
                    
            # Is string closed?
            if in_string_val:
                if char == "\"":
                    new_code += "%s " % mapper[buf]
                    buf = ""
                continue
                
            # Is char closed?  
            if in_char_val:
                if char == "\'":
                    new_code += "%s " % mapper[buf]
                    buf = ""
                continue
            
            # Is inline comment closed?
            # Do not store in lex, just eliminate
            if in_inline_comment:
                if char == "\n":
                    buf = ""
                continue
            
            # Is multiline comment closed?
            # Do not store in lex, just eliminate
            if in_multi_comment:
                if buf[-2:]== "*/" and len(buf) > 3: # Corner case: "/*/"
                    buf = ""
                continue    
                
            # Preprocessor directive
            if in_directive:
                if char == "\n":
                    new_code += "\n%s" % buf
                    buf = ""
                continue

            # Is current chracter whitespace? 
            if char in CHAR_CUT:
                if buf[:-1] != "":
                    new_code += "%s " % mapper[buf[:-1]]
                    buf = ""
                    continue
                
            # Type conflict: From TYPE_NAME
            # Conflict only when special character (except _) follows
            # Note: In valid program, "'# cannot follow, so do not check
            # e.g. bar*=3 | for(int i = 0; ... | x_12,x_13 | b=5
            #         ^   |    ^               |     ^     |  ^
            if buf_type == TYPE_NAME:
                if char in CHAR_SPECIAL:
                    new_code += "%s " % mapper[buf[:-1]]
                    buf = char
                    
                    # If current character cannot precede other special character,
                    # Put into lex[], too
                    if not char in CHAR_CAN_PRECEDE:
                        new_code += "%s " % mapper[buf]
                        buf = ""
                    else:
                        buf_type = TYPE_SPECIAL
                continue    
                
            # Type conflict: From TYPE_NUMERIC_VALUE
            # In valid program, conflict only when special character (except .) follows
            # Note: C does not support "_" (maybe)
            # Note: Sometimes alphabet can follow 
            #       So do not check alphabet strictly, because we assumes valid program
            # e.g. 0xffef; | 12352352325L*533 | 5.31279--; 
            #            ^ |             ^    |        ^  
            elif buf_type == TYPE_NUMERIC_VALUE:
                if char in CHAR_SPECIAL:
                    # Keep going if decimal point is here
                    if char == ".":
                        continue
                    
                    new_code += "%s " % mapper[buf[:-1]]
                    buf = char
                    
                    # If current character cannot precede other special character,
                    # Put into lex[], too
                    if not char in CHAR_CAN_PRECEDE:
                        new_code += "%s " % mapper[buf]
                        buf = ""
                    else:
                        buf_type = TYPE_SPECIAL
                continue
            
            # Type conflict: From TYPE_SPECIAL
            # Here, the special character in buffer may be able to precede
            # Do not conflict only when follow-able special character follows
            # e.g. a+=15; | a=*pointer | a<<=15 | a+=_value;
            #         ^   |   ^        |     ^  |    ^
            elif buf_type == TYPE_SPECIAL:
                if char in CHAR_CAN_FOLLOW:
                    # If following char cannot precede, then just put into lex
                    if not char in CHAR_CAN_PRECEDE: 
                        new_code += "%s " % mapper[buf]
                        buf = ""
                        continue
                    
                    # Precede-able? then continue
                    # e.g. >>=
                    #       ^
                    else:
                        continue
                
                else:
                    new_code += "%s " % mapper[buf[:-1]]
                    buf = char
                    
                    # Followng character check
                    # Note that numeric, string, or char can be here
                    if char.isdigit():
                        buf_type = TYPE_NUMERIC_VALUE
                        
                    elif char.isalpha() or char == "_":
                        buf_type = TYPE_NAME
                    
                    elif char == "\"":
                        in_string_val = True
                        
                    elif char == "\'":
                        in_char_val = True
   
                    continue    

    #print(new_code)
    # print_list(list(mapper.items()))
    
    # Finally, write on file
    with open(output, 'w') as f:
        f.write(new_code)
    
                            
main()
