import pygame as pg
import sys
import end_state
import time

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


size_possibilities = ["1. 4x4 Tiles Grid", "2. 6x6 Tiles Grid", "3. 8x8 Tiles Grid"]
size_option_surfaces = []
size_option_positions = []

for i,choice in enumerate(size_possibilities):
                text_surface = font.render(choice, True, YELLOW)
                text_position = (WIDTH // 2 - text_surface.get_width() // 2, 200 + i * 50)
                size_option_surfaces.append(text_surface)
                size_option_positions.append(text_position)

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
END_GAME = 4
SEARCH_PLAYING = 5
SELECT_SIZE = 6
state = INTRO
game_over = False


grid_size = 0
game_board = None

def handle_events():
    global state
    global grid_size
    global game_board
    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            if state == INTRO:
                state = MENU
            elif state == MENU:
                if event.key == pg.K_1:
                    state = SELECT_SIZE
                elif event.key == pg.K_2:
                    state = SEARCH_PLAYING
                    game_board = GameBoard(WIDTH, HEIGHT, 4)
                    game_board.reset_game_state()
                    initial_info = (0, 0, game_board.playablegrid, 0, None)
                    game_board.start_timer()
                    
                    print("\n\n\n")
                    print("Searching for solution...")
                    game_board.a_star_search(initial_info)
                    game_board.greedy_bfs_search(initial_info)
                    node = game_board.weighted_a_star_search(initial_info)
                    
                   # game_board.iterative_deepening_search(initial_info, 20)


                    game_board.counter = node[3]

                    state = END_GAME
                    game_board.stop_timer()
                    #else:
                        #print("No solution found")

                elif event.key == pg.K_3:
                    print("Exploring Concept...") #debug
                    state = CONCEPT_DISPLAY
                elif event.key == pg.K_4:
                    pg.quit()
                    sys.exit()
            elif state == SELECT_SIZE:
                if event.key == pg.K_1:
                    grid_size = 4
                    game_board = GameBoard(WIDTH, HEIGHT, grid_size)
                    state = PLAYING
                    game_board.reset_game_state()

                    game_board.start_timer()
                elif event.key == pg.K_2:
                    grid_size = 6
                    game_board = GameBoard(WIDTH, HEIGHT, grid_size)
                    state = PLAYING
                    game_board.reset_game_state()

                    game_board.start_timer()
                elif event.key == pg.K_3:
                    grid_size = 8
                    game_board = GameBoard(WIDTH, HEIGHT, grid_size)
                    state = PLAYING
                    game_board.reset_game_state()

                    game_board.start_timer()
            elif state == CONCEPT_DISPLAY:
                state = MENU
            elif state == PLAYING:
                if event.key == pg.K_ESCAPE:
                    state = MENU
                game_board.game_moves(event) 
                if game_board.end_condition_check():
                    state = END_GAME
                    game_board.stop_timer()

            elif state == SEARCH_PLAYING:
                if event.key == pg.K_ESCAPE:
                    state = MENU 


while True:
    if state == END_GAME:

        for event in pg.event.get():
        
            end_state_event_result = end_state.handle_end_state_events(event)
            if end_state_event_result == 'main_menu':
                state = MENU
            elif end_state_event_result == 'quit':
                pg.quit()
                sys.exit()
        end_state.render_end_screen(screen, game_board.counter, game_board.get_elapsed_time())
    else:
        handle_events()  
        screen.fill(BLACK)
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
            game_board.render_hint(screen)
        elif state == SELECT_SIZE:
            for surface, position in zip(size_option_surfaces, size_option_positions):
                    screen.blit(surface, position)
            
    pg.display.flip()
