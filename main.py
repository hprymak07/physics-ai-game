
from pygame import init, display, time, key, draw, image, transform
from pygame import event
from pygame.locals import Rect, K_SPACE, K_d, K_a, QUIT
from math import dist
from collections import namedtuple

from ctypes import POINTER, WINFUNCTYPE, windll
from ctypes.wintypes import BOOL, HWND, RECT 

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







def find_border_cords():
  hwnd = display.get_wm_info()['window']
  proto = WINFUNCTYPE(BOOL, HWND, POINTER(RECT))
  paramflags = (1, 'hwnd'), (2, '1prect')
  getwindowrect = proto(("GetWindowRect", windll.user32), paramflags)
  sqr = getwindowrect(hwnd)
  return sqr.top, sqr.left, sqr.bottom, sqr.right

class Direction():

    @staticmethod
    def update():
        return key.get_pressed()[K_a], key.get_pressed()[K_d], key.get_pressed()[K_SPACE]

class Player:
    def __init__(self, x, y):
        self.bdr_top, self.bdr_left, self.bdr_bottom, self.right = find_border_cords()
        self.rect = Rect(x, y, 10, 10)
        self.floor = Rect(0, self.bdr_bottom - 20, w, 200)
        self.endpt = Rect(1200, self.bdr_bottom - 250, 20, 20)
        self.objects_lvl_one = [
            Rect(100, self.bdr_bottom - 100, 100, 80),
            Rect(250, self.bdr_bottom - 140, 100, 25),
            Rect(400, self.bdr_bottom - 170, 100, 25),
            Rect(535, self.bdr_bottom - 170, 75, 25),
            Rect(735, self.bdr_bottom - 170, 75, 25),
            Rect(900, self.bdr_bottom - 200, 150, 25),
            Rect(1150, self.bdr_bottom - 230, 200, 25)
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

        screen.fill((50,50,50)) # background
        screen.blit(image.load('background.png'), (0,0)) # upload background



        for obj in self.objects_lvl_one: # platforms 
            draw.rect(screen, 'grey', obj)
        
        draw.rect(screen, 'forestgreen', (1200, self.bdr_bottom - 250, 20, 20)) # End of the lvl
        draw.rect(screen, 'red', player.rect) # Player
        draw.rect(screen, 'grey', (0, self.bdr_bottom - 20, w, 200)) # floor
        
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


    def play_step(self, action):
        self.frame_iteration += 1
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