"""The Game of Hog."""

from dice import four_sided, six_sided, make_test_dice
from ucb import main, trace, log_current_line, interact
from operator import sub, mul, add
GOAL_SCORE = 100 # The goal of Hog is to score 100 points.

######################
# Phase 1: Simulator #
######################

def roll_dice(num_rolls, dice=six_sided):
    """Roll DICE for NUM_ROLLS times.  Return either the sum of the outcomes,
    or 1 if a 1 is rolled (Pig out). This calls DICE exactly NUM_ROLLS times.

    num_rolls:  The number of dice rolls that will be made; at least 1.
    dice:       A zero-argument function that returns an integer outcome.
    """
    # These assert statements ensure that num_rolls is a positive integer.
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls > 0, 'Must roll at least once.'
    "*** YOUR CODE HERE ***"
    sum_of_outcomes = 0
    pig_out = 0
    while (num_rolls != 0):
        num_rolls  = num_rolls - 1
        dice_roll = dice() #Returns the number rolled
        if(dice_roll == 1): #Checks for pig out rule
            pig_out = 1
        sum_of_outcomes = sum_of_outcomes + dice_roll
    if (pig_out ==1 ): #If the player rolled a one, his score will be 1
        return 1
    return sum_of_outcomes

def take_turn(num_rolls, opponent_score, dice=six_sided):
    """Simulate a turn rolling NUM_ROLLS dice, which may be 0 (Free bacon).

    num_rolls:       The number of dice rolls that will be made.
    opponent_score:  The total score of the opponent.
    dice:            A function of no args that returns an integer outcome.
    """
    assert type(num_rolls) == int, 'num_rolls must be an integer.'
    assert num_rolls >= 0, 'Cannot roll a negative number of dice.'
    assert num_rolls <= 10, 'Cannot roll more than 10 dice.'
    assert opponent_score < 100, 'The game should be over.'
    "*** YOUR CODE HERE ***"
    if (num_rolls > 0):
        return roll_dice(num_rolls, dice)
    else:
        return abs(sub(opponent_score%10, opponent_score//10)) + 1 
        #Adds 1 to the absolute value of the difference of the tens and ones digit


def select_dice(score, opponent_score):
    """Select six-sided dice unless the sum of SCORE and OPPONENT_SCORE is a
    multiple of 7, in which case select four-sided dice (Hog wild).
    """
    "*** YOUR CODE HERE ***"
    if((score+opponent_score)%7 == 0):
        return four_sided
    else:
        return six_sided

def bid_for_start(bid0, bid1, goal=GOAL_SCORE):
    """Given the bids BID0 and BID1 of each player, returns three values:

    - the starting score of player 0
    - the starting score of player 1
    - the number of the player who rolls first (0 or 1)
    """
    assert bid0 >= 0 and bid1 >= 0, "Bids should be non-negative!"
    assert type(bid0) == int and type(bid1) == int, "Bids should be integers!"
    from random import randint
    # The buggy code is below:
    if bid0 == bid1:
        return goal, goal, randint(0, 1)
    if bid0 == bid1 - 5:
        return 0, 10, 1
    if bid1 == bid0 - 5:
        return 10, 0, 0
    if bid1 > bid0:
        return bid1, bid0, 1
    else:
        return bid1, bid0, 0

def other(who):
    """Return the other player, for a player WHO numbered 0 or 1.

    >>> other(0)
    1
    >>> other(1)
    0
    """
    return 1 - who

def play(strategy0, strategy1, score0=0, score1=0, goal=GOAL_SCORE):
    """Simulate a game and return the final scores of both players, with
    Player 0's score first, and Player 1's score second.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    strategy0:  The strategy function for Player 0, who plays first
    strategy1:  The strategy function for Player 1, who plays second
    score0   :  The starting score for Player 0
    score1   :  The starting score for Player 1
    """
    who = 0  # Which player is about to take a turn, 0 (first) or 1 (second)
    "*** YOUR CODE HERE ***"
    counter = max(score0,score1)
    while (counter < goal): #Game ends when someone reaches goal
        if(who == 0): #Which player is going           
            score0 =  score0 + take_turn(strategy0(score0,score1), score1, select_dice(score0,score1))
        else:
            score1 = score1 + take_turn(strategy1(score1,score0), score0, select_dice(score1,score0))   
        if(score1 == 2*score0 or score0 == 2*score1): #Swine swap
            score0,score1 = score1,score0
        who = other(who) #Switch players
        counter = max(score1,score0)
    return score0,score1

#######################
# Phase 2: Strategies #
#######################

def always_roll(n):
    """Return a strategy that always rolls N dice.

    A strategy is a function that takes two total scores as arguments
    (the current player's score, and the opponent's score), and returns a
    number of dice that the current player will roll this turn.

    >>> strategy = always_roll(5)
    >>> strategy(0, 0)
    5
    >>> strategy(99, 99)
    5
    """
    def strategy(score, opponent_score):
        return  int (n)
    return strategy

# Experiments

def make_averaged(fn, num_samples=1000):
    """Return a function that returns the average_value of FN when called.

    To implement this function, you will have to use *args syntax, a new Python
    feature introduced in this project.  See the project description.

    >>> dice = make_test_dice(3, 1, 5, 6)
    >>> averaged_dice = make_averaged(dice, 1000)
    >>> averaged_dice()
    3.75
    >>> make_averaged(roll_dice, 1000)(2, dice)
    6.0

    In this last example, two different turn scenarios are averaged.
    - In the first, the player rolls a 3 then a 1, receiving a score of 1.
    - In the other, the player rolls a 5 and 6, scoring 11.
    Thus, the average value is 6.0.
    """
    "*** YOUR CODE HERE ***"
    def averaged_dice(*args):
        avg = 0
        count = 0
        while (count < num_samples):
            avg = avg + fn(*args)
            count = count + 1
        return avg/num_samples
    return averaged_dice

def max_scoring_num_rolls(dice=six_sided):
    """Return the number of dice (1 to 10) that gives the highest average turn
    score by calling roll_dice with the provided DICE.  Print all averages as in
    the doctest below.  Assume that dice always returns positive outcomes.

    >>> dice = make_test_dice(3)
    >>> max_scoring_num_rolls(dice)
    10
    """
    "*** YOUR CODE HERE ***"
    temp_max= 1
    counter = 1
    highest_average_roll= 1
    while(counter <= 10):
        average = make_averaged(roll_dice, 1000)(counter, dice)
        
        if(average > temp_max):
            temp_max = average
            highest_average_roll = counter
        counter +=1
    return highest_average_roll
        

def winner(strategy0, strategy1):
    """Return 0 if strategy0 wins against strategy1, and 1 otherwise."""
    score0, score1 = play(strategy0, strategy1)
    if score0 > score1:
        return 0
    else:
        return 1

def average_win_rate(strategy, baseline=always_roll(5)):
    """Return the average win rate (0 to 1) of STRATEGY against BASELINE."""
    win_rate_as_player_0 = 1 - make_averaged(winner)(strategy, baseline)
    win_rate_as_player_1 = make_averaged(winner)(baseline, strategy)
    return (win_rate_as_player_0 + win_rate_as_player_1) / 2 # Average results

def run_experiments():
    """Run a series of strategy experiments and report results."""
    if True: # Change to False when done finding max_scoring_num_rolls
        six_sided_max = max_scoring_num_rolls(six_sided)
        print('Max scoring num rolls for six-sided dice:', six_sided_max)
        four_sided_max = max_scoring_num_rolls(four_sided)
        print('Max scoring num rolls for four-sided dice:', four_sided_max)

    if False: # Change to True to test always_roll(8)
        print('always_roll(8) win rate:', average_win_rate(always_roll(8)))

    if False: # Change to True to test bacon_strategy
        print('bacon_strategy win rate:', average_win_rate(bacon_strategy))

    if False: # Change to True to test swap_strategy
        print('swap_strategy win rate:', average_win_rate(swap_strategy))

    if True: # Change to True to test final_strategy
        print('final_strategy win rate:', average_win_rate(final_strategy))

    "*** You may add additional experiments as you wish ***"

# Strategies

def bacon_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice if that gives at least MARGIN points,
    and rolls NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    bacon = (abs(sub(opponent_score%10, opponent_score//10)) + 1)
    if(bacon >= margin):
        return 0
    else:
        return int (num_rolls)

def swap_strategy(score, opponent_score, margin=8, num_rolls=5):
    """This strategy rolls 0 dice when it would result in a beneficial swap and
    rolls NUM_ROLLS if it would result in a harmful swap. It also rolls
    0 dice if that gives at least MARGIN points and rolls
    NUM_ROLLS otherwise.
    """
    "*** YOUR CODE HERE ***"
    bacon = abs(sub(opponent_score%10, opponent_score//10)) + 1
    new_score = add(score, bacon)
    if( mul(new_score, 2) == opponent_score or bacon >= margin):
        if(new_score/2 == opponent_score):
            return num_rolls
        return 0
    else:
        return num_rolls

def final_strategy(score, opponent_score):
    """Write a brief description of your final strategy.

    *** YOUR DESCRIPTION HERE ***
    """
    "*** YOUR CODE HERE ***"
    
    bacon = abs(sub(opponent_score%10, opponent_score//10)) + 1
    roll = swap_strategy(score, opponent_score, 8, 6)

    #If bacon wins the game, return 0 and immediately win
    if (bacon+score)>=100:
        return 0
    #Forces opponent to roll 4-sided dice if your score is less than 15 away
    if(opponent_score - score < 15 and (score + bacon + opponent_score)%7 == 0):
        return 0

    #Increases expected value if forced to roll a 4-sided dice
    if((score + opponent_score)%7 == 0): 
        roll = swap_strategy(score, opponent_score, 4, 3)

    #If you are 1 away from half the opponent's score
    if(score + 1 == opponent_score/2 or score + 1 == (opponent_score +1)/2):
        roll = 10 

    #Roll less dice when the score is high enough
    if(score > 75): 
        if (bacon < 7):
            roll = 5
        else:
            roll = 0

    #Likely to finish in 3 turns
    if(score > 84): 
        if (bacon < 6):
            roll = 3
        else:
            roll = 0

    #Likely to finish in 2 turns
    if(score > 93): 
        if (bacon < 4):
            roll = 2
        else:
            roll = 0

    #Likely to finish in 1 turn
    if(score > 97): 
        if (bacon < 3):
            roll = 1
        else:
            roll = 0

    return roll

    

##########################
# Command Line Interface #
##########################

# Note: Functions in this section do not need to be changed.  They use features
#       of Python not yet covered in the course.


@main
def run(*args):
    """Read in the command-line argument and calls corresponding functions.

    This function uses Python syntax/techniques not yet covered in this course.
    """
    import argparse
    parser = argparse.ArgumentParser(description="Play Hog")
    parser.add_argument('--run_experiments', '-r', action='store_true',
                        help='Runs strategy experiments')
    args = parser.parse_args()

    if args.run_experiments:
        run_experiments()
