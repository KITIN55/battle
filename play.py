# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 20:04:34 2020

@author: Asus
"""
import torch
import torch.nn as nn
from torchsummary import summary
import numpy as np

class Player(nn.Module):
    def __init__(self):
        super(Player, self).__init__()
        self.layer1 = nn.Linear(100, 50)
        self.layer2 = nn.Linear(50, 1)
        
    def forward(self, x):
        return self.layer2(self.layer1(x))
    
def train():
    
    board = np.zeros((10,10))
    
 
    
def main():    
    
    '''
    print()
    if torch.cuda.is_available():
        DEVICE = torch.device("cuda:0")  # you can continue going on here, like cuda:1 cuda:2....etc. 
        print("Running on the GPU...")
    else:
        DEVICE = torch.device("cpu")
        print("Running on the CPU...")
    print()
    
    player = Player().to(DEVICE)    
    print(player)
    
    #summary(player, (100,))
    '''
    
    train()
    

if __name__ == '__main__':
    main()