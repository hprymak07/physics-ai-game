import pygame



# pygame setup
pygame.init()
w, h = 1250,720
screen = pygame.display.set_mode((w, h))
dt = 0

# reset
# reward
# play(action) --> direction
# game iteration
# is_collision

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 10, 10)
        self.floor = pygame.Rect(0, 370, w, 200)
        self.objects_lvl_one = [
            pygame.Rect(100, 300, 100, 100),
            pygame.Rect(250, 220, 100, 25),
            pygame.Rect(400, 150, 100, 25),
            pygame.Rect(535, 150, 75, 25),
            pygame.Rect(635, 170, 75, 25),
            pygame.Rect(735, 150, 75, 25),
            pygame.Rect(900, 130, 200, 25),
            pygame.Rect(1150, 90, 20, 20)
        ]
        self.collision_tol = 23
        self.vel_y = 0
        self.gravity = 0.5
        self.ground = False
        self.acc = 0

    def draw_lvl(self):
        screen.fill("white") # background
        pygame.draw.rect(screen, 'red', player.rect) # Player
        pygame.draw.rect(screen, 'black', (0, 370, w, 200))
        pygame.draw.rect(screen, 'forestgreen', (1150, 90, 20, 20)) # End of the lvl
        for obj in self.objects_lvl_one: # platforms 
            pygame.draw.rect(screen, 'black', obj)

    def update(self, dt):
        keys = pygame.key.get_pressed()
        self.acc = self.gravity
        list_in_use = self.objects_lvl_one + list(self.floor)

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

        if keys[pygame.K_SPACE] and self.ground:
            self.vel_y = -10
            self.acc = 0
            self.ground = False

        self.vel_y += self.acc
        self.rect.y += self.vel_y
        self.vel_x = 300 * dt

        if keys[pygame.K_d]:
            self.rect.x += self.vel_x
        if keys[pygame.K_a]:
            self.rect.x -= self.vel_x
        
        if player.rect.left <= 0:
           player.rect.x = 20
        if player.rect.right >= w:
           player.rect.x = 1220
    
    def is_game_over(self):
      if player.rect.colliderect(self.endpoint):
        player.rect.x = 30
        player.rect.y = 0
        print("Game Over")
      if player.rect.colliderect(self.floor):
          print("Game Over")

player = Player(30, h / 2)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            break

    player.draw_lvl()

    pygame.display.flip()
    dt = pygame.time.Clock().tick(60) / 1000
    player.update(dt)

pygame.quit()