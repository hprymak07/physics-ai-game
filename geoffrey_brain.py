import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as func
import os
import numpy as np
class Q_Net(nn.Module):
    
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()

        self.linear1 = nn.Linear(input_size, hidden_size)
        self.linear2 = nn.Linear(hidden_size, output_size)


    def forward(self, x):

        x = func.relu(self.linear1(x))
  
        x = self.linear2(x)
        return x
    
    def save(self, file_name = 'geoffrey.pth'):
        geoffrey_folder_path = './geoffrey'
        if not os.path.exists(geoffrey_folder_path):
            os.makedirs(geoffrey_folder_path)

        file_name = os.path.join(geoffrey_folder_path, file_name)
        torch.save(self.state_dict(), file_name)

class Qtrainer:
    def __init__(self, model, lr, gamma):
        self.lr = lr
        self.model = model
        self.gamma = gamma
   
        #https://pytorch.org/docs/stable/generated/torch.optim.Adam.html
        self.optimizer = optim.Adam(model.parameters(), lr=self.lr)

        #https://pytorch.org/docs/stable/generated/torch.nn.MSELoss.html
        self.criteration = nn.MSELoss()
    
    def train_step(self, state, action, reward, next_state, done):
        state = torch.tensor(np.array(state), dtype = torch.float)
        next_state = torch.tensor(np.array(next_state), dtype = torch.float)
        action = torch.tensor(np.array(action), dtype = torch.long)
        reward = torch.tensor(np.array(reward), dtype = torch.float)

        if len(state.shape) == 1:
            state = torch.unsqueeze(state, 0)
            next_state = torch.unsqueeze(next_state, 0)
            action = torch.unsqueeze(action, 0)
            reward = torch.unsqueeze(reward, 0)
            done = (done, )

        # Predicts Q vaules
        # https://pytorch.org/tutorials/intermediate/reinforcement_q_learning.html

        pred_q = self.model(state)
        # Additional processing and training steps


        clone = torch.clone(pred_q)
        
        for i in range(len(done)):
            new_q = reward[i]
            if not done:
                new_q = reward[i] + self.gamma * torch.max(self.model(next_state[i]))
            
            pred_q[i][torch.argmax(action[i]).item()] = new_q

        self.optimizer.zero_grad()

        loss = self.criteration(clone, pred_q)
        loss.backward()
        self.optimizer.step()