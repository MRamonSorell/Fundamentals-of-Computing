# Author M. Sorell
# Date: 03 - Feb- 2019

# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 950x392 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")

CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")    

# initialize global variables
deck = []
in_play = False
outcome = ""
# score is based on player win and lose
score = 0

# define globals for cards
SUITS = ['C', 'S', 'H', 'D']
RANKS = ['A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K']
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)
     
    # this calls the back card for drawing
    def draw_back(self, canvas, pos):
        canvas.draw_image(card_back, (36,48), CARD_BACK_SIZE, [pos[0], pos[1]], CARD_BACK_SIZE)
     
        
# define hand class
class Hand:
    global player_hand, dealer_hand
    
    def __init__(self):
        self.cards=[]
        self.hand_value=0

    def __str__(self):
        ans = " Contains "
        for i in self.cards:
            ans += str(i)
            ans += " "
        return ans

    def add_card(self, card):
        self.cards.append(card)
        

    # count aces as 1, if the hand has an ace, then add 10 to hand value if don't bust
    # gets rank of cards in hand and then sees if the 
    # card rand is in the key
    # if so it returns the item value
    def get_value(self):
        h_val = []
        c_ranks = []
        for key, items in VALUES.items():
            for item in self.cards:
                crank=Card.get_rank(item)
                if crank in key:
                    h_val.append(items)
                    c_ranks.append(crank)
        
        self.hand_value = sum(h_val)
        
        if 'A' in c_ranks and self.hand_value +10 <= 21: 
            self.hand_value = sum(h_val) + 10
        else:
            self.hand_value = sum(h_val)
            
        return self.hand_value                           

    def busted(self):
        if self.hand_value > 21:
            return True
    
    # this prints the normal cards
    def draw(self, canvas,pos, hole= False):
        for c in self.cards:
            c.draw(canvas, pos)
            pos[0]+= 100
            
        # this prints a 5th card to put on top of the image card.    
        for i in range(1):
            if i == 0 and hole:
                pos=[185,249]
                Card.draw_back(self,canvas,pos)
               

        
# define deck class
class Deck:
    def __init__(self):
        self.deck_cards=[]
        for suit in SUITS:
            for rank in RANKS:
                self.card=Card(suit,rank)
                self.deck_cards.append(self.card)
    
    def __str__(self):
        ans = "Deck contains "
        for i in self.deck_cards:
            ans += str(i)
            ans += " "
        return ans

    # add cards back to deck and shuffle
    def shuffle(self):
        return random.shuffle(self.deck_cards)

    def deal_card(self):
        return self.deck_cards.pop()


#define callbacks for buttons
def deal():
    global outcome, in_play, dealer_hand, player_hand, game_deck, score, outcome
    
    # your code goes here
    dealer_hand = Hand() #creates dealer instance
    player_hand = Hand() #create player instand
    
    game_deck=Deck() # calls deck assigns it to game_deck
    
    game_deck.shuffle() # shuffle cards
    
    # draw 2 random cards from deck to player hand class
    for temp_variable in range(2):
        player_hand.add_card(game_deck.deal_card())
    
    # draw 2 random cards from deck to dealer hand class
    for temp_variable in range(2):
        dealer_hand.add_card(game_deck.deal_card())
    
    #  print "Player hand" +str(player_hand) 
    #  print "Dealer hand" +str(dealer_hand)
    #  print player_hand.get_value()
    #  print dealer_hand.get_value()
    
    outcome = ""
    in_play = True
    

def hit():
    global outcome, in_play, dealer_hand, player_hand, game_deck, outcome, score
    
    # replace with your code below
    if in_play == True:
        for temp_variable in range(1):
            player_hand.add_card(game_deck.deal_card())
            
    #print "Player hand" +str(player_hand)   
    player_hand.get_value()
    # if busted, assign an message to outcome, update in_play and score
    if player_hand.busted() == True:
        #print "You have been busted"
        #print "Score " + str(player_hand.get_value())
        in_play = False
        outcome = "You went bust and lose"
        score -= 1
        
