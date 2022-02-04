import json
import numpy as np
import sys 

INDET = 0
BLANK = 1
MARKED = 2

# NOTE: some nonogram has non-unique solutions

# TODO: put zero into empty list

# verify input with basic check
# NOTE: some un-solvable input can pass
def verify_basic(size, row, col):
    r, c = size

    # size check
    if len(row) != r or len(col) != c:
        return 1

    # some row / column exceeds size?    
    for item in row:
        if sum(item) + len(item) - 1 > c:
            return 1

    for item in col:
        if sum(item) + len(item) - 1 > r:
            print("??", item, c)
            return 1

    return 0


# find all permutation
def find_p(cond, rc_length, init_length=0, restriction_blank=None, restriction_mark=None):
    all_p = []
    cond_cpy = cond[:]

    # base case: only one item
    first = cond_cpy[0]
    if len(cond_cpy) == 1:
        for i in range(rc_length - first + 1):
            sub_arr = np.zeros([rc_length], dtype=np.uint8)
            sub_arr[i:i+first] = 1
            all_p.append(sub_arr.copy())
    else:
        first = cond_cpy.pop(0)
        remaining = sum(cond_cpy) + len(cond_cpy) - 1
        niter = rc_length - remaining - first

        for i in range(niter):
            sub_arr = np.zeros([i+first+1], dtype=np.uint8)
            sub_arr[i:i+first] = 1   

            for j in find_p(cond_cpy, rc_length-(i+first+1)):
                tmp = np.concatenate((sub_arr, j))
                all_p.append(tmp)

    if init_length != 0 and init_length == len(all_p[0]):
        real_all_p = []
        for i in all_p:
            if np.array_equal(i & restriction_mark, restriction_mark) and np.array_equal(i & restriction_blank, restriction_blank):
                real_all_p.append(i)


        return real_all_p
            
        
    return all_p

# check if condition meets
# assumes the solver does not violate rule
def is_meet(cond, rc):
    return sum(cond) == np.count_nonzero(rc == 2)

# get chunk info
def chunk(rc):
    chklens = []
    chkstart = 0
    tmp_chklen = 0
    last = BLANK

    idx = 0
    for i in rc:        
        if last == BLANK and (i == INDET or i == MARKED):
            chkstart = idx
            tmp_chklen += 1
        elif i == INDET or i == MARKED:
            tmp_chklen += 1
        elif (last == INDET or last == MARKED) and i == BLANK:
            chklens.append([chkstart, chkstart+tmp_chklen-1])
            tmp_chklen = 0
            chkstart = 0

        last = i
        idx += 1

    if tmp_chklen != 0:
        chklens.append([chkstart, chkstart+tmp_chklen-1])
    
    return chklens

def first(sol, row, col):
    size = [len(row), len(col)]

    for i in range(size[0]):
        sub_arr_mark = np.ones([size[1]], dtype=np.uint8)
        sub_arr_blank = np.ones([size[1]], dtype=np.uint8)

        res = find_p(row[i], size[1])

        for j in res:
            sub_arr_mark &= j
            sub_arr_blank &= np.logical_not(j)

        for k in range(size[1]):
            if sub_arr_mark[k]:
                assert(sol[i, k] != BLANK)
                sol[i, k] = MARKED

            if sub_arr_blank[k]:
                assert(sol[i, k] != MARKED)
                sol[i, k] = BLANK

    for i in range(size[1]):
        sub_arr_mark = np.ones([size[0]], dtype=np.uint8)
        sub_arr_blank = np.ones([size[0]], dtype=np.uint8)

        res = find_p(col[i], size[0])

        for j in res:
            sub_arr_mark &= j
            sub_arr_blank &= np.logical_not(j)

        for k in range(size[0]):
            if sub_arr_mark[k]:
                assert(sol[k, i] != BLANK)
                sol[k, i] = MARKED

            if sub_arr_blank[k]:
                assert(sol[k, i] != MARKED)
                sol[k, i] = BLANK

    return 1

