import sys
import pygame
import numpy as np
import math

def __main__():

    #constants
    FPS = 2
    WIDTH, HEIGHT = 1000, 1000
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    RED = (255, 36, 0)

    pygame.init()

    window = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
    pygame.display.set_caption("Game of Life")
    running = True

    reference_rect = life(500,500, 20, 20, WHITE)
    second_rect = life(520, 520, 20, 20, RED)
    life_list = []
    life_list.append(reference_rect)
    life_list.append(second_rect)

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

        pygame.display.flip()

    pygame.quit()
    sys.exit()

def new_life(life_list):
    new_life_dict = {}
    new_life_list = []
    for life in life_list:
        # Top Left
        if new_life_dict.get((life.x - 20), (life.y + 20)) == None:
            new_life_dict[(life.x - 20), (life.y + 20)] = 1
        else:
            new_life_dict[(life.x - 20), (life.y + 20)] += 1
            
        # Top
        if new_life_dict.get((life.x), (life.y + 20)) == None:
            new_life_dict[(life.x), (life.y + 20)] = 1
        else:
            new_life_dict[(life.x), (life.y + 20)] += 1
        
        # Top Right
        if new_life_dict.get((life.x + 20), (life.y + 20)) == None:
            new_life_dict[(life.x + 20), (life.y + 20)] = 1
        else:
            new_life_dict[(life.x + 20), (life.y + 20)] += 1
        
        # Left
        if new_life_dict.get((life.x - 20), (life.y)) == None:
            new_life_dict[(life.x - 20), (life.y)] = 1
        else:
            new_life_dict[(life.x - 20), (life.y)] += 1
        
        # Right
        if new_life_dict.get((life.x + 20), (life.y)) == None:
            new_life_dict[(life.x + 20), (life.y)] = 1
        else:
            new_life_dict[(life.x + 20), (life.y)] += 1
            
        # Bot Left
        if new_life_dict.get((life.x - 20), (life.y - 20)) == None:
            new_life_dict[(life.x - 20), (life.y - 20)] = 1
        else:
            new_life_dict[(life.x - 20), (life.y - 20)] += 1
            
        # Bot
        if new_life_dict.get((life.x), (life.y - 20)) == None:
            new_life_dict[(life.x), (life.y - 20)] = 1
        else:
            new_life_dict[(life.x), (life.y - 20)] += 1
            
        # Bot Right
        if new_life_dict.get((life.x - 20), (life.y + 20)) == None:
            new_life_dict[(life.x - 20), (life.y + 20)] = 1
        else:
            new_life_dict[(life.x - 20), (life.y + 20)] += 1
    
    for key in new_life_dict:
        if new_life_dict[key] == 3:
            new_life = life(key[0],key[1], 20, 20, (255, 255, 255))
            new_life_list.append(new_life)
    

# Just generates a grid based on screen dimensions
def draw_grid(width, height, cell_size, zoom, screen, grid_color, camera_x, camera_y):
    for x in range(-width, width, int(cell_size * zoom)):
        pygame.draw.line(screen, grid_color, (x - camera_x % (cell_size * zoom), -height), (x - camera_x % (cell_size * zoom), height), 1)
    for y in range(-height, height, int(cell_size * zoom)):
        pygame.draw.line(screen, grid_color, (-width, y - camera_y % (cell_size * zoom)), (width, y - camera_y % (cell_size * zoom)), 1)

class life(pygame.Rect):
    def __init__(self, x, y, width, height, color):
        super().__init__(x, y, width, height)
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.position = (x, y)
    
    def position(self):
        return self.position

    def neighbors(self):
        pass

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x, self.y, self.width, self.height))

    def x(self):
        return self.x
    
    def y(self):
        return self.y
    
__main__()
