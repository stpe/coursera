# Memory
# https://class.coursera.org/interactivepython-002/human_grading/view/courses/970391/assessments/32/submissions

import simplegui
import math
import random

"""
note: as long as number of cards is set to an even
square (16, 25, 36, etc) all should look nice
"""
WIDTH = 400
HEIGHT = 400
NUM_CARDS = 16
SIDE = math.sqrt(NUM_CARDS)
CARD_WIDTH = WIDTH / SIDE
CARD_HEIGHT = HEIGHT / SIDE

# game state constants
STATE_START = 0
STATE_SINGLE_CARD = 1
STATE_END_OF_TURN = 2

# globals
cards = range(0, NUM_CARDS / 2) + range(0, NUM_CARDS / 2)
exposed = []
state = STATE_START
cards_in_play = [-1, -1]
turns = 0

def init():
    global exposed, turns
    random.shuffle(cards)
    exposed = [False] * len(cards)
    turns = 0
    label.set_text("Moves = " + str(turns))
    cards_in_play = [-1, -1]

     
def mouseclick(pos):
    global exposed, state, cards_in_play, turns

    # calculate what card was clicked
    card = (pos[1] // CARD_HEIGHT) * SIDE + pos[0] // CARD_WIDTH
    
    if not exposed[card]:
        exposed[card] = True
        
        if state == STATE_START:
            state = STATE_SINGLE_CARD
            cards_in_play[0] = card
        elif state == STATE_SINGLE_CARD:
            state = STATE_END_OF_TURN
            cards_in_play[1] = card
        else:
            state = STATE_SINGLE_CARD
            
            # hide the two exposed cards if not the same
            if cards[cards_in_play[0]] != cards[cards_in_play[1]]:
                exposed[cards_in_play[0]] = False
                exposed[cards_in_play[1]] = False            

            cards_in_play = [card, -1]

        # count turns
        if state == STATE_SINGLE_CARD:
            turns += 1
            label.set_text("Moves = " + str(turns))

            
def draw(c):    
    # draw cards
    for i in range(0, len(cards)):
        # calculate x, y position of card 
        x = i % SIDE * CARD_WIDTH
        y = i // SIDE * CARD_HEIGHT
        
        # if card currently in play, draw blue background
        if i in cards_in_play:
            c.draw_polygon([(x, y), (x + CARD_WIDTH, y), (x + CARD_WIDTH, y + CARD_HEIGHT), (x, y + CARD_HEIGHT), (x, y)], 1, "Black", "Blue")

        if exposed[i]:
            c.draw_text(str(cards[i]), (x - 10 + CARD_WIDTH // 2, y + 10 + CARD_HEIGHT // 2), 42, "White")
        else:
            c.draw_polygon([(x, y), (x + CARD_WIDTH, y), (x + CARD_WIDTH, y + CARD_HEIGHT), (x, y + CARD_HEIGHT), (x, y)], 1, "White", "Green")


# create frame and add a button and labels
frame = simplegui.create_frame("Memory", WIDTH, HEIGHT)
frame.add_button("Restart", init)
label = frame.add_label("Moves = 0")

# initialize global variables
init()

# register event handlers
frame.set_mouseclick_handler(mouseclick)
frame.set_draw_handler(draw)

# get things rolling
frame.start()
