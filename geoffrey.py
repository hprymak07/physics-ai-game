import torch
from numpy import np
from collections import deque
from main import Player, point, calc_score as score,  game_over as danger
from main import Direction, update as left, right, jump
MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001

class Agent:

    def __init__(self):
        self.n_games = 0
        self.epsilon = 0
        self.gamma = 0
        self.memory = deque(maxlen = MAX_MEMORY)

        #passing in none so there is no error; will do later 
        self.model = None
        self.trainer = None


    def get_state(self, game):
        cube = game.player[0]
        
        point_l = point(cube.x - 18, cube.y)
        point_r = point(cube.x + 18, cube.y)
        

        state = [
            # locate danger
            danger[0],
            danger[1],
            
            #Move/ Keystrokes
            left,
            right,
            jump,
            
            #calc the distance from itself and the endpoint
            score
        ]
        return np.array(state, dtype=int)
    
    def remember(self, state, action, reward, next_state, done):
        # will pop left is max memory is exceeded
        self.memory.append(state, action, reward, next_state, done)
    
    def train_long_memory(self):
        pass
    
    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)  
    
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