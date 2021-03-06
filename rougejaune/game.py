"""
main class for "make 4 inline" classical game using pygame module
20/11/2020
Author A.V.Korovin [a.v.korovin73@gmail.com]
"""
import sys
import numpy as np
import pygame

from common import message_box, make_sound
from .CONFIGS import *
from .grid import Grid
from .tools import placer_pion, coordinate, gagnant

pygame.font.init()
myfont = pygame.font.SysFont('monospace', 22)


class Game:
    def __init__(self):
        # init pygame display
        self.surface = pygame.display.set_mode(DISPLAY_SIZE, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
        pygame.display.set_caption('rouge contre jaune')

        # load ball images
        ball_red = pygame.image.load(BALL_RED_IMAGE).convert_alpha()
        ball_yellow = pygame.image.load(BALL_YELLOW_IMAGE).convert_alpha()
        ball_red = pygame.transform.scale(ball_red, (GRID_STEP[0]-GRID_THICKNESS,GRID_STEP[1]-GRID_THICKNESS))
        ball_yellow = pygame.transform.scale(ball_yellow, (GRID_STEP[0]-GRID_THICKNESS,GRID_STEP[1]-GRID_THICKNESS))
        self.balls = (ball_red,ball_yellow)

        self.game_over = True
        self.clock = pygame.time.Clock()

        # initialize background class
        self.grid = Grid(self.surface, GRID_NXY, GRID_STEP)

        # initialize game data
        self.restart()
        # test only
        # self.game_matrix = np.array(
        #       [[-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [ 0, -1, -1, -1, -1, -1],
        #        [ 1,  0, -1, -1, -1, -1],
        #        [ 1,  1,  0, -1, -1, -1],
        #        [ 0,  1,  1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1]])
        #
        # self.game_matrix = np.array(
        #       [[-1, -1, -1, -1, -1, -1],
        #        [ 1,  1,  0,  0, -1, -1],
        #        [ 0,  0,  0,  1, -1, -1],
        #        [ 1,  0,  1, -1, -1, -1],
        #        [ 1,  1,  0, -1, -1, -1],
        #        [ 0,  1,  1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1],
        #        [-1, -1, -1, -1, -1, -1]])


        pygame.init()

    def restart(self):
        # number of turns in the game
        self.game_turn = 0
        # lines for visualisation of successful combinations
        self.winner = []
        # initialize matrix for the game
        self.game_matrix = -np.ones(GRID_NXY,dtype=int)

    def mainloop(self):
        """
        main loop
        """
        while self.game_over:
            pygame.time.delay(150)
            self.clock.tick(10)

            # redraw game objects
            self.redraw()

            # define which player is in this turn
            player = self.game_turn % 2

            # show new unplaced ball
            x,y = pygame.mouse.get_pos()
            col = int(x // GRID_STEP[0])
            cur_ball = self.balls[player]
            y = (GRID_STEP[1]-cur_ball.get_height())/2
            x -= cur_ball.get_width()/2
            x = 0 if x<0 else x
            x = x if x<DISPLAY_SIZE[0]-cur_ball.get_width() else DISPLAY_SIZE[0]-cur_ball.get_width()
            self.surface.blit(cur_ball, (x,y))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # pygame.quit()
                    sys.exit()
                if event.type==pygame.MOUSEMOTION:
                    pass
                if event.type==pygame.MOUSEBUTTONDOWN:
                    isPlaced,self.game_matrix,self.winner = placer_pion(player, col, self.game_matrix)
                    if isPlaced:
                        if self.winner:
                            make_sound(2)

                            # redraw game objects to show winner combinations
                            self.redraw()

                            self.surface.blit(myfont.render(MESSAGE.WON.format(PLAYERS[player],self.game_turn),True, ((255,0,0),(255,255,0))[player]),(10,10))

                            # refresh image
                            pygame.display.flip()
                            pygame.display.update()

                            message_box(MESSAGE.WON.format(PLAYERS[player],self.game_turn), MESSAGE.AGAIN)
                            self.restart()

                            break
                        else:
                            self.game_turn += 1



            # refresh image
            pygame.display.flip()
            pygame.display.update()


    def redraw(self):  # redraw game objects
        # draw background image
        self.grid.draw()

        # draw placed balls
        for ix in range(self.game_matrix.shape[0]):
            for iy in range(self.game_matrix.shape[1]):
                player = self.game_matrix[ix,iy]
                if player!=-1:
                    ball = self.balls[player]
                    x,y = coordinate((ix,iy))
                    x -= ball.get_width()/2
                    y -= ball.get_height()/2
                    self.surface.blit(ball, (x,y))

        # draw lines for the winner combinations
        for line in self.winner:
            pygame.draw.line(self.surface, (255, 0, 0), coordinate(line[0]), coordinate(line[1]), 5)

