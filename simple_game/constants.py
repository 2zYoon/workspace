# several constants


#########
#  MAP  #
#########
MAP = 0
META = 1

MAP_PATH = "./map/"
MAP_NAME_PREFIX = "map"
MAP_META_NAME_PREFIX = "meta"

MAP_META_CODE = 0
MAP_META_REGION = 1
MAP_META_AREA = 2
MAP_META_MAPSIZE = 3
MAP_META_REV_X = 4
MAP_META_REV_Y = 5
MAP_META_RET_X = 6
MAP_META_RET_Y = 7

MAP_SIZE_TINY = (11, 11)
MAP_SIZE_SMALL = (21, 21)
MAP_SIZE_MEDIUM = (101, 101)
MAP_SIZE_LARGE = (1001, 1001)

# only wall and empty forces not to move.
# in other blocks, there's no assumption.
MAP_BLOCK_CHARACTER = "@"
MAP_BLOCK_CHARS = " | OO?N.O#&"
MAP_GROUND = 0 
MAP_WALL = 1  
MAP_EMPTY = 2
MAP_PORTAL = 3
MAP_LOCAL_PORTAL = 4
MAP_MSG_HELP = 5
MAP_NPC = 6
MAP_GROUND_DOT = 7
MAP_RETURN = 8
MAP_CHECK_GATE = 9
MAP_COST_GATE = 10


################
#  CHECK GATE  #
################
# can pass only when the character meets some condition
# do not need to ask before pass
#
# condition type:
#  item: check if you are having a certain number of items 
#  consumable: check if you are having a certain number of consumables 
#  stat: check if you are having at least X stat(hp, str, etc.)
#  money: check if you are having enough money
#  battlewin: check if you have defeated someone at least X times
CHECK_GATE_ITEM = 0
CHECK_GATE_CONSUMABLE = 1
CHECK_GATE_STAT = 2
CHECK_GATE_MONEY = 3
CHECK_GATE_BATTLEWIN = 4


###############
#  COST GATE  #
###############
# can pass only when the character pays something
# ask before pass!
#
# cost type:
#  item: pay a certain number of items
#  consumable: pay a certain number of consumables
#  money: pay some money
#
# amount -1 : pay ALL
COST_GATE_ITEM = 0
COST_GATE_CONSUMABLE = 1
COST_GATE_MONEY = 2


############
#  PORTAL  #
############
# CAUTION: do not manually put portal into map (use map_set_portal() function)
# portal changes map, local portal only changes coordinates 
# both does nothing except moving character. (i.e., does not involve event)

# portal:
# (x, y) -> (new_mapcode, new_x, new_y)
PORTAL_INFO = [
   {  (10, 5):    (1, 7, 4),},
   {  (7, 3):     (0, 9, 5),},
   {},
   {},
   {},
]

# local-portal:
# (x, y) -> (new_x, new_y)
LOCAL_PORTAL_INFO = [
   # index: mapcode
   {},
   {  (31, 39):    (11, 11),
      (31, 33):   (9, 10)},
   {},
   {},
   {},
]

#######################
#  ITEM & CONSUMABLE  #
#######################
ITEM = 0
CONSUMABLE = 1

ITEM_NONE = -1
CONSUMABLE_NONE = -1

ITEM_NAME = 0
ITEM_DESC = 1

# item code
ITEM_GUIDEBOOK = 0
ITEM_TOILET_TISSUE = 1
ITEM_CALENDAR = 2
ITEM_SLIPPER = 3
ITEM_RUNNING_SHOES = 4
ITEM_AIRFORCE = 5
ITEM_CPU_I3_2 = 6
ITEM_CPU_I9_10 = 7
ITEM_CPU_THREADRIPPER = 8

# consumable code
# 0-4: reversed for quickslot
CONSUMEABLE_TYLENOL = 0
CONSUMEABLE_MORPHINE = 1



CONSUMEABLE_HONGSAM = 5

ITEM_INFO = [
   ["Guidebook", "Press [F1] to see guide. You can collect tips from \"?\" block."],
   ["Toilet tissue", "You can freely use toilet, wow!"],
   ["Calendar", "You can check elapsed days."],
   ["Slippers", "Reduces fatigue in your feet."],
   ["Running shoes", "Further reduces fatigue in your feet."],
   ["NIKE Air Force", "Extremely reduces fatigue in your feet."],
   ["Intel i3-2120", "An old-fashioned CPU. But it still works."],
   ["Intel i9-10900K", "An expensive and high performance CPU."],
   ["AMD Threadripper PRO 3999WX", "One of most expensive and powerful processor. ALL HAIL LISA SU!"]
]
CONSUMABLE_INFO = [
   ["Tylenol", "Acetaminophen. Recover 50 HP."],
   ["Morphine", "An effective painkiller. Recover 350 HP."],
   [],
   [],
   [],
   ["Hongsam", "a.k.a. Korean Ginseng. Get 1 STRENGTH Permanently"],
   
]


