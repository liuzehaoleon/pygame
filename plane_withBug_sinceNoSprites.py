"""
-------------------------------------------------------
Lab/Assignment  Testing
-------------------------------------------------------
Author:  Zehao Liu
ID:      193074000
Email:  liux4000@mylaurier.ca
(Add a second set of Author/ID/Email if working in pairs)
__updated__ = '2020-05-24'
-------------------------------------------------------
"""

import pygame, sys, random, time
from pygame.locals import *
from RGB_code import *


class Plane():

    def __init__(self):
        self.bulletList = []
        self.lives=1
        
        # the dimension of the plane
        self.width = 100
        self.height = 124
        # the position of the plane
        self.x = 180
        self.y = 600
        # the constant moving speed of the plane
        self.speed = 20
        # temp speed created by hold the buttom  - list
        self.handleSpeed = [0, 0]
        # the image of plan
        self.image = pygame.image.load("source//image//plane.png")
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        self.window = screen  # self.window is a Surface object
        
        self.biu = False
        return
    
    def crash(self):
        self.image.fill(BLACK)
        return
    
    def draw(self):
        self.window.blit(self.image, (self.x, self.y))
        return
    
    def handle(self):
        if self.x < 0:
            self.x = 0
        elif self.x + self.width > WIDTH:
            self.x = WIDTH - self.width
        else:
            self.x += self.handleSpeed[0]
        
        if self.y < 0:
            self.y = 0
        elif self.y + self.height > HEIGHT:
            self.y = HEIGHT - self.height
        else:
            self.y += self.handleSpeed[1]
        self.rect.x , self.rect.y = self.x, self.y
            
    def shoot(self):
        if self.biu:
            bul_obj = Bullet(self)
            bul_obj.draw()
            self.bulletList.append(bul_obj)
            self.biu = False
        return


class Bullet():

    def __init__(self, plane):
        self.window = screen
        self.speed = 12
        self.width = 10
        self.height = 16

        self.x = plane.x + plane.width / 2
        self.y = plane.y - self.height

        image = pygame.image.load("source//image//bullet.png")
        self.image = pygame.transform.scale(image, (self.width, self.height))
        
        self.rect = self.image.get_rect()
        
    def get_pos(self):
        return (self.x, self.y, self.width, self.height)
    
    def draw(self):
        self.window.blit(self.image, (self.x, self.y))
    
    def move(self):
        self.y -= self.speed
        self.rect.x,self.rect.y=self.x,self.y


class Enemy():
    
    def __init__(self):
        self.window = screen
        self.width = 50
        self.height = 40
        
        self.speed = [10, 4]
        
        self.y = 0
        self.x = random.randrange(0, WIDTH - self.width)
        
        image = pygame.image.load("source//image//enemy.png")
        self.image = pygame.transform.scale(image, (self.width, self.height))
        
        self.rect = self.image.get_rect()
        
    def get_pos(self):
        return (self.x, self.y, self.width, self.height)
    
    def move(self):
        # rebound
        if self.x + self.width > WIDTH or self.x < 0:
            self.speed[0] = -self.speed[0]
            if self.x + self.width > WIDTH:
                self.x = WIDTH - self.width
            elif self.x < 0:
                self.x = 0
#         elif self.y + self.height > HEIGHT or self.y < 0:
#             self.y = 0
#             self.speed[1] = -self.speed[1]
        else:
            self.x += self.speed[0]
            self.y += self.speed[1]
        self.rect.x , self.rect.y = self.x, self.y
            
    def draw(self):
        self.window.blit(self.image, (self.x, self.y))  
        
    def crash(self):
        self.image.fill(BLACK)

            
class Manager():

    def __init__(self, plane):
        self.bulletList = plane.bulletList  # contain bullet object
        self.enemyList = []
        self.plane = plane  # Plane object
        self.score = 0

    # # bulletList manage    
    def bulletList_untility(self):
        self.plane.shoot()
        i = 0
        # move, clear
        while i < len(self.bulletList):
            self.bulletList[i].move()
            self.bulletList[i].draw()
            if self.bulletList[i].y < 0:
                self.bulletList = self.bulletList[:i] + self.bulletList[i + 1:]
            i += 1
        # refresh bulletList in Plane
        self.plane.bulletList = self.bulletList
        return
    
    # # enemyList manage
    def enemy_untility(self):
        '''Include enmey emrge, move and clear'''            
        if len(self.enemyList) < 3:
            enemy = Enemy()
            if random.choice((1, 0)):
                enemy.speed[0] = -enemy.speed[0]
            enemy.draw()
            self.enemyList.append(enemy)
        # move and clear
        i = 0
        while i < len(self.enemyList):
            self.enemyList[i].move()
            self.enemyList[i].draw()
            if self.enemyList[i].y > HEIGHT:
                self.enemyList = self.enemyList[:i] + self.enemyList[i + 1:]
            i += 1
    
    def plane_untility(self):
        self.plane.draw()
        self.plane.handle()
        
    def collide(self):
#         for i in range(len(self.bulletList)):
#             for j in range(len(self.enemyList)):
#                 if self.bulletList[i].rect.colliderect(self.enemyList[j].rect):
#                     self.enemyList[j].crash()
#                     self.bulletList = self.bulletList[:i] + self.bulletList[i + 1:]
#                     self.enemyList = self.enemyList[:j] + self.enemyList[j + 1: ]
#                     self.score += 1
        for z in range(len(self.enemyList)):
            if self.plane.rect.colliderect(self.enemyList[z].rect):
                print(self.plane.lives)
                self.plane.lives-=1
                self.enemyList[z].crash()
                print(z)
                print(len(self.enemyList))
                self.enemyList.remove(z)
    
    def update(self):
        '''basic holding motion of the plane'''
        self.bulletList_untility()
        self.enemy_untility()
        self.plane_untility()
        self.collide()



pygame.init()

SIZE = WIDTH, HEIGHT = 480, 800
screen = pygame.display.set_mode(SIZE)

background = pygame.image.load("source//image//background.png")
background = pygame.transform.scale(background, (480, 800))

fps = 300
fclock = pygame.time.Clock()

myplane = Plane()
controller = Manager(myplane)

running = True
while running:

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        if event.type == KEYDOWN:
            if event.key == K_a or event.key == K_LEFT:
                myplane.handleSpeed[0] = -myplane.speed
            elif event.key == K_d or event.key == K_RIGHT:
                myplane.handleSpeed[0] = myplane.speed
            elif event.key == K_s or event.key == K_DOWN:
                myplane.handleSpeed[1] = myplane.speed
            elif event.key == K_w or event.key == K_UP:
                myplane.handleSpeed[1] = -myplane.speed
            elif event.key == K_SPACE:
                myplane.biu = True
            elif event.key == K_ESCAPE:
                running = False
    
        if event.type == KEYUP:
            myplane.handleSpeed = [0, 0]
    
    if myplane.lives==0:
        running=False
    
    screen.blit(background, (0, 0))
    if pygame.display.get_active():
        controller.update()
        
    
        
    fclock.tick(fps)
    pygame.display.update()

sys.exit()
pygame.quit()
    
