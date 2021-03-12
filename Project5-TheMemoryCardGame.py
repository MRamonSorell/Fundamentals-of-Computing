# author : M Sorell
# implementation of card game - Memory
# Date: 31-January-2019

import simplegui
import random
import math

#define global variables
list1 = [0,1,2,3,4,5,6,7]
list2 = [0,1,2,3,4,5,6,7]
card_list= list1 +list2
state = 0
picks=[]
pindex=[]
counter = 0

exposed1 =[False, False, False, False, False, False, False , False,False, False, False, False, False, False, False , False]

CARD_WIDTH=50
FRAME_HEIGHT = 80
CARD_RADIUS= 100

# helper function to initialize globals
def new_game():
    global card_list, exposed1, state, counter, picks ,pindex
    exposed1 =[False, False, False, False, False, False, False , False,False, False, False, False, False, False, False , False]
    random.shuffle(card_list)
    state= 0
    counter = 0
    picks=[]
    pindex=[]
    label1.set_text("Turns = " + str(counter))
    
  
     
# define event handlers
def mouseclick(pos):
    # add game state logic here
    global list1, exposed1, state,picks,pindex, CARD_WIDTH, FRAME_HEIGHT, CARD_RADIUS, counter
    pick =[]
   
    a= pos[0]//50
    for x in range(len(exposed1)):
        if (x == a) and exposed1[x] == False:
            pick.append(x)
            pindex.append(x)
            state += 1
            
        
    # dry 
    #if state == 2:
        #counter = counter +1
        #label1.set_text("Turns = " + str(counter))
      
    if state == 1:
        for items in pick:
            exposed1[items] = True
            picks.append(card_list[items])
    
    if state == 2:
        for items in pick:
            exposed1[items] = True
            picks.append(card_list[items])
         
                  
    elif state == 3 :
        counter = counter +1
        label1.set_text("Turns = " + str(counter))
        a =picks[0]
        b = picks[1]
        if (a == b):
            state = 0
            picks=[]
            pindex=[]
            
            for items in pick:
                exposed1[items]=True
                state=1
                picks.append(card_list[items])
                pindex.append(items)
                
        else:
            for items in pindex:
                exposed1[items]=False
                picks =[]
                pindex=[] 
                
            for items in pick:
                exposed1[items]=True
                state=1
                picks.append(card_list[items])
                pindex.append(items)
                
                
                        
# cards are logically 50x100 pixels in size    
def draw(canvas):
    global list1, list2, card_list, exposed1, CARD_WIDTH, FRAME_HEIGHT, counter
    
    i = 0
    for item in range(len(exposed1)):
        if exposed1[item] == True:
            card=card_list[i]
            card_pos = CARD_WIDTH*i
            canvas.draw_text(str(card), (card_pos, FRAME_HEIGHT), 72, 'White')
        else:
            card=card_list[i]
            card_pos = CARD_WIDTH*i
            canvas.draw_polygon(([card_pos, 0], [card_pos, 100], [card_pos + 50, 100], [card_pos + 50, 0]), 1, "White", "Green")
        i =i+1
   
 # create frame and add a button and labels
frame = simplegui.create_frame("MSorell Memory Game", 800, 100)
frame.add_button("Reset", new_game)
label1 = frame.add_label('Turns = ' +str(counter))


# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
new_game()
frame.start()


# Always remember to review the grading rubric