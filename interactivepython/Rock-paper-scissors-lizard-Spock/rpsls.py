# Rock-paper-scissors-lizard-Spock
# https://class.coursera.org/interactivepython-002/human_grading/view/courses/970391/assessments/28/submissions

import random

def number_to_name(number):
    if number == 0:
        name = "rock"
    elif number == 1:
        name = "Spock"
    elif number == 2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    elif number == 4:
        name = "scissors"
    else:
        print "Invalid number!"
    
    return name

    
def name_to_number(name):
    if name == "rock":
        number = 0
    elif name == "Spock":
        number = 1
    elif name == "paper":
        number = 2
    elif name == "lizard":
        number = 3
    elif name == "scissors":
        number = 4
    else:
        print "Invalid name!"
    
    return number


def rpsls(name): 
    # convert name to player_number using name_to_number
    player_number = name_to_number(name)

    # compute random guess for comp_number using random.randrange()
    comp_number = random.randrange(0, 5)

    # compute difference of player_number and comp_number modulo five
    diff = (player_number - comp_number) % 5

    # print results
    print     
    print "Player chooses " + number_to_name(player_number)
    print "Computer chooses " + number_to_name(comp_number)

    # use if/elif/else to determine winner
    if diff == 0:
        print "Player and computer tie!"    
    elif diff <= 2:
        print "Player wins!"
    else:
        print "Computer wins!"
    
    
# test your code
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric
