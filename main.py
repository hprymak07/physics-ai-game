import pygame
from math import dist
from collections import namedtuple

point = namedtuple('Point', 'x, y')
w, h = 1250, 720

class Direction():
    @staticmethod
    def update(left, right, jump):
        return left, right, jump
    
class Player:
    def __init__(self, x=30, y=h / 2):
        self.rect = pygame.Rect(x, y, 10, 10)

class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((w, h))
        pygame.display.set_caption("AI Game")
        self.clock = pygame.time.Clock()

        self.collision_tol = 23
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.5
        self.ground = False
        self.acc = 0

        self.draw_game()
        self.reset()

    def draw_game(self):
        self.floor = pygame.Rect(0, h - 20, w, 200)
        self.endpt = pygame.Rect(1200, h - 250, 20, 20)
        self.objects_for_lvl = [
            pygame.Rect(100, h - 100, 100, 80),
            pygame.Rect(250, h - 140, 100, 25),
            pygame.Rect(400, h - 170, 100, 25),
            pygame.Rect(535, h - 170, 75, 25),
            pygame.Rect(735, h - 170, 75, 25),
            pygame.Rect(900, h - 200, 150, 25),
            pygame.Rect(1150, h - 230, 200, 25)
        ]

    def reset(self):
        self.player = Player()
        self.score = 1
        self.frame_iteration = 0
         
    def calc_score(self, neg):
        player_distance = [self.player.rect.x - (self.player.rect.width / 2), self.player.rect.y - (self.player.rect.height / 2)]
        endpt_distance = [self.endpt.x - (self.endpt.width / 2), self.endpt.y - (self.endpt.height / 2)]
        self.score = dist(player_distance, endpt_distance)
        game_over = True

        if neg == True: 
            reward = -10 
        else: 
            reward = 10
            self.score += 1

        return reward, game_over, self.score
#
    def step(self, action):      
        self.frame_iteration += 1

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                quit()

        dt = self.clock.tick(60) / 1000        
        reward = 0
        game_over = False
      
        left, right, jump = action
      
        self.move(left, right, jump)
      
        end = [self.player.rect.colliderect(self.endpt), self.player.rect.colliderect(self.floor) and self.player.rect.x > 200]
        [self.calc_score(True) for i in end if end[i]]
        
        self._update()

        return self.score

    def move(self, left, right, jump):

        self.acc = self.gravity
        list_in_use = self.objects_for_lvl + [self.floor]

        for objects in list_in_use:
            if self.player.rect.colliderect(objects):
                if abs(self.player.rect.right - objects.left) <= self.collision_tol:
                    self.player.rect.right = objects.left
                    self.ground = True
                elif abs(self.player.rect.left - objects.right) <= self.collision_tol:
                    self.player.rect.left = objects.right
                    self.ground = True
                elif self.player.rect.bottom >= objects.top:
                    self.player.rect.bottom = objects.top
                    self.ground = True
                    self.vel_y = 0
                elif self.player.rect.top <= objects.bottom:
                    self.player.rect.top = objects.bottom
                    self.ground = False
                else:
                    self.ground = False

        if jump == 1 and self.ground:
            self.vel_y = -10
            self.acc = 0
            self.ground = False

        self.vel_y += self.acc
        self.player.rect.y += self.vel_y
        self.vel_x = 300 #* dt
        if right == 1:
            self.player.rect.x += self.vel_x
        if left == 1:
            self.player.rect.x -= self.vel_x

        if self.player.rect.left <= 0:
            self.player.rect.x = 20
        if self.player.rect.right >= w:
            self.player.rect.x = w - self.player.rect.width

    def _update(self):
        self.display.fill('white')  
        pygame.draw.rect(self.display, (255, 0, 0), self.player.rect) 
        pygame.draw.rect(self.display, (0, 255, 0), self.endpt)  

        for obj in self.objects_for_lvl:  
            pygame.draw.rect(self.display, (128, 128, 128), obj)

        pygame.draw.rect(self.display, (0, 0, 0), self.floor)  

game = Game()

while True:
    #just a pointer you need to change state in geoffrey.py too i forgot to
    score = game.step([0,0,1])

    pygame.display.update()
