
import pygame as pg
import random
import time


RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
WHITE = (255,255,255)

class GameBoard:
    def __init__(self, width, height, grid_size):
        self.width = width
        self.height = height
        self.grid_size = grid_size
        self.playablegrid = self.generate_random_grid(grid_size)
        self.endgrid = self.generate_end_grid()
        self.counter = 0
        self.start_time = None
        self.position = (0,0)
        self.color = [RED, BLUE, YELLOW]

        # Vai faltar adicionar o end time para contabilizar tempo demorado ou entao actually tira-se o elapsed time


    def render_position(self, screen):
        cell_width = 100
        cell_height = 50
        border_width = 2 
        start_x = 75
        start_y = 275

        position_x = start_x + self.position[0] * (cell_width + border_width)
        position_y = start_y + self.position[1] * (cell_height + border_width)
        
        pg.draw.rect(screen, (255, 165, 0), (position_x, position_y, cell_width, cell_height), 2)


    def start_timer(self):
        self.start_time = time.time()

    def get_elapsed_time(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            return elapsed_time
        else:
            return 0

    def format_time(self, elapsed_time): # Minutos e segundios
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        return f"{minutes:02}:{seconds:02}"

    def render_clock(self, screen):
        font = pg.font.SysFont('Arial', 24)
        elapsed_time = self.get_elapsed_time()
        clock_text = font.render(self.format_time(elapsed_time), True, WHITE)
        clock_rect = clock_text.get_rect(topright=(self.width - 10, 10))
        screen.blit(clock_text, clock_rect)


    def move_counter(self):
        #Basicamente contar os presses de arrow keys codigo missing
        self.counter +=1



    def generate_end_grid(self):
        total_cells = self.grid_size ** 2
        colors = [RED] * (total_cells // 3) + [BLUE] * (total_cells // 3) + [YELLOW] * (total_cells // 3)
        if len(colors) < total_cells:
            missing_cells = total_cells - len(colors)
            colors += [BLUE] * missing_cells # Hope it randomnizes a bit more
        random.shuffle(colors)
        solution_board = []


        for i in range(self.grid_size):
            row = []
            for j in range(self.grid_size):
                color = colors.pop()
                row.append(color)
            solution_board.append(row)
        return solution_board
        

    def generate_random_grid(self, grid_size):
        total_cells = grid_size ** 2
        colors = [RED] * (total_cells // 3) + [BLUE] * (total_cells // 3) + [YELLOW] * (total_cells // 3)
        if len(colors) < total_cells:
            missing_cells = total_cells - len(colors)
            colors += [RED] * missing_cells
        random.shuffle(colors)

        grid = []
        for i in range(grid_size):
            row = []
            for j in range(grid_size):
                color = colors.pop()
                row.append(color)
            grid.append(row)
        return grid


    def render(self, screen, grid_size):
        if grid_size == 4:
            cell_width = 100
            cell_height = 50
            border_width = 2 

            start_x = 75  #Horizontal
            start_y = 275  #Vertical

            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    cell_color = self.playablegrid[row][col]
                    cell_x = start_x + col * (cell_width + border_width)  
                    cell_y = start_y + row * (cell_height + border_width)  


                    cell_rect = pg.Rect(cell_x, cell_y, cell_width, cell_height) 
                    pg.draw.rect(screen, (255, 255, 255), cell_rect) # Pygame desenhar bordas
                    cell_inner_rect = pg.Rect(cell_x + border_width // 2, cell_y + border_width // 2,
                                            cell_width - border_width, cell_height - border_width)
                    pg.draw.rect(screen, cell_color, cell_inner_rect)

            #Separador do amado
            vertical_bar_width = 10
            vertical_bar_height = 600
            vertical_bar_x = 500
            vertical_bar_y = 0
            pg.draw.rect(screen, (255, 255, 0), (vertical_bar_x, vertical_bar_y, vertical_bar_width, vertical_bar_height))
            self.render_position(screen)


    def render_end_grid(self, screen):
        if self.grid_size == 4:
            cell_width = 50
            cell_height = 30
            border_width = 2

            start_x = 550
            start_y = 150

            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    cell_color = self.endgrid[row][col]  
                    cell_x = start_x + col * (cell_width + border_width)
                    cell_y = start_y + row * (cell_height + border_width)


                    cell_rect = pg.Rect(cell_x, cell_y, cell_width, cell_height)
                    pg.draw.rect(screen, (255, 255, 255), cell_rect)
                    cell_inner_rect = pg.Rect(cell_x + border_width // 2, cell_y + border_width // 2,
                                            cell_width - border_width, cell_height - border_width)
                    pg.draw.rect(screen, cell_color, cell_inner_rect)

    def render_move_counter(self,screen):
        font = pg.font.SysFont('Arial', 24)
        counter_text = font.render(f"Moves: {self.counter}", True, WHITE)
        counter_rect = counter_text.get_rect(topleft=(10, 10))
        screen.blit(counter_text, counter_rect)


    def game_moves(self, event):
        if event.type == pg.KEYDOWN:
            x, y = self.position
            current_cell_color = self.playablegrid[y][x]

            new_position = None 

            if event.key == pg.K_UP and y > 0:
                new_position = (x, y - 1)
            elif event.key == pg.K_DOWN and y < self.grid_size - 1:
                new_position = (x, y + 1)
            elif event.key == pg.K_LEFT and x > 0:
                new_position = (x - 1, y)
            elif event.key == pg.K_RIGHT and x < self.grid_size - 1:
                new_position = (x + 1, y)

            if new_position:
                new_x, new_y = new_position
                if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                    destination_color = self.playablegrid[new_y][new_x]
                    if destination_color == current_cell_color:
                        self.position = new_position
                    else:
                        self.playablegrid[new_y][new_x] = self.get_transformed_color(current_cell_color, destination_color)
                        self.position = new_position 



    def get_transformed_color(self, current_color, destination_color):
        for color in self.color:
            if color != current_color and color != destination_color:
                return color
        return current_color



