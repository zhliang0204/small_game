import pygame
import os
import sys
import random
import math
import time
from pygame.locals import *

global Bullets, Bees, Width, Height, keys, Gamestatus, Lives, Score
Bullets = []
Bees = []
Gamestatus = False
Lives = 3
Score = 0
Width = 600
Height = 480

backgroud_img_filename = 'sky.jpg'
bee_img_filename = 'bee.png'
plane_img_filename = 'plane.png'


class Mypoint():
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def get_x(self):
        return self.x
    def get_y(self):
        return self.y
    def set_x(self, x):
        self.x = x
    def set_y(self, y):
        self.y = y


class Mymaterials():
    def __init__(self, x, y, vel, angle):
        self.pos_x = x
        self.pos_y = y
        self.vel = vel
        self.angle = angle
        

        self.alive = True

    def load_pic(self, picname):
        self.img = pygame.image.load(picname).convert_alpha()
        self.imgwidth = self.img.get_size()[0]
        self.imgheight = self.img.get_size()[1]
        return self.img

    def draw_img(self, surface):
        surface.blit(self.img, [(self.pos_x), (self.pos_y)])

    def set_size_angle(self, planewidth, planeheight):
        self.imgwidth = planewidth
        self.imgheight = planeheight
        self.img = pygame.transform.smoothscale(self.img, (self.imgwidth, self.imgheight))
        self.img = pygame.transform.rotate(self.img, self.angle)
        self.rect = Rect(self.pos_x, self.pos_y, self.imgwidth, self.imgheight)

    def rotate_m(self):
        self.img = pygame.transform.rotate(self.img, self.angle)
       

    def set_alive(self, status):
        self.alive = status
        
    def get_alive(self):
        return self.alive

    def update(self):
        if abs(self.vel) > 0.003:
            if self.vel > 0:
                self.vel -= 0.005
            if self.vel < 0:
                self.vel += 0.005
            
        self.vel_y = self.vel * math.sin(math.radians(self.angle))
        self.vel_x = self.vel * math.cos(math.radians(self.angle))
        self.pos_x += self.vel_x*2
        self.pos_y += self.vel_y*2
        if self.pos_x > Width - self.imgwidth:
            self.pos_x = 0
        if self.pos_x < 0:
            self.pos_x = Width - self.imgwidth
        if self.pos_y < 0:
            self.pos_y = Height - self.imgheight
        if self.pos_y > Height:
            self.pos_y = 0
        self.rect = Rect(self.pos_x, self.pos_y, self.imgwidth, self.imgheight)

    def get_vel(self):
        return [self.vel_x, self.vel_y]

    def get_myrect(self):
        return self.rect

class Mybee(Mymaterials):
    def __init__(self, x, y, vel, angle):
        Mymaterials.__init__(self, x, y, vel, angle)
    def update(self):
        
        self.vel_y = self.vel * math.sin(math.radians(self.angle))
        self.vel_x = self.vel * math.cos(math.radians(self.angle))
        self.pos_x += self.vel_x*2
        self.pos_y += self.vel_y*2
        if self.pos_x > Width - self.imgwidth:
            self.pos_x = 0
        if self.pos_x < 0:
            self.pos_x = Width - self.imgwidth
        if self.pos_y < 0:
            self.pos_y = Height - self.imgheight - 30
        if self.pos_y > Height:
            self.pos_y = 0
        self.rect = Rect(self.pos_x, self.pos_y, self.imgwidth, self.imgheight)

    
class MyBullet():
    def __init__(self, x, y, vel_x, vel_y):
        self.pos_x = x
        self.pos_y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.color = (250, 20, 20)
        self.alive = True
        self.rect = Rect(0,0,4,4)

    def draw_bullet(self, surface):
        pygame.draw.circle(surface, self.color, [int(self.pos_x),int(self.pos_y)], 4, 0)

    def set_alive(self, status):
        self.alive = status

    def get_alive(self):
        return self.alive

    def update(self):
        self.pos_x += self.vel_x *10
        self.pos_y += self.vel_y *10
        if self.pos_x < 0 or self.pos_x > Width:
            self.alive = False
        if self.pos_y < 0 or self.pos_y > Height:
            self.alive = False
        self.rect = Rect(self.pos_x, self.pos_y, 4, 4)

    def get_myrect(self):
        return self.rect
            
        
def fire_bullet(myplane, keys):
    if keys[K_SPACE]:
        new_bullet = MyBullet(int(myplane.pos_x + myplane.get_myrect()[2]/2), int(myplane.pos_y),0, -3)
        Bullets.append(new_bullet)
    
