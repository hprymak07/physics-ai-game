import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as func
import os

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
        self.optimizer = optim.Adam(model.parameters(), lr = self.lr)

        #https://pytorch.org/docs/stable/generated/torch.nn.MSELoss.html
        self.criteration = nn.MSELoss()
    
    def train_step(state, action, reward, next_state, done):
        pass

