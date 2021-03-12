# Rock-paper-scissors-lizard-Spock template
# Author: M.Ramon Sorell
# Date: 13-10-2018

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

# helper functions
import random

def name_to_number(name):
    # delete the following pass statement and fill in your code below
    # convert name to number using if/elif/else
    # don't forget to return the result!
    if name == "rock":
        number = 0
    elif name == "Spock":
        number = 1
    elif name == "paper":
        number = 2
    elif name == "lizard":
        number = 3
    elif name == "scissors":
        number = 4
    else:
        return "Error: Name is not valid"
    
    return number
        


def number_to_name(number):
    # delete the following pass statement and fill in your code below
    # convert number to a name using if/elif/else
    # don't forget to return the result!
    if number == 0:
        name = "rock"
    elif number == 1:
        name = "Spock"
    elif number == 2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    elif number == 4:
        name = "scissors"
    else:
        return "Error: Number not in range"
        
    return name

def rpsls(player_choice): 
    # delete the following pass statement and fill in your code below
    
    # print a blank line to separate consecutive games
    print "\n"

    # print out the message for the player's choice
    print "Player choses " + player_choice

    # convert the player's choice to player_number using the function name_to_number()
    play_number =name_to_number(player_choice)
    
    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0,5,1)
    
    # convert comp_number to comp_choice using the function number_to_name()
    comp_choice = number_to_name(comp_number)
    
    # print out the message for computer's choice
    print "Computer choses " + comp_choice
    
    # compute difference of comp_number and player_number modulo five
    compute_diff = (play_number - comp_number) % 5
    
    # use if/elif/else to determine winner, print winner message
    
    if (compute_diff == 1) or (compute_diff == 2):
        print "Player wins!"
    
    elif (compute_diff == 3) or (compute_diff == 4):
        print "Computer wins!"
    
    else:
        print "Player and computer tie!"
    
# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric

