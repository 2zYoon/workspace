# gamedata management
import os.path
import json
import pprint
from constants import *

# print gamedata (only for test)
def gamedata_print_data():
    with open(NAME_GAMEDATA_FNAME, 'r') as json_file:
        data = json.load(json_file)
        data_loaded = json.loads(data)
        pprint.pprint(data_loaded)

# load saved gamedata and return as dictionary
def gamedata_load_data():
    with open(NAME_GAMEDATA_FNAME, 'r') as json_file:
        data = json.load(json_file)
        data_loaded = json.loads(data)
        return data_loaded

# save current gamedata
def gamedate_save_data(data):
    JSON = json.dumps(data)

    with open(NAME_GAMEDATA_FNAME, "w") as json_file:
        json.dump(JSON, json_file)

# initialize gamedata
def gamedata_init_data(name):
    data = dict()

    # character name
    data['name'] = name
    
    # chatacter status
    stat = dict()
    stat['hp'] = INIT_GAMEDATA_HP
    stat['maxhp'] = INIT_GAMEDATA_HP

    stat['str'] = INIT_GAMEDATA_STR
    
    stat['int'] = INIT_GAMEDATA_INT

    stat['luck'] = INIT_GAMEDATA_LUCK

    stat['charm'] = INIT_GAMEDATA_CHARM

    stat['stamina'] = INIT_GAMEDATA_STAMINA

    stat['flags_ch'] = INIT_GAMEDATA_FLAG_CH
    stat['pos'] = INIT_GAMEDATA_POS
    stat['map'] = 1 # INIT_GAMEDATA_MAP
    
    stat['items'] = INIT_GAMEDATA_ITEMS
    stat['consumables'] = INIT_GAMEDATA_CONSUMABLES
    stat['money'] = INIT_GAMEDATA_MONEY
    stat['step'] = 0
    stat['returnmap'] = 0
    stat['prison'] = 0

    data['stat'] = stat

    # environment
    env = dict()
    env['time'] = 0 # in minute
    env['flags_env'] = INIT_GAMEDATA_FLAG_ENV
    env['stock'] = INIT_GAMEDATA_SHOP_STOCKS
    env['battlewin'] = INIT_GAMEDATA_BATTLE_WINS

    data['env'] = env

    # system
    sys = dict()
    sys['ic'] = ITEM # item / consumable
    sys['item_startidx'] = 0
    sys['consumable_startidx'] = 0

    data['sys'] = sys


    JSON = json.dumps(data)

    with open(NAME_GAMEDATA_FNAME, "w") as json_file:
        json.dump(JSON, json_file)

# check existence
def gamedata_check():
    return os.path.exists(NAME_GAMEDATA_FNAME) \
        and os.path.isfile(NAME_GAMEDATA_FNAME)

# create empty savedata
# must be called before initialized
def gamedata_create():
    f_save = open(NAME_GAMEDATA_FNAME, 'a')
    f_save.close()
