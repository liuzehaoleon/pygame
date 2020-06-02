"""
-------------------------------------------------------
Lab/Assignment  Testing
-------------------------------------------------------
Author:  Zehao Liu
ID:      193074000
Email:  liux4000@mylaurier.ca
(Add a second set of Author/ID/Email if working in pairs)
__updated__ = '2020-06-01'
-------------------------------------------------------
"""

import pygame,sys,random
from pygame.locals import * # import all pygame constant

#initial
pygame.init()
pygame.display.set_caption('Snakey')
FPS=12
BASICFONT = pygame.font.Font('freesansbold.ttf', 18)

#display
UNITSIZE=20
UNITWIDTH=32
UNITHEIGHT=24
SCREENSIZE=SCREENWIDTH , SCREENHEIGHT = UNITSIZE*UNITWIDTH, UNITSIZE*UNITHEIGHT
screen = pygame.display.set_mode(SCREENSIZE)
FPSCLOCK = pygame.time.Clock()

#color
GRAY=(80,80,80)
WHITE=pygame.Color('white')
BLACK=pygame.Color('black')
RED =pygame.Color('red')
GREEN=pygame.Color('green')
DARKGREEN =pygame.Color('darkgreen')

class Snake(object):
    def __init__(self,screen):
        self.screen=screen
        self.direction='right'
        self.gamein=True

        #random snake initial position
        startx = random.randint(5, UNITWIDTH - 6)
        starty = random.randint(5, UNITHEIGHT - 6)
        self.snake=[(startx, starty),(startx-1, starty),(startx-2, starty)]#snake is a list of tuple
    
    def move(self):
        if self.direction=='left':
            newHead=(self.snake[0][0]-1,self.snake[0][1])
        elif self.direction=='right':
            newHead=(self.snake[0][0]+1,self.snake[0][1])
        elif self.direction=='up':
            newHead=(self.snake[0][0],self.snake[0][1]-1)
        elif self.direction=='down':
            newHead=(self.snake[0][0],self.snake[0][1]+1)
        self.snake.insert(0,newHead)
        
        #check if the snake hit the wall or itself
        if self.snake[0][0]==-1 or self.snake[0][0]==UNITWIDTH\
         or self.snake[0][1]==-1 or self.snake[0][1]==UNITHEIGHT:
            gameOver()
            self.gamein=False
        for snakeSection in self.snake[1:]:
            if self.snake[0]==snakeSection:
                gameOver()
                self.gamein=False
    
    def draw(self):
        for coord in self.snake:
            x=coord[0]*UNITSIZE
            y=coord[1]*UNITSIZE
            snakeSectionRect=pygame.Rect(x,y,UNITSIZE,UNITSIZE)
            pygame.draw.rect(self.screen,DARKGREEN,snakeSectionRect)
            snakeInnerSectionRect=pygame.Rect(x+4,y+4,UNITSIZE-8,UNITSIZE-8)
            pygame.draw.rect(self.screen,GREEN,snakeInnerSectionRect)
    
class Apple(object):
    def __init__(self,screen):
        self.screen=screen
        self.location=self.getRandomPosition()
    
    def getRandomPosition(self):
        x=random.randint(0,UNITWIDTH-1)
        y=random.randint(0,UNITHEIGHT-1)
        return x,y

    def draw(self):
        x=self.location[0]*UNITSIZE
        y=self.location[1]*UNITSIZE
        appleRect=pygame.Rect(x,y,UNITSIZE,UNITSIZE)
        pygame.draw.rect(self.screen,RED,appleRect)
        
def gameOver():
    font = pygame.font.Font('freesansbold.ttf', 50)
    gameOverScreen= font.render('GameOver', True, RED)
    gameOverRect=gameOverScreen.get_rect()
    gameOverRect.center = (SCREENWIDTH//2, SCREENHEIGHT//2)
    screen.blit(gameOverScreen,gameOverRect)

def drawScore(score):
    scoreSurf = BASICFONT.render('Score: %s' % score, True, WHITE)
    scoreRect = scoreSurf.get_rect()
    scoreRect.topleft = (SCREENWIDTH - 120, 20)
    screen.blit(scoreSurf, scoreRect)

def drawDescription():
    desSurf = BASICFONT.render('press r for restart or press space for halt or press q/esc for exit', True, WHITE)
    desRect = desSurf.get_rect()
    desRect.topleft = (0, 0)
    screen.blit(desSurf, desRect)

def drawGrid():
    for x in range(0, SCREENWIDTH, UNITSIZE): # draw vertical lines
        pygame.draw.line(screen, GRAY, (x, 0), (x, SCREENHEIGHT))
    for y in range(0, SCREENHEIGHT, UNITSIZE): # draw horizontal lines
        pygame.draw.line(screen, GRAY, (0, y), (SCREENWIDTH, y))

def main():
    snake1=Snake(screen)
    apple=Apple(screen) # a xy tuple
    score=0
    running = True 
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            if event.type == pygame.KEYDOWN:  # 按键
                if event.key == K_a or event.key == K_LEFT:
                    snake1.direction = 'left'
                elif event.key == K_d or event.key == K_RIGHT:
                    snake1.direction = 'right'
                elif event.key == K_w or event.key == K_UP:
                    snake1.direction = 'up'
                elif event.key == K_s or event.key == K_DOWN:
                    snake1.direction = 'down'
                elif event.key== K_r:#restart
                    main()
                elif event.key == pygame.K_q or event.key==pygame.K_ESCAPE:
                    running=False
                elif event.key==pygame.K_SPACE and snake1.gamein:
                    snake1.gamein= not snake1.gamein
        
        if snake1.gamein:
            # logic of snake eat apple
            if apple.location==snake1.snake[0]:
                apple=Apple(screen)
                score+=1
            else:
                snake1.snake.pop() #remove tail since a newHead is added into the snake
            screen.fill(BLACK)
            snake1.move()
            snake1.draw()
            apple.draw()
            drawGrid()
        drawScore(score)
        drawDescription()

        
        pygame.display.update()
        FPSCLOCK.tick(FPS)

if __name__=='__main__':
    main()

pygame.quit()
sys.exit()