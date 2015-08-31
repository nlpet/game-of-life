"""Conway's game of life simulation."""
import numpy as np
from copy import deepcopy
from math import floor
import os


class Game(object):

    """Create a board for the game of life (width x height cells)."""

    def __init__(self, **kwargs):
        """Initialize game."""
        self.width = kwargs['width']
        self.height = kwargs['height']
        self.on = 1
        self.off = 0
        self.opts = [self.on, self.off]
        self.symbols = {0: ' .', 1: ' o'}
        self.parallel_symbols = {0: '.', 1: 'o'}
        if kwargs.get('state', 0):
            self.state = self.validate_state(kwargs['state'])
        else:
            self.state = self.generate_state()
        self.temp_state = deepcopy(self.state)

    def validate_state(self, state):
        """Adopt the supplied state."""
        assert len(state) == self.height,\
            "Supplied state's height does not match the supplied height."
        assert len(state[0]) == self.width,\
            "Supplied state's width does not match the supplied width."
        return np.array(state)

    def generate_state(self):
        """Generate board state using seed."""
        w, h = self.width, self.height
        return np.random.choice(self.opts, w * h).reshape(w, h)

    def get_neighbors(self, row, col):
        """Get number of neighbors of self.state[row][col]."""
        neighbors = 0
        indices = {
            "top_left": (row - 1, col - 1),
            "top_center": (row - 1, col),
            "top_right": (row - 1, col + 1),
            "left": (row, col - 1),
            "right": (row, col + 1),
            "bottom_left": (row + 1, col - 1),
            "bottom_center": (row + 1, col),
            "bottom_right": (row + 1, col + 1)
        }
        for r, c in indices.values():
            if 0 <= r < self.width and 0 <= c < self.height:
                if self.state[r][c]:
                    neighbors += 1
        return neighbors

    def is_cell_alive(self, row, col):
        """Process a cell of the board and determine its fate."""
        is_cell_alive = self.state[row][col]
        neighbors = self.get_neighbors(row, col)
        if is_cell_alive:
            if neighbors < 2 or neighbors > 3:
                return self.off
            return self.on
        else:
            if neighbors == 3:
                return self.on
            return self.off

    def display_state(self):
        """Print the game's state."""
        state = ""
        for row in range(self.height):
            for col in range(self.width):
                state += self.symbols[self.state[col][row]]
            state += "\n"
        print(state)

    def process_step(self):
        """Process a single step and return the new board."""
        for row in range(self.width):
            for col in range(self.height):
                self.temp_state[row][col] = self.is_cell_alive(row, col)
        return self.temp_state

    def process_steps(self, num):
        """Process n steps in the game. Display steps one by one."""
        print("\nInitial board state\n""")
        self.display_state()

        for step in range(num):
            self.state = deepcopy(self.process_step())

            print("\nStep: {} of {}.\n".format(step + 1, num))
            self.display_state()

    def process_steps_and_save_states(self, num):
        """Process n steps and save state to display all steps in a grid."""
        states = []
        width = map(int, os.popen('stty size', 'r').read().split())[1]
        grids_per_block = int(floor(width / (self.width * 2 + 6)))

        for step in range(num):
            self.state = deepcopy(self.process_step())
            states.append(self.state)

        states = np.array(states)
        grids = states.shape[0]

        print("\nPrinting %s grids. Progress is horizontal ----> \n" % grids)
        for start in range(0, grids, grids_per_block):
            end = start + grids_per_block
            end = end if end < grids else grids
            for row in range(self.height):
                for m in range(start, end):
                    for col in range(self.width):
                        print(self.parallel_symbols[states[m][col][row]]),
                    print("\t"),
                print("")
            print("\n")


# --------------------------------------------------------------------------- #
# Tests
# --------------------------------------------------------------------------- #
def test_example_patterns(name):
    """Test different patterns."""
    name = name.lower()
    defined_patterns = [
        'block', 'beehive', 'loaf', 'boat',
        'blinker', 'toad', 'beacon', 'pulsar',
        'pentadecathlon'
    ]
    if name not in defined_patterns:
        print("Name of pattern not defined.")
        return

    state, width, height, steps = [], 0, 0, 0

    if name == 'block':
        state = [
            [0, 0, 0, 0],
            [0, 1, 1, 0],
            [0, 1, 1, 0],
            [0, 0, 0, 0]
        ]
        steps = 3
    elif name == 'beehive':
        state = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 1, 0, 0, 1, 0],
            [0, 0, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        steps = 3
    elif name == 'blinker':
        state = [
            [0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0],
        ]
        steps = 4
    elif name == 'toad':
        state = [
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 1, 1, 1, 0],
            [0, 1, 1, 1, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        steps = 4
    elif name == 'beacon':
        state = [
            [0, 0, 0, 0, 0, 0],
            [0, 1, 1, 0, 0, 0],
            [0, 1, 1, 0, 0, 0],
            [0, 0, 0, 1, 1, 0],
            [0, 0, 0, 1, 1, 0],
            [0, 0, 0, 0, 0, 0]
        ]
        steps = 4
    elif name == 'pulsar':
        state = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        steps = 9
    else:
        return

    width = len(state[0])
    height = len(state)

    g = Game(width=width, height=height, state=state)
    g.process_steps(steps)


if __name__ == '__main__':
    g = Game(width=15, height=30)
    #g.process_steps(5)
    g.process_steps_and_save_states(5)
