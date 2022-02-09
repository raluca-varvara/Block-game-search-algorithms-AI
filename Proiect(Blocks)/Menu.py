import time
from enum import Enum

import pygame

import search
from search import *

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w = self.game.DISPLAY_W / 2
        self.mid_h = self.game.DISPLAY_H /2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100 # ca sa fie in staga scrisului

    def draw_cursor(self):
        self.game.draw_text('*', self.game.font_name1, 18, self.cursor_rect.x - 20, self.cursor_rect.y)

    def blit_screen(self):
        self.game.window.blit(self.game.display, (0,0))
        pygame.display.update()
        self.game.reset_keys()

class LevelMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = "Help"
        self.helpx = self.mid_w
        self.helpy = self.mid_h - 10
        self.easyx = self.mid_w
        self.easyy = self.mid_h + 30
        self.mediumx = self.mid_w
        self.mediumy = self.mid_h + 50
        self.hardx = self.mid_w
        self.hardy = self.mid_h + 70
        self.cursor_rect.midtop = (self.helpx + self.offset, self.helpy)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Choose the LEVEL', self.game.font_name1, 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 100)
            self.game.draw_text('Help', self.game.font_name1, 20, self.helpx, self.helpy)
            self.game.draw_text('Easy Mode', self.game.font_name1, 20, self.easyx, self.easyy)
            self.game.draw_text('Medium Mode', self.game.font_name1, 20, self.mediumx, self.mediumy)
            self.game.draw_text('Hard Mode', self.game.font_name1, 20, self.hardx, self.hardy)
            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'Easy':
                self.cursor_rect.midtop = (self.mediumx + self.offset, self.mediumy)
                self.state = 'Medium'
            elif self.state == 'Medium':
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
                self.state = 'Hard'
            elif self.state == 'Hard':
                self.cursor_rect.midtop = (self.helpx + self.offset, self.helpy)
                self.state = 'Help'
            elif self.state == 'Help':
                self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)
                self.state = 'Easy'
        if self.game.UP_KEY:
            if self.state == 'Easy':
                self.cursor_rect.midtop = (self.helpx + self.offset, self.helpy)
                self.state = 'Help'
            elif self.state == 'Medium':
                self.cursor_rect.midtop = (self.easyx + self.offset, self.easyy)
                self.state = 'Easy'
            elif self.state == 'Hard':
                self.cursor_rect.midtop = (self.mediumx + self.offset, self.mediumy)
                self.state = 'Medium'
            elif self.state == 'Help':
                self.cursor_rect.midtop = (self.hardx + self.offset, self.hardy)
                self.state = 'Hard'

    def check_input(self):
        self.move_cursor()
        if self.game.START_KEY:
            if self.state == 'Easy':
                self.game.alg_menu = AlgorithmsMenu(self.game, 1)
                self.game.curr_menu = self.game.alg_menu
            elif self.state == 'Medium':
                self.game.alg_menu = AlgorithmsMenu(self.game, 2)
                self.game.curr_menu = self.game.alg_menu
            elif self.state == 'Hard':
                self.game.alg_menu = AlgorithmsMenu(self.game, 3)
                self.game.curr_menu = self.game.alg_menu
            elif self.state == 'Help':
                self.game.help_menu = HelpMenu(self.game)
                self.game.curr_menu = self.game.help_menu
            self.run_display = False

class HelpMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

    def display_menu(self):
        self.run_display = True
        self.game.DISPLAY_W = 1800
        self.game.DISPLAY_H = 600
        self.game.display = pygame.Surface((self.game.DISPLAY_W, self.game.DISPLAY_H))
        self.game.window = pygame.display.set_mode(((self.game.DISPLAY_W, self.game.DISPLAY_H)))
        pygame.display.update()
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('*You can go through the pages by pressing the enter key and backspace key*', self.game.font_name1, 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 80)
            self.game.draw_text('*By pressing the backspace key you are redirrected to the previous meniu*',
                                self.game.font_name1, 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 55)
            self.game.draw_text('*By pressing  the enter key you are redirrected to the next meniu which have been selected by you*',
                                self.game.font_name1, 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 30)
            self.game.draw_text('*You can go through the options of a meniu using the arrow up and down keys*',
                                self.game.font_name1, 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 - 5)
            self.game.draw_text('*To start the animation press the enter key and to close the animation press the backspace key*',
                                self.game.font_name1, 20, self.game.DISPLAY_W / 2,
                                self.game.DISPLAY_H / 2 + 20)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.level_menu
            self.run_display = False

            self.game.DISPLAY_W = 480
            self.game.DISPLAY_H = 270
            self.game.display = pygame.Surface((self.game.DISPLAY_W, self.game.DISPLAY_H))
            self.game.window = pygame.display.set_mode(((self.game.DISPLAY_W, self.game.DISPLAY_H)))