def stand():
    global outcome, in_play, dealer_hand, player_hand, game_deck, outcome, score
     
    # replace with your code below
    # if player_hand.busted() == True:
        # print "You have been busted"
        # in_play = False 
        
        
    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more    
    if in_play == True:
        while(dealer_hand.get_value() <= 17):
            for temp_variable in range(1):
                dealer_hand.add_card(game_deck.deal_card())
            
    # assign a message to outcome, update in_play and score
    if dealer_hand.get_value() <= 21 and dealer_hand.get_value() >= player_hand.get_value():
        #print "Dealer wins"
        in_play = False
        outcome = "Dealer wins"
        score -= 1
                
    # assign a message to outcome, update in_play and score
    if player_hand.get_value() <= 21 and player_hand.get_value() > dealer_hand.get_value():
        #print "Player wins"
        in_play = False 
        outcome = "Player wins!"
        score += 1
    
    #print "Dealer hand" +str(dealer_hand)   
    dealer_hand.get_value()

    # assign a message to outcome, update in_play and score
    if dealer_hand.busted() == True:
        #print "Dealer went busted. You have won"
        #print "Score " + str(dealer_hand.get_value())
        in_play = False
        outcome = "Dealer went bust. You win"
        score += 1

        
        
        
def draw(canvas):
    global player_hand, dealer_hand, in_play, outcome, score
    
    game_in_play= in_play
    
    game_score = "Score " +str(score)
    
    # prints game name
    canvas.draw_text('Blackjack', (75, 75), 48, 'White')
    
    canvas.draw_text('Dealer ', (100, 175), 36, 'Black')
    dealer_hand.draw(canvas,[150,200], in_play)
    
    canvas.draw_text('Player ', (100, 375), 36, 'Black')
    player_hand.draw(canvas,[150,400])
    
    # prints outcome of game
    canvas.draw_text(outcome, (300, 175), 36, 'Black')
    
    # prints outcome of score
    canvas.draw_text(game_score, (375, 75), 36, 'Black')
    
    # if game in play message (hit or stand) not in play (new deal?)
    if in_play:
        canvas.draw_text('Hit or stand ? ', (300, 375), 36, 'Black')
    
    else: 
        canvas.draw_text('New deal ? ', (300, 375), 36, 'Black')
    
    


# initialization frame
frame = simplegui.create_frame("M.Sorell Blackjack Game", 800, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# deal an initial hand
deal()

# get things rolling
frame.start()


# Grading rubric - 18 pts total (scaled to 100)

# 1 pt - The program opens a frame with the title "Blackjack" appearing on the canvas.
# 3 pts - The program displays 3 buttons ("Deal", "Hit" and "Stand") in the control area. (1 pt per button)
# 2 pts - The program graphically displays the player's hand using card sprites. 
#		(1 pt if text is displayed in the console instead) 
# 2 pts - The program graphically displays the dealer's hand using card sprites. 
#		Displaying both of the dealer's cards face up is allowable when evaluating this bullet. 
#		(1 pt if text displayed in the console instead)
# 1 pt - Hitting the "Deal" button deals out new hands to the player and dealer.
# 1 pt - Hitting the "Hit" button deals another card to the player. 
# 1 pt - Hitting the "Stand" button deals cards to the dealer as necessary.
# 1 pt - The program correctly recognizes the player busting. 
# 1 pt - The program correctly recognizes the dealer busting. 
# 1 pt - The program correctly computes hand values and declares a winner. 
#		Evalute based on player/dealer winner messages. 
# 1 pt - The dealer's hole card is hidden until the hand is over when it is then displayed.
# 2 pts - The program accurately prompts the player for an action with the messages 
#        "Hit or stand?" and "New deal?". (1 pt per message)
# 1 pt - The program keeps score correctly.