############
#  BATTLE  #
############
# indices
BATTLE_NAME = 0
BATTLE_CODE = 1
BATTLE_HP = 2
BATTLE_STR = 3
BATTLE_LUCK = 4
BATTLE_REWARD_INIT = 5
BATTLE_REWARD_REPEAT = 6
BATTLE_PRISON_PROB = 7

# commands
BATTLE_CMD_ATTACK = 0
BATTLE_CMD_QUIT = 1

# result
BATTLE_CONTINUE = 0
BATTLE_WIN = 1
BATTLE_LOSE = 2

# reward
BATTLE_REWARD_MONEY = 0
BATTLE_REWARD_COMMON_ITEM = 1
BATTLE_REWARD_COMMON_ITEM_NUMBER = 2
BATTLE_REWARD_COMMON_CONSUMABLE = 3
BATTLE_REWARD_COMMON_CONSUMABLE_NUMBER = 4
BATTLE_REWARD_RARE_ITEM = 5
BATTLE_REWARD_RARE_ITEM_PROB = 6
BATTLE_REWARD_RARE_CONSUMABLE = 7
BATTLE_REWARD_RARE_CONSUMABLE_PROB = 8

# idx = battle_code
# name, code, hp, str, luck, REWARD_init, REWARD_repeat, prison_prob
#     REWARD: [money, 
#              common_item_code(-1 for none),
#              common_item_numbers,
#              common_consumable_code(-1 for none),
#              common_consumable_numbers,
#              special_item_code(-1 for none),
#              special_item_prob(0-1),
#              special_consumable_code(-1 for none),
#              special_consumable_prob(0-1)]
BATTLE_INFO = [
   ["John Nace", 0,
      100, 25, 0,
      [1000, ITEM_TOILET_TISSUE, 1, CONSUMEABLE_HONGSAM, 1, ITEM_NONE, 0, CONSUMABLE_NONE, 0], 
      [100, ITEM_NONE, 0, CONSUMABLE_NONE, 0, ITEM_NONE, 0, CONSUMABLE_NONE, 0],
      0.02],
   
]

# some constants
# miss rate = 1 + 9 * CURRENT_LUCK/BATTLE_MAX_LUCK
BATTLE_MISS_RATE_BASE = 1
BATTLE_MISS_RATE_MAX_BONUS = 9
BATTLE_MAX_LUCK = 1000

# damage = STR * HP_percent * (100-DEV, 100+DEV)%
BATTLE_DAMAGE_DEV = 30

# battle turn delay (ms)
BATTLE_TURN_DELAY = 500


###########################
#  GAME SYSTEM CONSTANTS  #
###########################
# after revive, I have such a percent of HP
GAMESYS_REVIVE_HP_PERCENT = 10  

# time passage after battle: A(turn) + B
GAMESYS_TURN_TIME_PASS_A = 3
GAMESYS_TURN_TIME_PASS_B = 10

# time passage after die: base * (100-DEV, 100+DEV)% * (1-STA/MAX_STA)
GAMESYS_DIE_TIME_PASS_BASE = 180
GAMESYS_DIE_TIME_PASS_MAX_STA = 1000
GAMESYS_DIE_TIME_PASS_DEV = 50

#########
#  NPC  #
#########
# use map_set_NPC() function
#
# NPC Info list length varies, but ensured that at least 2 item exist
# length depends on NPC TYPE
# (x, y) -> [NPC TYPE, SYMBOL(char), ...]

# simply say something, without any action / interaction
# [code, name, dialog]
NPC_SIMPLE = 0

# sells something
# stock is saved in environment
# [code, name, dialog, [item_code, ...] ]
NPC_SHOP = 1

# wanna fight (yes or no)
# [code, name, dialog, yes_saying, no_saying, no_reply, lose_saying, battle_code]
NPC_FIGHT = 2

# after revive, requires money
# if don't have, go to jail
# [code, name, dialog, thank, local_position, cost_base]
# cost: base + money * rate
NPC_DOCTOR = 3
NPC_DOCTOR_COST_RATE = 0.35


