#!/usr/bin/env python3
from functools import reduce
from os import name, system, urandom
from random import sample
from time import sleep

# This is a slight spin on the usual Game of Life. It defaults to Conway's rule
# B3/S23, but can be switched to a well-known rule such as Day-Night, a custom
# user-defined rule, or even a random rule!

# USAGE: 'python3 life.py [conway | day_night | random]'

# NOTE: Try the other worlds in the WORLDS section
# NOTE: Try the other rules, details in 'main'

# HOWTO: Modify the 'WORLD' array to change the initial state

# TODO: Allow the 'WORLD' to expand/shrink at runtime


###################
#### CONSTANTS ####
###################

ALIVE = "X"
DEAD = " "

WIDTH = 11
HEIGHT = 12
HBORDER = "-" * (WIDTH + 2)
VBORDER = "|"


################
#### WORLDS ####
################

# Tetromino example
# WORLD = [[DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
#         [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
#         [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
#         [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
#         [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
#         [DEAD, DEAD, DEAD, DEAD, DEAD, ALIVE, DEAD, DEAD, DEAD, DEAD, DEAD],
#         [DEAD, DEAD, DEAD, DEAD, ALIVE, ALIVE, ALIVE, DEAD, DEAD, DEAD, DEAD],
#         [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
#         [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
#         [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
#         [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
#         [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD]]

# Glider example
WORLD = [
    [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
    [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
    [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
    [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
    [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
    [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
    [DEAD, DEAD, DEAD, DEAD, ALIVE, ALIVE, ALIVE, DEAD, DEAD, DEAD, DEAD],
    [DEAD, DEAD, DEAD, DEAD, ALIVE, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
    [DEAD, DEAD, DEAD, DEAD, DEAD, ALIVE, DEAD, DEAD, DEAD, DEAD, DEAD],
    [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
    [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
    [DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD, DEAD],
]


##############
#### GAME ####
##############

# Returns the number of living cell in the Moore
# neighborhood of 'past[row][col]'
def call(past, row, col):
    minRow = row - 1 if row - 1 >= 0 else HEIGHT - 1
    maxRow = row + 1 if row + 1 < HEIGHT else 0
    minCol = col - 1 if col - 1 >= 0 else WIDTH - 1
    maxCol = col + 1 if col + 1 < WIDTH else 0
    nabes = [
        (minRow, minCol),
        (minRow, col),
        (minRow, maxCol),
        (row, minCol),
        (row, maxCol),
        (maxRow, minCol),
        (maxRow, col),
        (maxRow, maxCol),
    ]
    return reduce(
        lambda x, y: x + y, map(lambda t: 1 if past[t[0]][t[1]] == ALIVE else 0, nabes)
    )


# Calculate entropy(?) based on rule
def next(rule):
    past = list([list(row) for row in WORLD])
    for row in range(HEIGHT):
        for col in range(WIDTH):
            WORLD[row][col] = rule(past[row][col], call(past, row, col))


# Prints a formatted state of the 'WORLD'
def show():
    print(HBORDER)
    for row in WORLD:
        print(VBORDER + "".join(row) + VBORDER)
    print(HBORDER)


###############
#### RULES ####
###############

# Generates a rule given born/survive lists;
# defaults to generating Conway's Game of Life, B3/S23
def mkRule(bs=(3,), ss=(2, 3)):
    def rule(state, count):
        if state == DEAD and count in bs:
            return ALIVE
        elif state == ALIVE and count in ss:
            return ALIVE
        else:
            return DEAD

    return rule


# Random Rule Generator, B[0-8]*/S[0-8]*
# NOTE: mkRand returns a rule, it is NOT a rule itself
def mkRand():
    bs = sample(list(range(9)), ord(urandom(1)) % 9)
    ss = sample(list(range(9)), ord(urandom(1)) % 9)
    return (bs, ss)


RULES = {
    "conway": ((3,), (2, 3)),
    "day_night": ((3, 6, 7, 8), (3, 4, 6, 7, 8)),
    "random": mkRand(),
}


##############
#### Main ####
##############


def main():
    clear = lambda: system("cls" if name == "nt" else "clear")

    import sys

    if len(sys.argv) > 1:
        try:
            rule = mkRule(*RULES[sys.argv[1]])
        except:
            sys.exit(-1)
    else:
        rule = mkRule()

    delay = 1
    iteration = 0
    while True:
        clear()
        show()
        next(rule)
        print("Iteration: " + str(iteration))
        iteration += 1
        sleep(delay)


if __name__ == "__main__":
    main()
