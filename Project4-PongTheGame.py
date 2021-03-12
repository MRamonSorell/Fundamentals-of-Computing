# Author Michael R. Sorell
# Fundamentals of Computing: Interactive Programming (Part 1)
# 14- November -2018

# Implementation of classic arcade game Pong

import simplegui
import random

# initialize globals - pos and vel encode vertical info for paddles
WIDTH = 600
HEIGHT = 400       
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
ball_pos = [WIDTH / 2, HEIGHT / 2]
ball_vel = [0,0] 
PLAY_1 = 0
PLAY_2 = 0
paddle1_pos=180
paddle2_pos=180
paddle1_vel = 0
paddle2_vel = 0

# initialize ball_pos and ball_vel for new bal in middle of table
# if direction is RIGHT, the ball's velocity is upper right, else upper left
def spawn_ball(direction):
    global ball_pos, ball_vel # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [0, 0] #pixels per update (1/60 seconds)
    
    if direction == "RIGHT":
        ball_vel[0] = random.randrange(2, 3)
        ball_vel[1] = - random.randrange(2, 3)
       
    elif direction == "LEFT":
        ball_vel[0] = - random.randrange(2, 3)
        ball_vel[1] = - random.randrange(2, 3)
        

# define event handlers
def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel,PLAY_1,PLAY_2  # these are numbers
    global score1, score2  # these are ints
    PLAY_1 = 0
    PLAY_2 = 0
    spawn_ball("RIGHT")
    
   
def draw(canvas):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel, PLAY_1,PLAY_2, paddle1_vel, paddle2_vel
 
    # draw mid line and gutters
    canvas.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
        
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # if the ball goes to the right than player 1 (left gets a point)
    if ball_pos[0] >= (WIDTH- BALL_RADIUS):
        PLAY_1 += 1
        spawn_ball("LEFT")
     
    # if the ball goes to the left than player 2(right get a point)
    if ball_pos[0] <= (0 + BALL_RADIUS):
        PLAY_2 += 1
        spawn_ball("RIGHT")
    
    if ball_pos[1] == (HEIGHT -BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
     
    if ball_pos[1] == (0 + BALL_RADIUS):
        ball_vel[1] = -ball_vel[1]
            
    # draw ball
    canvas.draw_circle(ball_pos, BALL_RADIUS, 2, "White", "White")

    # update paddle's vertical position, keep paddle on the screen
    
    paddle1_pos += paddle1_vel
    
    if paddle1_pos < (0 + HALF_PAD_HEIGHT):
        paddle1_vel = 0
    
    if paddle1_pos > (280 + HALF_PAD_HEIGHT):
        paddle1_vel = 0
       
    paddle2_pos += paddle2_vel
    
    if paddle2_pos < (0 + HALF_PAD_HEIGHT):
        paddle2_vel = 0
    
    if paddle2_pos > (280 + HALF_PAD_HEIGHT):
        paddle2_vel = 0
        
    
    
    # draw paddles
    canvas.draw_line([HALF_PAD_WIDTH, paddle1_pos- HALF_PAD_HEIGHT],[HALF_PAD_WIDTH, paddle1_pos + PAD_HEIGHT], 8, 'White')
    canvas.draw_line([WIDTH-HALF_PAD_WIDTH, paddle2_pos- HALF_PAD_HEIGHT],[WIDTH-HALF_PAD_WIDTH, paddle2_pos + PAD_HEIGHT], 8, 'White')
    
    
    # determine whether paddle and ball collide
    # orgigal had (40,40) but this doesn't capture edges of paddles well 
    # values were chaged to +/- 4 to caputure edges
    
    if ball_pos[0] <=(BALL_RADIUS+PAD_WIDTH) and ball_pos[1]>(paddle1_pos-34) and ball_pos[1]<(paddle1_pos+44):
        ball_vel[0] += 0.2 * ball_vel[0]
        ball_vel[0] = - ball_vel[0]
    
    if ball_pos[0] >= WIDTH-(BALL_RADIUS+PAD_WIDTH) and ball_pos[1]>(paddle2_pos-34) and ball_pos[1]<(paddle2_pos+44):
        ball_vel[0] += 0.2 * ball_vel[0]
        ball_vel[0] = - ball_vel[0]
    
    # draw scores
    score1 = str(PLAY_1)
    score2 = str(PLAY_2)
    canvas.draw_text(score1, [150,50], 48, "white")
    canvas.draw_text(score2, [450,50], 48, "white")
        
def keydown(key):
    global paddle1_vel, paddle2_vel
    # acc increased from 1 to 1.5
    acc=1.5
    if key==simplegui.KEY_MAP["w"]:
        paddle1_vel -= acc
    if key==simplegui.KEY_MAP["s"]:
        paddle1_vel += acc
        
    if key==simplegui.KEY_MAP["up"]:
        paddle2_vel -= acc
    if key==simplegui.KEY_MAP["down"]:
        paddle2_vel += acc
        
def keyup(key):
    global paddle1_vel, paddle2_vel
    paddle1_vel = 0
    paddle2_vel = 0
    
def restart():
    new_game()


# create frame
frame = simplegui.create_frame("M.R.Sorell Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Restart", restart,200) 


# start frame
new_game()
frame.start()
