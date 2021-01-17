# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 20:44:40 2020

@author: Asus
"""
import numpy as np 
import random
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt

def test_func(values):
    return values.sum()

class Battleship():
    
    def __init__(self, boats = 3):
        
        self.num_boats = boats

        self.main_board = np.zeros((9,9))
        
        self.win = False
        self.hits = []
        self.attempts = []
        
        self.boat_list = []
        self.not_possible = []
        for _ in range(self.num_boats):
            self.boat_list.append(self.add_boat())
            rows, cols = np.where(self.main_board == -1)
            self.not_possible = [(rows[i], cols[i]) for i in range(len(rows))]
        
        self.main_board = np.where(self.main_board!=1, 0, self.main_board)
        
        self.player_cols = [str(n) for n in range(1, 10)]
        self.player_rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        
        self.player_board = [list(" ") + self.player_cols]
        
        for i in range(len(self.player_rows)):
            self.player_board.append(list(self.player_rows[i]) + [" "]*9)
            
    def play(self):
        
        print("Welcome to Battleship!")
        print("You have 5 ships to destroy (all with 3 cells of size). Good luck!")
        
        self.num_attempts = 0
        
        self.print_player_board()
        
        while self.win==False:
            
            guess = input("\nInsert your guess (ROWCOL): ")
            valid = self.add_guess(guess)
            if valid:
                self.num_attempts = self.num_attempts + 1
                self.print_player_board()
            else:
                print(">> Repeated guess!")
            
        print("\n\nCongratulations, you won with {} attempts!".format(self.num_attempts))   
            
    def add_guess(self, guess):
        
        guess_row = self.player_rows.index(guess[0])
        guess_col = int(guess[1])-1
        
        if (guess_row, guess_col) in self.attempts:
            return False
        
        print(guess_row, guess_col)
        self.attempts.append((guess_row, guess_col))
        
        is_boat = any((guess_row, guess_col) in sublist for sublist in self.boat_list) 
        
        if is_boat:       
            self.player_board[guess_row+1][guess_col+1] = "x"
            self.hits.append((guess_row, guess_col))
            print(">> You hit a boat!")
            print(self.hits)
        else:
            self.player_board[guess_row+1][guess_col+1] = "o"
            print(">> Oops...whater!")
            
        self.win = self.check_win()
        
        return True
        
    def check_win(self):
        
        boat_cells = [item for sublist in self.boat_list for item in sublist]
        
        win = False
        if len(self.hits) == len(boat_cells):
            win = True
            
        return win
            
    def print_player_board(self):
        
        print()
        for x in self.player_board:
            print(*x, sep=' ')
               
    def get_board(self):     
        return self.main_board
    
    def get_boats(self):
        return self.boat_list
    
    def show_board(self):
        
        colors = {   0:  [90,  155,  255],
                     1:  [88,  88,  88]}    
        
        image = np.array([[colors[val] for val in row] for row in self.main_board], dtype='B')
        plt.imshow(image)
        plt.axis('off')
        plt.show()
    
    def save_board_pic(self, path):
        
        colors = {   0:  [90,  155,  255],
                     1:  [88,  88,  88]}    
        
        image = np.array([[colors[val] for val in row] for row in self.main_board], dtype='B')
        plt.imshow(image)
        plt.axis('off')
        plt.savefig(path)

    def add_boat(self):
        
        done = False
        while done == False:
        
            board = np.zeros((9,9))
            
            boat = []
            
            invalid = True
            while invalid:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
                if self.main_board[row, col] == 0:
                    invalid = False
                
            board[row, col] = 1
            
            boat.append((row, col))
            
            possible = [(boat[-1][0]-1, boat[-1][1]), (boat[-1][0]+1, boat[-1][1]), (boat[-1][0], boat[-1][1]-1), (boat[-1][0], boat[-1][1]+1)]
            
            possible = [coordinates for coordinates in possible if -1 not in coordinates and self.main_board.shape[0] not in coordinates and coordinates not in self.not_possible]
            
            row, col = random.sample(possible, 1)[0]
            board[row, col] = 1
            
            boat.append((row, col))
            
            if boat[-1][0] == boat[0][0]:
                if boat[-1][1] > boat[0][1]:
                    possible = [(boat[-1][0], boat[0][1]-1), (boat[-1][0], boat[-1][1]+1)]
                else:
                    possible = [(boat[-1][0], boat[0][1]+1), (boat[-1][0], boat[-1][1]-1)]
            else:
                if boat[-1][0] > boat[0][0]:
                    possible = [(boat[0][0]-1, boat[-1][1]), (boat[-1][0]+1, boat[-1][1])]
                else:
                    possible = [(boat[0][0]+1, boat[-1][1]), (boat[-1][0]-1, boat[-1][1])]
                
            possible = [coordinates for coordinates in possible if -1 not in coordinates and self.main_board.shape[0] not in coordinates and coordinates not in boat and coordinates not in self.not_possible]
            
            try:
                row, col = random.sample(possible, 1)[0]
            except:
                continue
            
            board[row, col] = 1    
            
            
            boat.append((row, col))
        
            
            footprint = np.array([[1,1,1],
                                  [1,0,1],
                                  [1,1,1]])
            
            board = ndimage.generic_filter(board, test_func, footprint=footprint)
            
            board = np.where(board!=0, -1, board)
            
            for row, col in boat:
                board[row, col] = 1
                    
            self.main_board = self.main_board + board
            
            done = True
    
        return boat
    
       
game = Battleship(boats=3)  
board = game.get_board()
boats = game.get_boats()
print(boats)
# game.show_board()
#game.save_board_pic("C:/Users/Asus/Desktop/Battleship/board.png")


game.play()



