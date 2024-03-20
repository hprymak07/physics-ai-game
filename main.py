
import pygame
from pygame import init, display, time, key, draw
from pygame import event
from pygame.locals import Rect, K_SPACE, K_d, K_a, QUIT
from math import dist
from collections import namedtuple

# pygame setup
init()
w, h = 1250,720
screen = display.set_mode((w, h))
dt = 0
point = namedtuple('Point', 'x, y')

# reset
# reward
# play(action) --> direction
# game iteration
# is_collision

class Direction():

    @staticmethod
    def update():
        return key.get_pressed()[K_a], key.get_pressed()[K_d], key.get_pressed()[K_SPACE]

class Player:
    def __init__(self, x, y):
        self.rect = Rect(x, y, 10, 10)
        self.floor = Rect(0, 370, w, 200)
        self.endpt = Rect(1150, 90, 20, 20)
        self.objects_lvl_one = [
            Rect(100, 300, 100, 100),
            Rect(250, 220, 100, 25),
            Rect(400, 150, 100, 25),
            Rect(535, 150, 75, 25),
            Rect(635, 170, 75, 25),
            Rect(735, 150, 75, 25),
            Rect(900, 130, 200, 25),
            Rect(1150, 90, 20, 20)
        ]
        self.collision_tol = 23
        self.vel_y = 0
        self.gravity = 0.5
        self.ground = False
        self.acc = 0

    def reset(self):
        self.current_pos = point(30, h / 2)
        draw.rect(point, 10,10)
        self.frame_iteration = 0
        

    def draw_lvl(self):
        screen.fill((225, 225, 225)) # background

        for obj in self.objects_lvl_one: # platforms 
            draw.rect(screen, 'black', obj)
            
        draw.rect(screen, 'forestgreen', (1150, 90, 20, 20)) # End of the lvl
        draw.rect(screen, 'red', player.rect) # Player
        draw.rect(screen, 'black', (0, 370, w, 200)) # floor
        
    def update(self, dt):
        left, right, jump = Direction.update()

        self.acc = self.gravity
        list_in_use = self.objects_lvl_one + [self.floor]

        for objects in list_in_use:
            if self.rect.colliderect(objects):
                if abs(self.rect.right - objects.left) <= self.collision_tol:
                    self.rect.right = objects.left
                    self.ground = True
                elif abs(self.rect.left - objects.right) <= self.collision_tol:
                    self.rect.left = objects.right
                    self.ground = True
                elif self.rect.bottom >= objects.top:
                    self.rect.bottom = objects.top
                    self.ground = True
                    self.vel_y = 0
                elif self.rect.top <= objects.bottom:
                    self.rect.top = objects.bottom
                    self.ground = False
                else:
                    self.ground = False

        if jump and self.ground:
            self.vel_y = -10
            self.acc = 0
            self.ground = False

        self.vel_y += self.acc
        self.rect.y += self.vel_y
        self.vel_x = 300 * dt

        if right:
            self.rect.x += self.vel_x
        if left:
            self.rect.x -= self.vel_x
        
        if player.rect.left <= 0:
           player.rect.x = 20
        if player.rect.right >= w:
           player.rect.x = w - self.rect.width

    def calc_score(self):
        player_distance = [self.rect.x - (self.rect.width / 2), self.rect.y - (self.rect.height / 2)]
        endpt_distance = [self.endpt.x - (self.endpt.width / 2), self.endpt.y - (self.endpt.height / 2)]
        distance = dist(player_distance, endpt_distance)
        return distance
    
    
    def is_game_over(self):    
      game_over = [player.rect.colliderect(self.endpt), player.rect.colliderect(self.floor) and player.rect.x > 200]
      return [player.calc_score() for i in game_over if game_over[i]]

player = Player(30, h / 2)


while True:
    for ev in event.get():
        if ev.type == QUIT:
            break

    player.draw_lvl()
    player.is_game_over() 


    display.flip()
    dt = time.Clock().tick(60) / 1000
    player.update(dt)

display.quit()