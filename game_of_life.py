import sys
import pygame
import numpy as np
import math

def __main__():

    #constants
    FPS = 1
    WIDTH, HEIGHT = 1000, 1000
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255, 36, 0)

    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Game of Life")
    running = True

    reference_rect = Life(500,500, 20, 20, WHITE)
    second_rect = Life(520, 520, 20, 20, WHITE)
    third_rect = Life(540, 520, 20, 20, WHITE)
    fourth_rect = Life(560, 520, 20, 20, WHITE)

    #Gosper Glider Gun
    a1 = Life(100, 500, 20, 20, WHITE)
    a2 = Life(120, 500, 20, 20, WHITE)
    a3 = Life(100, 520, 20, 20, WHITE)
    a4 = Life(120, 520, 20, 20, WHITE)

    b1 = Life(740, 480, 20, 20, WHITE)
    b2 = Life(740, 460, 20, 20, WHITE)
    b3 = Life(760, 480, 20, 20, WHITE)
    b4 = Life(760, 460, 20, 20, WHITE)

    c1 = Life(260, 500, 20, 20, WHITE)
    c2 = Life(280, 480, 20, 20, WHITE)
    c3 = Life(300, 460, 20, 20, WHITE)
    c4 = Life(320, 460, 20, 20, WHITE)
    c5 = Life(260, 520, 20, 20, WHITE)
    c6 = Life(260, 540, 20, 20, WHITE)
    c7 = Life(280, 560, 20, 20, WHITE)
    c8 = Life(300, 580, 20, 20, WHITE)
    c9 = Life(340, 520, 20, 20, WHITE)
    c10 = Life(380, 520, 20, 20, WHITE)
    c11 = Life(400, 520, 20, 20, WHITE)
    c12 = Life(380, 500, 20, 20, WHITE)
    c13 = Life(360, 480, 20, 20, WHITE)
    c14 = Life(360, 540, 20, 20, WHITE)

    d1 = Life(460,500, 20, 20, WHITE)
    d2 = Life(460, 480, 20, 20, WHITE)
    d3 = Life(460, 460, 20, 20, WHITE)
    d4 = Life(480, 500, 20, 20, WHITE)
    d5 = Life(480, 480, 20, 20, WHITE)
    d6 = Life(480, 460, 20, 20, WHITE)
    d7 = Life(500, 440, 20, 20, WHITE)
    d8 = Life(540, 440, 20, 20, WHITE)
    d9 = Life(540, 420, 20, 20, WHITE)
    d10 = Life(540, 520, 20, 20, WHITE)
    d11 = Life(540, 540, 20, 20, WHITE)
    life_list = [a1,a2,a3,a4,b1,b2,b3,b4,c1,c2,c3,c4,c5,c6,c7,c8,
                 c9,c10,c11,c12,c13,c14,d1,d2,d3,d4,d5,
                 d6,d7,d8,d9,d10,d11]
    """
    life_list = []
    
    life_list.append(reference_rect)
    life_list.append(second_rect)
    life_list.append(third_rect)
    life_list.append(fourth_rect)
    """
    clock = pygame.time.Clock()

    # Grid constants, but I don't think this is the way to handle it...
    cell_size = 20
    grid_color = WHITE
    camera_x, camera_y = 0, 0
    zoom = 1.0

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

        window.fill(BLACK)
        for square in life_list:
            square.draw(window)
            print(square.position)
        #draw_grid(WIDTH, HEIGHT, cell_size, zoom, window, WHITE, camera_x, camera_y)
        life_list = new_life(life_list)
        pygame.display.flip()

    pygame.quit()
    sys.exit()

def new_life(life_list):
    new_life_dict = {}
    new_life_list = []
    surviving_life_List = []
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
    print(new_life_dict)
    for key in new_life_dict:
        if new_life_dict[key] == 3:
            print(f"Key[0] is {key[0]}, key[1] is {key[1]}")
            new_life = Life(key[0],key[1], 20, 20, (255, 255, 255))
            new_life_list.append(new_life)
    
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
    return next_generation

# Just generates a grid based on screen dimensions
def draw_grid(width, height, cell_size, zoom, screen, grid_color, camera_x, camera_y):
    for x in range(-width, width, int(cell_size * zoom)):
        pygame.draw.line(screen, grid_color, (x - camera_x % (cell_size * zoom), -height), (x - camera_x % (cell_size * zoom), height), 1)
    for y in range(-height, height, int(cell_size * zoom)):
        pygame.draw.line(screen, grid_color, (-width, y - camera_y % (cell_size * zoom)), (width, y - camera_y % (cell_size * zoom)), 1)

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

    def neighbors(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x_coord, self.y_coord, self.width, self.height))

    def get_x(self):
        return self.x
    
    def get_y(self):
        return self.y
    
__main__()
