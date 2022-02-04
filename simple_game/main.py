from os import system
import shutil
import time
import threading
import random

from prompt_toolkit import Application
from prompt_toolkit.document import Document
from prompt_toolkit.key_binding.key_bindings import KeyBindings
from prompt_toolkit.layout.containers import VSplit, HSplit, Window, WindowAlign, WindowRenderInfo
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.buffer import Buffer

from map import *
from constants import *
from gamedata import *

#################
#  GENERAL USE  #
#################

# currently running application
current_app = None
status = STATUS_TITLE

# should be updated whenever terminal size is changed
t_size = shutil.get_terminal_size() # cols / lines
log_width = 0  # log, dialog
mid_width = 0  # hp bar
map_height = 0 # map

# ro buffer
buffer_ro1 = Buffer(read_only=True)
buffer_ro2 = Buffer(read_only=True)
buffer_ro3 = Buffer(read_only=True)
buffer_ro4 = Buffer(read_only=True)
buffer_ro5 = Buffer(read_only=True)
buffer_ro6 = Buffer(read_only=True)
buffer_ro7 = Buffer(read_only=True)
buffer_ro8 = Buffer(read_only=True)
buffer_ro9 = Buffer(read_only=True)

# rw buffer
buffer_rw1 = Buffer(read_only=False)

# misc
dummy_window = Window()

# update terminal size info
def update_t_size():
    global t_size
    global log_width
    global mid_width
    global map_height

    t_size = shutil.get_terminal_size()
    log_width = t_size[0] - WINDOW_LOWER_LEFT_WIDTH - 4
    mid_width = t_size[0] - WINDOW_UPPER_LEFT_WIDTH - 4
    map_height = t_size[1] - WINDOW_UPPER_HEIGHT - WINDOW_LOWER_HEIGHT - 4


###########
#  TITLE  #
###########

# globals for title
kb_title = KeyBindings()
title_switch_value = 0      # NEW GAME / LOAD GAME / EXIT
title_enable_switch = 1
title_enable_LR = 0
title_choice = 0            # OK / CANCEL

def title_section_update():
    global title_switch_value
    global buffer_ro3

    buffer_ro3.set_document(value=Document("\n\n\n\n\n"), bypass_readonly= True)

    if title_switch_value == 0:
        buffer_ro1.set_document(value=Document(TEXT_NEW_GAME_SELECTED), bypass_readonly=True)
    elif title_switch_value == 1:
        buffer_ro1.set_document(value=Document(TEXT_LOAD_GAME_SELECTED), bypass_readonly=True)
    else:
        buffer_ro1.set_document(value=Document(TEXT_EXIT_SELECTED), bypass_readonly=True)

def title_choice_update():
    global title_enable_LR
    global buffer_ro3

    if title_choice == 0:
        buffer_ro3.set_document(value=Document(TEXT_MAY_OVERWRITE_SAVE_DATA_OK), bypass_readonly= True)
    elif title_choice == 1:
        buffer_ro3.set_document(value=Document(TEXT_MAY_OVERWRITE_SAVE_DATA_CANCEL), bypass_readonly= True)


@kb_title.add('c-c')
def kb_title_ctrlC(event):
    global status
    status = STATUS_EXIT_NORMAL

    event.app.exit()

@kb_title.add('enter')
@kb_title.add('space')
def kb_title_enter_space(event):
    global title_switch_value
    global title_enable_switch
    global title_enable_LR
    global title_choice
    global buffer_ro3
    global status

    # reset buffer
    buffer_ro3.set_document(value=Document("\n\n\n\n\n"), bypass_readonly= True)

    # some popup
    if title_enable_switch == 0:
        title_enable_switch = 1

        if title_enable_LR == 1:
            title_enable_LR = 0
            
            if title_choice == 0: # OK
                status = STATUS_CREATE
                event.app.exit()
        return
    
    # if no popup, select action
    # NEW GAME
    if title_switch_value == 0:
        # warn before overwrite
        if gamedata_check():
            title_enable_LR = 1
            title_enable_switch = 0
            title_choice = 0
            buffer_ro3.set_document(value=Document(TEXT_MAY_OVERWRITE_SAVE_DATA_OK), bypass_readonly= True)

        # create new gamedata
        else:
            gamedata_create()
            status = STATUS_CREATE
            event.app.exit()

    # LOAD GAME
    elif title_switch_value == 1:
        if not gamedata_check():
            buffer_ro3.set_document(value=Document(TEXT_NO_SAVE_DATA), bypass_readonly= True)
            title_enable_switch = 0
        else:
            status = STATUS_MAIN
            event.app.exit()

    # EXIT
    else:
        status = STATUS_EXIT_NORMAL
        event.app.exit()

@kb_title.add('up')
def kb_title_up(event):
    global title_switch_value
    global title_enable_switch

    if title_enable_switch == 0:
        return

    title_switch_value = (title_switch_value - 1) % 3
    title_section_update()

@kb_title.add('down')
def kb_title_down(event):
    global title_switch_value
    global title_enable_switch

    if title_enable_switch == 0:
        return

    title_switch_value = (title_switch_value + 1) % 3
    title_section_update()

@kb_title.add('left')
def kb_title_left(event):
    global title_enable_LR
    global title_choice

    if title_enable_LR == 0:
        return
    
    title_choice = (title_choice - 1) % 2
    title_choice_update()

@kb_title.add('right')
def kb_title_right(event):
    global title_enable_LR
    global title_choice

    if title_enable_LR == 0:
        return
    
    title_choice = (title_choice + 1) % 2
    title_choice_update()

