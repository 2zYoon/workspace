import pygame

pygame.init()

#############
# CONSTANTS #
############# 
# mode: int
# mapcode: int
# rect: (x, y, w, h)
# size: (w, h)
# pos: (x, y)

MODE_TITLE = 0
MODE_GAME = 1
MODE_INGAME_MENU = 2

DISABLED = -1

SIZE_SCREEN = (800, 800)
SIZE_GAMESCREEN = (800, 600)
RECT_GAMESCREEN = (0, 0, 800, 600)
RECT_TERMINAL = (0, 600, 600, 200)
RECT_PROMPT = (0, 780, 600, 20)
RECT_TXT_PROMPT = (0, 785, 600, 12)
SIZE_ICON = (40, 40)

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

MAX_TERMINAL_LINES = 15

MAP_XP_VILLAGE = 0

RECT_START = (300, 650, 200, 50)

DIR_IMAGE = "asset/image/"
DIR_FONT = "asset/font/"
DIR_DATA = "data/"

PREFIX_TERMINAL = "player@game:"

TIMER_TICK = 60

DEF_SPEED = 11

##################
# PYGAME OBJECTS #
##################

IMGS_BG = [
    pygame.transform.scale(pygame.image.load(DIR_IMAGE + "map/xp_village.jpg"), SIZE_GAMESCREEN),
    None
]

IMG_PC = pygame.transform.scale(pygame.image.load(DIR_IMAGE + "icon/pc.png"), SIZE_ICON)


FONT_CONSOLAS_12 = pygame.font.Font(DIR_FONT + "consolas.ttf", 12)
FONT_CONSOLAS_20 = pygame.font.Font(DIR_FONT + "consolas.ttf", 20)
FONT_BASIC_40 = pygame.font.Font(DIR_FONT + "malgun.ttf", 40)
FONT_BOLD_40 = pygame.font.Font(DIR_FONT + "malgunbd.ttf", 40)


####################
# COMMON FUNCTIONS #
####################

# pos: (x,y)
# rect: (x,y,w,h)
def isin(pos, rect):
    return pos[0] >= rect[0] and \
            pos[1] >= rect[1] and \
            pos[0] <= rect[0] + rect[2] and \
            pos[1] <= rect[1] + rect[3]

# text: rendered text
# rect: (x,y,w,h)
def get_pos_center_aligned_text(text, rect):
    return ((rect[0] + rect[2] // 2) - text.get_width() // 2, 
            (rect[1] + rect[3] // 2) - text.get_height() // 2)

# string: str
def parse(string):
    return [i for i in string.split(' ') if i != '']

