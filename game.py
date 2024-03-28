import pygame
from math import dist

pygame.init()
w, h = 1250, 720

class Direction:
    @staticmethod
    def update(left=0, right=0, jump=0):
        return left, right, jump

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 0.2
        self.ground = False
        self.collision_tol = 5

    def update_velo(self, left, right, jump):
        self.vel_x = 300 if right == 1 else 0 if left == 1 else 0
        self.vel_y += self.gravity
        self.vel_y = -10 if jump == 1 else self.vel_y
        print("Velocity X:", self.vel_x)
        print("Velocity Y:", self.vel_y)

    def move(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        print("Player Position:", self.rect.x, self.rect.y)

    def collisions(self, objects, walls):

        for object in objects:
            if self.rect.colliderect(object):
                print("Collision detected with object:", object)
                if abs(self.rect.right - object.left) <= self.collision_tol:
                    self.rect.right = object.left
                    self.ground = True
                elif abs(self.rect.left - object.right) <= self.collision_tol:
                    self.rect.left = object.right
                    self.ground = True
                elif self.rect.bottom >= object.top:
                    self.rect.bottom = object.top
                    self.ground = True
                    self.vel_y = 0
                elif self.rect.top <= object.bottom:
                    self.rect.top = object.bottom
                    self.ground = False
                else:
                    self.ground = False
        
        for wall in walls:
            if self.rect.colliderect(wall):
                print("Collision detected with wall:", wall)
                if self.vel_x > 0:
                    self.rect.right = wall.left
                elif self.vel_x < 0:
                    self.rect.left = wall.right

                if self.vel_y > 0:
                    self.rect.bottom = wall.top
                    self.vel_y = 0
                    self.ground = True
                    
                elif self.vel_y < 0:
                    self.rect.top = wall.bottom
                    self.vel_y = 0

    def update(self, left, right, jump, objects, walls):
        self.update_velo(left, right, jump)
        self.move()
        self.collisions(objects, walls)
        print("Player position:", self.rect.x, self.rect.y)

class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((w, h))
        pygame.display.set_caption("AI Game")
        self.clock = pygame.time.Clock()
        self.endpt = pygame.Rect(1200, h - 250, 20, 20)
        self.floor = pygame.Rect(0, h - 20, w, 200)
        self.left_wall = pygame.Rect(0, 0, 20, h)
        self.right_wall = pygame.Rect(w - 20, 0, 20, h)
        self.objects_for_lvl = [
            pygame.Rect(100, h - 100, 100, 80),
            pygame.Rect(250, h - 140, 100, 25),
            pygame.Rect(400, h - 170, 100, 25),
            pygame.Rect(535, h - 170, 75, 25),
            pygame.Rect(735, h - 170, 75, 25),
            pygame.Rect(900, h - 200, 150, 25),
            pygame.Rect(1150, h - 230, 200, 25)
        ]

        self.player = Player(30, 600)
        self.running = True
        self.reset()

    def reset(self):
        self.score = 0
        self.frame_iteration = 0

    def step(self, action):
        self.frame_iteration += 1

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                quit()

        left, right, jump = action
        self.player.update(left, right, jump, self.objects_for_lvl, [self.floor, self.left_wall, self.right_wall])

        reward, game_over = self.calculate_score()

        self._update()

        return reward, game_over, self.score

    def calculate_score(self):
        reward = 0
        game_over = False

        if self.player.rect.colliderect(self.endpt):
            reward += 10
        elif self.player.rect.colliderect(self.floor):
            reward -= 5

        self.score += reward
        game_over = self.player.rect.colliderect(self.left_wall) or self.player.rect.colliderect(self.right_wall)

        return reward, game_over

    def _update(self):    
        self.display.fill('white')  

        for obj in self.objects_for_lvl:  
            pygame.draw.rect(self.display, (128, 128, 128), obj)

        pygame.draw.rect(self.display, (128, 128, 128), self.floor)  
        pygame.draw.rect(self.display, (128, 128, 128), self.left_wall)
        pygame.draw.rect(self.display, (128, 128, 128), self.right_wall)
    
        pygame.draw.rect(self.display, (255, 0, 0), self.player.rect)  # Draw player object
        pygame.draw.rect(self.display, (0, 255, 0), self.endpt)  

        pygame.display.update()


if __name__ == "__main__":
    game = Game()
    while game.running:
        action = Direction.update(1, 0, 0) # move left once 
        print("Action:", action)
        reward, game_over, score = game.step(action)
        if game_over:
            print("Game Over")
            game.running = False