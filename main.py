from math import *
import pygame
import pygame_textinput
import random
from library.function import *
from library.graph import *
import copy
WIDTH = 1024
HEIGHT = 768
FPS = 60
ZOOM_AMOUNT = 2

def setup():
    global main_graph, screen, clock, prev, text_mode, text_prompt
    pygame.init()
    pygame.mixer.init()
    main_graph = graph()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("AmbyDesmos-v1")
    icon = pygame.image.load("icon.png")
    pygame.display.set_icon(icon)
    clock = pygame.time.Clock()
    prev = None
    text_prompt = pygame_textinput.TextInputVisualizer()
    text_prompt.font_object = pygame.font.SysFont("Consolas", 25, False)
    text_mode = False

def loop():
    global main_graph, screen, clock, prev, text_mode, text_prompt
    delta_time = clock.tick(FPS) / 1000
    events = pygame.event.get()
    if text_mode:
        text_prompt.update(events)
    for event in events: 
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False
            if event.key == pygame.K_RETURN:
                if text_mode == True:
                    func = text_prompt.value
                    if func != "":
                        try:
                            main_graph.add_function(
                                function(
                                    lambda x: eval(func),
                                    (
                                        random.randrange(0, 256),
                                        random.randrange(0, 256),
                                        random.randrange(0, 256)
                                    )
                                )
                            )
                        except ...:
                            pass
                    text_prompt.value = ""
                text_mode = not text_mode
            if event.key == pygame.K_BACKSPACE and not text_mode:
                main_graph.x_offset = 0
                main_graph.y_offset = 0
        if event.type == pygame.MOUSEBUTTONDOWN and not text_mode:
            if event.button == 4:
                main_graph.zoom_change(ZOOM_AMOUNT)
            if event.button == 5:
                main_graph.zoom_change(- ZOOM_AMOUNT)
    
    if pygame.mouse.get_pressed()[0] and not text_mode:
        if prev == None:
            prev = pygame.mouse.get_pos()
        else:
            curr = pygame.mouse.get_pos()
            dx = ((curr[0] - prev[0]) / main_graph.zoom_level)
            dy = ((curr[1] - prev[1]) / main_graph.zoom_level)
            main_graph.move_vector(- dx, dy)
            prev = curr
    else:
        prev = None
    screen.blit(main_graph.draw(WIDTH, HEIGHT), (0, 0))
    if text_mode:
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, text_prompt.surface.get_height()))
        screen.blit(text_prompt.surface, (0, 0))
    pygame.display.flip()
    return True

if __name__ == "__main__":
    setup()
    while(loop()):
        pass