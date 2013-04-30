# Guess the number
# https://class.coursera.org/interactivepython-002/human_grading/view/courses/970391/assessments/29/submissions

import random
import simplegui
import math

# initialize global variables used in your code
secret = 0
guesses = 0
range = 100

def start_game(start_range):
    global range, secret, guesses

    # store range so any subsequent games uses the same range
    range = start_range
    
    # randomize secret number
    secret = random.randrange(0, start_range)    

    # calculate allowed number of guesses
    guesses = math.ceil(math.log(start_range + 1, 2))

    print "Starting new game in range 0 - " + str(start_range) + " with " + str(guesses) + " allowed guesses."
    
# define event handlers for control panel    
def range100():
    # button that changes range to range [0,100) and restarts
    start_game(100)

def range1000():
    # button that changes range to range [0,1000) and restarts
    start_game(1000)
    
def input_guess(guess):
    # main game logic goes here
    global guesses
    guesses = guesses - 1
    
    if int(guess) > secret:
        print "Sorry, the number is lower than " + guess + "! " + str(guesses) + " guesses left."
    elif int(guess) < secret:
        print "Sorry, the number is higher than " + guess + "! " + str(guesses) + " guesses left."
    else:
        print "Right on! " + guess + " was correct!"
        start_game(range)
        return
    
    if (guesses == 0):
        print "You loose!"
        start_game(range)
    
# create frame
frame = simplegui.create_frame("Guess the number", 0, 200, 150)

# register event handlers for control elements
frame.add_button("Range: 0 - 100", range100, 150)
frame.add_button("Range: 0 - 1000", range1000, 150)
frame.add_input("Your guess:", input_guess, 100)

# start frame
frame.start()

# start game
range100()
