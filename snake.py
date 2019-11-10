#!/usr/bin/python
# -*- coding: utf-8 -*-

import curses
import random
import locale

NUM_ROWS = 18
NUM_COLUMNS = 42

DIRECTION_UP = 'up'
DIRECTION_LEFT = 'left'
DIRECTION_RIGHT = 'right'
DIRECTION_DOWN = 'down'

HEAD_CHAR = '@'
BODY_CHAR = 'o'
FOOD_CHAR = '*'
WALL_CHAR_HORIZONTAL = '-'
WALL_CHAR_VERTICAL = '|'
WALL_CHAR_CORNER = '+'

def main():
    curses.wrapper(start_snake)

def start_snake(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(1)

    stdscr.addstr(0, 0, WALL_CHAR_CORNER)
    stdscr.addstr(0, NUM_COLUMNS - 1, WALL_CHAR_CORNER)
    stdscr.addstr(NUM_ROWS - 1, NUM_COLUMNS - 1, WALL_CHAR_CORNER)
    stdscr.addstr(NUM_ROWS - 1, 0, WALL_CHAR_CORNER)
    for row in range(1, NUM_ROWS - 1):
        stdscr.addstr(row, 0, WALL_CHAR_VERTICAL)
        stdscr.addstr(row, NUM_COLUMNS - 1, WALL_CHAR_VERTICAL)
    for column in range(1, NUM_COLUMNS - 1):
        stdscr.addstr(0, column, WALL_CHAR_HORIZONTAL)
        stdscr.addstr(NUM_ROWS - 1, column, WALL_CHAR_HORIZONTAL)

    stdscr.addstr(NUM_ROWS, 0, 'SCORE: 0')
    stdscr.addstr(NUM_ROWS + 1, 0, 'PRESS Q TO QUIT')
    stdscr.addstr(NUM_ROWS + 2, 0, 'PRESS P TO PAUSE')

    available_positions = set()
    for row in range(1, NUM_ROWS - 1):
        for column in range(1, NUM_COLUMNS - 1):
            available_positions.add((column, row))

    start_row = int(NUM_ROWS / 2)
    start_column = 6
    snake_positions = [(start_column, start_row)]
    stdscr.addstr(start_row, start_column, HEAD_CHAR)
    available_positions.remove((start_column, start_row))
    for i in range(1, 6):
        snake_positions.append((start_column - i, start_row))
        stdscr.addstr(start_row, start_column - i, BODY_CHAR)
        available_positions.remove((start_column - i, start_row))

    food_position = random.sample(available_positions, 1)[0]
    stdscr.addstr(food_position[1], food_position[0], FOOD_CHAR)

    direction = DIRECTION_RIGHT
    score = 0
    dead = False
    paused = False
    add_segment = False
    second_chance = True

    while(True):
        key = stdscr.getch()
        if key == ord('q'):
            break
        elif key == ord('p'):
            paused = not paused
            paused_string = 'PAUSED' if paused else '      '
            stdscr.addstr(NUM_ROWS, int(NUM_COLUMNS / 2), paused_string)
        elif dead and key == ord('r'):
            for position in snake_positions:
                stdscr.addstr(position[1], position[0], ' ')
                available_positions.add(position)
            snake_positions = [(start_column, start_row)]
            stdscr.addstr(start_row, start_column, HEAD_CHAR)
            for i in range(1, 6):
                snake_positions.append((start_column - i, start_row))
                stdscr.addstr(start_row, start_column - i, BODY_CHAR)
            direction = DIRECTION_RIGHT
            score = 0
            stdscr.addstr(NUM_ROWS, 0, 'SCORE: 0' + (' ' * (NUM_COLUMNS - 8)))
            stdscr.addstr(NUM_ROWS + 2, 0, 'PRESS P TO PAUSE  ')
            dead = False
            add_segment = False
            second_chance = True
        elif key == curses.KEY_LEFT and direction != DIRECTION_LEFT and direction != DIRECTION_RIGHT:
            direction = DIRECTION_LEFT
        elif key == curses.KEY_RIGHT and direction != DIRECTION_RIGHT and direction != DIRECTION_LEFT:
            direction = DIRECTION_RIGHT
        elif key == curses.KEY_UP and direction != DIRECTION_UP and direction != DIRECTION_DOWN:
            direction = DIRECTION_UP
        elif key == curses.KEY_DOWN and direction != DIRECTION_DOWN and direction != DIRECTION_UP:
            direction = DIRECTION_DOWN

        if not dead and not paused:
            old_head_position = snake_positions[0]
            if direction == DIRECTION_UP:
                new_head_position = (old_head_position[0], old_head_position[1] - 1)
            elif direction == DIRECTION_LEFT:
                new_head_position = (old_head_position[0] - 1, old_head_position[1])
            elif direction == DIRECTION_RIGHT:
                new_head_position = (old_head_position[0] + 1, old_head_position[1])
            elif direction == DIRECTION_DOWN:
                new_head_position = (old_head_position[0], old_head_position[1] + 1)
            if new_head_position[0] == 0 or new_head_position[0] == NUM_COLUMNS - 1 or new_head_position[1] == 0 or new_head_position[1] == NUM_ROWS - 1 or new_head_position in snake_positions:
                if second_chance:
                    second_chance = False
                else:
                    dead = True
                    stdscr.addstr(NUM_ROWS, int(NUM_COLUMNS / 2), 'DEAD')
                    stdscr.addstr(NUM_ROWS + 2, 0, 'PRESS R TO RESTART')
            else:
                second_chance = True
                snake_positions.insert(0, new_head_position)
                stdscr.addstr(new_head_position[1], new_head_position[0], HEAD_CHAR)
                available_positions.remove(new_head_position)
                stdscr.addstr(old_head_position[1], old_head_position[0], BODY_CHAR)
                if not add_segment:
                    old_tail_position = snake_positions.pop()
                    stdscr.addstr(old_tail_position[1], old_tail_position[0], ' ')
                    available_positions.add(old_tail_position)
                add_segment = False
                if new_head_position == food_position:
                    add_segment = True
                    score += 1
                    stdscr.addstr(NUM_ROWS, 7, str(score))
                    food_position = random.sample(available_positions, 1)[0]
                    stdscr.addstr(food_position[1], food_position[0], FOOD_CHAR)

        curses.napms(250)

if __name__ == "__main__":
    main()
