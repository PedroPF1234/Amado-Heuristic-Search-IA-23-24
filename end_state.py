import pygame as pg
import sys

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)


def render_end_screen(screen):
    screen.fill(BLACK)
    
    font = pg.font.SysFont('Arial', 30)
    end_message = font.render("Congratulations! You've won the game!", True, WHITE)
    screen.blit(end_message, (50, 100)) 
    

    instructions = font.render("Press 'M' to return to the main menu or 'Q' to quit", True, WHITE)
    screen.blit(instructions, (50, 200)) 


def handle_end_state_events(event):
    if event.type == pg.KEYDOWN:
        if event.key == pg.K_m: 
            return 'main_menu'
        elif event.key == pg.K_q: 
            pg.quit()
            sys.exit()

    return None  
