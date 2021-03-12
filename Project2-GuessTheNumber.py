# template for "Guess the number" mini-project
# input will come from buttons and an input field
# all output for the game will be printed in the console

#Author: M.Ramon Sorell
#Date: 20-October-2018

import simplegui
import random
import math

# define global variable
num_range = 100
player_tries = 7
player_count= 0
secret_number= random.randrange(0,num_range)


# helper function to start and restart the game
def new_game():
    global num_range,secret_number, player_tries
    # initialize global variables used in your code here
    secret_number= random.randrange(0,num_range)
    print "New Game. Range is 0 to " + str(num_range)
    print "Number of remaining guesses " +str(player_tries)+ "\n"

 
    
    
# define event handlers for control panel
def range100():
    # button that changes the range to [0,100) and starts a new game 
    global num_range, secret_number, player_tries, player_count
    num_range = 100
    player_tries = 7
    player_count = 0
    new_game()
    
    
def range1000():
    # button that changes the range to [0,1000) and starts a new game     
    global num_range, secret_number, player_tries, player_count
    num_range = 1000
    player_tries = 10
    player_count = 0
    new_game()
    
    
def input_guess(guess):
    global secret_number, player_tries, player_count
    # main game logic goes here
    player_guess = int(guess)
    print "Guess was " + (guess)
    
    if player_tries > 0:
        if player_guess > secret_number:
            player_tries -= 1
            player_count += 1
            print "Number of guesses remaining is " +str(player_tries)
            print "Lower \n"
        elif player_guess < secret_number:
            player_tries -=1
            player_count +=1
            print "Number of guesses remaining is " +str(player_tries)
            print "Higher \n"
        elif player_guess == secret_number:
            print "Correct \n"
            print str(player_tries)
            print str(player_count)
            player_tries += player_count
            player_count = 0
            new_game()
    

    if player_tries == 0:
        print "Sorry, you ran out of guesses. The number was " +str(secret_number) +"\n"
        player_tries = player_count
        player_count=0
        new_game()
    
# create frame

frame = simplegui.create_frame("Guess My Number", 300, 300)


# register event handlers for control elements and start frame
frame.add_button("Range is [0,100)", range100, 200)
frame.add_button("Range is [0,1000)", range1000, 200)
frame.add_input("Enter a guess", input_guess, 200)


# call new_game 
new_game()


# always remember to check your completed program against the grading rubric