# main routine for title
def app_title():
    global dummy_window
    buffer_ro1.set_document(value=Document(TEXT_NEW_GAME_SELECTED), bypass_readonly=True)
    buffer_ro2.set_document(value=Document(TEXT_TITLE), bypass_readonly=True)

    # here, buffer_ro3 is always 6-line  
    buffer_ro3.set_document(value=Document("\n\n\n\n\n"), bypass_readonly= True)
    
    
    title_container = HSplit([
        dummy_window,
        Window(content=BufferControl(buffer=buffer_ro2), align=WindowAlign.CENTER),
        Window(content=FormattedTextControl(text=""), align=WindowAlign.CENTER),
        Window(content=BufferControl(buffer=buffer_ro3), align=WindowAlign.CENTER),
        Window(content=FormattedTextControl(text=""), align=WindowAlign.CENTER),
        Window(content=BufferControl(buffer=buffer_ro1), align=WindowAlign.CENTER),
    ])


    title_layout = Layout(title_container,
                          focused_element=dummy_window)
    
    current_app = Application(layout=title_layout,
                            full_screen=True,
                            key_bindings=kb_title)
    current_app.run()


############
#  CREATE  #
############
kb_create = KeyBindings()

def create_typer(char):
    global buffer_ro2

    buffer_content = buffer_ro2.document.text 
    buffer_length = len(buffer_content)

    if len(char) == 1:
        if buffer_length < MAX_NAME_LENGTH:
            buffer_ro2.set_document(value=Document(buffer_content + char.upper()),
                                    bypass_readonly=True)
    elif char == 'BACKSPACE':
        if buffer_length > 0:
            buffer_ro2.set_document(value=Document(buffer_content[:-1]), 
                                    bypass_readonly=True)
    
    elif char == 'SPACE':
        if buffer_length < MAX_NAME_LENGTH:
            buffer_ro2.set_document(value=Document(buffer_content + " "),
                                    bypass_readonly=True)
    
@kb_create.add('a')
def kb_create_a(e): create_typer('a')  
@kb_create.add('b')
def kb_create_a(e): create_typer('b')
@kb_create.add('c')
def kb_create_a(e): create_typer('c')
@kb_create.add('d')
def kb_create_a(e): create_typer('d')
@kb_create.add('e')
def kb_create_a(e): create_typer('e')
@kb_create.add('f')
def kb_create_a(e): create_typer('f')
@kb_create.add('g')
def kb_create_a(e): create_typer('g')
@kb_create.add('h')
def kb_create_a(e): create_typer('h')
@kb_create.add('i')
def kb_create_a(e): create_typer('i')
@kb_create.add('j')
def kb_create_a(e): create_typer('j')
@kb_create.add('k')
def kb_create_a(e): create_typer('k')
@kb_create.add('l')
def kb_create_a(e): create_typer('l')
@kb_create.add('m')
def kb_create_a(e): create_typer('m')
@kb_create.add('n')
def kb_create_a(e): create_typer('n')
@kb_create.add('o')
def kb_create_a(e): create_typer('o')
@kb_create.add('p')
def kb_create_a(e): create_typer('p')
@kb_create.add('q')
def kb_create_a(e): create_typer('q')
@kb_create.add('r')
def kb_create_a(e): create_typer('r')
@kb_create.add('s')
def kb_create_a(e): create_typer('s')
@kb_create.add('t')
def kb_create_a(e): create_typer('t')
@kb_create.add('u')
def kb_create_a(e): create_typer('u')
@kb_create.add('v')
def kb_create_a(e): create_typer('v')
@kb_create.add('w')
def kb_create_a(e): create_typer('w')
@kb_create.add('x')
def kb_create_a(e): create_typer('x')
@kb_create.add('y')
def kb_create_a(e): create_typer('y')
@kb_create.add('z')
def kb_create_a(e): create_typer('z')
@kb_create.add('0')
def kb_create_a(e): create_typer('0')
@kb_create.add('1')
def kb_create_a(e): create_typer('1')
@kb_create.add('2')
def kb_create_a(e): create_typer('2')
@kb_create.add('3')
def kb_create_a(e): create_typer('3')
@kb_create.add('4')
def kb_create_a(e): create_typer('4')
@kb_create.add('5')
def kb_create_a(e): create_typer('5')
@kb_create.add('6')
def kb_create_a(e): create_typer('6')
@kb_create.add('7')
def kb_create_a(e): create_typer('7')
@kb_create.add('8')
def kb_create_a(e): create_typer('8')
@kb_create.add('9')
def kb_create_a(e): create_typer('9')
@kb_create.add('c-h')
def kb_create_a(e): create_typer('BACKSPACE')
@kb_create.add('space')
def kb_create_a(e): create_typer('SPACE')

@kb_create.add('left')
@kb_create.add('right')
@kb_create.add('down')
@kb_create.add('up')
def kb_create_do_nothing(e):
    return

@kb_create.add('enter')
def kb_create_enter(event):
    global buffer_ro2
    global status

    buffer_content = buffer_ro2.document.text.strip()
    buffer_length = len(buffer_content)

    if buffer_length <= 0:
        return
    else:
        gamedata_init_data(buffer_content)
        
        status = STATUS_MAIN
        event.app.exit()

@kb_create.add('c-c')
def kb_create_ctrlC(event):
    global status
    status = STATUS_EXIT_NORMAL

    event.app.exit()


# main routine for create
def app_create():
    global dummy_window

    buffer_ro1.set_document(value=Document(TEXT_CREATE_NAME_UPPER), bypass_readonly=True)
    buffer_ro2.set_document(value=Document(""), bypass_readonly=True)
    buffer_ro2.multiline = False
    buffer_ro3.set_document(value=Document(TEXT_CREATE_NAME_LOWER), bypass_readonly=True)


    create_subcontainer_name = VSplit([
        Window(content=FormattedTextControl(text="")),
        Window(content=BufferControl(buffer=buffer_ro2),
                align=WindowAlign.LEFT, height=1, width=MAX_NAME_LENGTH+1),
        Window(content=FormattedTextControl(text="")),
    ],   
    padding_char="| ",
    padding=2)

    create_container = HSplit([
        dummy_window,
        Window(content=BufferControl(buffer=buffer_ro1),
                align=WindowAlign.CENTER, height=3),
    
        create_subcontainer_name,
        Window(content=BufferControl(buffer=buffer_ro3),
                align=WindowAlign.CENTER),
    ],
    align=WindowAlign.CENTER)

    create_layout = Layout(create_container,
                            focused_element=buffer_ro2)
    
    current_app = Application(layout=create_layout,
                            full_screen=True,
                            key_bindings=kb_create)
    current_app.run()


