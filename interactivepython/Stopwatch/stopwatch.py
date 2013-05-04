# Stopwatch: The Game
# https://class.coursera.org/interactivepython-002/human_grading/view/courses/970391/assessments/30/submissions

import simplegui

# define global variables
count = 0
attempts = 0
success = 0

# define helper function format that converts time
# in tenths of seconds into formatted string A:BC.D
def format(t):
    min = t // 600
    sec = t // 10 - min * 60
    tenth = t % 10

    if (sec < 10):
        sec = "0" + str(sec)
    else:
        sec = str(sec)
    
    return str(min) + ":" + sec + "." + str(tenth)

# define event handlers for buttons; "Start", "Stop", "Reset"
def start():
    timer.start()

def stop():
    global attempts, success
    
    # do nothing if timer is already stopped
    if not timer.is_running():
        return

    timer.stop()

    # test if stopped on whole second
    attempts = attempts + 1
    if count % 10 == 0:
        success = success + 1

def reset():
    global count, attempts, success
    count = 0
    attempts = 0
    success = 0
    timer.stop()

# define event handler for timer with 0.1 sec interval
def timer_handler():
    global count
    count = count + 1

# define draw handler
def draw_handler(canvas):
    # time
    canvas.draw_text(format(count), (50, 100), 42, "white")
    
    # success / attempts
    canvas.draw_text(str(success) + "/" + str(attempts), (165, 20), 18, "white")
    
# create frame
frame = simplegui.create_frame("Stopwatch", 200, 200, 150)

# register event handlers
frame.add_button("Start", start, 150)
frame.add_button("Stop", stop, 150)
frame.add_button("Reset", reset, 150)

frame.set_draw_handler(draw_handler)

timer = simplegui.create_timer(100, timer_handler)

# start frame
frame.start()
