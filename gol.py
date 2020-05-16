#!/usr/bin/env python

#Credits to https://github.com/mwharrisjr/Game-of-Life
#GPLv3 License.

from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time
import os
import random
import sys

led_panel_height = 32
led_panel_width = 64

### RGBMatrixSetting
def rgbmatrix_options():
  options = RGBMatrixOptions()
  options.multiplexing = 0
  options.row_address_type = 0
  options.brightness = 100 
  options.rows = led_panel_height
  options.cols = led_panel_width
  options.chain_length = 1
  options.parallel = 1
  options.hardware_mapping = 'regular'
  options.inverse_colors = False
  options.led_rgb_sequence = "RGB"
  options.gpio_slowdown = 3 
  options.pwm_lsb_nanoseconds = 150
  options.show_refresh_rate = 0 
  options.disable_hardware_pulsing = True
  options.scan_mode = 0 
  options.pwm_bits = 11
  options.daemon = 0
  options.drop_privileges = 0
  return options;

opts = rgbmatrix_options()
display = RGBMatrix(options=opts)

def create_initial_grid(rows, cols):
    """
    Creates a random list of lists that contains 1s and 0s to represent the cells in Conway's Game of Life.

    :param rows: Int - The number of rows that the Game of Life grid will have
    :param cols: Int - The number of columns that the Game of Life grid will have
    :return: Int[][] - A list of lists containing 1s for live cells and 0s for dead cells
    """

    grid = []
    for row in range(rows):
        grid_rows = []
        for col in range(cols):
            # Generate a random number and based on that decide whether to add a live or dead cell to the grid
            if random.randint(0, 7) == 0:
                grid_rows += [1]
            else:
                grid_rows += [0]
        grid += [grid_rows]
    return grid


def refresh_grid(rows, cols, grid, generation):
    """
    Refresh the Game of Life grid

    :param rows: Int - The number of rows that the Game of Life grid has
    :param cols: Int - The number of columns that the Game of Life grid has
    :param grid: Int[][] - The list of lists that will be used to represent the Game of Life grid
    :param generation: Int - The current generation of the Game of Life grid
    """

    display.Clear()

    R = random.randint(1, 255)
    G = random.randint(1, 255)
    B = random.randint(1, 255)

    for row in range(rows):
        for col in range(cols):
            if grid[row][col] == 0:
                display.SetPixel(col, row, 0, 0, 0)
            else:
                display.SetPixel(col, row, R, G, B)

def create_next_grid(rows, cols, grid, next_grid):
    """
    Analyzes the current generation of the Game of Life grid and determines what cells live and die in the next
    generation of the Game of Life grid.

    :param rows: Int - The number of rows that the Game of Life grid has
    :param cols: Int - The number of columns that the Game of Life grid has
    :param grid: Int[][] - The list of lists that will be used to represent the current generation Game of Life grid
    :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Game of Life
    grid
    """

    for row in range(rows):
        for col in range(cols):
            # Get the number of live cells adjacent to the cell at grid[row][col]
            live_neighbors = get_live_neighbors(row, col, rows, cols, grid)

            # If the number of surrounding live cells is < 2 or > 3 then we make the cell at grid[row][col] a dead cell
            if live_neighbors < 2 or live_neighbors > 3:
                next_grid[row][col] = 0
            # If the number of surrounding live cells is 3 and the cell at grid[row][col] was previously dead then make
            # the cell into a live cell
            elif live_neighbors == 3 and grid[row][col] == 0:
                next_grid[row][col] = 1
            # If the number of surrounding live cells is 3 and the cell at grid[row][col] is alive keep it alive
            else:
                next_grid[row][col] = grid[row][col]


def get_live_neighbors(row, col, rows, cols, grid):
    """
    Counts the number of live cells surrounding a center cell at grid[row][cell].

    :param row: Int - The row of the center cell
    :param col: Int - The column of the center cell
    :param rows: Int - The number of rows that the Game of Life grid has
    :param cols: Int - The number of columns that the Game of Life grid has
    :param grid: Int[][] - The list of lists that will be used to represent the Game of Life grid
    :return: Int - The number of live cells surrounding the cell at grid[row][cell]
    """

    life_sum = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            # Make sure to count the center cell located at grid[row][col]
            if not (i == 0 and j == 0):
                # Using the modulo operator (%) the grid wraps around
                life_sum += grid[((row + i) % rows)][((col + j) % cols)]
    return life_sum


def grid_changing(rows, cols, grid, next_grid):
    """
    Checks to see if the current generation Game of Life grid is the same as the next generation Game of Life grid.

    :param rows: Int - The number of rows that the Game of Life grid has
    :param cols: Int - The number of columns that the Game of Life grid has
    :param grid: Int[][] - The list of lists that will be used to represent the current generation Game of Life grid
    :param next_grid: Int[][] - The list of lists that will be used to represent the next generation of the Game of Life
    grid
    :return: Boolean - Whether the current generation grid is the same as the next generation grid
    """

    for row in range(rows):
        for col in range(cols):
            # If the cell at grid[row][col] is not equal to next_grid[row][col]
            if not grid[row][col] == next_grid[row][col]:
                return True
    return False


def run_game():
    """
    Start of the game
    """

    display.Clear()

    # Get the number of rows and columns for the Game of Life grid
    rows = led_panel_height
    cols = led_panel_width

    # Get the number of generations that the Game of Life should run for (between 1 and 100000
    generations = 100000

    # Create the initial random Game of Life grids
    current_generation = create_initial_grid(rows, cols)
    next_generation = create_initial_grid(rows, cols)

    # Run Game of Life sequence
    gen = 1
    for gen in range(1, generations + 1):
        if not grid_changing(rows, cols, current_generation, next_generation):
            break
        refresh_grid(rows, cols, current_generation, gen)
        create_next_grid(rows, cols, current_generation, next_generation)
        #time.sleep(1 / 5.0)
        current_generation, next_generation = next_generation, current_generation

    refresh_grid(rows, cols, current_generation, gen)
    print("End of the game.")

# Start the Game of Life
print("Simple Game of Live")
print("Press <Ctrl-C> to exit.")
run_game()