##########
#  MAIN  #
##########
kb_main = KeyBindings()
dat = dict()
current_map = []

# logs
game_log = []
battle_log = []

# now movable?
system_movable = MODE_SYSTEM_MOVABLE
def get_system_movable():
    global system_movable

    if system_movable:
        buffer_ro2.set_document(value=Document(KEY_HELP_MOVEMODE),      
                            bypass_readonly=True)
    return system_movable

def set_system_movable(v):
    global system_movable
    global buffer_ro2

    system_movable = v
    if system_movable:
        buffer_ro2.set_document(value=Document(KEY_HELP_MOVEMODE),      
                            bypass_readonly=True)


# doing battle?
on_battle = 0
def get_on_battle():
    global on_battle

    return on_battle

def set_on_battle(v):
    global on_battle
    global buffer_ro2

    on_battle = v
    if on_battle:
        buffer_ro2.set_document(value=Document(KEY_HELP_BATTLEMODE),      
                            bypass_readonly=True)

# when the result of battle is determined
# show result, reward, etc.
battle_finished = 0

# marked after fight
goto_jail = 0

# item/consumable page/cursor
ic_page = 0
ic_cursor = 0

def get_battle_finished():
    global battle_finished

    return battle_finished

def set_battle_finished(v):
    global battle_finished

    battle_finished = v

# battle turn
# must reset before start
turn = 0

# follows NPC type code, none (-1)
dialog_choice = -1

# temporary NPC data
tmp_NPC_data = None

# temporary battle data
tmp_battle_data = None
tmp_battle_curhp = 0



def increase_time(t):
    global dat
    dat['env']['time'] += t
    update_char_info()


# update map display
def update_map():
    global dat
    global current_map
    global t_size
    global map_height

    global buffer_ro5
    
    cols = t_size[0] - 3

    txt = map_display_string(cols,  map_height, current_map, dat['stat']['pos'])

    buffer_ro5.set_document(value=Document(txt),
                            bypass_readonly=True)
    buffer_ro5.cursor_position = 0

# write log into buffer_ro4
# usually called after appending log
def show_log():
    global buffer_ro4
    global log_width

    txt = ""
    for i in range(len(game_log)):
        subtxt = game_log[i]
        nww = len(subtxt) // log_width
        if nww:
            for j in range(nww+1):
                txt += subtxt[j * log_width : min((j+1) * log_width, len(subtxt))] + "\n"
        else:
            txt += subtxt + "\n"

    buffer_ro4.set_document(value=Document(txt), bypass_readonly=True)

# show NPC dialog
def show_dialog(mode, data, special=0):
    global buffer_ro4
    global log_width
    global dialog_choice
    global tmp_NPC_data
    global dat

    # update dialog mode
    dialog_choice = mode

    txt = "[ %s ]\n" % data[NPC_NAME]

    if special:
        # when you refuse to fight
        if mode == NPC_FIGHT and special == NPC_DIALOG_REFUSE_FIGHT:
            subtxt = data[NPC_REFUSE_REPLY]
            nww_dialog = len(subtxt) // log_width
            if nww_dialog:
                for i in range(nww_dialog+1):
                    txt += subtxt[i * log_width : min((i+1)*log_width, len(subtxt))] + "\n"
            else:
                txt += subtxt + "\n"
        # when 
        elif mode == NPC_FIGHT and special == NPC_DIALOG_LOSE:
            subtxt = data[NPC_LOSE_SAYING]
            nww_dialog = len(subtxt) // log_width
            if nww_dialog:
                for i in range(nww_dialog+1):
                    txt += subtxt[i * log_width : min((i+1)*log_width, len(subtxt))] + "\n"
            else:
                txt += subtxt + "\n"
        elif mode == NPC_DOCTOR and special == NPC_DIALOG_DISCHARGE:
            subtxt = data[NPC_DOCTOR_THANK]
            nww_dialog = len(subtxt) // log_width
            if nww_dialog:
                for i in range(nww_dialog+1):
                    txt += subtxt[i * log_width : min((i+1)*log_width, len(subtxt))] + "\n"
            else:
                txt += subtxt + "\n"

        # undefined
        else:
            assert(False)

    else:
        subtxt = data[NPC_DIALOG]
        nww_dialog = len(subtxt) // log_width
        if nww_dialog:
            for i in range(nww_dialog+1):
                txt += subtxt[i * log_width : min((i+1)*log_width, len(subtxt))] + "\n"
        else:
            txt += subtxt + "\n"

        if mode == NPC_SHOP:
            pass
            
            # enable pgup / pgdown for choice
            # enable space to confirm

        elif mode == NPC_FIGHT:
            # choice fight or not
            txt += "\n <Y> %s\n <N> %s\n" % (data[NPC_YES_CHOICE], data[NPC_NO_CHOICE])

            # enable y/n for choice
            tmp_NPC_data = data

        elif mode == NPC_DOCTOR:
            # discharge
            txt += "\n <Y> Discharge (cost: %d money)" % (data[NPC_DOCTOR_COST] + int(dat['stat']['money'] * NPC_DOCTOR_COST_RATE))

            # enable y for choice
            tmp_NPC_data = data


    buffer_ro4.set_document(value=Document(txt), bypass_readonly=True)

