import sys
import pygame
import numpy as np
import math
import random
import time
#average time is approximately 0.0085 seconds = 8.5 ms, next step is thinking of a faster algorithm

WHITE = (255, 255, 255)

def main():

    #constants
    FPS = 120
    WIDTH, HEIGHT = 1000, 1000
    BLACK = (0,0,0)
    RED = (255, 36, 0)

    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Game of Life")
    running = True

    life_list = build_life(gosper_glider_builder())

    clock = pygame.time.Clock()

    # Grid constants, but I don't think this is the way to handle it...
    cell_size = 20
    grid_color = WHITE
    camera_x, camera_y = 0, 0
    zoom = 1.0
    shift = [0,0]
    
    # Timing constants
    count_timer = 0
    board_control = 20

    # Pygame constant
    pygame.key.set_repeat(5,50)

    # Mouse Drag
    drag = False
    
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
                
                #scroll through grid
                if event.key == pygame.K_LEFT:
                    shift[0] = shift[0] + 10
                    pygame.display.flip()
                if event.key == pygame.K_RIGHT:
                    shift[0] = shift[0] - 10
                    pygame.display.flip()
                if event.key == pygame.K_UP:
                    shift[1] = shift[1] + 10
                    pygame.display.flip()
                if event.key == pygame.K_DOWN:
                    shift[1] = shift[1] - 10
                    pygame.display.flip()
                
                #zoom in and out
                if event.key == pygame.K_n:
                    if zoom > 0.1:
                        zoom = zoom - 0.1
                
                if event.key == pygame.K_m:
                    zoom = zoom + 0.1
                    
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                mouseX, mouseY = pygame.mouse.get_pos()
                print(mouseX, mouseY)
                click_life = Life(mouseX - ((mouseX + shift[0]) % 20) - shift[0], mouseY - ((mouseY + shift[1]) % 20) - shift[1], 20, 20, WHITE)
                life_list.append(click_life)
                click_life.draw(window, shift[0], shift[1])
                pygame.display.update()
            
        # Need to update board in a manner seperate from updating screen so can add blocks from clicking smoothly
        if count_timer == board_control:
            window.fill(BLACK)
            for square in life_list:
                square.draw(window, shift[0], shift[1], zoom)
            draw_grid(WIDTH, HEIGHT, cell_size, zoom, window, WHITE, shift[0], shift[1])
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
def draw_grid(width, height, cell_size, zoom, screen, grid_color, shift_x, shift_y):
    for x in range(0, math.floor(width*zoom), int(cell_size)):
        pygame.draw.line(screen, grid_color, (math.floor((x - shift_x % cell_size) * zoom),math.floor( -height * zoom)), (math.floor((x - shift_x % cell_size) * zoom), math.floor(height*zoom)), 1)
    for y in range(0, math.floor(height * zoom), int(cell_size)):
        pygame.draw.line(screen, grid_color, (math.floor(-width * zoom), math.floor(y - shift_y % cell_size)*zoom), (math.floor(width * zoom), math.floor((y - shift_y % cell_size)*zoom)), 1)

def build_life(inputList):
    returnList = []
    for coord in inputList:
        newLife = Life(coord[0], coord[1], 50, 50, WHITE)
        returnList.append(newLife)
    return returnList

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

    def draw(self, surface, shift_x, shift_y, zoom):
        # Hmm wondering why this doesn't work...
        resolved_x = math.floor((self.x_coord + shift_x)*zoom)
        resolved_y = math.floor((self.y_coord + shift_y)*zoom)
        pygame.draw.rect(surface, self.color, (resolved_x, resolved_y, math.floor(self.width * zoom), math.floor(self.height*zoom)))

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y

def gosper_glider_builder():

    figure_a = [(100, 500), (120, 500), (100, 520), (120, 520)]
    
    figure_b = [(780, 480), (780, 460), (800, 480), (800, 460)]

    figure_c = [(300, 500), (300, 520), (300, 540), (320, 480), (320, 560),
                (340, 460), (340, 580), (360, 460), (360, 580), (380, 520),
                (400, 480), (400, 560), (420, 500), (420, 520), (420, 540),
                (440, 520)]

    figure_d = [(500, 500), (500, 480), [500, 460], (520, 500), (520, 480), (520, 460),
                (540, 440), (540, 520), (580, 420), (580, 440), (580, 520), (580, 540)]

    fig_list = figure_a + figure_b + figure_c + figure_d

    return fig_list

if __name__ == "__main__":
    main()
