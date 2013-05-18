# Implementation of classic arcade game Pong
# https://class.coursera.org/interactivepython-002/human_grading/view/courses/970391/assessments/31/submissions

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
PAD_VELOCITY = 4

ball_pos = [0, 0]
ball_vel = [0, 0]

# helper function that spawns a ball by updating the 
# ball's position vector and velocity vector
# if right is True, the ball's velocity is upper right, else upper left
def ball_init(right):
    global ball_pos, ball_vel # these are vectors stored as lists

    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = [random.randrange(3, 6), -random.randrange(2, 5)]

    if not right:
        ball_vel[0] *= -1
    
# define event handlers

def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel  # these are floats
    global score1, score2  # these are ints
    
    score1 = 0
    score2 = 0
    
    paddle1_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle2_pos = HEIGHT / 2 - HALF_PAD_HEIGHT
    paddle1_vel = 0
    paddle2_vel = 0
    
    start_ball_direction = random.choice([True, False])
    ball_init(start_ball_direction)

def draw(c):
    global score1, score2, paddle1_pos, paddle2_pos, ball_pos, ball_vel
 
    # update paddle's vertical position, keep paddle on the screen
    if (paddle1_pos + paddle1_vel < HEIGHT - PAD_HEIGHT and paddle1_pos + paddle1_vel > 0):
        paddle1_pos += paddle1_vel
        
    if (paddle2_pos + paddle2_vel < HEIGHT - PAD_HEIGHT and paddle2_pos + paddle2_vel > 0):
        paddle2_pos += paddle2_vel
        
    # draw mid line and gutters
    c.draw_line([WIDTH / 2, 0],[WIDTH / 2, HEIGHT], 1, "White")
    c.draw_line([PAD_WIDTH, 0],[PAD_WIDTH, HEIGHT], 1, "White")
    c.draw_line([WIDTH - PAD_WIDTH, 0],[WIDTH - PAD_WIDTH, HEIGHT], 1, "White")
    
    # draw paddles
    c.draw_polygon([(0, paddle1_pos), (PAD_WIDTH, paddle1_pos), (PAD_WIDTH, paddle1_pos + PAD_HEIGHT), (0, paddle1_pos + PAD_HEIGHT), (0, paddle1_pos)], 2, "Green", "Green")
    c.draw_polygon([(WIDTH - PAD_WIDTH, paddle2_pos), (WIDTH, paddle2_pos), (WIDTH, paddle2_pos + PAD_HEIGHT), (WIDTH - PAD_WIDTH, paddle2_pos + PAD_HEIGHT), (WIDTH - PAD_WIDTH, paddle2_pos)], 2, "Green", "Green")
     
    # update ball
    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]
    
    # gutter hit
    if ball_pos[0] <= PAD_WIDTH + BALL_RADIUS or ball_pos[0] > WIDTH - PAD_WIDTH - BALL_RADIUS:
        # check if paddle hit
        if ((ball_vel[0] < 0 and ball_pos[1] >= paddle1_pos and ball_pos[1] <= paddle1_pos + PAD_HEIGHT) or
            (ball_vel[0] > 0 and ball_pos[1] >= paddle2_pos and ball_pos[1] <= paddle2_pos + PAD_HEIGHT)):
            # bounce
            ball_vel[0] *= -1
            # increase velocity
            ball_vel[0] *= 1.1
            ball_vel[1] *= 1.1
        else:
            if ball_vel[0] > 0:
                score1 += 1
            else:
                score2 += 1
                
            ball_init(ball_vel[0] < 0)
    
    # top/bottom bounce
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] > HEIGHT - BALL_RADIUS:
        ball_vel[1] *= -1

    # draw ball and scores
    c.draw_circle(ball_pos, BALL_RADIUS, 2, "Green", "Black")
    c.draw_text(str(score1), (50, 50), 36, "Orange")
    c.draw_text(str(score2), (WIDTH - 50, 50), 36, "Orange")
    
def keydown(key):
    global paddle1_vel, paddle2_vel
    
    # set paddle velocity
    if key == simplegui.KEY_MAP["w"]:
        paddle1_vel = -PAD_VELOCITY
    elif key == simplegui.KEY_MAP["s"]:
        paddle1_vel = PAD_VELOCITY
    elif key == simplegui.KEY_MAP["up"]:
        paddle2_vel = -PAD_VELOCITY
    elif key == simplegui.KEY_MAP["down"]:
        paddle2_vel = PAD_VELOCITY
        
def keyup(key):
    global paddle1_vel, paddle2_vel

    # reset paddle velocity
    if key in [simplegui.KEY_MAP["w"], simplegui.KEY_MAP["s"]]:
        paddle1_vel = 0
    elif key in [simplegui.KEY_MAP["up"], simplegui.KEY_MAP["down"]]:
        paddle2_vel = 0

# create frame
frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
frame.set_draw_handler(draw)
frame.set_keydown_handler(keydown)
frame.set_keyup_handler(keyup)
frame.add_button("Reset", new_game)

new_game()

# start frame
frame.start()