# update mapinfo
def update_mapinfo():
    global dat
    global current_map

    name_region = current_map[1][MAP_META_REGION]
    name_area = current_map[1][MAP_META_AREA]

    x, y = dat['stat']['pos']
    xypos = "X: %d, Y: %d" % (x, y)

    string = " [ %s ]\n %s\n\n %s" % (name_region, name_area, xypos)

    buffer_ro3.set_document(value=Document(string), bypass_readonly=True)


# show HP
def show_hp():
    global mid_width
    global buffer_ro7
    global dat

    txt = " HP  %4d/%4d " % (dat['stat']['hp'], dat['stat']['maxhp'])
    l = len(txt)
    
    if dat['stat']['hp'] == dat['stat']['maxhp']:
        txt += CHAR_HP_FILL * (mid_width - l - 1)
    else:
        ratio = dat['stat']['hp'] / dat['stat']['maxhp']
        txt += "▮" * int(ratio * (mid_width - l - 1)) + "▯" * (mid_width - l - 1 - int(ratio * (mid_width - l - 1)))

    buffer_ro7.set_document(value=Document(txt), bypass_readonly=True)
    buffer_ro7.cursor_position = 0



# update hp (delta)
# do not use on battle
def inc_hp(v):
    global dat
    
    dat['stat']['hp'] = min(dat['stat']['maxhp'], max(dat['stat']['hp']+v, 0))

    # check/handle death
    if dat['stat']['hp'] <= 0:
        pass

    show_hp()

# update hp (abs)
# do not use on battle
def set_hp(v):
    global dat
    
    dat['stat']['hp'] = min(dat['stat']['maxhp'], max(v, 0))

    # check/handle death
    if dat['stat']['hp'] <= 0:
        pass

    show_hp()


# battle log
def show_battle_log():
    global battle_log
    global buffer_ro4
    global log_width

    txt = ""
    for i in range(len(battle_log)):
        nww = len(battle_log[i]) // log_width
        if nww:
            for j in range(nww+1):
                txt += battle_log[i][j * log_width : min((j+1) * log_width, len(battle_log[i]))] + "\n"
        else:
            txt += battle_log[i] + "\n"

    buffer_ro4.set_document(value=Document(txt), bypass_readonly=True)


def battle_get_reward():
    global tmp_battle_data
    global dat
    global battle_log

    tmp_battle_data[BATTLE_REWARD_MONEY]

    # initial reward
    if dat['env']['battlewin'][tmp_battle_data[BATTLE_CODE]] == 1:
        reward = tmp_battle_data[BATTLE_REWARD_INIT]
    # repeat reward
    else:
        reward = tmp_battle_data[BATTLE_REWARD_REPEAT]

    # money
    if reward[BATTLE_REWARD_MONEY] != 0:
        dat['stat']['money'] += reward[BATTLE_REWARD_MONEY]
        battle_log.append(" - Money: %d" % reward[BATTLE_REWARD_MONEY])

    # ensured reward item
    if reward[BATTLE_REWARD_COMMON_ITEM] != ITEM_NONE:
        dat['stat']['items'][reward[BATTLE_REWARD_COMMON_ITEM]] += reward[BATTLE_REWARD_COMMON_ITEM_NUMBER]
        battle_log.append(" - %s X %d" % (ITEM_INFO[reward[BATTLE_REWARD_COMMON_ITEM]][ITEM_NAME],
                                          reward[BATTLE_REWARD_COMMON_ITEM_NUMBER]))

    # ensured reward consumable
    if reward[BATTLE_REWARD_COMMON_CONSUMABLE] != CONSUMABLE_NONE:
        dat['stat']['consumables'][reward[BATTLE_REWARD_COMMON_CONSUMABLE]] += reward[BATTLE_REWARD_COMMON_CONSUMABLE_NUMBER]
        battle_log.append(" - %s X %d" % (CONSUMABLE_INFO[reward[BATTLE_REWARD_COMMON_CONSUMABLE]][ITEM_NAME],
                                          reward[BATTLE_REWARD_COMMON_CONSUMABLE_NUMBER]))
    # rare item
    if reward[BATTLE_REWARD_RARE_ITEM] != ITEM_NONE:
        if reward[BATTLE_REWARD_RARE_ITEM_PROB] > random.random():
            dat['stat']['items'][reward[BATTLE_REWARD_RARE_ITEM]] += 1
            battle_log.append(" - %s X 1" % (ITEM_INFO[reward[BATTLE_REWARD_COMMON_ITEM]][ITEM_NAME]))

    # rare consumable
    if reward[BATTLE_REWARD_RARE_CONSUMABLE] != CONSUMABLE_NONE:
        if reward[BATTLE_REWARD_RARE_CONSUMABLE_PROB] > random.random():
            dat['stat']['consumables'][reward[BATTLE_REWARD_RARE_CONSUMABLE]] += 1
            battle_log.append(" - %s X 1" % (ITEM_INFO[reward[BATTLE_REWARD_COMMON_CONSUMABLE]][ITEM_NAME]))


def battle_check():
    global tmp_battle_data
    global tmp_battle_curhp
    global on_battle
    global battle_log
    global goto_jail
    global dat
    
    # LOSE
    if dat['stat']['hp'] <= 0:
        set_battle_finished(BATTLE_LOSE)
        battle_log.append("")
        battle_log.append("!!! YOU LOSE !!!")
        
        battle_log.append("")
        battle_log.append("Press SPACE to continue")
        return BATTLE_LOSE

    # WIN
    elif tmp_battle_curhp <= 0:
        set_battle_finished(BATTLE_WIN)
        battle_log.append("")
        battle_log.append("!!! YOU WIN !!!")
        battle_log.append("REWARD:")

        # update win count
        dat['env']['battlewin'][tmp_battle_data[BATTLE_CODE]] += 1

        # reward
        battle_get_reward()

        # prisoned?
        if tmp_battle_data[BATTLE_PRISON_PROB] > random.random():
            goto_jail = 1
            battle_log.append("WARNING!! A police found your fight. You will be prisoned...")
        else:
            goto_jail = 0

        battle_log.append("")
        battle_log.append("Press SPACE to continue")
        return BATTLE_WIN
    else:
        set_battle_finished(BATTLE_CONTINUE)
        return BATTLE_CONTINUE


