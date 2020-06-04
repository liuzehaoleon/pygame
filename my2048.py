"""
-------------------------------------------------------
Lab/Assignment  Testing
-------------------------------------------------------
Author:  Zehao Liu
ID:      193074000
Email:  liux4000@mylaurier.ca
(Add a second set of Author/ID/Email if working in pairs)
__updated__ = '2020-06-02'
-------------------------------------------------------
"""

import pygame, random
from pygame.locals import *

# initial
pygame.init()

UNITSIZE = 50
UNITWIDTH = UNITHEIGHT = 4
SCREENWIDTH = SCREENHEIGHT = UNITSIZE * UNITHEIGHT
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
BASICFONT = pygame.font.Font('freesansbold.ttf', 30)

# Color
LIGHTGRAY = pygame.Color('lightgray')
GRAY=pygame.Color('gray')
WHITE = pygame.Color('white')
BLACK = pygame.Color('black')
RED = pygame.Color('red')
Metallic_gold = 212,175,55


class Game():

    def __init__(self, screen):
        self.gamein = True
        self.gameSet = self._getEmptySet()
        self.move = None
        self.screen = screen
        self._largest

    def _getEmptySet(self):
        '''this a empty number set'''
        emptySet = []
        for i in range(UNITHEIGHT):
            emptySet.append([])
            for _ in range(UNITWIDTH):
                emptySet[i].append(None)
        return emptySet
    
    def getRandomNum(self):
        '''random choice a num and place it into a random place'''
        gameover = False
        num = random.choice((2, 4))
        temp = []  # a list of tuple
        for i in range(UNITHEIGHT):
            for j in range(UNITWIDTH):
                if self.gameSet[i][j] == None:
                    temp.append((i, j))
        x, y = random.choice(temp)
        if temp != []:
            self.gameSet[x][y] = num
            self.largest = num
        else:
            gameover = True
        return gameover
    
    def checkOver(self):
        '''a gamein var define whether gameOver'''
        self.gamein = False
        if self.ableMoveUp() or self.ableMoveDown() or self.ableMoveLeft()or self.ableMoveRight():
            self.gamein = True
        return
    
    def drawGrid(self):
        '''draw basic game layout/background'''
        for x in range(0, SCREENWIDTH, UNITSIZE):  # draw vertical lines
            pygame.draw.line(screen, LIGHTGRAY, (x, 0), (x, SCREENHEIGHT))
        for y in range(0, SCREENHEIGHT, UNITSIZE):  # draw horizontal lines
            pygame.draw.line(screen, LIGHTGRAY, (0, y), (SCREENWIDTH, y))
        return
    
    def moveUp(self):

        def tighten(cloumn):
            newCloumn = []
            for a in cloumn:
                if a != None:
                    newCloumn.append(a)
            for _ in range(UNITWIDTH - len(newCloumn)):
                newCloumn.append(None)
            return newCloumn

        def merge(cloumn):
            pair = False
            newCloumn = []
            for i in range(UNITWIDTH):
                if pair:
                    newCloumn.append(2 * cloumn[i])
                    pair = False
                else:
                    if i + 1 < len(cloumn) and cloumn[i] != None and cloumn[i] == cloumn[i + 1]:
                        pair = True
                        newCloumn.append(None)
                    else:
                        newCloumn.append(cloumn[i])
            return newCloumn
        
        i = 0
        for column in self.gameSet:
            newOne = tighten(merge(tighten(column)))
            self.gameSet[i] = newOne
            i += 1
        return
    
    def _invert_UD(self):
        i = 0
        for column in self.gameSet:
            self.gameSet[i] = column[::-1]
            i += 1
        return
    
    def _invert_LR(self):
        self.gameSet = self.gameSet[::-1]
    
    # y=-x transpose
    def _transpose(self):
        new_gameSet = []
        for i in range(UNITWIDTH):
            for j in range(UNITHEIGHT): 
                if i == 0:
                    new_gameSet.append([])
                new_gameSet[j].append(self.gameSet[i][j])
        self.gameSet = new_gameSet
        return
    
    def moveDown(self):
        
        self._invert_UD()
        self.moveUp()
        self._invert_UD()
        return 
    
    def moveLeft(self):
        self._transpose()
        self.moveUp()
        self._transpose()
        return 
    
    def moveRight(self):
        self._transpose()
        self.moveDown()
        self._transpose()
    
    def ableMoveLeft(self):
        able = False
        # there is a hollow exit
        for i in range(UNITWIDTH - 1):
            for j in range(UNITHEIGHT):
                for x in range(i, UNITHEIGHT - 1):
                    if self.gameSet[i][j] == None and self.gameSet[x][j] != None:
                        able = True
        # there can be merge
        for i in range(UNITWIDTH - 1):
            for j in range(UNITHEIGHT):
                if self.gameSet[i][j] == self.gameSet[i + 1][j]:
                    able = True
        return able
    
    def ableMoveRight(self):
        self._invert_LR()
        able = self.ableMoveLeft()
        self._invert_LR()
        return able
    
    def ableMoveUp(self):
        self._transpose()
        able = self.ableMoveLeft()
        self._transpose()
        return able
    
    def ableMoveDown(self):
        self._invert_UD()
        able = self.ableMoveUp()
        self._invert_UD()
        return able
    
    def draw(self):
        for i in range(UNITWIDTH):
            for j in range(UNITHEIGHT):
                if self.gameSet[i][j] != None:
                    numSurf = BASICFONT.render('{}'.format(self.gameSet[i][j]), True, WHITE)
                    numRect = numSurf.get_rect()
                    numRect.topleft = (i * UNITSIZE + 10, j * UNITSIZE + 10)
                    self.screen.blit(numSurf, numRect)
    
    def drawGameOver(self):
        font = pygame.font.Font('freesansbold.ttf', 30)
        gameOverScreen = font.render('GameOver', True, RED)
        gameOverRect = gameOverScreen.get_rect()
        gameOverRect.center = (SCREENWIDTH // 2, SCREENHEIGHT // 2)
        screen.blit(gameOverScreen, gameOverRect)
    
    def _largest(self):
        for i in range(UNITWIDTH):
            for j in range(UNITHEIGHT):
                if self.gameSet[i][j] is not None and self.gameSet[i][j] > self.largest:
                    self.largest = self.gameSet[i][j]
        return
    
    def drawWin(self):
        print('here')
        self._largest()
        if int(self.largest) >= 8:
            screen.fill(GRAY)
            font = pygame.font.Font('freesansbold.ttf', 25)
            winScreen = font.render('Congratulation', True, Metallic_gold)
            winRect = winScreen.get_rect()
            winRect.center = (SCREENWIDTH // 2, SCREENHEIGHT // 2)
            screen.blit(winScreen, winRect)

                
game = Game(screen)
game.getRandomNum()
running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_a:
                game.move = 'left'
            elif event.key == K_d:
                game.move = 'right'
            elif event.key == K_w:
                game.move = 'up'
            elif event.key == K_s:
                game.move = 'down'
    
    if game.gamein:
        screen.fill(BLACK)
        game.drawGrid()

        # if the key be press
        if game.move != None:
            print('A new loop')
            print(game.move)
            temp = game.gameSet
            if game.move == 'left' and game.ableMoveLeft():
                game.moveLeft()
            elif game.move == 'right' and game.ableMoveRight():
                game.moveRight()
            elif game.move == 'up' and game.ableMoveUp():
                game.moveUp()
            elif game.move == 'down' and game.ableMoveDown():
                game.moveDown()
            if temp != game.gameSet:
                gameover = game.getRandomNum()
                if gameover:
                    game.gamein = False
            game.move = None

        game.draw()
        game.checkOver()
    else:
        screen.fill(GRAY)
        game.drawGameOver()
    
    game.drawWin()    
    pygame.display.update()
pygame.quit()
