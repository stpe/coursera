# Memory
# https://class.coursera.org/interactivepython-002/human_grading/view/courses/970391/assessments/32/submissions

import simplegui
import random

WIDTH = 800
HEIGHT = 100
NUM_CARDS = 16
CARD_WIDTH = WIDTH / NUM_CARDS

cards = range(0, NUM_CARDS / 2) + range(0, NUM_CARDS / 2)
exposed = []

# helper function to initialize globals
def init():
    global exposed
    random.shuffle(cards)
    exposed = [False] * len(cards)
    exposed[3] = True

     
# define event handlers
def mouseclick(pos):
    global exposed
    card = pos[0] // CARD_WIDTH
    if not exposed[card]:
        exposed[card] = True
    
                        
# cards are logically 50x100 pixels in size    
def draw(c):
    for i in range(0, len(cards)):
        if exposed[i]:
            c.draw_text(str(cards[i]), (15 + i * CARD_WIDTH, 65), 42, "White")
        else:
            c.draw_polygon([(i * CARD_WIDTH, 0), (i * CARD_WIDTH + CARD_WIDTH, 0), (i * CARD_WIDTH + CARD_WIDTH, 100), (i * CARD_WIDTH, 100), (i * CARD_WIDTH, 0)], 1, "White", "Green")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", 800, 100)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()


# Always remember to review the grading rubric