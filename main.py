import json

from pprint import pprint

from common import *


screen = pygame.display.set_mode(SIZE_SCREEN)
clock = pygame.time.Clock()

rect_ch = pygame.Rect(0, 0, SIZE_ICON[0], SIZE_ICON[1])
stat = dict()
fs = dict()
cur_dir = ["", ""]
log = ["",]


def cmd_cd(argv):
    if len(argv) == 1:
        return

    dest = argv[1]
    if dest == "..":
        if len(cur_dir) == 2:
            if cur_dir[-1] == "":
                return
            else:
                cur_dir[-1] = ""
                return
        else:
            cur_dir.pop()
    else:
        pass

def cmd_exit():
    global stat
    stat['exp'] += 1

    with open(DIR_DATA + "stat.json", "w") as f:
        json.dump(stat, f, indent=4)

    pygame.quit()
    quit()

def handler(argv):
    if len(argv) == 0:
        return 

    cmd = argv[0]
    if cmd not in stat['bin']: # TODO
       log.append("%s: command not found" % cmd)


    if cmd == "exit":
        cmd_exit()
    elif cmd == "ls":
        pass
    elif cmd == "man":
        pass
    elif cmd == "cat":
        pass

    elif cmd == "cd":
        cmd_cd(argv)

            


def main_init():
    global stat
    global fs

    with open(DIR_DATA + "stat.json") as f:
        stat = json.load(f)
        pprint(stat)
    
    with open(DIR_DATA + "fs.json") as f:
        fs = json.load(f)
        pprint(fs)



def main_menu():
    while True:
        screen.fill(BLACK)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

            if e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
                return MODE_GAME
        
            if e.type == pygame.MOUSEBUTTONDOWN:
                if isin(pygame.mouse.get_pos(), RECT_START):
                    return MODE_GAME
        
        if isin(pygame.mouse.get_pos(), RECT_START):
            pygame.draw.rect(screen, BLUE, RECT_START, 5)
            txt_start = FONT_BOLD_40.render("START", True, BLUE)

        else:
            pygame.draw.rect(screen, GREEN, RECT_START, 5)
            txt_start = FONT_BOLD_40.render("START", True, GREEN)

        screen.blit(txt_start, get_pos_center_aligned_text(txt_start, RECT_START))

        pygame.display.update()
        clock.tick(TIMER_TICK)

def main_game():
    global log

    delta = [0, 0]
    terminal_active = False
    img_bg = IMGS_BG[0]
    buffer = " "

    while True:
        # load map info
        # ...
        

        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, (0, 450), (800, 450), 1)
        pygame.draw.line(screen, WHITE, (400, 450), (400, 600), 1)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                cmd_exit()

            if e.type == pygame.KEYDOWN:
                # move
                if e.key == pygame.K_LEFT:
                    delta[0] -= DEF_SPEED
                if e.key == pygame.K_RIGHT:
                    delta[0] += DEF_SPEED
                if e.key == pygame.K_UP:
                    delta[1] -= DEF_SPEED
                if e.key == pygame.K_DOWN:
                    delta[1] += DEF_SPEED

                if terminal_active:
                    if e.key == pygame.K_BACKSPACE:
                        buffer = buffer[:-1] if buffer != " " else " "
                    elif e.key == pygame.K_RETURN:
                        if buffer != " ":
                            log.append(PREFIX_TERMINAL + "/" + buffer)
                            handler(parse(buffer))
                            buffer = ' '
                        else:
                            terminal_active = False
                    else:
                        buffer += e.unicode
                else:
                    if e.key == pygame.K_RETURN:
                        terminal_active = True


            if e.type == pygame.KEYUP:
                # move
                if e.key == pygame.K_LEFT:
                    delta[0] += DEF_SPEED
                if e.key == pygame.K_RIGHT:
                    delta[0] -= DEF_SPEED
                if e.key == pygame.K_UP:
                    delta[1] += DEF_SPEED
                if e.key == pygame.K_DOWN:
                    delta[1] -= DEF_SPEED
        
        if isin((rect_ch.x+delta[0], rect_ch.y+delta[1]), 
                 (0, 0, SIZE_GAMESCREEN[0]-SIZE_ICON[0], SIZE_GAMESCREEN[1]-SIZE_ICON[1])):
            rect_ch.move_ip(delta)

        # terminal
        for i in range(MAX_TERMINAL_LINES):
            txt_terminal = FONT_CONSOLAS_12.render(
                log[max(0, len(log) - MAX_TERMINAL_LINES + i)], True, WHITE)
            screen.blit(txt_terminal, (0, 600+12*i))
        
        # prompt
        txt_prompt = FONT_CONSOLAS_12.render(PREFIX_TERMINAL + "/" + "$" + buffer, True, WHITE)
        screen.blit(txt_prompt, RECT_TXT_PROMPT)

        # footer
        pygame.draw.rect(screen, WHITE, RECT_TERMINAL, 1)
        pygame.draw.rect(screen, WHITE if terminal_active else GRAY, RECT_PROMPT, 1)
        

        # background
        screen.blit(img_bg, RECT_GAMESCREEN)            
        
        # character
        screen.blit(IMG_PC, rect_ch)     

        pygame.display.update()
        clock.tick(TIMER_TICK)

def main():
    main_init()
    mode = MODE_TITLE

    while True:
        if mode == MODE_TITLE:
            mode = main_menu()
        elif mode == MODE_GAME:
            mode = main_game()
        elif mode == MODE_INGAME_MENU:
            break
        else:
            break

if __name__ == "__main__":
    main()
    