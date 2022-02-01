from telnetlib import BM
from init import *

mode = MODE_TITLE
mode_resv = MODE_TITLE

# saved data
dat_score = dict()
dat_endings = dict()

ingame_choices = []
ingame_scene = 1

dialog = ENABLED
menu = DISABLED
bg = 1
bgm = "none"
alpha_fade = 0
alpha_bg_fade = 0
alpha_msg_fade = 0
speaker = ""

msg_msg_fade = ""

fade = FADE_DISABLED

def save():
    to_save = dict()
    to_save["scores"] = dat_score
    to_save["scene"] = ingame_scene
    to_save["endings"] = dat_endings
    to_save["bg"] = bg
    to_save["bgm"] = bgm
    to_save["speaker"] = speaker
    to_save["dialog"] = dialog
    
    with open("data.sav", "w") as f:
        json.dump(to_save, f, indent=4)

def save_onlyending():
    a = dict()
    with open("data.sav") as f:
        a = json.load(f)
    
    a["endings"] = dat_endings
    with open("data.sav", "w") as f:
        json.dump(a, f, indent=4)

def load_ingame():
    global dat_score
    global ingame_scene
    global bg
    global bgm
    global speaker
    global dialog

    with open("data.sav") as f:
        to_load = json.load(f)
        dat_score = to_load["scores"]
        ingame_scene = to_load["scene"]
        bg = to_load["bg"]
        bgm = to_load["bgm"]
        speaker = to_load["speaker"]
        dialog = to_load["dialog"]

def load_outgame():
    global dat_endings
    with open("data.sav") as f:
        to_load = json.load(f)
        dat_endings = to_load["endings"]

def change_bgm(bgm_new, fadeout=-1):
    global bgm
    if bgm_new == "pass":
        return

    if bgm_new == "none":
        if fadeout >= 0:
            pygame.mixer.music.fadeout(fadeout)
        else:
            pygame.mixer.music.pause()
    elif bgm_new == bgm:
        return
    else:
        try:
            pygame.mixer.music.load(DIR_BGM + "{}.mp3".format(bgm_new))
        except:
            pass
        pygame.mixer.music.play(-1)

def sound_effect(sound):
    if sound == "none":
        return

    try:
        pygame.mixer.Sound(DIR_SOUND + "{}.mp3".format(sound)).play()
    except:
        pygame.mixer.Sound(DIR_SOUND + "{}.wav".format(sound)).play()

