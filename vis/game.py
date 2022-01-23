from init import *

mode = MODE_TITLE
mode_resv = MODE_TITLE

ingame_status = INGAME_NORMAL
ingame_scene = 1

dialog = ENABLED
menu = DISABLED
bg = 1
alpha_fade = 0
fade = FADE_DISABLED


def main():
    global mode
    global bg
    global alpha_fade
    global fade
    global mode_resv
    global ingame_status, ingame_scene

    while True:
        mpos = pygame.mouse.get_pos()

        # SCREEN 
        screen.blit(IMG_BG(bg), RECT_GAMESCREEN)
        surf_alpha.fill((0, 0, 0, 0))
        surf_fade.fill((0, 0, 0, alpha_fade))
        
        # SCRIPT LOAD
        cur_script = SCRIPT[str(ingame_scene)]
        ingame_status = bool(cur_script["choice"])

        if mode == MODE_TITLE:
            # button highlight
            if isin(mpos, RECT_NEWGAME):
                pygame.draw.rect(surf_alpha, (255, 255, 255, 96), RECT_NEWGAME, 0, 3)
            elif isin(mpos, RECT_CONTINUE):
                pygame.draw.rect(surf_alpha, (255, 255, 255, 96), RECT_CONTINUE, 0, 3)
            elif isin(mpos, RECT_EXIT):
                pygame.draw.rect(surf_alpha, (255, 255, 255, 96), RECT_EXIT, 0, 3)

            screen.blit(FONT("malgun", 22, WHITE, "New Game"), (50, 520))
            screen.blit(FONT("malgun", 22, WHITE, "Continue"), (200, 520))
            screen.blit(FONT("malgun", 22, WHITE, "Exit"), (700, 520))


        elif mode == MODE_GAME:
            # button highlight
            if isin(mpos, RECT_MENU):
                pygame.draw.rect(surf_alpha, (255, 255, 255, 192), RECT_MENU, 0, 3)
            else:
                pygame.draw.rect(surf_alpha, (255, 255, 255, 96), RECT_MENU, 0, 3)
            screen.blit(FONT("malgunB", 25, WHITE, "="), (756, 15))

            bg = cur_script["bg"]

            if dialog == ENABLED or dialog == ENABLED_TEMPORARY:
                pygame.draw.rect(surf_alpha, (255, 255, 255, 192), RECT_DIALOG)
                pygame.draw.line(surf_alpha, (255, 0, 0, 192), (0, 450), (800, 450), 3)
                pygame.draw.rect(surf_alpha, (255, 255, 255, 192), RECT_SPEAKER)

                surf_alpha.blit(FONT("malgun", 20, (0, 0, 0, 200), cur_script["text"]), (100, 500))

        # EVENT HANDLER
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

            if e.type == pygame.MOUSEBUTTONDOWN and fade == FADE_DISABLED:
                if mode == MODE_TITLE:
                    if isin(mpos, RECT_NEWGAME):
                        mode_resv = MODE_GAME
                        fade = FADE_OUT

                    elif isin(mpos, RECT_CONTINUE):
                        mode = MODE_GAME

                    elif isin(mpos, RECT_EXIT):
                        pygame.quit()
                        quit()

                if mode == MODE_GAME:
                    # normal
                    if ingame_status == INGAME_NORMAL: 
                        #TODO: exclude menu buttons 
                        if not isin(mpos, RECT_MENU):
                            ingame_scene = cur_script["next"]

        # FADE-IN / FADE-OUT          
        if fade == FADE_IN:
            if alpha_fade == 0:
                fade = FADE_DISABLED
            else:
                alpha_fade -= FADE_SPEED
        elif fade == FADE_OUT or fade == FADE_OUT_SKIP_IN:
            if alpha_fade == 255:
                if fade == FADE_OUT_SKIP_IN:
                    alpha_fade = 0
                    fade = FADE_DISABLED
                else:
                    fade = FADE_IN
                mode = mode_resv
            else:
                alpha_fade += FADE_SPEED

        # SCREEN
        screen.blit(surf_alpha, (0, 0))
        screen.blit(surf_fade, (0, 0))
        pygame.display.update()
        clock.tick(TIMER_TICK)


if __name__ == "__main__":
    main()