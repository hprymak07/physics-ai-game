import torch
import numpy
from collections import deque

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = deque(maxlen = MAX_MEMORY)
        # MODEL AND TRAINER GO HERE


    def get_state(self, game):
        pass
    
    def remember(self, state, action, reward, next_state, done):
        pass
    
    def train_long_memory(self):
        pass
    
    def train_short_memory(self, state, action, reward, next_state, done):
        pass  
    
    def get_action(self, state):
        pass

def train():
    plot_scores = []
    plot_mean_scores =[]
    total_score = 0
    record = 0
    agent = Agent()
    game = Player
    while True:
        # get old state / current
        state_old = agent.get_state(game)

        # get move on current state
        final_move = agent.get_action(state_old)

        # reward, done, score = game // ADD AI PLAY STUFF
        state_new = agent.get_state(game)

        #train short term memory
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        if done:
            game.reset()
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                #agent.model.save

if __name__ == '__main__':
    train()