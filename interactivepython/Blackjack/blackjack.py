# Mini-project #6 - Blackjack

import simplegui
import random

# load card sprite - 949x392 - source: jfitz.com
CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
rounds = 0

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

DEALER_CARD_POS = [20, 120]
PLAYER_CARD_POS = [20, 340]


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        # create Hand object
        self.hand = []

    def __str__(self):
        # return a string representation of a hand
        result = []
        for card in self.hand:
            result.append(str(card))

        return " ".join(result) + ": " + str(self.get_value())

    def add_card(self, card):
        # add a card object to a hand
        self.hand.append(card)

    def get_value(self):
        # count aces as 1, if the hand has an ace, then add 10 to hand value if it doesn't bust
        result = 0
        for card in self.hand:
            result += VALUES[card.get_rank()]
            
        if [c for c in self.hand if c.get_rank() == "A"] and result + 10 <= 21:
            result += 10
            
        return result
   
    def is_busted(self):
        return self.get_value() > 21
    
    def draw(self, canvas, pos):
        offset = 0
        for i in range(0, len(self.hand)):
            self.hand[i].draw(canvas, (pos[0] + i * (CARD_SIZE[0] + 10), pos[1]))
             
        
# define deck class 
class Deck:
    def __init__(self):
        self.shuffle()

    def shuffle(self):
        # add cards back to deck and shuffle
        self.deck = []
        for suit in SUITS:
            for rank in RANKS:
                self.deck.append(Card(suit, rank))

        random.shuffle(self.deck)
        
    def deal_card(self):
        # deal a card object from the deck
        return self.deck.pop()
    
    def __str__(self):
        # return a string representing the deck
        result = []
        for card in self.deck:
            result.append(str(card))

        return "Length: " + str(len(result)) + ": " + ", ".join(result)


#define event handlers for buttons
def deal():
    global outcome, in_play, deck, dealer, player, rounds

    if in_play:
        outcome = "You lost. New round - hit or stand?"
    else:
        in_play = True
        outcome = "Hit or Stand?"

    rounds += 1
        
    deck.shuffle()
    player = Hand()
    dealer = Hand()
    
    player.add_card(deck.deal_card());
    player.add_card(deck.deal_card());
    dealer.add_card(deck.deal_card());
    dealer.add_card(deck.deal_card());

def hit():
    global in_play, outcome
    
    if in_play:
        # if the hand is in play, hit the player
        player.add_card(deck.deal_card())
            
        # if busted, assign a message to outcome, update in_play and score
        if player.is_busted():
            outcome = "You have busted."
            in_play = False
   
       
def stand():
    global in_play, score, outcome
    
    if player.is_busted():
        return

    if in_play:        
        # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
   
        in_play = False
        
        # assign a message to outcome, update in_play and score
        if dealer.is_busted():
            outcome = "Dealer have busted."
            score += 1
        elif player.get_value() < dealer.get_value():
            outcome = "Dealer won."
        elif player.get_value() == dealer.get_value():
            outcome = "Tie! Dealer won."
        else:
            outcome = "Player won."
            score += 1
           

# draw handler    
def draw(canvas):
    # draw title
    canvas.draw_text("Black Jack", [200, 40], 42, "Yellow")
    
    # draw outcome
    msg = outcome
    if not in_play:
        msg += " New deal?"
    canvas.draw_text(msg, [20, 270], 32, "White")
    
    # draw cards
    dealer.draw(canvas, DEALER_CARD_POS)
    player.draw(canvas, PLAYER_CARD_POS)

    canvas.draw_text("Dealer", [DEALER_CARD_POS[0], DEALER_CARD_POS[1] - 16], 24, "Black")
    canvas.draw_text("Player", [PLAYER_CARD_POS[0], PLAYER_CARD_POS[1] - 16], 24, "Black")

    # draw score
    canvas.draw_text("Wins: " + str(score) + ", Rounds: " + str(rounds), [220, 80], 18, "Yellow")

    # if in play, hide dealer's hole card
    if in_play:
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE, [DEALER_CARD_POS[0] + CARD_BACK_CENTER[0], DEALER_CARD_POS[1] + CARD_BACK_CENTER[1]], CARD_BACK_SIZE)
    

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)

# init
deck = Deck()
dealer = Hand()
player = Hand()

# get things rolling
frame.start()