class AlgorithmsMenu(Menu):
    def __init__(self, game, no_puzzle=0):
        Menu.__init__(self, game)
        self.no_puzzle = no_puzzle
        self.state = "BFS"
        self.bfsx = self.mid_w
        self.bfsy = self.mid_h - 30
        self.dfsx = self.mid_w
        self.dfsy = self.mid_h - 10
        self.ucsx = self.mid_w
        self.ucsy = self.mid_h + 10
        self.manx = self.mid_w
        self.many = self.mid_h + 30
        self.eucx = self.mid_w
        self.eucy = self.mid_h + 50
        self.chex = self.mid_w
        self.chey = self.mid_h + 70
        self.chix = self.mid_w
        self.chiy = self.mid_h + 90
        self.cursor_rect.midtop = (self.bfsx + self.offset, self.bfsy)

        self.START = BlockPuzzleState(None)
        if self.no_puzzle == 1:
            self.START = BlockPuzzleState(BlockPuzzleState.random_generation(3, 3))
        elif self.no_puzzle == 2:
            self.START = BlockPuzzleState(BlockPuzzleState.random_generation(3, 5))
        elif self.no_puzzle == 3:
            self.START = BlockPuzzleState(BlockPuzzleState.random_generation(3, 6))

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Choose the ALGORITHM', self.game.font_name1, 20, self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2 - 70)
            self.game.draw_text('BFS', self.game.font_name1, 20, self.bfsx, self.bfsy)
            self.game.draw_text('DFS', self.game.font_name1, 20, self.dfsx, self.dfsy)
            self.game.draw_text('UCS', self.game.font_name1, 20, self.ucsx, self.ucsy)
            self.game.draw_text('Manhattan', self.game.font_name1, 20, self.manx, self.many)
            self.game.draw_text('Euclidean', self.game.font_name1, 20, self.eucx, self.eucy)
            self.game.draw_text('Chebisev', self.game.font_name1, 20, self.chex, self.chey)
            self.game.draw_text('ChiSquared', self.game.font_name1, 20, self.chix, self.chiy)

            self.draw_cursor()
            self.blit_screen()

    def move_cursor(self):
        if self.game.DOWN_KEY:
            if self.state == 'BFS':
                self.cursor_rect.midtop = (self.dfsx + self.offset, self.dfsy)
                self.state = 'DFS'
            elif self.state == 'DFS':
                self.cursor_rect.midtop = (self.ucsx + self.offset, self.ucsy)
                self.state = 'UCS'
            elif self.state == 'UCS':
                self.cursor_rect.midtop = (self.manx + self.offset, self.many)
                self.state = 'MAN'
            elif self.state == 'MAN':
                self.cursor_rect.midtop = (self.eucx + self.offset, self.eucy)
                self.state = 'EUC'
            elif self.state == 'EUC':
                self.cursor_rect.midtop = (self.chex + self.offset, self.chey)
                self.state = 'CHE'
            elif self.state == 'CHE':
                self.cursor_rect.midtop = (self.chix + self.offset, self.chiy)
                self.state = 'CHI'
            elif self.state == 'CHI':
                self.cursor_rect.midtop = (self.bfsx + self.offset, self.bfsy)
                self.state = 'BFS'
        if self.game.UP_KEY:
            if self.state == 'BFS':
                self.cursor_rect.midtop = (self.chix + self.offset, self.chiy)
                self.state = 'CHI'
            elif self.state == 'DFS':
                self.cursor_rect.midtop = (self.bfsx + self.offset, self.bfsy)
                self.state = 'BFS'
            elif self.state == 'UCS':
                self.cursor_rect.midtop = (self.dfsx + self.offset, self.dfsy)
                self.state = 'DFS'
            elif self.state == 'MAN':
                self.cursor_rect.midtop = (self.ucsx + self.offset, self.ucsy)
                self.state = 'UCS'
            elif self.state == 'EUC':
                self.cursor_rect.midtop = (self.manx + self.offset, self.many)
                self.state = 'MAN'
            elif self.state == 'CHE':
                self.cursor_rect.midtop = (self.eucx + self.offset, self.eucy)
                self.state = 'EUC'
            elif self.state == 'CHI':
                self.cursor_rect.midtop = (self.chex + self.offset, self.chey)
                self.state = 'CHE'

    def check_input(self):
        self.move_cursor()
        if self.game.BACK_KEY:
            self.game.curr_menu = self.game.level_menu
            self.run_display = False
        if self.game.START_KEY:
            if self.state == 'BFS':
                self.game.animation_menu = AnimationMenu(self.game, self.game.alg_menu.no_puzzle,"bfs", self.game.alg_menu.START)
                self.game.curr_menu = self.game.animation_menu
            elif self.state == 'DFS':
                self.game.animation_menu = AnimationMenu(self.game, self.game.alg_menu.no_puzzle,"dfs", self.game.alg_menu.START)
                self.game.curr_menu = self.game.animation_menu
            elif self.state == 'UCS':
                self.game.animation_menu = AnimationMenu(self.game, self.game.alg_menu.no_puzzle,"ucs", self.game.alg_menu.START)
                self.game.curr_menu = self.game.animation_menu
            elif self.state == 'MAN':
                self.game.animation_menu = AnimationMenu(self.game, self.game.alg_menu.no_puzzle,"man", self.game.alg_menu.START)
                self.game.curr_menu = self.game.animation_menu
            elif self.state == 'EUC':
                self.game.animation_menu = AnimationMenu(self.game, self.game.alg_menu.no_puzzle,"euc", self.game.alg_menu.START)
                self.game.curr_menu = self.game.animation_menu
            elif self.state == 'CHE':
                self.game.animation_menu = AnimationMenu(self.game, self.game.alg_menu.no_puzzle,"che", self.game.alg_menu.START)
                self.game.curr_menu = self.game.animation_menu
            elif self.state == 'CHI':
                self.game.animation_menu = AnimationMenu(self.game, self.game.alg_menu.no_puzzle,"chi", self.game.alg_menu.START)
                self.game.curr_menu = self.game.animation_menu
            self.run_display = False

