import pygame as pg
import sys

from game_board import GameBoard


pg.init()

# Tamanho Window
WIDTH, HEIGHT = 800, 600
screen = pg.display.set_mode((WIDTH, HEIGHT))

# Text Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

font = pg.font.SysFont('Arial', 36)



menu_possibilities = ["1. A M A D O", "2. Discovery", "3. Concept", "4. Quit"]
option_surfaces = []
option_positions = []

# Display do menu
for i,choice in enumerate(menu_possibilities):
    text_surface = font.render(choice, True, YELLOW)
    text_position = (WIDTH // 2 - text_surface.get_width() // 2, 200 + i * 50)
    option_surfaces.append(text_surface)
    option_positions.append(text_position)


concept_image = pg.image.load("images/concept.png")
concept_image = pg.transform.scale(concept_image, (WIDTH, HEIGHT))

intro_image = pg.image.load("images/intro.png")
intro_image = pg.transform.scale(intro_image,(WIDTH,HEIGHT))

continue_text = font.render("Press any key to continue", True, YELLOW)
continue_text_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT - 200))

INTRO = 0
MENU = 1
PLAYING = 2
CONCEPT_DISPLAY = 3
state = INTRO


# Create a GameBoard instance
grid_size = 4  # You can adjust the grid size as needed
game_board = GameBoard(WIDTH, HEIGHT, grid_size)

def handle_events():
    global state
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if state == INTRO:
                state = MENU
            elif state == MENU:
                if event.key == pg.K_1:
                    state = PLAYING
                    game_board.start_timer()

                elif event.key == pg.K_2:
                    print("Launching Discovery...") #debug
                    #Ainda estou a pensar se vale a pena na verdade incluir este step so se for mais numa de 
                    #Board testing
                    
                elif event.key == pg.K_3:
                    print("Exploring Concept...") #debug
                    state = CONCEPT_DISPLAY
                elif event.key == pg.K_4:
                    pg.quit()
                    sys.exit()
            elif state == CONCEPT_DISPLAY:
                state = MENU
            elif state == PLAYING:
                if event.key == pg.K_ESCAPE:
                    state = MENU 


while True:
    handle_events()  # Handle events such as key presses

    screen.fill(BLACK)  # Clear the screen
    if state == INTRO:
        screen.blit(intro_image, (0, 0))
        screen.blit(continue_text, continue_text_rect)
    elif state == MENU:
        for surface, position in zip(option_surfaces, option_positions):
            screen.blit(surface, position)
    elif state == CONCEPT_DISPLAY:
        screen.blit(concept_image, (0, 0))
    elif state == PLAYING:
        game_board.render(screen,grid_size)
        game_board.render_end_grid(screen)
        game_board.render_move_counter(screen)
        game_board.render_clock(screen)

    pg.display.flip()