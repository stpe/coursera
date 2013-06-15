# Spaceship
# https://class.coursera.org/interactivepython-002/human_grading/view/courses/970391/assessments/34/submissions
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
started = False

# game constants
SHIP_TURN_VEL = 0.1
SHIP_THRUST_ACC = 0.15
SHIP_FRICTION = 0.99
ROCK_ANG_VEL_INTERVAL = 0.15
ROCK_VEL_INTERVAL = 2
MISSILE_VEL_FACTOR = 5
ROCK_LIMIT = 12
    
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
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

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
        image_center = [self.image_center[0] + (self.image_size[0] * int(self.thrust)), self.image_center[1]]
        canvas.draw_image(self.image, image_center, self.image_size, self.pos, self.image_size, self.angle)

    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel

        self.vel[0] *= SHIP_FRICTION
        self.vel[1] *= SHIP_FRICTION
        
        if self.thrust:
            forward_acc_vec = angle_to_vector(self.angle)
            self.vel[0] += SHIP_THRUST_ACC * forward_acc_vec[0]
            self.vel[1] += SHIP_THRUST_ACC * forward_acc_vec[1]
        
    def turn(self, dir):
        self.angle_vel = dir * SHIP_TURN_VEL
            
    def toggle_thrust(self, enabled):
        self.thrust = enabled

        if enabled:
            ship_thrust_sound.play()
        else:
            ship_thrust_sound.rewind()

    def shoot(self):
        global missile_group

        forward_acc_vec = angle_to_vector(self.angle)
        missile_pos = [self.pos[0] + (ship_info.get_radius() + 5) * forward_acc_vec[0], self.pos[1] + (ship_info.get_radius() + 5) * forward_acc_vec[1]]
        missile_vel = [self.vel[0] + MISSILE_VEL_FACTOR * forward_acc_vec[0], self.vel[1] + MISSILE_VEL_FACTOR * forward_acc_vec[1]]
        
        missile_group.add(Sprite(missile_pos, missile_vel, self.angle, 0, missile_image, missile_info, missile_sound))

    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos

    
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
        center = self.image_center
        
        if self.animated:
            center = [center[0] + self.image_size[0] * self.age, center[1]]

        canvas.draw_image(self.image, center, self.image_size, self.pos, self.image_size, self.angle)
                
    def update(self):
        self.pos[0] = (self.pos[0] + self.vel[0]) % WIDTH
        self.pos[1] = (self.pos[1] + self.vel[1]) % HEIGHT
        self.angle += self.angle_vel
        
        self.age += 1

        return self.lifespan <= self.age

    def collide(self, other_object):
        other_pos = other_object.get_position()
        other_radius = other_object.get_radius()
                
        return dist(other_pos, self.pos) < other_radius + self.radius
        
    def get_radius(self):
        return self.radius
    
    def get_position(self):
        return self.pos

    def get_velocity(self):
        return self.vel

def process_sprite_group(group, canvas):
    for sprite in set(group):
        sprite.draw(canvas)
        if sprite.update():
            group.remove(sprite)


def group_collide(group, other_object):
    collisions = 0
    for obj in set(group):
        if obj.collide(other_object):
            group.remove(obj)
            
            explosion_group.add(Sprite(obj.get_position(), obj.get_velocity(), 0, 0, explosion_image, explosion_info, explosion_sound))

            collisions += 1
            explosion_sound.play()

    return collisions

def group_group_collide(group1, group2):
    collisions = 0
    for obj in set(group1):
        if group_collide(group2, obj):
            group1.remove(obj)
            collisions += 1

    return collisions

def start():
    global lives, score, started
    
    lives = 3
    score = 0
    started = True
    soundtrack.rewind()
    soundtrack.play()

    
def draw(canvas):
    global time, lives, score, started, rock_group
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    # ui
    canvas.draw_text("Lives: " + str(lives), (110, 25), 24, "#00FF00", "monospace")
    canvas.draw_text("Score: " + str(score), (580, 25), 24, "#00FF00", "monospace")
    
    # ship
    my_ship.draw(canvas)
    my_ship.update()

    process_sprite_group(missile_group, canvas)
    process_sprite_group(rock_group, canvas)
    process_sprite_group(explosion_group, canvas)
    
    score += group_group_collide(missile_group, rock_group)
    
    if group_collide(rock_group, my_ship):
        lives -= 1
    
    if lives == 0:
        started = False
        soundtrack.pause()
        rock_group = set()
    
    if not started:
        center = splash_info.get_center()
        size = splash_info.get_size()
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH / 2, HEIGHT / 2], splash_info.get_size())
            

# timer handler that spawns a rock    
def rock_spawner():
    global rock_group
        
    # skip if not started or too many rocks
    if not started or len(rock_group) == ROCK_LIMIT:
        return

    pos = [random.randrange(0, WIDTH), random.randrange(0, HEIGHT)]
    
    # avoid having rocks spawn too close to the player
    if dist(pos, my_ship.get_position()) < my_ship.get_radius() * 4:
        return
    
    vel = [-ROCK_VEL_INTERVAL + random.random() * 2*ROCK_VEL_INTERVAL, -ROCK_VEL_INTERVAL + random.random() * 2*ROCK_VEL_INTERVAL]
    ang_vel = -ROCK_ANG_VEL_INTERVAL + random.random() * 2*ROCK_ANG_VEL_INTERVAL
    
    a_rock = Sprite(pos, vel, 0, ang_vel, asteroid_image, asteroid_info)
    rock_group.add(a_rock)

    
def keydown_handler(key):
    if key == simplegui.KEY_MAP["left"]:
        # turn left
        my_ship.turn(-1)
    elif key == simplegui.KEY_MAP["right"]:
        # turn right
        my_ship.turn(1)
    elif key == simplegui.KEY_MAP["up"]:
        # thruster
        my_ship.toggle_thrust(True)
    elif key == simplegui.KEY_MAP["space"]:
        # shoot
        my_ship.shoot()

        
def keyup_handler(key):
    if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
        # no turning
        my_ship.turn(0)
    elif key == simplegui.KEY_MAP["up"]:
        my_ship.toggle_thrust(False)

        
def mouseclick_handler(pos):
    if not started:
        start()
    
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

rock_group = set()
missile_group = set()
explosion_group = set()

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown_handler)
frame.set_keyup_handler(keyup_handler)
frame.set_mouseclick_handler(mouseclick_handler)
                             
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