def battle_cmd(cmd):
    global dat
    global turn
    global battle_log
    global on_battle
    global tmp_battle_curhp
    global tmp_battle_data

    # already finished / not started (this maybe a bug)
    if get_battle_finished():
        return

    if cmd == BATTLE_CMD_ATTACK:
        battle_log.append("[TURN %d]" % turn)

        # first attack: me
        dmg1 = int(dat['stat']['str'] *
                    max(0, min(1, dat['stat']['hp']/dat['stat']['maxhp'])) *
                    (random.randint(100-BATTLE_DAMAGE_DEV, 100+BATTLE_DAMAGE_DEV) / 100))
        
        # miss?
        if (BATTLE_MISS_RATE_BASE + BATTLE_MISS_RATE_MAX_BONUS * min(tmp_battle_data[BATTLE_LUCK]/BATTLE_MAX_LUCK, 1)) > random.randint(1, 101):
            battle_log.append("> My attack! ...miss")
        else:
            tmp_battle_curhp = max(tmp_battle_curhp - dmg1, 0)
            battle_log.append("> My attack! %d damage" % dmg1)
            battle_log.append("> %s's HP: %d / %d" % (tmp_battle_data[BATTLE_NAME], 
                                                      tmp_battle_curhp, 
                                                      tmp_battle_data[BATTLE_HP])) 
            
        show_battle_log()

        # check
        if battle_check():
            show_battle_log()
            return


        # second attack: enemy
        dmg2 = int(tmp_battle_data[BATTLE_STR] * 
                    max(0, min(1, tmp_battle_curhp / tmp_battle_data[BATTLE_HP])) *
                    (random.randint(100-BATTLE_DAMAGE_DEV, 100+BATTLE_DAMAGE_DEV) / 100))

        # miss?
        if (BATTLE_MISS_RATE_BASE + BATTLE_MISS_RATE_MAX_BONUS * min(dat['stat']['luck']/BATTLE_MAX_LUCK, 1)) > random.randint(1, 101):
            battle_log.append("> %s's attack! ...miss" % tmp_battle_data[BATTLE_NAME])
        else:
            dat['stat']['hp'] = max(dat['stat']['hp'] - dmg2, 0) 
            show_hp()
            battle_log.append("> %s's attack! %d damage" % (tmp_battle_data[BATTLE_NAME], dmg2))        
            battle_log.append("> My HP: %d / %d" % (dat['stat']['hp'], 
                                                      dat['stat']['maxhp'])) 

        show_battle_log()

        # check
        if battle_check():
            show_battle_log()
            return

        turn += 1

        pass
    if cmd == BATTLE_CMD_QUIT:
        pass


# initialize battle mode
def battle(battle_code):
    global dat
    global turn
    global battle_log
    global system_movable
    global tmp_battle_curhp
    global tmp_battle_data
    global on_battle


    tmp_battle_data = BATTLE_INFO[battle_code]
    tmp_battle_curhp = tmp_battle_data[BATTLE_HP]

    # disable move
    set_system_movable(0)
    set_on_battle(1)

    # clear battle log
    battle_log = ["<BATTLE START>",
                   "> ENEMY: %s" % tmp_battle_data[BATTLE_NAME],
                   "> HP: %d STR: %d LUCK: %d" % (tmp_battle_data[BATTLE_HP], 
                                                  tmp_battle_data[BATTLE_STR], 
                                                  tmp_battle_data[BATTLE_LUCK] )]
    show_battle_log()
    return

# teleport the character
def teleport(x, y, timeinc=0, lazy_log=False):
    global current_map
    global dat

    dat['stat']['pos'][0] = x
    dat['stat']['pos'][1] = y
    increase_time(timeinc)
    
    update_mapinfo()
    update_map()
    if not lazy_log:
        show_log()