def main():
    global mode
    global bg
    global alpha_fade, alpha_bg_fade, alpha_msg_fade
    global fade
    global mode_resv
    global ingame_choices, ingame_scene
    global speaker
    global dialog
    global menu
    global bgm
    global msg_msg_fade

    change_bgm("bensound-anewbeginning")
    load_outgame()

    while True:
        mpos = pygame.mouse.get_pos()

        # SCREEN 
        surf_alpha.fill((0, 0, 0, 0))
        surf_alpha_2.fill((0, 0, 0, 0))
        surf_fade.fill((0, 0, 0, alpha_fade))
        
        # SCRIPT LOAD
        cur_script = SCRIPT.get(str(ingame_scene), None)
        if cur_script == None:
            print("end of script")
            pygame.quit()
            quit()

        ingame_choices = cur_script.get("choice", list())

        if mode == MODE_TITLE:
            screen.blit(IMG_TITLE(1), RECT_GAMESCREEN)
            surf_alpha.blit(IMG_TITLE(2), RECT_GAMESCREEN)

            # button highlight
            if isin(mpos, RECT_NEWGAME):
                pygame.draw.rect(surf_alpha, BLACK, RECT_NEWGAME, 0, 3)
                surf_alpha_2.blit(FONT("malgun", 22, WHITE, "New Game"), (50, 520))
            else:
                pygame.draw.rect(surf_alpha, WHITE, RECT_NEWGAME, 0, 3)
                surf_alpha_2.blit(FONT("malgun", 22, BLACK, "New Game"), (50, 520))


            if isin(mpos, RECT_CONTINUE):
                pygame.draw.rect(surf_alpha, BLACK, RECT_CONTINUE, 0, 3)
                surf_alpha_2.blit(FONT("malgun", 22, WHITE, "Continue"), (190, 520))
            else:
                pygame.draw.rect(surf_alpha, WHITE, RECT_CONTINUE, 0, 3)
                surf_alpha_2.blit(FONT("malgun", 22, BLACK, "Continue"), (190, 520))


            if isin(mpos, RECT_COLLECTION):
                pygame.draw.rect(surf_alpha, BLACK, RECT_COLLECTION, 0, 3)
                surf_alpha_2.blit(FONT("malgun", 22, WHITE, "Collection"), (310, 520))
            else:
                pygame.draw.rect(surf_alpha, WHITE, RECT_COLLECTION, 0, 3)
                surf_alpha_2.blit(FONT("malgun", 22, BLACK, "Collection"), (310, 520))

            if isin(mpos, RECT_EXIT):
                pygame.draw.rect(surf_alpha, BLACK, RECT_EXIT, 0, 3)
                surf_alpha_2.blit(FONT("malgun", 22, WHITE, "Exit"), (700, 520))
            else:
                pygame.draw.rect(surf_alpha, WHITE, RECT_EXIT, 0, 3)
                surf_alpha_2.blit(FONT("malgun", 22, BLACK, "Exit"), (700, 520))
                

            
            screen.blit(FONT("malgun", 44, (20, 20, 20), "the salvaged"), (40, 30))


        elif mode == MODE_GAME:
            screen.blit(IMG_BG(bg), RECT_GAMESCREEN)

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
            
            # character
            for i in range(1, 4):
                ch = cur_script.get("c{}".format(i), None)
                if ch != None:
                    surf_alpha.blit(IMG_CH(ch), (50+200*(i-1), 50))

                chb = cur_script.get("c{}b".format(i), None)
                if chb != None:
                    surf_alpha.blit(IMG_CH(chb, alpha=128), (50+200*(i-1), 75))

            # dialog
            dialog = cur_script.get("dialog", dialog)
            if dialog == ENABLED or dialog == ENABLED_TEMPORARY:
                rgba_dialog = cur_script.get("color", (0, 0, 0, 200))

                for i in range(200):
                    pygame.draw.line(surf_alpha_2, (255, 255, 255, 200-i), (0, 600-i), (800, 600-i), 1)

                speaker = cur_script.get("speaker", speaker)

                if speaker != "none":
                    surf_alpha_2.blit(FONT("cafe24", 20, BLACK, speaker), (80, 490))

                surf_alpha_2.blit(FONT("malgunB", 20, rgba_dialog, cur_script.get("text1", "")), (80, 470+50))
                surf_alpha_2.blit(FONT("malgunB", 20, rgba_dialog, cur_script.get("text2", "")), (80, 495+50))

            # choice
            if len(ingame_choices) > 0:
                rects = RECT_CHOICE[len(ingame_choices) - 1]
                for i in range(len(ingame_choices)):
                    if isin(mpos, rects[i]):
                        pygame.draw.rect(surf_alpha, (255, 255, 255, 255), rects[i], 0, 3)
                    else:
                        pygame.draw.rect(surf_alpha, (255, 255, 255, 128), rects[i], 0, 3)
                    surf_alpha_2.blit(FONT("malgunB", 20, (0, 0, 0, 255), ingame_choices[i]), (rects[i][0]+10, rects[i][1]+10))
            
            # menu
            if menu == ENABLED:
                alphas = [isin(mpos, RECT_MENUITEM_1), isin(mpos, RECT_MENUITEM_2), isin(mpos, RECT_MENUITEM_3)]
                pygame.draw.rect(surf_alpha_2, (255, 255, 255, [96, 192][alphas[0]]), RECT_MENUITEM_1, 0, 3)
                pygame.draw.rect(surf_alpha_2, (255, 255, 255, [96, 192][alphas[1]]), RECT_MENUITEM_2, 0, 3)
                pygame.draw.rect(surf_alpha_2, (255, 255, 255, [96, 192][alphas[2]]), RECT_MENUITEM_3, 0, 3)

                surf_alpha_2.blit(FONT("malgunB", 18, WHITE, "Save Game"), (670, 55))
                surf_alpha_2.blit(FONT("malgunB", 18, WHITE, "Load Game"), (670, 86))
                surf_alpha_2.blit(FONT("malgunB", 18, WHITE, "Go to title"), (670, 117))
            
            # bgm
            change_bgm(cur_script.get("bgm", "pass"))

            # msg
            if alpha_msg_fade >= 5:
                pygame.draw.rect(surf_alpha_2, (0, 0, 0, alpha_msg_fade), RECT_MSG, 0, 3)
                if msg_msg_fade == "Saved!":
                    surf_alpha_2.blit(FONT("malgunB", 20, WHITE, msg_msg_fade), (65, 22))
                else:
                    surf_alpha_2.blit(FONT("malgunB", 20, WHITE, msg_msg_fade), (58, 22))


        elif mode == MODE_COLLECTION:
            screen.blit(IMG_TITLE(1), RECT_GAMESCREEN)
            screen.blit(FONT("malgunB", 44, BLACK, "Collection"), (50, 30))
            surf_alpha.blit(IMG_TITLE(2), RECT_GAMESCREEN)

            for i in range(24):                
                ending = dat_endings.get("{}".format(i), ["0", "???", "???", "???", "", ""])
                if isin(mpos, (50+351*(i//12), 100+31*(i%12), 350, 30)):
                    pygame.draw.rect(surf_alpha, (0, 0, 0, 192), (50+351*(i//12), 100+31*(i%12), 350, 30), 0, 3)
                    
                    pygame.draw.rect(surf_alpha_2, (0, 0, 0, 255), (mpos[0], mpos[1], 200, 100), 0, 3)
                    surf_alpha_2.blit(FONT("malgunB", 18, WHITE, ending[2]), (mpos[0]+10, mpos[1]+10))
                    pygame.draw.line(surf_alpha_2, WHITE, (mpos[0]+10, mpos[1]+35), (mpos[0]+190, mpos[1]+35), 1)
                    surf_alpha_2.blit(FONT("malgunB", 12, WHITE, ending[3]), (mpos[0]+10, mpos[1]+40))
                    surf_alpha_2.blit(FONT("malgunB", 12, WHITE, ending[4]), (mpos[0]+10, mpos[1]+55))
                    surf_alpha_2.blit(FONT("malgunB", 12, WHITE, ending[5]), (mpos[0]+10, mpos[1]+70))

                else:
                    pygame.draw.rect(surf_alpha, (0, 0, 0, 128), (50+351*(i//12), 100+31*(i%12), 350, 30), 0, 3)
                
                surf_alpha.blit(FONT("malgunB", 18, WHITE, ending[1]), (55+351*(i//12), 102+31*(i%12)))

            if isin(mpos, RECT_BACK):
                pygame.draw.rect(surf_alpha, BLACK, RECT_BACK, 0, 3)
                surf_alpha_2.blit(FONT("malgun", 22, WHITE, "Back"), (700, 520))
            else:
                pygame.draw.rect(surf_alpha, WHITE, RECT_BACK, 0, 3)
                surf_alpha_2.blit(FONT("malgun", 22, BLACK, "Back"), (700, 520))


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
                        change_bgm("none", fadeout=1500)
                        sound_effect("beep-short")

                        ingame_choices = []
                        ingame_scene = 1

                        dialog = ENABLED
                        menu = DISABLED
                        bg = 1
                        bgm = "none"
                        alpha_fade = 0
                        alpha_bg_fade = 0
                        speaker = ""

                    elif isin(mpos, RECT_CONTINUE):
                        mode = MODE_GAME
                        sound_effect("beep-short")
                        load_ingame()
                        change_bgm("none", fadeout=1500)

                    elif isin(mpos, RECT_COLLECTION):
                        mode = MODE_COLLECTION
                        load_outgame()
                        sound_effect("beep-short")

                    elif isin(mpos, RECT_EXIT):
                        sound_effect("beep-short")
                        pygame.quit()
                        quit()

                elif mode == MODE_GAME:
                    if len(ingame_choices) == 0: 
                        escape = False
                        scene_changed = False

                        if isin(mpos, RECT_MENU):
                            menu = not menu
                            sound_effect("beep-short")

                        if cur_script.get("ending", None) != None:
                            dat_endings[str(cur_script["ending"][0])] = cur_script["ending"]
                            mode = MODE_TITLE
                            change_bgm("bensound-anewbeginning")
                            save_onlyending()
                            escape = True

                        if menu == ENABLED and not escape:
                            if not isin(mpos, RECT_MENU) and not isin_or(mpos, [RECT_MENUITEM_1, RECT_MENUITEM_2, RECT_MENUITEM_3]):
                                branch = cur_script.get("auto-branch", None)

                                if branch != None:
                                    if dat_score.get(branch[0], 0) >= branch[1]:
                                        ingame_scene = branch[2]
                                    else:
                                        ingame_scene = branch[3]
                                else:
                                    ingame_scene = cur_script.get("next", [ingame_scene+1, ])[0]
                                scene_changed = True

                            elif isin(mpos, RECT_MENUITEM_1):
                                save()
                                alpha_msg_fade = 255
                                msg_msg_fade = "Saved!"
                                sound_effect("beep-short")
                            elif isin(mpos, RECT_MENUITEM_2):
                                sound_effect("beep-short")
                                alpha_msg_fade = 255
                                msg_msg_fade = "Loaded!"
                                load_ingame()
                            elif isin(mpos, RECT_MENUITEM_3):
                                sound_effect("beep-short")
                                mode = MODE_TITLE
                                change_bgm("bensound-anewbeginning")


                        elif not escape:
                            if not isin(mpos, RECT_MENU):
                                branch = cur_script.get("auto-branch", None)
                                if branch != None:
                                    if dat_score.get(branch[0], 0) >= branch[1]:
                                        ingame_scene = branch[2]
                                    else:
                                        ingame_scene = branch[3]
                                else:
                                    ingame_scene = cur_script.get("next", [ingame_scene+1, ])[0]

                                scene_changed = True

                        if not escape and scene_changed:
                            script_tmp = SCRIPT.get(str(ingame_scene), None)
                            if script_tmp != None:
                                sound_effect(script_tmp.get("sound", "none"))


                    else:
                        rects = RECT_CHOICE[len(ingame_choices) - 1]
                        for i in range(len(ingame_choices)):
                            if isin(mpos, rects[i]):
                                scores = cur_script.get("score", None)
                                if scores != None:
                                    for k, v in scores.items():
                                        if dat_score.get(k, None) != None:
                                            dat_score[k] += v[i]
                                        else:
                                            dat_score[k] = v[i]

                                ingame_scene = cur_script.get("next", [ingame_scene+1])[i]
                        
                                script_tmp = SCRIPT.get(str(ingame_scene), None)
                                if script_tmp != None:
                                    sound_effect(script_tmp.get("sound", "none"))


                        if isin(mpos, RECT_MENU):
                            sound_effect("beep-short")
                            menu = not menu

                        if menu == ENABLED:
                            if isin(mpos, RECT_MENUITEM_1):
                                save()
                                alpha_msg_fade = 255
                                msg_msg_fade = "Saved!"
                                sound_effect("beep-short")
                            elif isin(mpos, RECT_MENUITEM_2):
                                alpha_msg_fade = 255
                                msg_msg_fade = "Loaded!"
                                load_ingame()
                                sound_effect("beep-short")
                            elif isin(mpos, RECT_MENUITEM_3):
                                mode = MODE_TITLE
                                sound_effect("beep-short")
                                change_bgm("bensound-anewbeginning")

                elif mode == MODE_COLLECTION:
                    if isin(mpos, RECT_BACK):
                        sound_effect("beep-short")
                        mode = MODE_TITLE

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
            alpha_bg_fade += 5
        if alpha_bg_fade >= 250:
            alpha_bg_fade = 0
            bg = bg_tmp

        # MESSAGE FADE
        if alpha_msg_fade >= 5:
            alpha_msg_fade -= 5

        # SCREEN
        screen.blit(surf_alpha, (0, 0))
        screen.blit(surf_alpha_2, (0, 0))
        screen.blit(surf_fade, (0, 0))
        pygame.display.update()
        clock.tick(TIMER_TICK)


if __name__ == "__main__":
    main()