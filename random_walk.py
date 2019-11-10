import random
from turtle import *

def random_walk_grid():
    '''Executes a random walk about an infinite grid.
    Illustrates the path taken using a turtle.
    The turtle can move to any of the eight points
    in the Moore neighborhood around its current position
    except for the point it just moved from.
    '''
    color('red')
    # Cannot rotate 180 degrees
    step = 20
    squareRootOfTwo = 1.4142135624
    rotationOptions = [-135, -90, -45, 0, 45, 90, 135]
    while True:
        answer = input('Number of steps: ')
        if answer.isdigit():
            numberOfSteps = int(answer)
            for _ in range(numberOfSteps):
                randomIndex = random.randint(0, len(rotationOptions) - 1)
                rotation = rotationOptions[randomIndex]
                left(rotation)

                # Forward distance is greater by a factor of
                # square root of two when traveling diagonally
                forwardDistance = step
                if heading() in [45, 135, 225, 315]:
                    forwardDistance *= squareRootOfTwo
                forward(forwardDistance)
        else:
            exit()

def random_walk_angle():
    '''Executes a random walk around an infinite space.
    Illustrates the path taken using a turtle.
    At each step the turtle will turn at a random angle
    and move forward a random number of units between 1 and 20.
    '''
    color('red')
    while True:
        answer = input('Number of steps: ')
        if answer.isdigit():
            numberOfSteps = int(answer)
            for _ in range(numberOfSteps):
                # random.randint(-180, 180) would make turning 180 degrees
                # twice as likely as any other option.
                randomAngle = random.randint(-179, 180)
                randomDistance = random.randint(1, 20)
                left(randomAngle)
                forward(randomDistance)
        else:
            exit()
