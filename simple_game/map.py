# map management
import numpy as np
import json
from constants import *

# Map metadata format:
# [region] [area] [map-size] [revive_x] [revive_y] [return_x] [return_y] 

def map_set_NPC(map_to_set):
    mapcode = map_to_set[META][MAP_META_CODE]

    for i in list(NPCS[mapcode]):
        map_to_set[MAP][i[1], i[0]] = MAP_NPC

# sets portal and local-portal
# @map_to_set: whole current mapdata (with map and meta)
def map_set_portal(map_to_set):
    for i in list(PORTAL_INFO[map_to_set[META][MAP_META_CODE]]):
        map_to_set[MAP][i[1], i[0]] = MAP_PORTAL

    for j in list(LOCAL_PORTAL_INFO[map_to_set[META][MAP_META_CODE]]):
        map_to_set[MAP][j[1], j[0]] = MAP_LOCAL_PORTAL


# returns map display
# @cols: map display columns
# @lines: map display lines
# @curmap: current map and metadata
# @xy: target xy-tuple
def map_display_string(cols, lines, curmap, xy):
    ret = ""
    x, y = xy
    cmap = curmap[MAP]
    mapsize = curmap[META][MAP_META_MAPSIZE]

    # center of display
    center = cols // 2, lines // 2  # x, y

    # spaces except center
    left = center[0]
    right = cols - (center[0] + 1)
    up = center[1]
    down = lines - (center[1] + 1)

    # is padding needed?
    padding_upper = max(center[1] - y, 0)
    padding_lower = max(lines - (center[1] + 1) - (mapsize - 1 - y) , 0)
    padding_left = max(center[0] - x, 0)
    padding_right = max(cols - (center[0] + 1) - (mapsize - 1 - x), 0)

    ret = ""
    line = 0

    start_idx = 0 if padding_left else x - left
    end_idx = start_idx + (cols - (padding_left + padding_right))

    for i in range(padding_upper):
        ret += MAP_BLOCK_CHARS[MAP_EMPTY] * cols + "\n"
        line += 1
    
    for j in range(lines - padding_upper - padding_lower):
        t = ""
        t += MAP_BLOCK_CHARS[MAP_EMPTY] * padding_left
        
        cur_y = j if padding_upper else y - up + j
        subarr = cmap[cur_y, start_idx:end_idx].copy()

        for ii in subarr:
            t += MAP_BLOCK_CHARS[ii]

        t += MAP_BLOCK_CHARS[MAP_EMPTY] * padding_right

        if padding_upper + j == center[1]:
            ret += t[:center[0]] + MAP_BLOCK_CHARACTER + t[center[0]+1:] + "\n"
        else:
            ret += t + "\n"
        line += 1
    
    for k in range(padding_lower):
        ret += MAP_BLOCK_CHARS[MAP_EMPTY] * cols + "\n"
        line += 1

    
    debug_msg = "%d %d %d %d | %d %d\n" % (
        padding_upper, padding_left, padding_lower, padding_right,
        start_idx, end_idx)
    debug_msg = "" # uncomment when I need

    return debug_msg + ret 


# performs boundary check
# @curmap: current map metadata
# @xy: target xy-tuple
# returns 1 if ok, 0 otherwise
def map_boundary_check(curmap, xy):
    mapsize = int(curmap[MAP_META_MAPSIZE])

    return 0 <= xy[0] < mapsize and 0 <= xy[1] < mapsize

def map_loader(map_number, do_print=False):
    map_dat = np.load(MAP_PATH + MAP_NAME_PREFIX + str(map_number) + ".npy")
    with open(MAP_PATH + MAP_META_NAME_PREFIX + str(map_number), 'r') as f:
        meta_dat = f.readlines()
        for i in range(len(meta_dat)):
            meta_dat[i] = meta_dat[i].strip()
            if i == MAP_META_CODE or i >= 3:
                meta_dat[i] = int(meta_dat[i])

        if do_print:
            print(meta_dat)
            print(map_dat)
        
        return [map_dat, meta_dat]


# not be called in game
def map_generator():
    maps = []


    # [0] start point
    map0 = np.ones(MAP_SIZE_TINY, dtype=np.uint8)
    map0_meta = [0, "???", "Start point", MAP_SIZE_TINY[0], 1, 1, 1, 1]
    maps.append([map0, map0_meta])

    map0[1:-1, 1:-1] = MAP_GROUND
    map0[:9, 2:5] = MAP_WALL
    map0[2:, 6:9] = MAP_WALL
    map0[:8, 3] = MAP_EMPTY
    map0[3:, 7] = MAP_EMPTY
    map0[7:, 7:] = MAP_EMPTY
    map0[6, 9] = MAP_WALL


    # [1] AKA Village
    map1 = np.ones(MAP_SIZE_MEDIUM, dtype=np.uint8)
    map1_meta = [1, "ABCD", "AKA Village", MAP_SIZE_MEDIUM[0], 57, 2, 7, 11]
    maps.append([map1, map1_meta])

    map1[1:-1, 1:-1] = MAP_GROUND

    # first home
    map1[2:11, 2:13] = MAP_WALL
    map1[3:10, 3:12] = MAP_GROUND
    map1[10, 7] = MAP_GROUND

    map1[2:11, 16:31] = MAP_WALL
    map1[3:10, 17:30] = MAP_GROUND
    map1[10, 23] = MAP_GROUND

    map1[:11, 33:60] = MAP_WALL
    map1[1:10, 35:58] = MAP_GROUND
    map1[3, 44:49] = MAP_WALL
    map1[2:5, 46] = MAP_WALL

    # [2] jail
    map2 = np.ones(MAP_SIZE_SMALL, dtype=np.uint8)
    map2_meta = [2, "Somewhere", "JAIL", MAP_SIZE_SMALL[0], 1, 1, 1, 1]
    maps.append([map2, map2_meta])

    map2[1:-1, 1:-1] = MAP_GROUND
    map2[20, 10] = MAP_RETURN

    map2[19, 9:12] = MAP_WALL









    # additional set / map save
    for i in range(len(maps)):
        # set portal
        map_set_portal(maps[i])

        # set npcs
        map_set_NPC(maps[i])

        # save map
        np.save(MAP_PATH + MAP_NAME_PREFIX + str(i), maps[i][0])

        # save metadata
        with open(MAP_PATH + MAP_META_NAME_PREFIX + str(i), 'w+') as f:
            for j in maps[i][1]:
                f.write(str(j)+"\n")



if __name__ == "__main__":
    map_generator()
    #map_loader(0, True)