# move the character
def move(x, y, skip_timeinc=False):
    global dat
    global system_movable
    global current_map
    global dialog_choice

    # remove if overhead is too big
    update_t_size()
    

    if get_system_movable():
        
    
        tmp_x = dat['stat']['pos'][0] + x
        tmp_y = dat['stat']['pos'][1] + y

        # OOB?
        if not map_boundary_check(current_map[1], [tmp_x, tmp_y]):
            return
        
        # now, it is safe to refer
        target = current_map[0][tmp_y, tmp_x]

        # non-movable target?
        if target == MAP_WALL or target == MAP_EMPTY:
            return

        # conditional-movable target?
        
        #
        # now, ensured that it can move.
        #

        show_hp()

        # portal?
        if target == MAP_PORTAL:
            dat['stat']['returnmap'] = current_map[META][MAP_META_CODE]

            # dest: mapcode, x, y
            dest = PORTAL_INFO[current_map[META][MAP_META_CODE]][(tmp_x, tmp_y)]
            dat['stat']['map'] = dest[0]
            dat['stat']['pos'][0] = dest[1]
            dat['stat']['pos'][1] = dest[2]
            
            dat['stat']['step'] += abs(x) + abs(y)
            if dat['stat']['step'] % dat['stat']['stamina'] == 0 and not skip_timeinc:
                increase_time(1)
            
            load_map()
            update_mapinfo()
            update_map()

            game_log.append("[INFO] Moved to %s" %current_map[META][MAP_META_AREA])
            show_log()

            return

        # local portal?
        if target == MAP_LOCAL_PORTAL:
            # dest: x, y
            dest = LOCAL_PORTAL_INFO[current_map[META][MAP_META_CODE]][(tmp_x, tmp_y)]
            dat['stat']['pos'][0] = dest[0]
            dat['stat']['pos'][1] = dest[1]
            
            dat['stat']['step'] += abs(x) + abs(y)
            if dat['stat']['step'] % dat['stat']['stamina'] == 0 and not skip_timeinc:
                increase_time(1)
            
            update_mapinfo()
            update_map()
            return

        # return portal?
        if target == MAP_RETURN:

            dat['stat']['map'] = dat['stat']['returnmap']

            load_map()

            dat['stat']['pos'][0] = current_map[META][MAP_META_RET_X]
            dat['stat']['pos'][1] = current_map[META][MAP_META_RET_Y]

            dat['stat']['step'] += abs(x) + abs(y)
            if dat['stat']['step'] % dat['stat']['stamina'] == 0 and not skip_timeinc:
                increase_time(1)

            update_mapinfo()
            update_map()

            game_log.append("[INFO] Returned to %s" % current_map[META][MAP_META_AREA])
            show_log()

            return
        # event?

        # NPC?
        if target == MAP_NPC:
            # simple?
            npc_type = NPCS[current_map[META][MAP_META_CODE]][(tmp_x, tmp_y)][0]
            npc_data = NPCS[current_map[META][MAP_META_CODE]][(tmp_x, tmp_y)]

            show_dialog(npc_type, npc_data)


        else:
            # reset choice flags
            dialog_choice = -1

            # switch to log mode
            show_log()

        dat['stat']['pos'][0] += x
        dat['stat']['pos'][1] += y

        dat['stat']['step'] += abs(x) + abs(y)

        if dat['stat']['step'] % dat['stat']['stamina'] == 0 and not skip_timeinc:
            increase_time(1)

        update_mapinfo()
        update_map()

# called when init, or map is changed (by portal, etc.)
def load_map():
    global dat
    global current_map

    current_map = map_loader(dat['stat']['map'])
    update_mapinfo()
    update_map()
    update_t_size()


# go to jail
def prison():
    global dat

    dat['stat']['prison'] += 1
    dat['stat']['returnmap'] = current_map[META][MAP_META_CODE]

    dat['stat']['map'] = 2
    dat['stat']['pos'][0] = 1
    dat['stat']['pos'][1] = 1
                
    load_map()
    update_mapinfo()
    update_map()


# update upper-left (clock, character info, money)
def update_char_info():
    global dat
    global buffer_ro6


    now = dat['env']['time']
    
    now_day = now // 1440
    smtwtfs = now_day % 7
    now_hour = (now % 1440) // 60
    now_minute = (now % 1440) % 60

    clock_digits = [now_hour // 10,
                    now_hour % 10,
                    now_minute // 10,
                    now_minute % 10]

    
    str_1 = "   [" + TEXT_SMTWTFS[smtwtfs] + "]  " + "%12s" % ("Day " + str(now_day))
    str_2 = "\n   "
    str_3 = "\n   "
    str_4 = "\n   "
    for i in range(4):
        if clock_digits[i] in [0, 2, 3, 5, 7, 8, 9]:
            str_2 += " __ "
        else:
            str_2 += "    "
        
        if clock_digits[i] in [4, 8, 9]:
            str_3 += "|__|"
        elif clock_digits[i] in [0]:
            str_3 += "|  |"
        elif clock_digits[i] in [1, 7]:
            str_3 += "   |"
        elif clock_digits[i] in [2, 3]:
            str_3 += " __|"
        else:
            str_3 += "|__ "
        
        if clock_digits[i] in [0, 6, 8]:
            str_4 += "|__|"
        elif clock_digits[i] in [1, 4, 7, 9]:
            str_4 += "   |"
        elif clock_digits[i] in [3, 5]:
            str_4 += " __|"
        else:
            str_4 += "|__ "
        
        if i == 1:
            str_2 += "   "
            str_3 += " · "
            str_4 += " · "


    money_formatted = format(dat['stat']['money'], ',') # MAX: 9,999,999,999,999

    # 25 length
    txt = '''
--------------------------
 {:<12}     {:>1}{:>4}{:>2}
 {:<12}     {:>1}{:>4}{:>2}
 {:<12}     {:>1}{:>4}{:>2}
 {:<12}     {:>1}{:>4}{:>2}
 {:<12}     {:>1}{:>4}{:>2}
--------------------------
 {:<5}{:>18}\
'''.format("STRENGTH", "[", str(dat['stat']['str']), " ]",
           "INTELLIGENCE", "[", str(dat['stat']['int']), " ]",
           "CHARMISMA", "[", str(dat['stat']['charm']), " ]",
           "LUCK", "[", str(dat['stat']['luck']), " ]",
           "STAMINA", "[", str(dat['stat']['stamina']), " ]",
           "MONEY", money_formatted,
)

    buffer_ro6.set_document(value=Document(str_1+str_2+str_3+str_4+txt), bypass_readonly=True)

