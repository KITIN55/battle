# -*- coding: utf-8 -*-
"""
Created on Sat Jan 23 21:55:10 2021

@author: João Afonso
"""

import numpy as np 
import random
import scipy.ndimage as ndimage
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Agg")
import sys
import tkinter as tk
import os
from PIL import ImageTk, Image

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
        
        self.player_rows = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
        
        #create the board that will be presented to the player
        self.player_board = np.zeros_like(self.main_board)
            
        if not os.path.exists('temporary'):
            os.makedirs('temporary')
            
        self.save_board_pic(self.main_board, 'temporary/secret_board.png')
        self.save_board_pic(self.player_board, 'temporary/player_board.png')
        
        self.root = tk.Tk()
        
        self.root.configure(bg="white")
        self.root.geometry("750x1000")
        # self.root.state('zoomed')
        
        self.root.title("Battleship")
        
        frame1 = tk.Frame(self.root, bg="#0e0ba7")
        frame1.pack(anchor="n", fill="x")
        
        label = tk.Label(frame1, text="Battleship", font="none 18 bold", bg="#0e0ba7", fg="white")
        label.pack(anchor="n", pady=20, fill="x")
        
        frame2 = tk.Frame(self.root, bg="white")
        frame2.pack(anchor="n")

        label = tk.Label(frame2, text="Your guess: ", font="none 13 bold", bg="white")
        label.pack(side="left", anchor="c", fill="y", pady=30)
        
        self.entry_guess = tk.Entry(frame2, width=5, font="none 12", selectborderwidth=3, bd=3, justify=tk.CENTER)
        self.entry_guess.pack(side="right", anchor="c")
        
        button = tk.Button(self.root, text="Try guess", width=20, command=lambda: self.add_guess(self.entry_guess.get()))
        button.pack(anchor="n")
        
        self.result = tk.Label(self.root, text="", font="none 11 bold", bg="white")
        self.result.pack(anchor="n", pady=10, fill="x")
        
        self.boats_destroyed_label = tk.Label(self.root, text="{} / {} boats destroyed".format(len(self.boats_destroyed), self.num_boats), font="none 10", bg="white")
        self.boats_destroyed_label.pack(anchor="n", pady=10, fill="x")
        
        self.board_frame = tk.Frame(self.root, bg="blue")
        self.board_frame.pack(anchor="n")
        
        self.show_board()

        
            
    def add_guess(self, guess):
        
        guess = guess.upper()
        
        #insert a guess
        
        #validate the guess
        if len(guess) != 2:
            self.result.configure(text = "Invalid guess!", fg="red")
            return
        
        if not guess[0].isalpha() or not guess[1].isdigit():
            self.result.configure(text = "Invalid guess!", fg="red")
            return
        
        if guess[0] not in self.player_rows or int(guess[1]) < 0 or int(guess[1]) > 9:
            self.result.configure(text = "Invalid guess!", fg="red")
            return
        
        #get the row and column of the guess (correspondent to the game board, not the player board)
        guess_row = self.player_rows.index(guess[0])
        guess_col = int(guess[1])-1
        
        #check if is repeated guess
        if (guess_row, guess_col) in self.attempts:
            self.result.configure(text = "Repeated guess!", fg="red")
            return
        
        self.attempts.append((guess_row, guess_col))
        
        #check if the guess hit a boat
        is_boat = any((guess_row, guess_col) in sublist for sublist in self.boat_list) 
        if is_boat:       
            self.player_board[guess_row][guess_col] = "3"
            self.hits.append((guess_row, guess_col))
            self.result.configure(text = "You hit a boat!", fg="#081947")
            self.check_boats_destroyed()
            
        else:
            self.player_board[guess_row][guess_col] = "2"
            self.result.configure(text = "Oops...whater!", fg="#081947")
            
        self.save_board_pic(self.player_board, 'temporary/player_board.png')
        self.show_board()
        
        
        
        self.entry_guess.delete(0, tk.END)
        
        self.root.update_idletasks()
            
        #check if game was won
        self.win = self.check_win()
        
        if self.win == True:
            self.result.configure(text = "You won with {} attempts!".format(len(self.attempts)), fg="green")
            
        return
    
    def check_boats_destroyed(self):
        
        #check for destroyed boats
        
        for i in range(len(self.boat_list)):
            if all(i in self.hits for i in self.boat_list[i]) and i not in self.boats_destroyed:
                self.boats_destroyed.append(i)
                self.boats_destroyed_label.configure(text="{} / {} boats destroyed".format(len(self.boats_destroyed), self.num_boats))
        
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
        
        for widget in self.board_frame.winfo_children():
            widget.destroy()
        
        img = Image.open('temporary/player_board.png')
        
        basewidth = 800
        wpercent = (basewidth/float(img.size[0]))
        hsize = int((float(img.size[1])*float(wpercent)))
        img = img.resize((basewidth,hsize), Image.ANTIALIAS)
        
        self.img = ImageTk.PhotoImage(img)
        
        self.panel_board = tk.Label(self.board_frame, image = self.img, bg="white")
        self.panel_board.pack(fill = "both", expand = "yes", anchor="n")
        
        self.root.update_idletasks()
    
    def save_board_pic(self, board, path):
        
        #create image and save it as png
        
        colors = {   0:  [90,  155,  255],
                     1:  [88,  88,  88],
                     2:  [14,  11,  167],
                     3:  [255,  0,  0]}
        
        image = np.array([[colors[val] for val in row] for row in board], dtype='B')
        plt.imshow(image)
        plt.axis('off')
        plt.tight_layout()
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
    game.root.mainloop()

    #game.show_board()
    # game.save_board_pic("board.png")
    
    # game.play()
    
if __name__ == '__main__':
    
    main()




