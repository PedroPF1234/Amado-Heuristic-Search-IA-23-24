import pygame
import sys


pygame.init()

# Tamanho Window
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))


# Text Colors
BLACK = (0, 0, 0)
YELLOW = (255, 255, 0)

font = pygame.font.SysFont('Arial', 36)



menu_possibilities = ["1. A M A D O", "2. Discovery", "3. Concept", "4. Quit"]
option_surfaces = []
option_positions = []

# Display do menu
for i,choice in enumerate(menu_possibilities):
    text_surface = font.render(choice, True, YELLOW)
    text_position = (WIDTH // 2 - text_surface.get_width() // 2, 200 + i * 50)
    option_surfaces.append(text_surface)
    option_positions.append(text_position)


concept_image = pygame.image.load("images/concept.png")
concept_image = pygame.transform.scale(concept_image, (WIDTH, HEIGHT))

intro_image = pygame.image.load("images/intro.png")
intro_image = pygame.transform.scale(intro_image,(WIDTH,HEIGHT))

continue_text = font.render("Press any key to continue", True, YELLOW)
continue_text_rect = continue_text.get_rect(center=(WIDTH // 2, HEIGHT - 200))

INTRO = 0
MENU = 1
CONCEPT_DISPLAY = 3
state = INTRO


def handle_events():
    global state
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if state == INTRO:
                state = MENU
            elif state == MENU:
                if event.key == pygame.K_1:
                    print("Starting Amado...") #debug
                elif event.key == pygame.K_2:
                    print("Launching Discovery...") #debug
                elif event.key == pygame.K_3:
                    print("Exploring Concept...") #debug
                    state = CONCEPT_DISPLAY
                elif event.key == pygame.K_4:
                    pygame.quit()
                    sys.exit()
            elif state == CONCEPT_DISPLAY:
                    state = MENU

def update_display():
    screen.fill(BLACK)
    if state == INTRO:
        screen.blit(intro_image, (0, 0))
        screen.blit(continue_text, continue_text_rect)
    elif state == MENU:
        for surface, position in zip(option_surfaces, option_positions):
            screen.blit(surface, position)
    elif state == CONCEPT_DISPLAY:
        screen.blit(concept_image, (0, 0))
    pygame.display.flip()


while True:
    handle_events()
    update_display()