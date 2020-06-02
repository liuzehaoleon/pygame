"""
-------------------------------------------------------
Lab/Assignment  Testing
-------------------------------------------------------
Author:  Zehao Liu
ID:      193074000
Email:  liux4000@mylaurier.ca
(Add a second set of Author/ID/Email if working in pairs)
__updated__ = '2020-05-18'
-------------------------------------------------------
"""

import pygame
from RGB_code import *
from pygame.locals import *

pygame.init()

# 设置图标与标题
pygame.display.set_caption("壁球：鼠标演练")
icon = pygame.image.load('source//image//box.png')
pygame.display.set_icon(icon)

# any image be loaded become a surface object
ball = pygame.image.load('source//image//ball.gif')


def main():
    WIDTH = 600
    HEIGHT = 400
    # Way to change into a full screen games
    # Vinfo=pygame.display.Info()
    # WIDTH=Vinfo.current_w
    # HEIGHT=Vinfo.current_h
    
    # screen is also a surface object
    screen = pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
    # /or/ screen=pygame.display.set_mode((WIDTH,HEIGHT),NOFRAME) 无边框模式
    # /or/ screen=pygame.display.set_mode((WIDTH,HEIGHT),FULLSCREEN) 全屏模式
    # print(pygame.display.Info())

    speed = [10, 10]
    is_moving = True
    # After get_rect the ballrect become a rectangular object
    ballrect = ball.get_rect()
    fps = 100
    fclock = pygame.time.Clock()    
    running = True
    
    bgcolor = pygame.Color('black')
    
    def RGBChannel(a):
        return 0 if a < 0 else (255 if a > 255 else int(a))
    
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            # the basic controll of player
            elif event.type == VIDEORESIZE:
                # size[0] is width and size[1] is height
                WIDTH, HEIGHT = event.size[0], event.size[1]
                pygame.display.set_mode((WIDTH, HEIGHT), RESIZABLE)
                
            elif event.type == KEYDOWN:
                if event.key == K_RIGHT or event.key == K_d:
                    speed[0] += 5 
                elif event.key == K_LEFT or event.key == K_a:
                    speed[0] -= 5
                elif event.key == K_DOWN or event.key == K_s:
                    speed[1] += 5
                elif event.key == K_UP or event.key == K_w:
                    speed[1] -= 5
                elif event.key == K_ESCAPE or event.key == K_q:
                    running = False
                elif event.key == K_r:
                    main()
    
            elif event.type == MOUSEMOTION:
                right_click = event.buttons[0]
                if right_click == True:
                    is_moving = False
                    ballrect.move_ip(event.rel)
                    
            elif event.type == MOUSEBUTTONUP:
                is_moving = True
    
        # initial ball moving speed
        if is_moving and pygame.display.get_active():
            ballrect = ballrect.move(speed[0], speed[1])
        
        # rebound of the ball
        if ballrect.left < 0 or ballrect.right > WIDTH:
            speed[0] = -speed[0]
    #         note: the followed two if codes are necessary
            if ballrect.left < 0 and speed[0] < 0:
                speed[0] = -speed[0]
            if ballrect.right > WIDTH and speed[0] > 0:
                speed[0] = -speed[0]
        if ballrect.top < 0 or ballrect.bottom > HEIGHT:
            speed[1] = -speed[1]
            # note: the followed two if codes are necessary
            if ballrect.top < 0 and speed[1] < 0:
                speed[1] = -speed[1]
            if ballrect.bottom > HEIGHT and speed[1] > 0:
                speed[1] = -speed[1]
            
        bgcolor.r = RGBChannel(ballrect.left * 255 / WIDTH)
        bgcolor.g = RGBChannel(ballrect.top * 255 / HEIGHT)
        bgcolor.b = RGBChannel(min(speed[0], speed[1]) / max(speed[0], speed[1]))  # 有些不太懂
        
        # 填补ball的运动轨迹
        screen.fill(bgcolor)
        
        # blit  将ball的图像-surface obj 绘制到 ballrect-surface obj 上  
        screen.blit(ball, ballrect)
        
        # tick 控制窗口的刷新速度
        fclock.tick(fps)
        
        # untilities
        pygame.display.update()


main()

pygame.quit()
