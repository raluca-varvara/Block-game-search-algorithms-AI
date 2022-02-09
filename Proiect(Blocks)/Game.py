import pygame
from Menu import *

class Game():
    def __init__(self):
        pygame.init()
        self.running = True
        self.playing = False

        self.DISPLAY_W = 480
        self.DISPLAY_H = 270
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode(((self.DISPLAY_W, self.DISPLAY_H)))
        self.font_name1 = '8-BIT WONDER.TTF'
        self.font_name2 = 'Calibri.TTF'
        pygame.display.set_caption("Blocks Puzzle")
        self.BLACK = (0, 0, 0)
        self.WHITE = (255, 255, 255)

        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.PAUSE_KEY = False

        self.help_menu = HelpMenu(self)
        self.level_menu = LevelMenu(self)
        self.alg_menu = AlgorithmsMenu(self)
        self.animation_menu = AnimationMenu(self)
        self.curr_menu = self.level_menu

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                self.curr_menu.run_display = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.START_KEY = True
                if event.key == pygame.K_BACKSPACE:
                    self.BACK_KEY = True
                if event.key == pygame.K_UP:
                    self.UP_KEY = True
                if event.key == pygame.K_DOWN:
                    self.DOWN_KEY = True
                if event.key == pygame.K_p:
                    self.PAUSE_KEY = True

    def reset_keys(self):
        self.UP_KEY = False
        self.DOWN_KEY = False
        self.START_KEY = False
        self.BACK_KEY = False
        self.PAUSE_KEY = False

    def game_loop(self):
        while self.playing:
            self.check_events()
            if self.START_KEY:
                self.playing = False

        self.display.fill(self.BLACK)
        self.window.blit(self.display, (0,0))
        pygame.display.update()
        self.reset_keys()

    def draw_text(self, text, font_name, size, x, y):
        font = pygame.font.Font(font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect() # x,y,w,h
        text_rect.center = (x,y)
        self.display.blit(text_surface, text_rect)

    def draw_block(self, colour, x ,y, w, h):
        pygame.draw.rect(self.display, colour, [x, y, w, h])
