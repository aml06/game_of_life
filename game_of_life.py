import sys
import pygame
import numpy as np
import math
import random

def __main__():

    #constants
    FPS = 120
    WIDTH, HEIGHT = 1000, 1000
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255, 36, 0)
    
    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Game of Life")
    running = True

    """
    reference_rect = Life(500,500, 20, 20, WHITE)
    second_rect = Life(520, 520, 20, 20, WHITE)
    third_rect = Life(540, 520, 20, 20, WHITE)
    fourth_rect = Life(560, 520, 20, 20, WHITE)
    
    
    life_list = []
    
    life_list.append(reference_rect)
    life_list.append(second_rect)
    life_list.append(third_rect)
    life_list.append(fourth_rect)
    """
    
    life_list = gosper_glider_generation()
    
    clock = pygame.time.Clock()

    # Grid constants, but I don't think this is the way to handle it...
    cell_size = 20
    grid_color = WHITE
    camera_x, camera_y = 0, 0
    zoom = 1.0
    screen_center = [0,0]
    
    # Timing constants
    count_timer = 0
    board_control = 20
    
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.VIDEORESIZE:
                new_width, new_height = event.size
                WIDTH, HEIGHT = new_width, new_height
                window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
                pygame.display.update()
            if event.type == pygame.KEYDOWN:

                #Program quits with escape
                if event.key == pygame.K_ESCAPE:
                    running = False
                    
                if event.key == pygame.K_MINUS:
                    board_control += 1
                    
                if event.key == pygame.K_EQUALS:
                    if board_control > 1:
                        board_control -= 1
                        # Makes sure we can't have count_timer ever get larger than board_control
                        if count_timer > board_control:
                            count_timer = board_control
                
                if event.key == pygame.K_LEFT:
                    screen_center[0] = screen_center[0] - 2
                
                if event.key == pygame.K_RIGHT:
                    screen_center[0] = screen_center[0] + 2
                    
                if event.key == pygame.K_UP:
                    screen_center[1] = screen_center[1] - 2
                    
                if event.key == pygame.K_DOWN:
                    screen_center[1] = screen_center[1] + 2
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                mouseX, mouseY = pygame.mouse.get_pos()
                print(mouseX, mouseY)
                click_life = Life(mouseX - (mouseX % 20), mouseY - (mouseY % 20), 20, 20, WHITE)
                life_list.append(click_life)
                click_life.draw(window)
                pygame.display.update()

            # Allows for zooming and scrolling grid
            """
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    camera_y += 10 / zoom
                if event.y < 0:
                    camera_y -= 10 / zoom
                if event.x > 0:
                    camera_x += 10 / zoom
                if event.x < 0:
                    camera_x -= 10 / zoom
            """
        # Need to update board in a manner seperate from updating screen so can add blocks from clicking smoothly
        if count_timer == board_control:
            window.fill(BLACK)
            for square in life_list:
                square.draw(window)
            draw_grid(WIDTH, HEIGHT, cell_size, zoom, window, WHITE, camera_x, camera_y)
            life_list = new_life(life_list)
            life_list = life_fence(life_list)
            pygame.display.flip()
            count_timer = 0
        count_timer += 1

    pygame.quit()
    sys.exit()