# indices
# common
NPC_CODE = 0
NPC_NAME = 1
NPC_DIALOG = 2

# fight
NPC_YES_CHOICE = 3
NPC_NO_CHOICE = 4
NPC_REFUSE_REPLY = 5
NPC_LOSE_SAYING = 6
NPC_BATTLE_CODE = 7

# doctor
NPC_DOCTOR_THANK = 3
NPC_DOCTOR_POS = 4
NPC_DOCTOR_COST = 5

NPCS = [
   # index: mapcode
   # 0
   {},
   # 1
   {
      (8, 9): [NPC_SIMPLE, 
               "Guide Kim",
               "Hi, I am a guide, but there's nothing to guide for you. Get information by yourself."],
      (13, 3): [NPC_SIMPLE,
               "Drunken boy",
               "Zzzz..."],
      (15, 5): [NPC_SIMPLE,
               "Drunken child",
               "Umm...I love..spaghetti....mmm..."],
      (12, 1): [NPC_FIGHT,
               "John Nace",
               "Why are you fucking looking at me? Wanna lose your life?",
               "Come on, yo",
               "S..Sorry",
               "Then get off right now.",
               "Uggh....fuck...",
               0],
      (34, 9): [NPC_DOCTOR,
               "Dr. ME",
               "I hate apple...",
               "Thanks, take care.",
               (34, 11),
               4500],
      (56, 2): [NPC_SIMPLE, 
               "Karen the nurse",
               "Where is my apple? It was my breakfast..."],
      (57, 7): [NPC_SIMPLE, 
               "Kwame",
               "I lost my leg 17 years ago. My wife's calf kick was too strong."],


   
   },
   # 2
   {},
]

# dialog modes
NPC_DIALOG_REFUSE_FIGHT = 1   # when refused to fight
NPC_DIALOG_LOSE = 2           # when you lose
NPC_DIALOG_DISCHARGE = 3      # when discharge (doc's thank you)



####################
#  INITIAL VALUES  #
####################

# gamedata - status
INIT_GAMEDATA_LEVEL = 1
INIT_GAMEDATA_HP = 100
INIT_GAMEDATA_STR = 10
INIT_GAMEDATA_INT = 10
INIT_GAMEDATA_CHARM = 10
INIT_GAMEDATA_LUCK = 0
INIT_GAMEDATA_MONEY = 1000 # 1221474836471
INIT_GAMEDATA_STAMINA = 10
INIT_GAMEDATA_MAP = 0
INIT_GAMEDATA_POS = [1, 1]
INIT_GAMEDATA_ITEMS = [0] * 50
INIT_GAMEDATA_CONSUMABLES = [0] * 50

# for safety, use < 31 bits
INIT_GAMEDATA_FLAG_CH = [0, 0, 0, 0, 0]




# gamedata - env
INIT_GAMEDATA_FLAG_ENV = [0, 0, 0, 0, 0]
INIT_GAMEDATA_SHOP_STOCKS = [0] * 50
INIT_GAMEDATA_BATTLE_WINS = [0] * 50 # idx: battlecode

############
#  LIMITS  #
############
MAX_NAME_LENGTH = 21


###########
#  NAMES  #
###########
NAME_GAMEDATA_FNAME = "SAVE.savedata"


############
#  STATUS  #
############
STATUS_TITLE = 1
STATUS_CREATE = 2
STATUS_MAIN = 3
STATUS_EXIT_NORMAL = 0
STATUS_EXIT_ABNORMAL = -1



###########
#  MODES  #
###########
MODE_LOWER_LOG = 0
MODE_LOWER_DIALOG = 1

MODE_SYSTEM_MOVABLE = 1
MODE_SYSTEM_NOT_MOVABLE = 0

#######################
#  VALUES FOR WINDOW  #
#######################
WINDOW_UPPER_LEFT_WIDTH = 25
WINDOW_LOWER_LEFT_WIDTH = 25
WINDOW_UPPER_HEIGHT = 11
WINDOW_LOWER_HEIGHT = 15
WINDOW_IC_HEIGHT = 6

#####################
#  TEXT FOR WINDOW  #
#####################
KEY_HELP_MOVEMODE = "[MOVE MODE] (←, →, ↑, ↓) Move   (Tab)  Item/Consumable switch  (Ctrl+C) Save and Exit"
KEY_HELP_BATTLEMODE = "[BATTLE MODE] (Q) Attack   (W) Quit"

PADDING_HORIZONTAL = "-"
PADDING_VERTICAL = "|"

