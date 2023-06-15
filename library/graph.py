from math import *
import pygame
from library.function import *
import copy

BG = (255, 255, 255)
GRID = (0, 0, 0)
LINE_WIDTH = 3

class graph:
    f_list = []
    MIN_ZOOM = 5
    zoom_level = 32
    x_offset = 0
    y_offset = 0
    def __init__(self):
        self.f_list = []
    def add_function(self, f : function):
        self.f_list.append(f)
    def remove_function_at_idx(self, idx : int):
        self.f_list.pop(idx)
    def print_function_list(self):
        for f in self.f_list:
            print(f.__str__())
    def print_function_test(self, x):
        for f in self.f_list:
            print(f.evaluate(x))
    def zoom_change(self, value):
        self.zoom_level += value
        if self.zoom_level < self.MIN_ZOOM:
            self.zoom_level = self.MIN_ZOOM
    def move_vector(self, dx, dy):
        self.x_offset += dx
        self.y_offset += dy
    def draw(self, width, height):
        draw_surface = pygame.Surface((width, height))
        draw_surface.fill(BG)
        x_0 = round((width // 2) - self.x_offset * self.zoom_level)
        y_0 = round((height // 2) + self.y_offset * self.zoom_level)
        if 0 <= x_0 and x_0 <= width:
            pygame.draw.line(draw_surface, GRID,
                             (x_0, 0), (x_0, height), 3)
        if 0 <= y_0 and y_0 <= height:
            pygame.draw.line(draw_surface, GRID,
                             (0, y_0), (width, y_0), 3)
        
        xl = floor(self.x_offset)
        while (width // 2) - (self.x_offset - xl) * self.zoom_level >= 0:
            draw_x = (width // 2) - (self.x_offset - xl) * self.zoom_level
            pygame.draw.line(draw_surface, GRID,
                             (draw_x, 0), (draw_x, height), 1)
            xl -= 1
        
        xr = ceil(self.x_offset)
        while (width // 2) + (xr - self.x_offset) * self.zoom_level < width:
            draw_x = (width // 2) + (xr - self.x_offset) * self.zoom_level
            pygame.draw.line(draw_surface, GRID,
                             (draw_x, 0), (draw_x, height), 1)
            xr += 1

        yd = floor(self.y_offset)
        while (height // 2) + (self.y_offset - yd) * self.zoom_level < height:
            draw_y = (height // 2) + (self.y_offset - yd) * self.zoom_level
            pygame.draw.line(draw_surface, GRID,
                             (0, draw_y), (width, draw_y), 1)
            yd -= 1
        
        yu = ceil(self.y_offset)
        while (height // 2) - (yu - self.y_offset) * self.zoom_level >= 0:
            draw_y = (height // 2) - (yu - self.y_offset) * self.zoom_level
            pygame.draw.line(draw_surface, GRID,
                             (0, draw_y), (width, draw_y), 1)
            yu += 1

        upper_bound = self.y_offset + (height // 2) / self.zoom_level
        lower_bound = self.y_offset - (height // 2) / self.zoom_level
        prev = [None for i in range(len(self.f_list))]
        for w in range(0, width):
            x = self.x_offset + ((w - (width // 2)) / self.zoom_level)
            for idx, f in enumerate(self.f_list):
                y = f.evaluate(x)
                if y == None:
                    prev[idx] = None
                else:
                    h = height // 2 - (y - self.y_offset) * self.zoom_level
                    if lower_bound < y and y <= upper_bound:
                        pygame.draw.rect(draw_surface, f.color, (w, h, 1, 1))
                        if prev[idx] != None:
                            pygame.draw.line(draw_surface, f.color, (w, h), prev[idx], LINE_WIDTH)
                    prev[idx] = (w, h)

        return draw_surface
        