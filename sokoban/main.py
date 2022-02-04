import sys
import os
import platform
import re
import keyboard


def init():
    global board
    global RC
    global holes
    global clear_command

    platform_name = platform.system()
    if platform_name == "Windows":
        clear_command = 'cls'
    elif platform_name == "Linux" or platform_name == "Darwin":
        clear_command = 'clear'

    if len(sys.argv) >= 2:
        with open(os.path.dirname(os.path.realpath(__file__)) + "/" + sys.argv[1]) as f:
            board = f.read().split("\n")
    else:
        with open(os.path.dirname(os.path.realpath(__file__)) + "/map.txt") as f:
            board = f.read().split("\n")
    for i in range(len(board)):
        for k in re.finditer("O", board[i]):
            holes.append([i, k.start()])

    if len(board) == 0:
        sys.stderr.write("ERROR: Invalid game board(empty board), abort.\n")
        exit(1)


    isUnique = False
    Bcount = 0
    Ocount = 0

    for i in range(len(board)):
        tmp1 = board[i].find("@")
        if tmp1 != -1:
            if isUnique:
                sys.stderr.write("ERROR: Invalid game board(non-unique player), abort.\n")
                exit(1)
            isUnique = True
            RC = [i, tmp1]
        Bcount += board[i].count("B")
        Ocount += board[i].count("O")

    if Bcount != Ocount:
        sys.stderr.write("ERROR: Invalid game board(unmatched box and hole), abort.\n")
        exit(1)
    elif Bcount == 0:
        sys.stderr.write("ERROR: Invalid game board(no box or hole), abort.\n")
        exit(1)


def board_replace(char, coor):
    global board
    board[coor[0]] = "".join((board[coor[0]][:coor[1]], char, board[coor[0]][coor[1]+1:]))


def key_handler(key_input):
    global board
    global RC

    key = key_input.lower()
    temp = RC

    if key == "w":
        temp = [temp[0] + -1, temp[1] + 0]
    elif key == "s":
        temp = [temp[0] + 1, temp[1] + 0]
    elif key == "a":
        temp = [temp[0] + 0, temp[1] + -1]
    elif key == "d":
        temp = [temp[0] + 0, temp[1] + 1]
    elif key == "esc":
        exit(0)
    elif key == "r":
        init()
        return

    if temp[0] < 0 or temp[1] < 0 or \
            temp[0] >= len(board) or temp[1] >= len(board[temp[0]]): # invalid move
        return 0
    if board[temp[0]][temp[1]] in " #": # invalid move
        return 0

    temp_map = board[temp[0]][temp[1]]

    if temp_map == "." or temp_map == "O": # just move
        if RC in holes:
            board_replace("O", RC)
        else:
            board_replace(".", RC)
        board_replace("@", temp)
        RC = temp

    elif temp_map == "B": # box
        box_temp = [-1, -1]
        if key == "w":
            box_temp = [temp[0] + -1, temp[1] + 0]
        elif key == "s":
            box_temp = [temp[0] + 1, temp[1] + 0]
        elif key == "a":
            box_temp = [temp[0] + 0, temp[1] + -1]
        elif key == "d":
            box_temp = [temp[0] + 0, temp[1] + 1]

        if box_temp[0] < 0 or box_temp[1] < 0 or \
                box_temp[0] >= len(board) or box_temp[1] >= len(board[box_temp[0]]): # invalid move
            return 0
        if board[box_temp[0]][box_temp[1]] in "# ":  # invalid move
            return 0

        if board[box_temp[0]][box_temp[1]] == "." or board[box_temp[0]][box_temp[1]] == "O":  # just move
            if temp in holes:
                board_replace("O", temp)
            else:
                board_replace(".", temp)
            board_replace("B", box_temp)

            if RC in holes:
                board_replace("O", RC)
            else:
                board_replace(".", RC)
            board_replace("@", temp)
            RC = temp

            if box_temp in holes:
                if win_check():
                    os.system(clear_command)
                    sys.stdout.write("\n " + "-" * 38 + " \n"
                                                        "| YOU WIN!! Press ESC to quit.         |\n"
                                                        " " + "-" * 38 + " \n"
                                     + "\n".join(board))
                    keyboard.wait("esc")
                    exit()


def win_check():
    for i in range(len(board)):
        for k in re.finditer("B", board[i]):
            if [i, k.start()] not in holes:
                return 0
    return 1


# MAIN
board = []
RC = [-1, -1]
holes = []
clear_command = "cls"

init()

while 1:
    sys.stdout.write("\n " + "-" * 38 + " \n"
                                        "| WASD: Move | ESC: Quit | R: Restart  |\n"
                                        " " + "-" * 38 + " \n"
                     + "\n".join(board))
    key_handler(keyboard.read_hotkey())
    keyboard.stash_state()

    os.system(clear_command)