class AnimationMenu(Menu):
    class Colour(Enum):
        COLOUR0 = (6, 77, 135)  # nuanta de albastru
        COLOUR1 = (0, 83, 98)  # nunata de albastru
        COLOUR2 = (255, 130, 67)  # mango tango
        #######################################
        COLOUR3 = (226, 114, 91)  # terra cotta
        COLOUR4 = (221, 160, 216)  # nuanta de roz
        COLOUR5 = (147, 112, 219)  # nuanta de mov
        #######################################
        COLOUR6 = (21, 119, 40)  # nuanta de verde
        COLOUR7 = (135, 135, 0)  # nuanta de galben
        COLOUR8 = (123, 156, 169)  # nuanta de albastru
        COLOUR9 = (196, 0, 0)  # nuanta de rosu
        COLOUR10 = (0, 150, 141)  # nuanta de verde
        COLOUR11 = (114, 73, 32)  # nuanta de maro
        COLOUR12 = (246, 29, 98)  # nuanta de roz
        COLOUR13 = (131, 38, 26)  # nuanta de maro
        COLOUR14 = (42, 42, 42)

        def give_rgb(poz):
            i = 0
            for data in AnimationMenu.Colour:
                if i == poz:
                    return data.value
                i += 1

    def __init__(self, game, no_puzzle=0, type="", start=None):
        Menu.__init__(self, game)
        self.no_puzzle = no_puzzle
        self.type = type
        self.START = start
        self.animation_running = False
        self.animation_done = False
        self.animation_paused = False
        self.iterate_animation = 0

        self.n_expanded = 0
        self.n_generated = 0

        self.problem = BlockPuzzleSearchProblem(self.START)
        self.SOL = []
        if self.type == "bfs":
            self.SOL = breadthFirstSearch(self.problem, self.no_puzzle)
            self.n_expanded = search.nb_expanded
            self.n_generated = search.nb_generated
        elif self.type == "dfs":
            self.SOL = depthFirstSearch(self.problem, self.no_puzzle)
            self.n_expanded = search.nb_expanded
            self.n_generated = search.nb_generated
        elif self.type == "ucs":
            self.SOL = uniformCostSearch(self.problem, self.no_puzzle)
            self.n_expanded = search.nb_expanded
            self.n_generated = search.nb_generated
        elif self.type == "man":
            self.SOL = aStarSearch(self.problem, self.no_puzzle, searchAgent.manhattanHeuristic)
            self.n_expanded = search.nb_expanded
            self.n_generated = search.nb_generated
        elif self.type == "euc":
            self.SOL = aStarSearch(self.problem, self.no_puzzle, searchAgent.euclideanHeuristic)
            self.n_expanded = search.nb_expanded
            self.n_generated = search.nb_generated
        elif self.type == "che":
            self.SOL = aStarSearch(self.problem, self.no_puzzle, searchAgent.chebisevDistance)
            self.n_expanded = search.nb_expanded
            self.n_generated = search.nb_generated
        elif self.type == "chi":
            self.SOL = aStarSearch(self.problem, self.no_puzzle, searchAgent.chiSquaredDistance)
            self.n_expanded = search.nb_expanded
            self.n_generated = search.nb_generated
        # print(len(self.SOL))

        self.BLOCK_H = 100
        self.BLOCK_W = 300

        self.score_value = 0
        self.scorex = self.mid_w
        self.scorey = self.mid_h

        self.legendax = self.mid_w
        self.legenday = self.mid_h

        self.stivex = [self.mid_w] * 3
        self.position = [self.mid_h] * 6
        self.blockx = [0] * 6
        self.blocky = [0] * 6
        self.blockc = [(255, 255, 255)] * 6

    def display_menu(self):
        self.run_display = True

        if self.type :
            self.game.DISPLAY_W = 1400
            self.game.DISPLAY_H = 800
            self.game.display = pygame.Surface((self.game.DISPLAY_W, self.game.DISPLAY_H))
            self.game.window = pygame.display.set_mode(((self.game.DISPLAY_W, self.game.DISPLAY_H)))
            pygame.display.update()

            self.scorex = 60
            self.scorey = 20

            self.legendx = 250
            self.legendy = 20

            self.position[0], self.position[1], self.position[2], self.position[3], self.position[4], self.position[5] = 675, 575, 475, 375, 275, 175
            self.stivex[0], self.stivex[1], self.stivex[2] = 200, 550, 900


        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.show_score_and_values()
            self.show_legend()

            if not self.animation_running and not self.animation_done:
                self.prepare_the_scene()
            elif self.animation_running:
                self.start_animation(self.iterate_animation, len(self.SOL))
                if not self.animation_paused:
                    self.iterate_animation += 1
                    self.score_value -= 10
            elif self.animation_done:
                self.final_scene(len(self.SOL) - 1)

            self.blit_screen()


    def check_input(self):
        if self.game.BACK_KEY:
            self.animation_running = False
            self.game.curr_menu = self.game.alg_menu
            self.run_display = False

            self.game.DISPLAY_W = 480
            self.game.DISPLAY_H = 270
            self.game.display = pygame.Surface((self.game.DISPLAY_W, self.game.DISPLAY_H))
            self.game.window = pygame.display.set_mode(((self.game.DISPLAY_W, self.game.DISPLAY_H)))

        if self.game.START_KEY:
            self.animation_running = True

        # if self.game.PAUSE_KEY:
        #     self.animation_paused = not self.animation_paused

    def show_score_and_values(self):
        self.game.draw_text("Score: " + str(self.score_value), self.game.font_name2, 20, self.scorex, self.scorey)
        self.game.draw_text("Number of generated nodes: " + str(self.n_generated), self.game.font_name2, 20, self.scorex + 105, self.scorey + 40)
        self.game.draw_text("Number of expandaded nodes: " + str(self.n_expanded), self.game.font_name2, 20, self.scorex + 105, self.scorey + 60)

    def show_legend(self):
        self.game.draw_text('Legend: ', self.game.font_name2, 20, self.legendx, self.legendy)
        self.game.draw_text('Block0: ', self.game.font_name2, 20, self.legendx + 100, self.legendy)
        self.game.draw_text('Block1: ', self.game.font_name2, 20, self.legendx + 250, self.legendy)
        self.game.draw_text('Block2: ', self.game.font_name2, 20, self.legendx + 400, self.legendy)

        self.game.draw_block(self.Colour.give_rgb(0), self.legendx + 100 + 50, self.legendy - 10, 15, 15)
        self.game.draw_block(self.Colour.give_rgb(1), self.legendx + 250 + 50, self.legendy - 10, 15, 15)
        self.game.draw_block(self.Colour.give_rgb(2), self.legendx + 400 + 50, self.legendy - 10, 15, 15)

        if self.no_puzzle == 2 or self.no_puzzle == 3:
            self.game.draw_text('Block3: ', self.game.font_name2, 20, self.legendx + 550, self.legendy)
            self.game.draw_text('Block4: ', self.game.font_name2, 20, self.legendx + 700, self.legendy)
            self.game.draw_block(self.Colour.give_rgb(3), self.legendx + 550 + 50, self.legendy - 10, 15, 15)
            self.game.draw_block(self.Colour.give_rgb(4), self.legendx + 700 + 50, self.legendy - 10, 15, 15)

        if self.no_puzzle == 3:
            self.game.draw_text('Block5: ', self.game.font_name2, 20, self.legendx + 850, self.legendy)
            self.game.draw_block(self.Colour.give_rgb(5), self.legendx + 850 + 50, self.legendy - 10, 15, 15)

    def prepare_the_scene(self):
        the_stacks = self.START.getStacks()
        l1 = len(the_stacks)
        for i in range(l1):
            the_stack = the_stacks[i].list
            l2 = len(the_stack)
            for j in range(l2):
                self.game.draw_block(self.Colour.give_rgb(the_stack[j]), self.stivex[i], self.position[j], self.BLOCK_W, self.BLOCK_H)
                self.blockx[the_stack[j]] = self.stivex[i]
                self.blocky[the_stack[j]] = self.position[j]
                self.blockc[the_stack[j]] = self.Colour.give_rgb(the_stack[j])

    def final_scene(self, max):
        the_stacks = self.SOL[max].getStacks()
        l1 = len(the_stacks)
        for j in range(l1):
            the_stack = the_stacks[j].list
            l2 = len(the_stack)
            for l in range(l2):
                self.game.draw_block(self.blockc[the_stack[l]], self.blockx[the_stack[l]], self.blocky[the_stack[l]], self.BLOCK_W, self.BLOCK_H)

    def start_animation(self, i, max):
        time.sleep(0.5)
        if i == max:
            self.animation_running = False
            self.animation_done = True
            if self.no_puzzle == 1:
                self.score_value += 300
            if self.no_puzzle == 2:
                self.score_value += 500
            if self.no_puzzle == 3:
                self.score_value += 1000
        else:
            the_stacks = self.SOL[i].getStacks()
            l1 = len(the_stacks)
            for j in range(l1):
                the_stack = the_stacks[j].list
                l2 = len(the_stack)
                for l in range(l2):
                    self.game.draw_block(self.blockc[the_stack[l]], self.blockx[the_stack[l]], self.blocky[the_stack[l]], self.BLOCK_W, self.BLOCK_H)
                    self.blockx[the_stack[l]] = self.stivex[j]
                    self.blocky[the_stack[l]] = self.position[l]
                    self.blockc[the_stack[l]] = self.Colour.give_rgb(the_stack[l])