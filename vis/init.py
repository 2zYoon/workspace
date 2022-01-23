# init: initializes system and sets constants

import pygame
import json

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
MODE_SAVE_INGAME = 2
MODE_SAVE_TITLE = 3

DISABLED = 0
ENABLED = 1
DISABLED_TEMPORARY = 2
ENABLED_TEMPORARY = 3

SIZE_GAMESCREEN = (800, 600) 
RECT_GAMESCREEN = (0, 0, 800, 600)

FADE_DISABLED = 0
FADE_IN = 1
FADE_OUT = 2
FADE_OUT_SKIP_IN = 3

INGAME_NORMAL = 0 
INGAME_CHOICE = 1

FADE_SPEED = 5

# rect for something
RECT_NEWGAME = (40, 520, 130, 30)
RECT_CONTINUE = (190, 520, 110, 30)
RECT_EXIT = (690, 520, 55, 30)
RECT_MENU = (750, 20, 30, 30)

RECT_DIALOG = (0, 450, 800, 150)
RECT_SPEAKER = (20, 430, 100, 40)

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DIR_IMAGE = "asset/image/"
DIR_FONT = "asset/font/"
DIR_DATA = "data/"

TIMER_TICK = 60

##############################
# PYGAME FUNCTIONS & GLOBALS #
##############################

screen = pygame.display.set_mode(SIZE_GAMESCREEN)
surf_alpha = pygame.Surface((800, 600)).convert_alpha()
surf_fade = pygame.Surface((800, 600)).convert_alpha()

clock = pygame.time.Clock()

with open("asset/script.json", encoding="utf-8") as f:
    SCRIPT = json.load(f)

# use:
# screen.blit(IMG_BG(num), RECT_GAMESCREEN)
def IMG_BG(number):
    try:
        ret = pygame.transform.scale(pygame.image.load(DIR_IMAGE + "bg/" + str(number) + ".png"), SIZE_GAMESCREEN)
    except:
        ret = pygame.transform.scale(pygame.image.load(DIR_IMAGE + "bg/" + str(number) + ".jpg"), SIZE_GAMESCREEN)
    return ret

# use:
# screen.blit(FONT(...), (x, y))
def FONT(font, size, color, text):
    fonts = {
        "consolas": DIR_FONT + "consolas.ttf",
        "malgun": DIR_FONT + "malgun.ttf",
        "malgunB": DIR_FONT + "malgunbd.ttf"
    }

    return pygame.font.Font(fonts[font], size).render(text, True, color)


    

#IMG_PC = pygame.transform.scale(pygame.image.load(DIR_IMAGE + "icon/pc.png"), SIZE_ICON)


FONT_CONSOLAS_12 = pygame.font.Font(DIR_FONT + "consolas.ttf", 12)
FONT_CONSOLAS_20 = pygame.font.Font(DIR_FONT + "consolas.ttf", 20)
FONT_BASIC_20 = pygame.font.Font(DIR_FONT + "malgun.ttf", 20)
FONT_BOLD_20 = pygame.font.Font(DIR_FONT + "malgunbd.ttf", 20)
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
