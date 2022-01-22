import json

from init import *

mode = MODE_TITLE
dialog = ENABLED
bg = 1

def main():
    global mode 

    while True:
        # SCREEN - EARLY
        screen.blit(IMG_BG(bg), RECT_GAMESCREEN)
        surf_alpha.fill((0, 0, 0, 0))
        
        if mode == MODE_TITLE:
            # button highlight
            mpos = pygame.mouse.get_pos()
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
            if dialog == ENABLED or dialog == ENABLED_TEMPORARY:
                pygame.draw.rect(surf_alpha, (255, 255, 255, 192), (0, 450, 800, 150))
                pygame.draw.line(surf_alpha, (255, 0, 0, 192), (0, 450), (800, 450), 3)


        # EVENT HANDLER
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                quit()

            if e.type == pygame.MOUSEBUTTONDOWN:
                if mode == MODE_TITLE:
                    if isin(mpos, RECT_NEWGAME):
                        mode = MODE_GAME
                    elif isin(mpos, RECT_CONTINUE):
                        mode = MODE_GAME
                    elif isin(mpos, RECT_EXIT):
                        pygame.quit()
            


        screen.blit(surf_alpha, (0, 0))
        pygame.display.update()
        clock.tick(TIMER_TICK)


if __name__ == "__main__":
    main()