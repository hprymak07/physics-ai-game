import torch
import random
import numpy as np
from collections import deque
from game import Game, Direction
from geoffrey_brain import Q_Net, Qtrainer
from collections import namedtuple

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001      
Point = namedtuple('Point', ['x', 'y'])


class Agent:
    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Q_Net(11, 256, 3)
        self.trainer = Qtrainer(self.model, lr=LR, gamma=self.gamma)

    def get_state(self, game):
        player = game.player
        cube = player.rect

        left, right, jump = Direction.update(left=0, right=0, jump=0)

        danger = [1 if cube.colliderect(game.endpt) else 0,  1 if cube.colliderect(game.floor) and cube.x > 100 else 0]
        state = np.array([
            danger[0],
            danger[1],
            left,
            right,
            jump,
            game.endpt.x < cube.x,
            game.endpt.x > cube.x,
            game.endpt.y < cube.y,
            game.endpt.y > cube.y,
            0,
            0
        ], dtype=int)

        return np.array(state, dtype=int)

    def remember(self, state, action, reward, next_state, done):
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
    
    def get_action(self, state):
        self.epsilon = 80 - self.n_games
        final_action = [0, 0, 0]

        if random.randint(0, 200) < self.epsilon:
            action = random.randint(0, 2)
            final_action[action] = 1
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            action = torch.argmax(prediction).item()
            final_action[action] = 1

        return final_action  # Return the action
    
    def play_game(self):
        agent = Agent()
        game = Game()
        record = 0
        reward = 0
        done = True
        state_new = None

        while True:
            state_old = agent.get_state(game)
            action = agent.get_action(state_old)
            reward, done, state_new = game.step(action)  # Update reward from game step
            score = game.score

            agent.remember(state_old, action, reward, state_new, done)
            agent.train_short_memory(state_old, action, reward, state_new, done)
            agent.train_long_memory()

            if done:
                game.reset()
                agent.n_games += 1

                if agent.n_games > 200:
                    break

                if score > record:
                    record = score
                    agent.model.save()

                print('Game', agent.n_games, 'Score', score, 'Record:', record)

if __name__ == '__main__':
    agent = Agent()
    agent.play_game()