<<<<<<< HEAD
=======
# shows item / consumables
def show_ic():
    global dat
    global buffer_ro1
    global ic_page
    global ic_cursor
    global mid_width

    txt = ""
    txt_desc = ""
    idx = WINDOW_IC_HEIGHT * ic_page + ic_cursor
    
    # show item
    if dat['sys']['ic'] == ITEM:
        item_having = []
        for i in range(len(dat['stat']['items'])):
            if dat['stat']['items'][i] != 0:
                item_having.append(i)

        divisible = len(item_having) % WINDOW_IC_HEIGHT == 0

        # Case if: divisible
        # Case else: otherwise
        max_page_idx = len(item_having) // WINDOW_IC_HEIGHT - 1 if divisible \
            else len(item_having) // WINDOW_IC_HEIGHT
        ic_page = min(ic_page, max_page_idx)

        # Case if: last page (case if: divisible, case else: otherwise)
        # Case else: otherwise
        max_cursor_idx = len(item_having) % WINDOW_IC_HEIGHT - 1 if ic_page == max_page_idx and not divisible \
            else WINDOW_IC_HEIGHT - 1
        ic_cursor = min(ic_cursor, max_cursor_idx)

        txt += " [--ITEM--]  [  CONSUMABLE  ]\n"

        for j in range(max_cursor_idx+1):
            # selected
            if j == ic_cursor:
                selected = item_having[ic_page * WINDOW_IC_HEIGHT + j]
                txt += " -> %s [%d]\n" % (ITEM_INFO[item_having[ic_page * WINDOW_IC_HEIGHT + j]][0], dat['stat']['items'][item_having[j]])
            # non-selected
            else:
                txt += "    %s [%d]\n" % (ITEM_INFO[item_having[ic_page * WINDOW_IC_HEIGHT + j]][0], dat['stat']['items'][item_having[j]])

        # word wrap
        subtxt = " " + ITEM_INFO[selected][1]
        nww = len(subtxt) // mid_width
        if nww:
            for j in range(nww+1):
                txt_desc += subtxt[j * mid_width : min((j+1) * mid_width, len(subtxt))]
                if j != nww:
                    txt_desc += "\n"
        else:
            txt_desc += subtxt
        

    # show consumable
    else:
        txt += " [  ITEM  ]  [--CONSUMABLE--]\n"

    buffer_ro1.set_document(value=Document(txt), bypass_readonly=True)
    buffer_ro8.set_document(value=Document(txt_desc), bypass_readonly=True)
    buffer_ro1._set_cursor_position(0)
>>>>>>> c0c83ecdf151e718a290b1538e75a27eb3361c84

@kb_main.add('c-c')
def kb_main_ctrlC(event):
    global status
    global dat

    gamedate_save_data(dat)

    status = STATUS_EXIT_NORMAL
    event.app.exit()

@kb_main.add('f1')
def kb_main_test_1(e):
    increase_time(1)

@kb_main.add('f2')
def kb_main_test_2(e):
    increase_time(60)

@kb_main.add('a')
@kb_main.add('left')
def kb_left(event):
    global dat

    if system_movable:
        move(-1, 0)

@kb_main.add('d')
@kb_main.add('right')
def kb_right(event):
    global dat

    if system_movable:
        move(1, 0)

@kb_main.add('w')
@kb_main.add('up')
def kb_up(event):
    global dat

    if system_movable:
        move(0, -1)

@kb_main.add('s')
@kb_main.add('down')
def kb_down(event):
    global dat

    if system_movable:
        move(0, 1)

@kb_main.add('c-left')
def kb_left(event):
    global dat

    if system_movable:
        move(-2, 0)

# for test
@kb_main.add('c-right')
def kb_right(event):
    global dat

    if system_movable:
        move(2, 0)

@kb_main.add('c-up')
def kb_up(event):
    global dat

    if system_movable:
        move(0, -2)

@kb_main.add('c-down')
def kb_down(event):
    global dat

    if system_movable:
        move(0, 2)

@kb_main.add('pageup')
def kb_down(event):
    global buffer_ro4

    buffer_ro4.cursor_up()

@kb_main.add('pagedown')
def kb_down(event):
    global buffer_ro4

    buffer_ro4.cursor_down()

@kb_main.add('y')
def kb_y(e):
    global dialog_choice
    global tmp_NPC_data
    global dat
    global current_map


    if get_on_battle():
        return

    if dialog_choice == NPC_FIGHT:
        battle(tmp_NPC_data[NPC_BATTLE_CODE])

    elif dialog_choice == NPC_DOCTOR:
        cost = tmp_NPC_data[NPC_DOCTOR_COST] + int(dat['stat']['money'] * NPC_DOCTOR_COST_RATE)
        if dat['stat']['money'] >= cost:
            dat['stat']['money'] -= cost

            show_dialog(NPC_DOCTOR, tmp_NPC_data, NPC_DIALOG_DISCHARGE)
            update_char_info()
            teleport(tmp_NPC_data[NPC_DOCTOR_POS][0], tmp_NPC_data[NPC_DOCTOR_POS][1], lazy_log=True)
        else:
            prison()
            game_log.append("[INFO] You are not have enough money... go to jail.")

            show_log()

@kb_main.add('n')
def kb_n(e):
    global dialog_choice
    global tmp_NPC_data

    if get_on_battle():
        return

    if dialog_choice == NPC_FIGHT:
        show_dialog(NPC_FIGHT, tmp_NPC_data, NPC_DIALOG_REFUSE_FIGHT)

# on_battle: attack
@kb_main.add('q')
def kb_q(e):
    global tmp_battle_data
    global tmp_battle_curhp
    global dat
    global on_battle

    if on_battle:
        battle_cmd(BATTLE_CMD_ATTACK)

<<<<<<< HEAD
=======
@kb_main.add('tab')
def kb_tab(e):
    global ic_page
    global dat

    ic_page = 0
    dat['sys']['ic'] = not dat['sys']['ic']
    show_ic()
>>>>>>> c0c83ecdf151e718a290b1538e75a27eb3361c84

# decrease ic cursor (and possibly ic page)
@kb_main.add('home')
def kb_home(e):
    global ic_page
    global ic_cursor

    if ic_cursor == 0:
        if ic_page == 0:
            show_ic()
        else:
            ic_page -= 1
            ic_cursor = WINDOW_IC_HEIGHT - 1
            show_ic()
    else:
        ic_cursor -= 1
        show_ic()

# increase ic cursor (and possibly ic page)
@kb_main.add('end')
def kb_home(e):
    global ic_page
    global ic_cursor

    ic_cursor += 1
    if ic_cursor == WINDOW_IC_HEIGHT:
        ic_page += 1
        ic_cursor = 0
        show_ic()
    else:
        show_ic()


