from common import *


screen = pygame.display.set_mode(SIZE_SCREEN)
clock = pygame.time.Clock()

rect_ch = pygame.Rect(0, 0, SIZE_ICON[0], SIZE_ICON[1])

def main_init():
    pass

def main_menu():
    while True:
        screen.fill(BLACK)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()
        
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
    delta = [0, 0]
    terminal_active = False
    img_bg = IMGS_BG[0]

    while True:
        # load map info
        # ...
        

        screen.fill(BLACK)
        pygame.draw.line(screen, WHITE, (0, 450), (800, 450), 1)
        pygame.draw.line(screen, WHITE, (400, 450), (400, 600), 1)
        
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

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
            
                # terminal activation
                if terminal_active == False:
                    terminal_active = True
                else:
                    # submit the command
                    terminal_active = False # remove this, later


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
        
        rect_ch.move_ip(delta)

        # TODO: multiline text -> iteration
        txt_terminal = FONT_CONSOLAS_12.render("$ lsYMSDMD!@02012,f exit", True, WHITE)


        screen.blit(txt_terminal, RECT_TERMINAL)
        
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