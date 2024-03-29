import torch
import random
import numpy as np
from collections import deque
from game import Game, Direction, Player
from geoffrey_brain import Q_Net, Qtrainer
from math import dist
from collections import namedtuple
from pygame import Rect

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001      
Point = namedtuple('Point', ['x', 'y'])

def score(player, endpt, neg=False):

    player_distance = [player.rect.x - (player.rect.width / 2), player.rect.y - (player.rect.height / 2)]
    endpt_distance = [endpt.x - (endpt.width / 2), endpt.y - (endpt.height / 2)]
    score = int(round(dist(player_distance, endpt_distance), 0))
    game_over = True

    if neg: 
        reward = -10 
    else: 
        reward = 10
        score += 1

    return reward, game_over, score

# https://www.youtube.com/watch?v=L8ypSXwyBds - video
class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9 # Can be any number as long as it's lower than 1
        self.memory = deque(maxlen = MAX_MEMORY)

         
        self.model = Q_Net(11,256,3)
        self.trainer = Qtrainer(self.model, lr = LR, gamma = self.gamma)

    def get_state(self, game):
        player = Player(30, 1250 // 2)
        cube = player.rect # get player cube from Player

        point_l = Point(cube.x - 18, cube.y)
        point_r = Point(cube.x + 18, cube.y)

        
        danger_nearby = 1 if (cube.colliderect(game.floor) and cube.x > 200) != -1 else 0
        danger_end = 1 if cube.colliderect(game.endpt) else 0

        left, right, jump = Direction.update(left = 0, right = 0, jump = 0)


        danger = [cube.colliderect(game.endpt), cube.colliderect(game.floor) and cube.x > 200]
        [score(cube, game.endpt, True) for d in danger if d]
        state = np.array([
            # locate danger
            danger[0],
            danger[1],
            
            #Move/ Keystrokes
            left,
            right,
            jump,
            
           
            game.endpt.x <  cube.x,# left
            game.endpt.x > cube.x, # right
            game.endpt.y < cube.y, # up
            game.endpt.y > cube.y, # down

            0,
            0
        ], dtype=int)


        return np.array(state, dtype=int)
    

    def remember(self, state, action, reward, next_state, done):
        # will pop left is max memory is exceeded
        self.memory.append((state, action, reward, next_state, done))
    
    def train_long_memory(self):
        if len(self.memory) >= BATCH_SIZE:
            sample = random.sample(self.memory, BATCH_SIZE)
        else:
            sample = self.memory

        states, actions, rewards, next_states, dones = zip(*sample)

        self.trainer.train_step(states, actions, rewards, next_states, dones)


    def train_short_memory(self, state_old, action, reward, next_state, done):
        self.trainer.train_step(state_old, action, reward, next_state, done)  
    
    def get_action(self, state): # Using the epsilon-greedy exploration method

        self.epsilon = 80 - self.n_games #makes sure the epsilon doesnt go negtive
        final_action = [0,0,0]
        if random.randint(0,200) < self.epsilon: # randomly choose action
            action = random.randint(0,2)
            final_action[action] = 1
        else: # Exploitate the highest Q-value action
            state0 = torch.tensor(state, dtype = torch.float)

            
            prediction = self.model(state0)
            action = torch.argmax(prediction).item()
            final_action[action] = 1
        return final_action
    
def train():
    plot_scores = []
    plot_mean_scores =[]
    total_score = 0
    agent = Agent()
    game = Game()

    record = 0

    reward = 0
    done = True
    state_new = None

    while True:

        state_old = agent.get_state(game)
        action = agent.get_action(state_old)


        reward, done, state_new = game.step(action)
        score = game.score


        agent.remember(state_old, action, reward, state_new, done)
        agent.train_short_memory(state_old, action, reward, state_new, done)
        agent.train_long_memory()

        if done:
            game.reset()
            agent.n_games += 1

            if agent.n_games == 1000:
                break


            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.n_games, 'Score', score, 'Record:', record)
            






if __name__ == '__main__':
     train()