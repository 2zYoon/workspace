from init import *

mode = MODE_TITLE
mode_resv = MODE_TITLE

ingame_choices = []
ingame_scene = 1

dialog = ENABLED
menu = DISABLED
bg = 1
alpha_fade = 0
alpha_bg_fade = 0
fade = FADE_DISABLED
speaker = ""

def main():
    global mode
    global bg
    global alpha_fade, alpha_bg_fade
    global fade
    global mode_resv
    global ingame_choices, ingame_scene
    global speaker
    global dialog

    while True:
        mpos = pygame.mouse.get_pos()

        # SCREEN 
        screen.blit(IMG_BG(bg), RECT_GAMESCREEN)
        surf_alpha.fill((0, 0, 0, 0))
        surf_fade.fill((0, 0, 0, alpha_fade))
        
        # SCRIPT LOAD
        cur_script = SCRIPT[str(ingame_scene)]
        ingame_choices = cur_script.get("choice", list())

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

            bg_tmp = cur_script.get("bg", bg)

            # background fade in 
            if bg != bg_tmp and cur_script.get("bg-fadein", 1):
                if alpha_bg_fade == 0:
                    alpha_bg_fade = 5
                surf_alpha.blit(IMG_BG(bg_tmp, alpha=alpha_bg_fade), RECT_GAMESCREEN)
            else:
                bg = bg_tmp
            
            # dialog
            dialog = cur_script.get("dialog", dialog)
            if dialog == ENABLED or dialog == ENABLED_TEMPORARY:
                for i in range(200):
                    pygame.draw.line(surf_alpha, (255, 255, 255, 200-i), (0, 600-i), (800, 600-i), 1)

                speaker = cur_script.get("speaker", speaker)

                if speaker != "none":
                    surf_alpha.blit(FONT("cafe24", 20, BLACK, speaker), (80, 490))

                surf_alpha.blit(FONT("malgun", 20, (0, 0, 0, 200), cur_script.get("text1", "")), (80, 470+50))
                surf_alpha.blit(FONT("malgun", 20, (0, 0, 0, 200), cur_script.get("text2", "")), (80, 495+50))

            # choice
            if len(ingame_choices) > 0:
                rects = RECT_CHOICE[len(ingame_choices) - 1]
                for i in range(len(ingame_choices)):
                    if isin(mpos, rects[i]):
                        pygame.draw.rect(surf_alpha, (255, 255, 255, 255), rects[i], 0, 3)
                    else:
                        pygame.draw.rect(surf_alpha, (255, 255, 255, 128), rects[i], 0, 3)
                    surf_alpha.blit(FONT("malgun", 20, (0, 0, 0, 255), ingame_choices[i]), (rects[i][0]+10, rects[i][1]+10))


        # EVENT HANDLER
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

            if e.type == pygame.MOUSEBUTTONDOWN and fade == FADE_DISABLED and alpha_bg_fade == 0:
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
                    if len(ingame_choices) == 0: 
                        if not isin(mpos, RECT_MENU):
                            ingame_scene = cur_script.get("next", [ingame_scene+1, ])[0]
                        else:
                            print("menu clicked")
                    else:
                        rects = RECT_CHOICE[len(ingame_choices) - 1]
                        for i in range(len(ingame_choices)):
                            if isin(mpos, rects[i]):
                                print("{} is chosen".format(i))
                                ingame_scene = cur_script.get("next", [ingame_scene+1])[i]
                        if isin(mpos, RECT_MENU):
                            print("menu clicked")


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

        # BG-FADE
        if alpha_bg_fade >= 5:
            alpha_bg_fade += 2
        if alpha_bg_fade >= 250:
            alpha_bg_fade = 0
            bg = bg_tmp


        # SCREEN
        screen.blit(surf_alpha, (0, 0))
        screen.blit(surf_fade, (0, 0))
        pygame.display.update()
        clock.tick(TIMER_TICK)


if __name__ == "__main__":
    main()