def cycle(sol, row, col):
    sol_backup = sol.copy()
    size = [len(row), len(col)]


    for i in range(size[0]): # row
        # find already satisfying rc
        # if pass, eliminate indetermined space
        if is_meet(row[i], sol[i]):
            sol[i][sol[i] == INDET] = BLANK

        else:
            pass
            
    for i in range(size[1]): # column
        # find already satisfying rc
        # if pass, eliminate indetermined space
        if is_meet(col[i], sol[:,i]):
            sol[:,i][sol[:,i] == INDET] = BLANK

        else:
            pass    


    # find permutation, with restriction
    for i in range(size[0]):
        sub_arr_mark = np.ones([size[1]], dtype=np.uint8)
        sub_arr_blank = np.ones([size[1]], dtype=np.uint8)

        filter_blank = []
        filter_marked = []

        for t in sol[i]:
            if t == BLANK:
                filter_blank.append(1)
                filter_marked.append(0)
            elif t == MARKED:
                filter_marked.append(1)
                filter_blank.append(0)
            else:
                filter_blank.append(0)
                filter_marked.append(0)
        
        res = find_p(row[i], size[1])


        for j in res:
            if np.array_equal( np.array(filter_blank) & j, np.zeros([size[1]],dtype=np.uint8)):
                sub_arr_mark &= j
            
            if np.array_equal( np.array(filter_marked) & np.logical_not(j), np.zeros([size[1]],dtype=np.uint8)):
                sub_arr_blank &= np.logical_not(j)

        for k in range(size[1]):
            if sub_arr_mark[k]:
                assert(sol[i, k] != BLANK)
                sol[i, k] = MARKED

            if sub_arr_blank[k]:
                assert(sol[i, k] != MARKED)
                sol[i, k] = BLANK

    for i in range(size[1]):
        sub_arr_mark = np.ones([size[0]], dtype=np.uint8)
        sub_arr_blank = np.ones([size[0]], dtype=np.uint8)


        filter_blank = []
        filter_marked = []

        for t in sol[:, i]:
            if t == BLANK:
                filter_blank.append(1)
                filter_marked.append(0)
            elif t == MARKED:
                filter_marked.append(1)
                filter_blank.append(0)
            else:
                filter_blank.append(0)
                filter_marked.append(0)
    
        res = find_p(col[i], size[0])

        for j in res:
            if np.array_equal( np.array(filter_blank) & j, np.zeros([size[0]],dtype=np.uint8)):
                sub_arr_mark &= j
            
            if np.array_equal( np.array(filter_marked) & np.logical_not(j), np.zeros([size[0]],dtype=np.uint8)):
                sub_arr_blank &= np.logical_not(j)


        for k in range(size[0]):
            if sub_arr_mark[k]:
                assert(sol[k, i] != BLANK)
                sol[k, i] = MARKED

            if sub_arr_blank[k]:
                assert(sol[k, i] != MARKED)
                sol[k, i] = BLANK  



    # no longer progress
    if np.array_equal(sol, sol_backup):
        return 0
    # continue
    else:
        return 1

# visualize
def visualization(sol, row, col, just_print_arr=False):
    if just_print_arr:
        print(sol)
        print("")
        return



    max_col_cond = 1
    max_row_cond = 1

    for t in col:
        max_col_cond = max(max_col_cond, len(t))
    for u in row:
        max_row_cond = max(max_row_cond, len(u))


    col_str = []
    cols = ""
    
    for i in range(len(col)):
        col_pad = ["   ", ] * (max_col_cond - len(col[i]))

        real_col = ["%2s " % str(k) for k in col[i]]
        col_str.append(col_pad + real_col)

    for i in range(max_col_cond):
        cols += "   " * max_row_cond + " "
        for j in range(len(col_str)):
            cols += col_str[j][i]
        cols += "\n"
    cols += "   " * max_row_cond + " " + "___" * len(col) + "\n"

    txt = cols
    idx = 0
    for i in sol:
        txt += "   " * (max_row_cond - len(row[idx])) 
        for p in row[idx]:
            txt += "%2d " % p                
        txt += "|"

        for j in i:
            if j == INDET:
                txt += "   "
            elif j == BLANK:
                txt += " X "
            else:
                txt += "███"
        txt += "\n"
        idx += 1
    print(txt)

# JSON resolver
# returns row-column pair
def json_to_rc(json_fname):
    with open(json_fname) as f:
        s = json.load(f)
        return s['row'], s['column']


RET_SUCCESS = 0
RET_VERIFY_FAIL = 1
RET_CANNOT_PROCEED = 2
RET_NO_ARG_GIVEN = 3

# main solver
# returns RESULT, SOLUTION, cycles
# RESULT: 0 only when successful, otherwise nonzero
# SOLUTION: solution numpy array
def solver(argv, vis=False):
    r, c = json_to_rc(argv[1])
    size = [len(r), len(c)]
    sol = np.zeros(size, dtype=np.uint8)

    if verify_basic(size, r, c):
        return RET_VERIFY_FAIL, sol, 0

    cnt = 0
    while True:
        if cnt == 0:
            res = first(sol, r, c)
        else:
            res = cycle(sol, r, c)

        cnt += 1
        print(cnt, res)
        if not res:
            break


    
    ret = RET_CANNOT_PROCEED if np.count_nonzero(sol == INDET) else RET_SUCCESS
    if vis:
        visualization(sol, r, c)

    return ret, sol, cnt


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("[ERROR] No argument was given.")
        exit(RET_NO_ARG_GIVEN)

    ret, solution, cnt = solver(sys.argv, True)
    if ret == RET_VERIFY_FAIL:
        print("[ERROR] Verification failed.")
    elif ret == RET_SUCCESS:
        print("[INFO] Successfully solved.")
    elif ret == RET_CANNOT_PROCEED:
        print("[INFO] The solver cannot proceed more.")
    elif ret == RET_NO_ARG_GIVEN:
        print("[INFO] Successfully solved.")
    exit(ret)