# Handles generating new live squares and calculating and removing live squares that will die
def new_life(life_list):
    rand_color = False
    new_life_dict = {}
    new_life_list = []
    surviving_life_List = []
    # Generate dictionary with keys which are locations adjacent to live squares and the value is the count
    # of neighboring live squares
    for life in life_list:
        # Top Left
        if ((life.get_x() - 20), (life.get_y() + 20)) in new_life_dict:
            new_life_dict[(life.get_x() - 20), (life.get_y() + 20)] += 1
        else:
            new_life_dict[(life.get_x() - 20), (life.get_y() + 20)] = 1
            
        # Top
        if ((life.get_x()), (life.get_y() + 20)) in new_life_dict:
            new_life_dict[(life.get_x()), (life.get_y() + 20)] += 1
        else:
            new_life_dict[(life.get_x()), (life.get_y() + 20)] = 1
        
        # Top Right
        if ((life.get_x() + 20), (life.get_y() + 20)) in new_life_dict:
            new_life_dict[(life.get_x() + 20), (life.get_y() + 20)] += 1
        else:
            new_life_dict[(life.get_x() + 20), (life.get_y() + 20)] = 1
        
        # Left
        if ((life.get_x() - 20), (life.get_y())) in new_life_dict:
            new_life_dict[(life.get_x() - 20), (life.get_y())] += 1
        else:
            new_life_dict[(life.get_x() - 20), (life.get_y())] = 1
        
        # Right
        if ((life.get_x() + 20), (life.get_y())) in new_life_dict:
            new_life_dict[(life.get_x() + 20), (life.get_y())] += 1
        else:
            new_life_dict[(life.get_x() + 20), (life.get_y())] = 1
            
        # Bot Left
        if ((life.get_x() - 20), (life.get_y() - 20)) in new_life_dict:
            new_life_dict[(life.get_x() - 20), (life.get_y() - 20)] += 1
        else:
            new_life_dict[(life.get_x() - 20), (life.get_y() - 20)] = 1
            
        # Bot
        if ((life.get_x()), (life.get_y() - 20)) in new_life_dict:
            new_life_dict[(life.get_x()), (life.get_y() - 20)] += 1
        else:
            new_life_dict[(life.get_x()), (life.get_y() - 20)] = 1
            
        # Bot Right
        if ((life.get_x() + 20), (life.get_y() - 20)) in new_life_dict:
            new_life_dict[(life.get_x() + 20), (life.get_y() - 20)] += 1
        else:
            new_life_dict[(life.get_x() + 20), (life.get_y() - 20)] = 1
    
    # Check dictionary for dead squares with 3 live neighbors and generate new live square at that location
    # From the key value pairs in the dictionary
    for key in new_life_dict:
        if new_life_dict[key] == 3:
            if rand_color == False:
                new_life = Life(key[0],key[1], 20, 20, (255, 255, 255))
            else:
                new_life = Life(key[0],key[1], 20, 20, (random.randint(0,255), random.randint(0,255), random.randint(0,255)))
            new_life_list.append(new_life)
    
    # Check how many neighbors each square has and do not add it to the next generation list if it has too many or too few
    for life in life_list:
        neighbor_count = 0
        for sub_life in life_list:
            if sub_life != life:
                # Top Left
                if life.get_x() - 20 == sub_life.get_x() and life.get_y() +20 == sub_life.get_y():
                    neighbor_count += 1
                # Top
                if life.get_x() == sub_life.get_x() and life.get_y() + 20 == sub_life.get_y():
                    neighbor_count += 1
                # Top Right
                if life.get_x() + 20 == sub_life.get_x() and life.get_y() + 20 == sub_life.get_y():
                    neighbor_count += 1
                # Left
                if life.get_x() - 20 == sub_life.get_x() and life.get_y() == sub_life.get_y():
                    neighbor_count += 1
                # Right
                if life.get_x() + 20 == sub_life.get_x() and life.get_y() == sub_life.get_y():
                    neighbor_count += 1
                # Bottom Left
                if life.get_x() - 20 == sub_life.get_x() and life.get_y() - 20 == sub_life.get_y():
                    neighbor_count += 1
                # Bottom
                if life.get_x() == sub_life.get_x() and life.get_y() - 20 == sub_life.get_y():
                    neighbor_count += 1
                # Bottom Right
                if life.get_x() + 20 == sub_life.get_x() and life.get_y() - 20 == sub_life.get_y():
                    neighbor_count += 1

        if neighbor_count == 2 or neighbor_count == 3:
            surviving_life_List.append(life)
    next_generation = new_life_list + surviving_life_List
    
    # Remove Duplicate live squares from the combined neighbor generated list and the surviving existing square list
    i = 0
    while i < len(next_generation):
        j = i+1
        while j < len(next_generation):
            if next_generation[i].get_position() == next_generation[j].get_position():
                next_generation.pop(j)
                j -= 1
            j+=1
        i+=1
        
    return next_generation

