from init import *

mode = MODE_TITLE
mode_resv = MODE_TITLE

ingame_status = INGAME_NORMAL
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
    global ingame_status, ingame_scene
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
        ingame_status = bool(cur_script.get("choice", 0))

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
            
            dialog = cur_script.get("dialog", dialog)
            if dialog == ENABLED or dialog == ENABLED_TEMPORARY:
                pygame.draw.rect(surf_alpha, (255, 255, 255, 192), RECT_DIALOG)
                pygame.draw.line(surf_alpha, COLOR_UNIST_NAVY, (0, 450), (800, 450), 3)

                speaker = cur_script.get("speaker", speaker)

                if speaker != "none":
                    pygame.draw.rect(surf_alpha, BLACK, RECT_SPEAKER_FACE)
                    
                    # speaker length estimation
                    margin_speaker = 25 + (6 - len(speaker)) * 10 + (speaker.count(" ") * 5 + speaker.count("?") * 3)
                    surf_alpha.blit(FONT("cafe24", 20, BLACK, speaker), (margin_speaker, 570))


                surf_alpha.blit(FONT("malgun", 20, (0, 0, 0, 200), cur_script.get("text1", "")), (180, 470))
                surf_alpha.blit(FONT("malgun", 20, (0, 0, 0, 200), cur_script.get("text2", "")), (180, 495))
                surf_alpha.blit(FONT("malgun", 20, (0, 0, 0, 200), cur_script.get("text3", "")), (180, 520))
                surf_alpha.blit(FONT("malgun", 20, (0, 0, 0, 200), cur_script.get("text4", "")), (180, 545))

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
                    if ingame_status == INGAME_NORMAL: 
                        #TODO: exclude menu buttons 
                        if not isin(mpos, RECT_MENU):
                            ingame_scene = cur_script.get("next", ingame_scene+1)

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