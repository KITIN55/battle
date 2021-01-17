# -*- coding: utf-8 -*-
"""
Created on Sun Dec 20 20:44:40 2020

@author: João Afonso
"""

import numpy as np 
import random
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
import sys

# method used with the ndimage function that checks the neighbors of a boat cell 
def get_neighbors(values):
    return values.sum()

# class of the game
class Battleship():
    
    def __init__(self, boats = 3):
        
        self.num_boats = boats

        #the board starts as 2D array with 9 rows, 9 columns and all values set to zero
        self.main_board = np.zeros((9,9))
        
        #initialization of some variables of the game
        self.win = False
        self.hits = []
        self.attempts = []
        self.boats_destroyed = []
        
        #create the board, getting the list of boats and the list of blocked cells (not possible to insert a boat cell) 
        self.boat_list = []
        self.not_possible = []
        for _ in range(self.num_boats):
            self.boat_list.append(self.add_boat())
            rows, cols = np.where(self.main_board == -1)
            self.not_possible = [(rows[i], cols[i]) for i in range(len(rows))]
        
        #sort the cells of each boat
        for boat in self.boat_list:
            boat = boat.sort()
        
        #replace all -1 in the board by 0, so now a boat cell is represented by one and the rest is 0
        self.main_board = np.where(self.main_board!=1, 0, self.main_board)
        
        #create the board that will be presented to the player (with letters in the rows and numbers in the columns)
        self.player_cols = [str(n) for n in range(1, 10)]
        self.player_rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        self.player_board = [list(" ") + self.player_cols]
        for i in range(len(self.player_rows)):
            self.player_board.append(list(self.player_rows[i]) + [" "]*9)
            
    def play(self):
        
        #top level method
        
        print("Welcome to Battleship!")
        print("You have 5 ships to destroy (all with 3 cells of size). Good luck!")
        
        self.print_player_board()
        
        while self.win==False:
            
            #ask for a guess
            guess = input("\n{} - Insert your guess (ROWCOL) or 'exit': ".format(len(self.attempts) + 1))
            
            #let the user insert lower or upper letters
            guess = guess.upper()
            
            #check for exit
            if guess == "EXIT":
                
                sys.exit()
                
            else:
                
                #add guess
                valid = self.add_guess(guess)
                
                #check if guess was valid
                if valid == "yes":
                    self.print_player_board()
                else:
                    print(valid)

        #won game  
        print("\n\nCongratulations, you won with {} attempts!".format(len(self.attempts)))   
            
    def add_guess(self, guess):
        
        #insert a guess
        
        #validate the guess
        if len(guess) != 2:
            return ">> Invalid guess!"
        
        if not guess[0].isalpha() or not guess[1].isdigit():
            return ">> Invalid guess!"
        
        if guess[0] not in self.player_rows or int(guess[1]) < 0 or int(guess[1]) > 9:
            return ">> Invalid guess!"
        
        #get the row and column of the guess (correspondent to the game board, not the player board)
        guess_row = self.player_rows.index(guess[0])
        guess_col = int(guess[1])-1
        
        #check if is repeated guess
        if (guess_row, guess_col) in self.attempts:
            return ">> Repeated guess!"
        
        self.attempts.append((guess_row, guess_col))
        
        #check if the guess hit a boat
        is_boat = any((guess_row, guess_col) in sublist for sublist in self.boat_list) 
        if is_boat:       
            self.player_board[guess_row+1][guess_col+1] = "x"
            self.hits.append((guess_row, guess_col))
            print(">> You hit a boat!")
            self.check_boats_destroyed()
            
        else:
            self.player_board[guess_row+1][guess_col+1] = "o"
            print(">> Oops...whater!")
            
        #check if game was won
        self.win = self.check_win()
        
        return "yes"
    
    def check_boats_destroyed(self):
        
        #check for destroyed boats
        
        for i in range(len(self.boat_list)):
            if all(i in self.hits for i in self.boat_list[i]) and i not in self.boats_destroyed:
                self.boats_destroyed.append(i)
                print(">> {} boat(s) destroyed!".format(len(self.boats_destroyed)))
        
    def check_win(self):
        
        #check if game was won
        
        win = False
        if self.num_boats == len(self.boats_destroyed):
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
        
        #show board as image with matplotlib 
        
        colors = {   0:  [90,  155,  255],
                     1:  [88,  88,  88]}    
        
        image = np.array([[colors[val] for val in row] for row in self.main_board], dtype='B')
        plt.imshow(image)
        plt.axis('off')
        plt.show()
    
    def save_board_pic(self, path):
        
        #create image and save it as png
        
        colors = {   0:  [90,  155,  255],
                     1:  [88,  88,  88]}    
        
        image = np.array([[colors[val] for val in row] for row in self.main_board], dtype='B')
        plt.imshow(image)
        plt.axis('off')
        plt.savefig(path)

    def add_boat(self):
        
        #add a 3 cell boat to the board
        
        done = False
        while done == False:
            
            #create temporary board
            board = np.zeros((9,9))
            
            boat = []
            
            #check if initial boat cell is valid
            invalid = True
            while invalid:
                row = random.randint(0, 8)
                col = random.randint(0, 8)
                if self.main_board[row, col] == 0:
                    invalid = False
            
            #get initial cell
            board[row, col] = 1
            boat.append((row, col))
            
            #possible second cell
            possible = [(boat[-1][0]-1, boat[-1][1]), (boat[-1][0]+1, boat[-1][1]), (boat[-1][0], boat[-1][1]-1), (boat[-1][0], boat[-1][1]+1)]
            
            #remove the invalid second cells
            possible = [coordinates for coordinates in possible if -1 not in coordinates and self.main_board.shape[0] not in coordinates and coordinates not in self.not_possible]
            
            #get the random second cell
            row, col = random.sample(possible, 1)[0]
            board[row, col] = 1
            boat.append((row, col))
            
            #possible third cell
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
            
            #validate possibilities
            possible = [coordinates for coordinates in possible if -1 not in coordinates and self.main_board.shape[0] not in coordinates and coordinates not in boat and coordinates not in self.not_possible]
            
            #add third cell
            try:
                row, col = random.sample(possible, 1)[0]
            except:
                continue
            board[row, col] = 1    
            boat.append((row, col))
        
            #get neighbors of the boat
            footprint = np.array([[1,1,1],
                                  [1,0,1],
                                  [1,1,1]])
            
            board = ndimage.generic_filter(board, get_neighbors, footprint=footprint)
            
            #define the neighbors and boats as -1
            board = np.where(board!=0, -1, board)
            
            #define boat cells as 1
            for row, col in boat:
                board[row, col] = 1
                
            #join the temporary board to the main board
            self.main_board = self.main_board + board
            
            done = True
    
        return boat
    
def main():   
    
    game = Battleship(boats=3)  

    #game.show_board()
    #game.save_board_pic("board.png")
    
    game.play()
    
if __name__ == '__main__':
    
    main()



