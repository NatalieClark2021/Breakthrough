import pygame
# from pygame.locals import *
import sys, os, math
from model import *
import time
from ChoiceMinimaxAgent import *

import os
from counter import *

print("Current working directory:", os.getcwd())
print("Pygame directory:", pygame.__file__)


class BreakthroughGame:

    
    def __init__(self):
        pygame.init()
        self.width, self.height = 700, 560
        self.a1algo= 'off'
        self.a2algo = 'off'
        cell = 70
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.screen.fill([255, 255, 255])
        # chessboard and workers
        self.board = 0
        self.blackchess = 0
        self.whitechess = 0
        self.outline = 0
        self.count = Counter()
        self.winner = 0

        # status 0: origin;  1: ready to move; 2: end
        # turn 1: black 2: white
        self.status = 0
        self.turn = 1
        # Variable for moving
        self.ori_x = 0
        self.ori_y = 0
        self.new_x = 0
        self.new_y = 0

        # matrix for position of chess, 0 - empty, 1 - black, 2 - white
        self.boardmatrix = [[1, 1, 1, 1, 1, 1, 1, 1],
                            [1, 1, 1, 1, 1, 1, 1, 1],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0],
                            [2, 2, 2, 2, 2, 2, 2, 2],
                            [2, 2, 2, 2, 2, 2, 2, 2]]

    
        self.eat_piece = 0
        # Caption
        pygame.display.set_caption("Breakthrough!")

        # initialize pygame clock
        self.clock = pygame.time.Clock()
        self.initgraphics()

    def run(self):

        # clear the screen
        self.screen.fill([255, 255, 255])


        if self.status == 5:
            # Black
            if self.turn == 1:
                self.ai_move(1, 1)

            elif self.turn == 2:
                self.ai_move(2, 2)


        # Events accepting
        for event in pygame.event.get():
            # Quit if close the windows

            if event.type == pygame.QUIT:
                exit()
            # reset button pressed
            if event.type == pygame.MOUSEBUTTONDOWN:

                x,y = event.pos
                if 590 <= x <= 670 and 340 <= y <= 420:
                    self.status = 5 

                #def a1
                if 565 <= x <= 625 and 95 <= y <= 125:
                    self.a1algo= "def"
                    self.defA1 = pygame.transform.scale(self.defA1, (55, 25))
                    self.screen.blit(self.defA1, (565, 90))
                #off a1
                if 630 <= x <= 690 and 95 <= y <= 125:
                    self.a1algo = "off"
                    self.offA1 = pygame.transform.scale(self.offA1, (55, 25))
                    self.screen.blit(self.offA1, (630, 90))
                #def a2
                if 565 <= x <= 625 and 195 <= y <= 235:
                    self.a2algo= "def"
                    self.defA2 = pygame.transform.scale(self.defA2, (55, 25))
                    self.screen.blit(self.defA2, (565, 210))
                #off a2
                if  630 <= x <= 690 and 195 <= y <= 235:
                    self.a2algo = "off"
                    self.offA2 = pygame.transform.scale(self.offA2, (55, 25))
                    self.screen.blit(self.offA2, (630, 210))
    #    self.screen.blit(self.defA2, (565, 195))
    #     self.screen.blit(self.offA2, (630, 195))
            # ====================================================================================
            # select chess
            elif event.type == pygame.MOUSEBUTTONDOWN and self.status == 0:
                x, y = event.pos
                coor_y = math.floor(x / 70)
                coor_x = math.floor(y / 70)
                if self.boardmatrix[coor_x][coor_y] == self.turn:
                    self.status = 1
                    self.ori_y = math.floor(x / 70)
                    self.ori_x = math.floor(y / 70)
            # check whether the selected chess can move, otherwise select other chess
            elif event.type == pygame.MOUSEBUTTONDOWN and self.status == 1:
                x, y = event.pos
                self.new_y = math.floor(x / 70)
                self.new_x = math.floor(y / 70)
                if self.isabletomove2():
                    self.movechess()
  
                elif self.boardmatrix[self.new_x][self.new_y] == self.boardmatrix[self.ori_x][self.ori_y]:
                    self.ori_x = self.new_x
                    self.ori_y = self.new_y
                    # display the board and chess
        self.display()
        # update the screen
        pygame.display.flip()

    # load the graphics and rescale them
    def initgraphics(self):
        self.board = pygame.image.load_extended('chessboard.jpg')
        self.board = pygame.transform.scale(self.board, (560, 560))
        self.blackchess = pygame.image.load_extended('blackchess.png')
        self.blackchess = pygame.transform.scale(self.blackchess, (50, 50))
        self.whitechess = pygame.image.load_extended('whitechess.png')
        self.whitechess = pygame.transform.scale(self.whitechess, (50, 50))
        self.outline = pygame.image.load_extended('square-outline.png')
        self.outline = pygame.transform.scale(self.outline, (70, 70))

        self.winner = pygame.image.load_extended('winner.png')
        self.winner = pygame.transform.scale(self.winner, (100, 40))
        self.auto = pygame.image.load_extended('play.png')
        self.auto = pygame.transform.scale(self.auto, (80, 80))

        pygame.font.init()
        self.font = pygame.font.Font(None, 30) 
        self.text_surface = self.font.render('Agent Black', True, (0, 0, 0))  

        self.defA1 =  pygame.image.load_extended('Def.png')
        self.defA1 = pygame.transform.scale(self.defA1, (60, 30))
        self.offA1 =  pygame.image.load_extended('Off.png')
        self.offA1 = pygame.transform.scale(self.offA1, (60, 30))
        
        self.font = pygame.font.Font(None, 30)  
        self.text_surface2 = self.font.render('Agent White', True, (0, 0, 0)) 


        self.defA2 =  pygame.image.load_extended('Def.png')
        self.defA2 = pygame.transform.scale(self.defA2, (60, 30))
        self.offA2 =  pygame.image.load_extended('Off.png')
        self.offA2 = pygame.transform.scale(self.offA2, (60, 30))
    # display the graphics in the window

    def display(self):
        self.screen.blit(self.board, (0, 0))
        self.screen.blit(self.auto, (590, 340))
        self.screen.blit(self.text_surface, (565, 65))  
        self.screen.blit(self.text_surface2, (565, 180))  

        #defense and offense assignment 
        self.screen.blit(self.defA1, (565, 90))
        self.screen.blit(self.offA1, (630, 90))
  

        self.screen.blit(self.defA2, (565, 210))
        self.screen.blit(self.offA2, (630, 210))

        for i in range(8):
            for j in range(8):
                if self.boardmatrix[i][j] == 1:
                    self.screen.blit(self.blackchess, (70 * j + 10, 70 * i + 10))
                elif self.boardmatrix[i][j] == 2:
                    self.screen.blit(self.whitechess, (70 * j + 10, 70 * i + 10))
        if self.status == 1:
            # only downward is acceptable
            if self.boardmatrix[self.ori_x][self.ori_y] == 1:
                x1 = self.ori_x + 1
                y1 = self.ori_y - 1
                x2 = self.ori_x + 1
                y2 = self.ori_y + 1
                x3 = self.ori_x + 1
                y3 = self.ori_y
                # left down
                if y1 >= 0 and self.boardmatrix[x1][y1] != 1:
                    self.screen.blit(self.outline,
                                     (70 * y1, 70 * x1))
                # right down
                if y2 <= 7 and self.boardmatrix[x2][y2] != 1:
                    self.screen.blit(self.outline,
                                     (70 * y2, 70 * x2))
                # down
                if x3 <= 7 and self.boardmatrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (70 * y3, 70 * x3))

            if self.boardmatrix[self.ori_x][self.ori_y] == 2:
                x1 = self.ori_x - 1
                y1 = self.ori_y - 1
                x2 = self.ori_x - 1
                y2 = self.ori_y + 1
                x3 = self.ori_x - 1
                y3 = self.ori_y
                # left up
                if y1 >= 0 and self.boardmatrix[x1][y1] != 2:
                    self.screen.blit(self.outline,
                                     (70 * y1, 70 * x1))
                # right up
                if y2 <= 7 and self.boardmatrix[x2][y2] != 2:
                    self.screen.blit(self.outline,
                                     (70 * y2, 70 * x2))
                # up
                if x3 >= 0 and self.boardmatrix[x3][y3] == 0:
                    self.screen.blit(self.outline,
                                     (70 * y3, 70 * x3))
        if self.status == 3:
            
            black_count = 0
            white_count = 0
            
            for row in self.boardmatrix:
                for cell in row:
                    if cell == 1:
                        black_count += 1
                    elif cell == 2:
                        white_count += 1
            capbywhite = 16 - black_count
            capbyblack = 16 - white_count
            print("Total Moves:", self.count.printMoves()) 
            print("captured by white", capbywhite) #D
            print("captured by black", capbyblack)
            print("a1", self.a1algo)
            print("a2", self.a2algo)
            #B
            #C
            ##good place to print B C D
            self.status = 20
        if self.status == 20:
            if self.winnerS == 'white':
                self.screen.blit(self.winner, (575, 125))   
            elif self.winnerS == 'black':
                self.screen.blit(self.winner, (575, 235))                  

            # HERE
            
    
    # def incNumMoves():
    #     global numMoves
    #     numMoves +=1
    
    # def printMoves():
    #     print(numMoves)

            
    def movechess(self):
        
        self.boardmatrix[self.new_x][self.new_y] = self.boardmatrix[self.ori_x][self.ori_y]
        self.boardmatrix[self.ori_x][self.ori_y] = 0
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.status = 0




  
    def isabletomove2(self): #FIXED 100
        atPiece = self.boardmatrix[self.ori_x][self.ori_y]
        nextPiece = self.boardmatrix[self.new_x][self.new_y] != atPiece
        
        if atPiece == 1:
            vertical = self.new_x - self.ori_x == 1
            horizontal = (self.ori_y - 1 <= self.new_y <= self.ori_y + 1)
        elif atPiece == 2:
            vertical = self.ori_x - self.new_x == 1
            horizontal = (self.ori_y - 1 <= self.new_y <= self.ori_y + 1)
        if (vertical != 1) and horizontal and nextPiece:
            if (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 2):
                return 0
            elif (self.ori_y == self.new_y and self.boardmatrix[self.new_x][self.new_y] == 1):
                return 0 
            return 1
        return 0
    
    def ai_move(self, searchtype, evaluation): #The function that chooses the player
        if searchtype == 1: #black move??
           
            return self.ai_move_minimax1(evaluation)
        elif searchtype == 2: #white move
            return self.ai_move_minimax2(evaluation)
        

    #gametype defense 2*(number_of_own_pieces_remaining) + random().

    #FIXEDish
    def ai_move_minimax1(self, function_type):
        function_type = self.a1algo
        board, nodes, piece = ChoiceMinimaxAgent(self.boardmatrix, self.turn, 3, function_type).minimax_decision()
        self.boardmatrix = board.getMatrix()
        if self.turn == 1:
            self.turn = 2
            
        elif self.turn == 2:
            self.turn = 1
            
        self.eat_piece = 16 - piece
        self.isgoalstate()
            #print(self.boardmatrix)

    def ai_move_minimax2(self, function_type):
        function_type = self.a2algo
        board, nodes, piece = ChoiceMinimaxAgent(self.boardmatrix, self.turn, 3, function_type).minimax_decision()
        self.boardmatrix = board.getMatrix()
        if self.turn == 1:
            self.turn = 2
        elif self.turn == 2:
            self.turn = 1
        self.eat_piece = 16 - piece
        self.isgoalstate()


    def isgoalstate(self): #checks for arival in goal state

        self.count.inc()
        if 2 in self.boardmatrix[0]:
            self.winnerS ='black'
            self.status = 3
        elif 1 in self.boardmatrix[7]:
            self.winnerS ='white'
            self.status = 3
            
        return False

def main():
    game = BreakthroughGame()
    while 1:
        game.run()


if __name__ == '__main__':
    main()