def move_plane(plane,keys):
    if keys[K_LEFT]:
        plane.vel = -1.5
    if keys[K_RIGHT]:
        plane.vel = 1.5

'''
def rotate_plane(plane, keys):
    if keys[K_LEFT]:
        plane.angle += 10
        plane.rotate_m()
    if keys[K_RIGHT]:
        plane.angle -= 10
        plane.rotate_m()
'''
    
        

def collision(m1, m2):
    rect1 = m1.get_myrect()
    rect2 = m2.get_myrect()
    #len1 = max(rect1[2], rect1[3])
    #len2 = max(rect2[2],rect2[3])
    l1 = rect1[0]
    r1 = rect1[2]
    u1 = rect1[1]
    d1 = rect1[3] 

    l2 = rect2[0]
    r2 = rect2[2]
    u2 = rect2[1]
    d2 = rect2[3] 
    if abs(l1 + r1/2.0 - l2 - r2/2.0) < max(r1/2.0, r2/2.0) and abs(u1 + d1/2.0 - u2 - d2/2.0) < max(d1/2.0, d2/2.0):
        return True
    else:
        return False
    
def surface_print(surface, font, x, y, text, color = (255, 255, 255)):
    imgText = font.render(text, True, color)
    surface.blit(imgText, (x,y))
        
        
pygame.init()
start_time = time.time()
time_count = 0

clock = pygame.time.Clock()
screen = pygame.display.set_mode((Width, Height), 0, 32)
background = pygame.image.load(backgroud_img_filename).convert()
screen.blit(background, [0,0])
font = pygame.font.Font(None, 30)

plane = Mymaterials(270, Height - 61, 0, 0)
plane.load_pic(plane_img_filename)
plane.set_size_angle(55,61)

plane.draw_img(screen)


while True:
    clock.tick(20) 
    ticks = pygame.time.get_ticks()
    screen.blit(background , [0,0])
    plane.draw_img(screen)
    surface_print(screen, font, 0, 0, "Your lives: " + str(Lives))
    surface_print(screen, font, Width - 150, 0, "Your Score: " + str(Score))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            os._exit(1)
        if event.type == KEYDOWN:
            if event.key == pygame.K_RETURN:
                Gamestatus = True
                Lives = 3
                Score = 0
                Bees = []
                Bullets = []
                
    if Gamestatus == False:
        surface_print(screen, font, 120, Height/2, "please press enter to begin the game")
        
            
    if Lives == 0: 
        Gamestatus = False
        surface_print(screen, font, 120, Height/2, "please press enter to begin the game")
        surface_print(screen, font ,120, Height/2 - 50, "Your final score is: " + str(Score))
        Gamestatus = False
            
    if Gamestatus == True and Lives > 0:
        keys = pygame.key.get_pressed()        
        move_plane(plane, keys)
        #rotate_plane(plane, keys)
        plane.update()
        fire_bullet(plane, keys)                      
        cur_time= time.time()
        if (cur_time - start_time)> time_count * 3 and (cur_time - start_time)< (time_count + 1)*3:
            bee_x = random.randint(24, Width-24)
            bee_y = random.randint(18, Height - 70)
            bee_angle = random.randint(0, 360)
            bee_vel = 1.5   
            bee = Mybee(bee_x, bee_y, bee_vel, bee_angle)
            bee.load_pic(bee_img_filename)
            bee.set_size_angle(32,26)
            Bees.append(bee)
            time_count += 1

        for bee in Bees:
            bee.update()
            bee.draw_img(screen)

        for bullet in Bullets:
            bullet.update()                  
            bullet.draw_bullet(screen)

        for bullet in Bullets:
            for bee in Bees:
                res = collision(bullet, bee)
                if res == True:
                    bee.alive = False
                    bullet.alive = False
                        
        for bullet in Bullets:
            if bullet.alive == False:
                Bullets.remove(bullet)

        for bee in Bees:
            if bee.alive == False:
                Score += 10
                Bees.remove(bee)

        for bee in Bees:
            res = collision(plane, bee)
            if res == True:
                plane.alive = False
                bee.alive = False


        if plane.alive == False:
            #print "inercondition"
            #print plane.alive
            Lives -= 1
            plane = Mymaterials(270, Height - 61, 0, 0)
            plane.load_pic(plane_img_filename)
            plane.set_size_angle(55,61)

    #print plane.alive         
                                
    pygame.display.update()
