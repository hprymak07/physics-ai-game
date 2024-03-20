import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as func
import os

class Q_Net(nn.Module):
    
    def __init__(self, input_size, hidden_size, output_size):
        super().__init__()