# init: initializes system and sets constants

import pygame
import json

pygame.init()

MODE_TITLE = 0
MODE_GAME = 1
MODE_COLLECTION = 2

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

FADE_SPEED = 5

RECT_NEWGAME = (40, 520, 130, 30)
RECT_CONTINUE = (180, 520, 110, 30)
RECT_COLLECTION = (300, 520, 120, 30)
RECT_EXIT = (690, 520, 55, 30)
RECT_MENU = (750, 20, 30, 30)
RECT_BACK = (690, 520, 63, 30)
RECT_MSG = (20, 20, 150, 30)

RECT_MENUITEM_1 = (660, 51, 120, 30)
RECT_MENUITEM_2 = (660, 82, 120, 30)
RECT_MENUITEM_3 = (660, 113, 120, 30)

RECT_DIALOG = (0, 500, 800, 150)
RECT_SPEAKER_FACE = (10, 460, 144, 108)
RECT_SPEAKER = (10, 460, 144, 108)

CHOICE_WIDTH = 400
CHOICE_HEIGHT = 50

RECT_CHOICE = [
    [
        [200, 200, CHOICE_WIDTH, CHOICE_HEIGHT],
    ],
    [
        [200, 150, CHOICE_WIDTH, CHOICE_HEIGHT],
        [200, 250, CHOICE_WIDTH, CHOICE_HEIGHT]
    ],
    [
        [200, 125, CHOICE_WIDTH, CHOICE_HEIGHT],
        [200, 200, CHOICE_WIDTH, CHOICE_HEIGHT],
        [200, 275, CHOICE_WIDTH, CHOICE_HEIGHT],
    ]]

BLACK = (0, 0, 0)
GRAY = (127, 127, 127)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

DIR_IMAGE = "asset/image/"
DIR_FONT = "asset/font/"
DIR_SOUND = "asset/sound/"
DIR_BGM = "asset/bgm/"

TIMER_TICK = 60


screen = pygame.display.set_mode(SIZE_GAMESCREEN)
pygame.display.set_icon(pygame.image.load(DIR_IMAGE + 'etc/icon.png'))
pygame.display.set_caption("the salvaged")

surf_alpha = pygame.Surface((800, 600)).convert_alpha()
surf_alpha_2 = pygame.Surface((800, 600)).convert_alpha()
surf_fade = pygame.Surface((800, 600)).convert_alpha()


clock = pygame.time.Clock()

with open("asset/script.json", encoding="utf-8") as f:
    SCRIPT = json.load(f)

# use:
# screen.blit(IMG_BG(num), RECT_GAMESCREEN)
def IMG_BG(number, alpha=255):
    try:
        img = pygame.image.load(DIR_IMAGE + "bg/" + str(number) + ".png")
    except:
        img = pygame.image.load(DIR_IMAGE + "bg/" + str(number) + ".jpg")
    if alpha != 255:
        img.set_alpha(alpha)
        
    ret = pygame.transform.scale(img, SIZE_GAMESCREEN)
    return ret

def IMG_TITLE(number, alpha=255):
    try:
        img = pygame.image.load(DIR_IMAGE + "bg/title-{}.png".format(number))
    except:
        img = pygame.image.load(DIR_IMAGE + "bg/title-{}.jpg".format(number))

    if alpha != 255:
        img.set_alpha(alpha)
        
    ret = pygame.transform.scale(img, SIZE_GAMESCREEN)
    return ret

# use:
# screen.blit(FONT(...), (x, y))
def FONT(font, size, color, text):
    fonts = {
        "consolas": DIR_FONT + "consolas.ttf",
        "malgun": DIR_FONT + "malgun.ttf",
        "malgunB": DIR_FONT + "malgunbd.ttf",
        "cafe24": DIR_FONT + "Cafe24Ssurround.ttf"
    }
    
    return pygame.font.Font(fonts[font], size).render(text, True, color)

def IMG_CH(name, alpha=255):
    try:
        img = pygame.image.load(DIR_IMAGE + "ch/" + name + ".png").convert_alpha()
    except:
        img = pygame.image.load(DIR_IMAGE + "ch/" + name + ".jpg").convert_alpha()
    
    if alpha != 255:
        img.set_alpha(alpha)
    
    ret = pygame.transform.scale(img, (300, 600))
    return ret
    

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

def isin_or(pos, rects):
    ret = False
    for i in rects:
        ret = ret or isin(pos, i)
    
    return ret

# text: rendered text
# rect: (x,y,w,h)
def get_pos_center_aligned_text(text, rect):
    return ((rect[0] + rect[2] // 2) - text.get_width() // 2, 
            (rect[1] + rect[3] // 2) - text.get_height() // 2)