CHAR_HP_EMPTY = "▯"
CHAR_HP_FILL = "▮"

# -----------------------
# | [WED]     Day 00000 | 
# |  __  __     __  __  |
# | |__||__| · |__||__| |
# | |__||__| · |__||__| |
# -----------------------
TEXT_SMTWTFS = ['SUN', 'MON', 'TUE', 'WED', 'THU', 'FRI', 'SAT']
TEXT_CLOCKS = '''\
 __  __  __      __      __  __      __
|__||__|   ||__ |__ |__| __| __|   ||  |
   ||__|   ||__| __|   | __||__    ||__|'''


TEXT_LOWER_INFOS = [
" Welcome",
" HI!"]

TEXT_CREATE_NAME_UPPER = '''\
 -----------------------
 | What's your name?     |
 |                       |'''

TEXT_CREATE_NAME_LOWER = '''\
 |                       |
 |             [-ENTER-] |
 -----------------------'''


TEXT_CREATE_MSG_DEFAULT = "-> Use 4-18 chracters only with alphabet and whitespace."
TEXT_CREATE_MSG_GOOD =    "-> You can use this name.                               "


TEXT_NO_SAVE_DATA = '''\
 ------------------------------
|  / \\                         |
| / ! \\ No saved data found.   |
| -----                        |
|            [-OK-]            |
 ------------------------------'''

TEXT_MAY_OVERWRITE_SAVE_DATA_OK='''\
 ---------------------------------------------------------------
|  ---                                                          |
| | ? | Saved data already exists, are you sure to overwrite?   |
|  ---                                                          |
|                       [-OK-] [ CANCEL ]                       |
 ---------------------------------------------------------------'''

TEXT_MAY_OVERWRITE_SAVE_DATA_CANCEL='''\
 ---------------------------------------------------------------
|  ---                                                          |
| | ? | Saved data already exists, are you sure to overwrite?   |
|  ---                                                          |
|                       [ OK ] [-CANCEL-]                       |
 ---------------------------------------------------------------'''

TEXT_NEW_GAME_SELECTED = '''\
---- ----------------
| -> | NEW GAME       |
---- ----------------
|    | LOAD GAME      |
---- ----------------
|    | EXIT           |
---- ----------------'''

TEXT_LOAD_GAME_SELECTED = '''\
---- ----------------
|    | NEW GAME       |
---- ----------------
| -> | LOAD GAME      |
---- ----------------
|    | EXIT           |
---- ----------------'''

TEXT_EXIT_SELECTED = '''\
---- ----------------
|    | NEW GAME       |
---- ----------------
|    | LOAD GAME      |
---- ----------------
| -> | EXIT           |
---- ----------------'''

TEXT_TITLE = '''\
                                                                                 
                                                                                 
         tttt         RRRRRRRRRRRRRRRRR  PPPPPPPPPPPPPPPPP          GGGGGGGGGGGGG
      ttt:::t         R::::::::::::::::R P::::::::::::::::P      GGG::::::::::::G
      t:::::t         R::::::RRRRRR:::::RP::::::PPPPPP:::::P   GG:::::::::::::::G
      t:::::t         RR:::::R     R:::::PP:::::P     P:::::P G:::::GGGGGGGG::::G
ttttttt:::::ttttttt     R::::R     R:::::R P::::P     P:::::PG:::::G       GGGGGG
t:::::::::::::::::t     R::::R     R:::::R P::::P     P:::::G:::::G              
t:::::::::::::::::t     R::::RRRRRR:::::R  P::::PPPPPP:::::PG:::::G              
tttttt:::::::tttttt     R:::::::::::::RR   P:::::::::::::PP G:::::G    GGGGGGGGGG
      t:::::t           R::::RRRRRR:::::R  P::::PPPPPPPPP   G:::::G    G::::::::G
      t:::::t           R::::R     R:::::R P::::P           G:::::G    GGGGG::::G
      t:::::t           R::::R     R:::::R P::::P           G:::::G        G::::G
      t:::::t    tttttt R::::R     R:::::R P::::P            G:::::G       G::::G
      t::::::tttt:::::RR:::::R     R:::::PP::::::PP           G:::::GGGGGGGG::::G
      tt::::::::::::::R::::::R     R:::::P::::::::P            GG:::::::::::::::G
        tt:::::::::::tR::::::R     R:::::P::::::::P              GGG::::::GGG:::G
          ttttttttttt RRRRRRRR     RRRRRRPPPPPPPPPP                 GGGGGG   GG'''