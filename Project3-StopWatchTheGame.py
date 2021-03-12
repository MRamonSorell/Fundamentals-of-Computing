# Author: Michael R.Sorell
# Fundamentals of Computing: Interactive Programming (Part 1)
# 8 November 2018

# template for "Stopwatch: The Game"


import simplegui
import random

# define global variables
count_message = ""
position = [250,250]
width= 500
height= 500
interval = 100 # program 100
counter=0
y=0
x=0
ms = 0
sw_run= True

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    global counter, count, count_message,check_minutes, ms
    count= int(counter)
    s = (count/10)%60
    m= count/600
    ms= count - (s*10)-(600*m) 
    
    minutes=str(m)
    milliseconds=str(ms)
    if s < 10:
        sa= str(s)
        sb= "0"
        seconds = sb+sa
    
    else:
        seconds=str(s)    
    
    count_message = minutes + ':' + seconds + '.' + milliseconds
    
    return count_message
    
# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    global counter, sw_run
    timer.start()
    sw_run= True
   
def stop():
    global y, x, counter, sw_run
    timer.stop()
    if (sw_run == True):
        y=y+1
        if (counter%10)== 0:
            x=x+1
        sw_run= False
    

def reset():
    global counter, y, x
    timer.stop()
    counter = 0
    y = 0
    x = 0
    sw_run = True
    
   

# define event handler for timer with 0.1 sec interval
def tick():
    global counter,y
    start()
    counter +=1
    #print counter
    
# define draw handler
def draw(canvas):
    global counter, count_message, y,x
    t= counter
    tries=str(y)
    hits = str(x)
    history= hits + '/' + tries
    stopwatch=format(t)
    canvas.draw_text(stopwatch, position, 48, "white")  
    canvas.draw_text(history, [450,35], 24, "red")
    
# create frame
frame = simplegui.create_frame("Home", width, height)

# register event handlers
timer = simplegui.create_timer(interval, tick)

frame.set_draw_handler(draw)
frame.add_button("Start", start, 200)
frame.add_button("Stop", stop, 200)
frame.add_button("Reset", reset, 200)

# start frame
frame.start()


# Please remember to review the grading rubric
