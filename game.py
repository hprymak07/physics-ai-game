import pygame

pygame.init()
w, h = 1250, 700

class Direction:
    @staticmethod
    def update(left, right, jump):
        return left, right, jump

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.vel_x = 0
        self.vel_y = 0
        self.gravity = 1
        self.ground = False
        self.collision_tol = 5
    def update_velo(self, left, right, jump, objects, walls):

        if left == 1:
            self.vel_x = -10
        elif right == 1:
            self.vel_x = 10
        else:
            self.vel_x = 0



        if jump == 1 and self.ground:

            self.vel_y = -10
        else:
            self.vel_y += self.gravity


    def move(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

    def collisions(self, objects, walls):
        self.ground = False
        for object in objects:
            if self.rect.colliderect(object):
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
                if self.vel_y > 0:
                    self.rect.bottom = wall.top - 10
                    self.vel_y = 0
                    self.ground = True
                else:
                    self.ground = False
    def update(self, left, right, jump, objects, walls):
        self.collisions(objects, walls)
        self.update_velo(left, right, jump, objects, walls)
        self.move()
        return self.rect.x, self.rect.y

class Game:
    def __init__(self):
        self.display = pygame.display.set_mode((w, h))
        pygame.display.set_caption("AI Game")
        self.clock = pygame.time.Clock()
        self.endpt = pygame.Rect(1200, h - 250, 20, 20)
        self.floor = pygame.Rect(0, h - 20, w, 200)
        self.left_wall = pygame.Rect(0, 0, 20, h)
        self.right_wall = pygame.Rect(w - 20, 0, 20, h)
        self.roof = pygame.Rect(0, 20, w, 20)
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
        self.calculate_score()
        self.score = 0
        self.frame_iteration = 0
        self.player.rect.x = 30
        self.player.rect.y = 600
        self.ground = True
    def step(self, action):
        self.frame_iteration += 1

        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                pygame.quit()
                quit()

        left, right, jump = action
        self.player.rect.x, self.player.rect.y = self.player.update(left, right, jump, self.objects_for_lvl, [self.floor, self.right_wall, self.left_wall, self.roof])
        self._update()
        reward, game_over = self.calculate_score()

        return reward, game_over, self.score

    def calculate_score(self):
        reward = 0

        distance = abs(self.player.rect.centerx - self.endpt.centerx)
        reward = max(0, (w - distance))
        reward += reward

        game_over = self.player.rect.colliderect(self.left_wall) or (self.player.rect.colliderect(self.floor) and self.player.rect.x >= 100)
        

        return reward, game_over

    def _update(self):    
        self.display.fill('white')  

        for obj in self.objects_for_lvl + [self.floor, self.right_wall, self.left_wall]:  
            pygame.draw.rect(self.display, (128, 128, 128), obj)

        pygame.draw.rect(self.display, (255, 0, 0), self.player.rect)  # Draw player object
        pygame.draw.rect(self.display, (0, 255, 0), self.endpt)  
        pygame.display.update()

# TESTING FUNCTION
# if __name__ == "__main__":
#     game = Game()
#     while game.running:
#         action = Direction.update(0, 0, 1) # move up once 
#         print("Action:", action)
#         reward, game_over, score = game.step(action)
#         game._update()
#         if game_over:
#             print("Game Over")
#             game.running = False