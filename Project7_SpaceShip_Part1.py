# Author:  Michael R. Sorell
# Date: 07 - Feb- 2019

# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0
new_WIDTH = 0
new_HEIGHT = 0
rock_group= []

class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.f2014.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# alternative upbeat soundtrack by composer and former IIPP student Emiel Stopler
# please do not redistribute without permission from Emiel at http://www.filmcomposer.nl
#soundtrack = simplegui.load_sound("https://storage.googleapis.com/codeskulptor-assets/ricerocks_theme.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "White", "White")
        # draw the thrust image when self.thust is true and draw the regular image otherwise.
        if self.thrust == True:
            canvas.draw_image(self.image, [135, 45], self.image_size, self.pos, self.image_size, self.angle)

        else: 
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
            
    def update(self):
        friction = .01 
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1] 
        
        # create forward calculation so ship moves forward in direction
        forward = angle_to_vector(self.angle)
        
        if self.thrust == True:
            self.vel[0] += (.20)*forward[0] 
            self.vel[1] += (.20)*forward[1]
        
        self.vel[0] *= (1-friction)
        self.vel[1] *= (1-friction)
        
        # update ships position to wrap around screen
        if self.pos[0] > (WIDTH + self.radius):
            self.pos[0] = new_WIDTH
         
        if self.pos[0] < 0:
            self.pos[0] = WIDTH
            
        if self.pos[1] < 0:
            self.pos[1] = HEIGHT
         
        if self.pos[1] > (HEIGHT + self.radius):
            self.pos[1] = new_HEIGHT
        
        
    def keydown(self, key):
        # velocity program from pong. see notes 
        ship_acc = 0.5
        ship_orient = 0.1
        
        if key==simplegui.KEY_MAP["left"]:
            self.angle_vel -= ship_orient
        
        elif key==simplegui.KEY_MAP["right"]:
            self.angle_vel += ship_orient
            
        elif key==simplegui.KEY_MAP["down"]:
            self.vel[1] += ship_acc
            
        if key==simplegui.KEY_MAP["space"]:
            self.shoot()
           
        # this sets the self.thrust to true when the up key is down.
        elif key==simplegui.KEY_MAP["up"]:
            self.vel[1] -= ship_acc
            self.thrust = True
            if self.thrust == True:
                ship_thrust_sound.play()

        
            
            
    def keyup(self, key):
        # reset all the original settings when keys are up.  ship should remain in last position.
        self.vel[0] = 0
        self.angle_vel = 0
        self.thrust = False
        if self.thrust == False:
                ship_thrust_sound.pause()
        
     
    def shoot(self):
        global a_missile
        forward = angle_to_vector(self.angle)
        # this creates the speed and direction of missile, I first create the
        # missile velocity using the ship's velocity
        miss_vel=[self.vel[0],self.vel[1]]
        miss_vel[0]= self.vel[0] + (5)*forward[0] 
        miss_vel[1]= self.vel[1] + (5)*forward[1]
        
        #this creates the position of the missile, i first take the ship's center
        #i then mulitply the forward by radians and add that to the ship's center
        
        miss_pos=[self.pos[0], self.pos[1]]
        miss_radius= self.radius
        miss_pos[0] =self.pos[0] + (forward[0] *miss_radius)
        miss_pos[1] =self.pos[1] + (forward[1] *miss_radius)
        a_missile=Sprite([miss_pos[0], miss_pos[1]], [miss_vel[0],miss_vel[1]], 0, 0, missile_image, missile_info, missile_sound)
        
    
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        #canvas.draw_circle(self.pos, self.radius, 1, "Red", "Red")
        #canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
        for items in rock_group:
            canvas.draw_image(self.image, self.image_center, self.image_size, self.pos, self.image_size, self.angle)
        
        if len(rock_group)== 2:
            rock_group.pop(0)
  
            
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
    
           
def draw(canvas):
    global time
    
    # animiate background
    time += 1
    wtime = (time / 4) % WIDTH
    center = debris_info.get_center()
    size = debris_info.get_size()
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, center, size, (wtime - WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))
    canvas.draw_image(debris_image, center, size, (wtime + WIDTH / 2, HEIGHT / 2), (WIDTH, HEIGHT))

    # draw ship and sprites
    my_ship.draw(canvas)
    a_rock.draw(canvas)
    a_missile.draw(canvas)
    
    # update ship and sprites
    my_ship.update()
    a_rock.update()
    a_missile.update()
    
    # print lives and score to canvas
    # prints outcome of score
    game_score = str(score)
    game_lives = str(lives)
    
    canvas.draw_text('Lives', (50, 35), 36, 'White')
    canvas.draw_text('Score', (650, 35), 36, 'White')
    
    canvas.draw_text(game_score, (675, 75), 36, 'White')
    canvas.draw_text(game_lives, (75, 75), 36, 'White')
            
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock
    x= random.randint(0,800)
    y= random.randint(0,400)
    a_rock=Sprite([x, y], [1, 1], 0, 0, asteroid_image, asteroid_info)
    rock_group.append(a_rock)
    
# initialize frame
frame = simplegui.create_frame("M. Sorell Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
a_rock = Sprite([WIDTH / 3, HEIGHT / 3], [1, 1], 0, 0, asteroid_image, asteroid_info)
a_missile = Sprite([2 * WIDTH/3 , 2 * HEIGHT/3 ], [-1,1], 0, 0, missile_image, missile_info, missile_sound)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(my_ship.keydown)
frame.set_keyup_handler(my_ship.keyup)

timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()