@kb_main.add('e')
@kb_main.add('r')
@kb_main.add('1')
@kb_main.add('2')
@kb_main.add('3')
@kb_main.add('4')
def a(a):
    return

@kb_main.add('space')
def kb_space(e):
    global tmp_NPC_data
    global current_map
    global turn
    global dat
    global dialog_choice
    global game_log
    global goto_jail

    # after battle
    if get_on_battle() and get_battle_finished():
        
        increase_time(GAMESYS_TURN_TIME_PASS_A * turn + GAMESYS_TURN_TIME_PASS_B)

        if get_battle_finished() == BATTLE_LOSE:
            game_log.append("[INFO] You were hospitalized.")

            # additional time passage after die
            tpass = int(GAMESYS_DIE_TIME_PASS_BASE * 
                        (random.randint(100-GAMESYS_DIE_TIME_PASS_DEV, 
                                        100+GAMESYS_DIE_TIME_PASS_DEV) / 100) * 
                        (1 - dat['stat']['stamina'] / GAMESYS_DIE_TIME_PASS_MAX_STA))

            # recover hp
            dat['stat']['hp'] = int(dat['stat']['maxhp'] * GAMESYS_REVIVE_HP_PERCENT / 100)
            teleport(current_map[META][MAP_META_REV_X], 
                     current_map[META][MAP_META_REV_Y],
                     tpass)
            
        else:
            if goto_jail:
                goto_jail = 0
                prison()
                
                game_log.append("[INFO] You were imprisoned for assault.")
                show_log()
            else:
                show_dialog(NPC_FIGHT, tmp_NPC_data, NPC_DIALOG_LOSE)

        set_battle_finished(0)
        set_on_battle(0)
        set_system_movable(1)
        show_hp()

        # prevent immediately re-fight or refuse
        dialog_choice = -1

# todo: hash these names 
def special_mode():
    global dat
    global game_log
    global current_map

    # todo: mode starts arbit pos, map

    myname = dat['name']
    if myname == "RICH":
        dat['stat']['money'] = 10000000
        game_log.append("[INFO] Cheat enabled. You are rich!")

    elif myname == "STRONG":
        hp_val = 596
        str_val = 19

        dat['stat']['maxhp'] = hp_val
        dat['stat']['hp'] = hp_val
        dat['stat']['str'] = str_val
        game_log.append("[INFO] Cheat enabled. so strong~")
<<<<<<< HEAD
    
=======

    elif myname == "ITEMTEST":
        dat['stat']['items'] = [1,2,3,4,1,1,1,12,13]
        game_log.append("[INFO] Cheat enabled. I have many items~")

>>>>>>> c0c83ecdf151e718a290b1538e75a27eb3361c84
# main routine for main
def app_main():
    # buffer info
    # ro1: 
    # ro2: lower info
    # ro3: lower-left  (map info / NPC info)
    # ro4: lower-right (log / dialog)
    # ro5: map
    # ro6: upper-left (clock, character info)
    # ro7: hp 
    # ro8: item/consumable description

    global status
    global dat
    global current_map
    global buffer_ro1
    global buffer_ro2
    global buffer_ro7
    global game_log


    buffer_ro1.set_document(value=Document(), bypass_readonly=True)
    dat = gamedata_load_data()
    game_log.append("[INFO] Welcome, %s!" % dat['name'])

    special_mode()
    update_t_size()
    load_map()
    update_char_info() 
    set_system_movable(1)
    
    
    show_hp()
    show_log()

    # upper-side
    main_subcontainer_upper = VSplit([
        Window(content=BufferControl(buffer=buffer_ro6), 
                width=WINDOW_UPPER_LEFT_WIDTH),
        HSplit([
<<<<<<< HEAD
            Window(),     
=======
            Window(content=BufferControl(buffer=buffer_ro1)),   
            Window(content=BufferControl(buffer=buffer_ro8), height=2),     
>>>>>>> c0c83ecdf151e718a290b1538e75a27eb3361c84
            Window(content=BufferControl(buffer=buffer_ro7), height=1),
        ], height=WINDOW_UPPER_HEIGHT, padding=1, padding_char=PADDING_HORIZONTAL)
    ], padding=1, padding_char=PADDING_VERTICAL)

    # lower-side
    main_subcontainer_lower = VSplit([
        Window(content=BufferControl(buffer=buffer_ro3), 
                width=WINDOW_LOWER_LEFT_WIDTH),
        Window(content=BufferControl(buffer=buffer_ro4)),
    ], padding=1, padding_char=PADDING_VERTICAL, height=12)

    
    main_container = HSplit([
        Window(height=0),
        VSplit([
            Window(width=0),
            HSplit([
                main_subcontainer_upper,
                Window(content=BufferControl(buffer_ro5), 
                        #height=MAP_DISPLAY_HEIGHT, 
                        align=WindowAlign.CENTER),
                main_subcontainer_lower,   
                Window(content=BufferControl(buffer=buffer_ro2), 
                        height=1),
            ], padding=1, padding_char=PADDING_HORIZONTAL),
            Window(width=0),
        ], padding=1, padding_char=PADDING_VERTICAL),
        Window(height=0),
    ], padding=1, padding_char=PADDING_HORIZONTAL)

    main_layout = Layout(main_container, 
                         focused_element=buffer_ro4) # 4 by default
    current_app = Application(layout=main_layout,
                            full_screen=True,
                            key_bindings=kb_main)
    current_app.run()

# main routine
def main():
    # TODO: wait until terminal size exceeds minimal
    
    while 1:
        if status == STATUS_TITLE:
            app_title()
        elif status == STATUS_CREATE:
            app_create()    
        elif status == STATUS_MAIN:
            app_main()
        elif status == STATUS_EXIT_NORMAL:
            return 0
        elif status == STATUS_EXIT_ABNORMAL:
            return 1                
    

if __name__ == "__main__":
    map_generator()
    exit(main())
