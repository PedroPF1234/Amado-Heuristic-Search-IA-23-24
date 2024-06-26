
import pygame as pg
import random
import time
from collections import deque
from multiprocessing.pool import ThreadPool
import heapq


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
        self.end_time = None

        self.position = (0,0)
        self.color = [RED, BLUE, YELLOW]

        self.displaying_hint = False
        #self.pool = ThreadPool(processes=1)
        #self.async_result = None
        self.hint_path = None

    def render_position(self, screen):
        cell_width = 400 // self.grid_size
        cell_height = 200 // self.grid_size
        border_width = 2 
        start_x = 75
        start_y = 275

        position_x = start_x + self.position[0] * (cell_width + border_width)
        position_y = start_y + self.position[1] * (cell_height + border_width)
        
        pg.draw.rect(screen, (0, 0, 0), (position_x, position_y, cell_width, cell_height), 2)

    def start_timer(self):
        self.start_time = time.time()

    def stop_timer(self):
        self.end_time = time.time()

    def get_elapsed_time(self):
        if self.start_time is not None:
            if self.end_time is not None:
                elapsed_time = self.end_time - self.start_time
                return elapsed_time
            else:
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
        cell_width = 400 // grid_size
        cell_height = 200 // grid_size
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

        font = pg.font.SysFont('Arial', 24)
        hint_text = font.render("Press 'H' for hint", True, WHITE)
        hint_rect = hint_text.get_rect(topleft=(10, 50))
        screen.blit(hint_text, hint_rect)


    def render_search(self, screen, grid_size, grid):
        if grid_size == 4:
            cell_width = 100
            cell_height = 50
            border_width = 2 

            start_x = 75  #Horizontal
            start_y = 275  #Vertical

            for row in range(self.grid_size):
                for col in range(self.grid_size):
                    cell_color = grid[row][col]
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
        cell_width = 200 // self.grid_size
        cell_height = 120 // self.grid_size
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

    def render_hint(self, screen):
        if self.displaying_hint and self.hint_path is not None:
            hint = self.hint_path[1]
            font = pg.font.SysFont('Arial', 24)
            hint_text = None
            

            if self.position[0] == hint[0] and self.position[1] == hint[1] - 1:
                hint_text = font.render("Hint: Move Down", True, WHITE)
                hint_rect = hint_text.get_rect(topleft=(10, 100))
            elif self.position[0] == hint[0] and self.position[1] == hint[1] + 1:
                hint_text = font.render("Hint: Move Up", True, WHITE)
                hint_rect = hint_text.get_rect(topleft=(10, 100))
            elif self.position[0] == hint[0] - 1 and self.position[1] == hint[1]:
                hint_text = font.render("Hint: Move Right", True, WHITE)
                hint_rect = hint_text.get_rect(topleft=(10, 100))
            elif self.position[0] == hint[0] + 1 and self.position[1] == hint[1]:
                hint_text = font.render("Hint: Move Left", True, WHITE)
                hint_rect = hint_text.get_rect(topleft=(10, 100))

            screen.blit(hint_text, hint_rect)    

    def game_moves(self, event):


        if event.type == pg.KEYDOWN:
            self.displaying_hint = False
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
            elif event.key == pg.K_h:
                self.displaying_hint = True
                if self.hint_path is not None and self.hint_path[1][2] == tuple(map(tuple, self.playablegrid)):
                    self.hint_path.pop(0)
                    return
                else:
                    print("Searching for hint...")
                    self.hint_path = None
                    info = (self.position[0], self.position[1], self.playablegrid, 0, None)
                    #self.hint_path = self.async_result.get()
                    self.hint_path = self.get_hint_movement(info)
                    return

            if new_position:
                new_x, new_y = new_position
                if 0 <= new_x < self.grid_size and 0 <= new_y < self.grid_size:
                    destination_color = self.playablegrid[new_y][new_x]
                    if destination_color == current_cell_color:
                        self.position = new_position
                        self.move_counter()

                    else:
                        self.playablegrid[new_y][new_x] = self.get_transformed_color(current_cell_color, destination_color)
                        self.position = new_position 
                        self.move_counter()
                
            '''
            if self.hint_path is not None and self.hint_path[1][3] == self.playablegrid:
                self.hint_path.pop(0)

            else:
                info = (self.position[0], self.position[1], self.playablegrid.copy, self.counter, None)
                self.pool.terminate()
                self.pool = ThreadPool(processes=1)
                self.async_result = self.pool.apply_async(self.get_hint_movement, (info,))
            '''

    def get_transformed_color(self, current_color, destination_color):
        for color in self.color:
            if color != current_color and color != destination_color:
                return color
        return current_color

    def end_condition_check(self):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if self.playablegrid[i][j] != self.endgrid[i][j]:
                    return False  
        return True
    
    def reset_game_state(self):
        self.playablegrid = self.generate_random_grid(self.grid_size)
        self.endgrid = self.generate_end_grid()
        self.counter = 0
        self.start_time = None
        self.end_time = None

        self.position = (0, 0)

    def get_neighbors(self, info):
        parent = (info[0], info[1], tuple(map(tuple, info[2])), info[3], info[4])
        x, y, grid, counter, _ = info
        current_cell_color = grid[y][x]
        neighbors = []
        if x > 0:
            destination_color =  grid[y][x-1]
            if destination_color == current_cell_color:
                neighbors.append((x - 1, y, grid, counter + 1, parent))
            else:
                new_grid = [row[:] for row in grid]
                new_grid[y][x-1] = self.get_transformed_color(current_cell_color, destination_color)
                neighbors.append((x - 1, y, new_grid, counter + 1, parent))
        if x < len(self.playablegrid) - 1:
            destination_color = grid[y][x+1]
            if destination_color == current_cell_color:
                neighbors.append((x + 1, y, grid, counter + 1, parent))
            else:
                new_grid = [row[:] for row in grid]
                new_grid[y][x+1] = self.get_transformed_color(current_cell_color, destination_color)
                neighbors.append((x + 1, y, new_grid, counter + 1, parent))
        if y > 0:
            destination_color = grid[y-1][x]
            if destination_color == current_cell_color:
                neighbors.append((x, y - 1, grid, counter + 1, parent))
            else:
                new_grid = [row[:] for row in grid]
                new_grid[y-1][x] = self.get_transformed_color(current_cell_color, destination_color)
                neighbors.append((x, y - 1, new_grid, counter + 1, parent))
        if y < len(self.playablegrid) - 1:
            destination_color = grid[y+1][x]
            if destination_color == current_cell_color:
                neighbors.append((x, y + 1, grid, counter + 1, parent))
            else:
                new_grid = [row[:] for row in grid]
                new_grid[y+1][x] = self.get_transformed_color(current_cell_color, destination_color)
                neighbors.append((x, y + 1, new_grid, counter + 1, parent))
        return neighbors
    
    def search_end_condition_check(self, grid):
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if grid[i][j] != self.endgrid[i][j]:
                    return False
        return True
    
    def basic_bfs_search(self):
        
        visited = set()

        queue = deque()
        queue.append((0, 0, self.playablegrid, 0))
        while queue:
            current = queue.popleft()
            if self.search_end_condition_check(current[2]):
                return current
            
            x, y, grid = current[0], current[1], tuple(map(tuple, current[2]))
            state = (x, y, grid)
            if state not in visited:
                visited.add(state)
                for neighbor in self.get_neighbors(current):
                    neighbor_ = (neighbor[0], neighbor[1], tuple(map(tuple, neighbor[2])))
                    if neighbor_ not in visited:
                        queue.append(neighbor)
        return None
    
    def calculate_unmatching_sets(self, grid):
        unmatching_sets = 0
        for i in range(self.grid_size - 1):
            for j in range(self.grid_size - 1):
                if grid[i][j] != self.endgrid[i][j] or grid[i][j+1] != self.endgrid[i][j+1] or grid[i+1][j] != self.endgrid[i+1][j] or grid[i+1][j+1] != self.endgrid[i+1][j+1]:
                    unmatching_sets += 1
        return unmatching_sets

    def calculate_unmatching_tiles(self, grid):
        unmatching_tiles = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                if grid[i][j] != self.endgrid[i][j]:
                    unmatching_tiles += 1
        return unmatching_tiles
    
    def heuristic_search(self, grid):
        return self.calculate_unmatching_tiles(grid) + self.calculate_unmatching_sets(grid)

    def greedy_bfs_search(self, initial_info):
        print("Greedy BFS Search")
        visited = set()
        queue = []
        
        initial_priority = self.heuristic_search(initial_info[2])
        heapq.heappush(queue, (initial_priority, initial_info))
        
        while queue:
            _, current = heapq.heappop(queue)
            if self.search_end_condition_check(current[2]):
                print("Counter: ", current[3])
                return current
            
            x, y, grid = current[0], current[1], tuple(map(tuple, current[2]))
            state = (x, y, grid)
            if state not in visited:
                visited.add(state)
                for neighbor in self.get_neighbors(current):
                    neighbor_state = (neighbor[0], neighbor[1], tuple(map(tuple, neighbor[2])))
                    if neighbor_state not in visited:
                        priority = self.heuristic_search(neighbor[2])
                        heapq.heappush(queue, (priority, neighbor))
        return None

    def a_star_search(self, initial_info):
        print("A* Search")
        visited = set()
        queue = []
        
        initial_priority = self.heuristic_search(initial_info[2])
        heapq.heappush(queue, (initial_priority, initial_info))
        
        while queue:
            _, current = heapq.heappop(queue)
            if self.search_end_condition_check(current[2]):
                print("Counter: ", current[3])
                return current
            
            x, y, grid = current[0], current[1], tuple(map(tuple, current[2]))
            state = (x, y, grid)
            if state not in visited:
                visited.add(state)
                for neighbor in self.get_neighbors(current):
                    neighbor_state = (neighbor[0], neighbor[1], tuple(map(tuple, neighbor[2])))
                    if neighbor_state not in visited:
                        priority = self.heuristic_search(neighbor[2]) + neighbor[3]
                        heapq.heappush(queue, (priority, neighbor))
        return None

    def weighted_a_star_search(self, initial_info):
        print("Weighted A* Search")
        visited = set()
        queue = []

        initial_priority = self.heuristic_search(initial_info[2])
        heapq.heappush(queue, (initial_priority, initial_info))
        
        while queue:
            _, current = heapq.heappop(queue)
            if self.search_end_condition_check(current[2]):
                print("Counter: ", current[3])
                return current
            
            x, y, grid = current[0], current[1], tuple(map(tuple, current[2]))
            state = (x, y, grid)
            if state not in visited:
                visited.add(state)
                for neighbor in self.get_neighbors(current):
                    neighbor_state = (neighbor[0], neighbor[1], tuple(map(tuple, neighbor[2])))
                    if neighbor_state not in visited:
                        priority = (self.heuristic_search(neighbor[2]) * 1.3)  + neighbor[3]
                        heapq.heappush(queue, (priority, neighbor))
        return None
    
    def basic_dfs_search(self, initial_info, depth=0):
        print("Basic DFS Search")
        stack = []
        visited = set()
        stack.append(initial_info)
        
        while stack:
            current = stack.pop()
            if self.search_end_condition_check(current[2]):
                return current
            
            x, y, grid = current[0], current[1], tuple(map(tuple, current[2]))
            state = (x, y, grid)
            if state not in visited:
                visited.add(state)
                if depth == 0 or current[3] < depth:
                    for neighbor in self.get_neighbors(current):
                        neighbor_state = (neighbor[0], neighbor[1], tuple(map(tuple, neighbor[2])))
                        if neighbor_state not in visited:
                            stack.append(neighbor)
        return None
    
    def iterative_deepening_search(self, initial_info, depth):
        print("Iterative Deepening Search")
        initial_depth = 1
        while initial_depth <= depth:
            result = self.basic_dfs_search(initial_info, initial_depth)
            if result:
                return result
            initial_depth += 1

    def construct_path(self, current):
        path = []
        while current:
            path.append(current)
            current = current[4]
        return path[::-1]
    
    def print_path(self, path):
        for i in range(len(path)):
            print("Step: ", i)
            print("Position: ", path[i][0], path[i][1])
            for row in path[i][2]:
                print(row)
            print("\n\n")

    def get_hint_movement(self, initial_info):
        result = self.weighted_a_star_search(initial_info)
        return self.construct_path(result)