# Removes live squares that get too far away to save on memory
def life_fence(my_life_list):
    fenced_list = list(filter(lambda life_cell: -2000 <= life_cell.get_x() <= 2000 or -2000 <= life_cell.get_y() <= 2000, my_life_list))
    return fenced_list

# Just generates a grid based on screen dimensions
def draw_grid(width, height, cell_size, zoom, screen, grid_color, camera_x, camera_y):
    for x in range(0, width, int(cell_size * zoom)):
        pygame.draw.line(screen, grid_color, (x - camera_x % (cell_size * zoom), -height), (x - camera_x % (cell_size * zoom), height), 1)
    for y in range(0, height, int(cell_size * zoom)):
        pygame.draw.line(screen, grid_color, (-width, y - camera_y % (cell_size * zoom)), (width, y - camera_y % (cell_size * zoom)), 1)
        
# The class of my 'living' squares
class Life(pygame.Rect):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self.x_coord = x
        self.y_coord = y
        self.width = width
        self.height = height
        self.color = color
        self.position = (x, y)
    
    def get_position(self):
        return self.position
    # Pondering a more graceful way to handle finding neighboring squares, both live and dead...
    def neighbors(self):
        pass

    def draw(self, surface, shift_x = 0, shift_y = 0):
        pygame.draw.rect(surface, self.color, (self.x_coord + shift_x, self.y_coord + shift_y, self.width, self.height))

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
# Generates a gosper glider gun at the hard coded location
def gosper_glider_generation():
    WHITE = (255, 255, 255)
    
    # Left Square
    a1 = Life(100, 500, 20, 20, WHITE)
    a2 = Life(120, 500, 20, 20, WHITE)
    a3 = Life(100, 520, 20, 20, WHITE)
    a4 = Life(120, 520, 20, 20, WHITE)

    # Right Square
    b1 = Life(780, 480, 20, 20, WHITE)
    b2 = Life(780, 460, 20, 20, WHITE)
    b3 = Life(800, 480, 20, 20, WHITE)
    b4 = Life(800, 460, 20, 20, WHITE)
    
    # Left Center Structure
    c1 = Life(300, 500, 20, 20, WHITE)
    c2 = Life(300, 520, 20, 20, WHITE)
    c3 = Life(300, 540, 20, 20, WHITE)
    c4 = Life(320, 480, 20, 20, WHITE)
    c5 = Life(320, 560, 20, 20, WHITE)
    c6 = Life(340, 460, 20, 20, WHITE)
    c7 = Life(340, 580, 20, 20, WHITE)
    c8 = Life(360, 460, 20, 20, WHITE)
    c9 = Life(360, 580, 20, 20, WHITE)
    c10 = Life(380, 520, 20, 20, WHITE)
    c11 = Life(400, 480, 20, 20, WHITE)
    c12 = Life(400, 560, 20, 20, WHITE)
    c13 = Life(420, 500, 20, 20, WHITE)
    c14 = Life(420, 520, 20, 20, WHITE)
    c15 = Life(420, 540, 20, 20, WHITE)
    c16 = Life(440, 520, 20, 20, WHITE)

    # Right Center Structure
    d1 = Life(500, 500, 20, 20, WHITE)
    d2 = Life(500, 480, 20, 20, WHITE)
    d3 = Life(500, 460, 20, 20, WHITE)
    d4 = Life(520, 500, 20, 20, WHITE)
    d5 = Life(520, 480, 20, 20, WHITE)
    d6 = Life(520, 460, 20, 20, WHITE)
    d7 = Life(540, 440, 20, 20, WHITE)
    d8 = Life(540, 520, 20, 20, WHITE)
    d9 = Life(580, 420, 20, 20, WHITE)
    d10 = Life(580, 440, 20, 20, WHITE)
    d11 = Life(580, 520, 20, 20, WHITE)
    d12 = Life(580, 540, 20, 20, WHITE)
    life_list = [a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,c5,c6,c7,c8,
                 c9,c10,c11,c12,c13,c14,c15,c16,d1,d2,d3,d4,d5,
                 d6,d7,d8,d9,d10,d11,d12]
    return life_list
    
__main__()
