u"""
Rules.

The universe of the Game of Life is an infinite two-dimensional orthogonal
grid of square cells, each of which is in one of two possible states, alive
or dead. Every cell interacts with its eight neighbours, which are the cells
that are horizontally, vertically, or diagonally adjacent. At each step in
time, the following transitions occur:

Any live cell with fewer than two live neighbours dies,
as if caused byunder-population.
Any live cell with two or three live neighbours lives
on to the next generation.
Any live cell with more than three live neighbours dies, as if by overcrowding.
Any dead cell with exactly three live neighbours becomes a live cell,
as if by reproduction.

The initial pattern constitutes the seed of the system. The first generation
is created by applying the above rules simultaneously to every cell in the
seed-births and deaths occur simultaneously, and the discrete moment at which
this happens is sometimes called a tick (in other words, each generation is
a pure function of the preceding one). The rules continue to be applied
repeatedly to create further generations.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from copy import deepcopy


def get_neighbors(row, col):
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
        if 0 <= r < h and 0 <= c < w and grid[r][c]:
            neighbors += 1
    return neighbors


def is_cell_alive(row, col):
    """Process a cell of the board and determine its fate."""
    is_cell_alive = grid[row][col]
    neighbors = get_neighbors(row, col)
    if is_cell_alive:
        if neighbors < 2 or neighbors > 3:
            return off
        return on
    else:
        if neighbors == 3:
            return on
        return off


def update(data):
    """Update animation."""
    global grid
    temp_state = deepcopy(grid)
    for row in range(h):
        for col in range(w):
            temp_state[row][col] = is_cell_alive(row, col)

    mat.set_data(temp_state)
    grid = temp_state
    return [mat]


if __name__ == '__main__':
    on = 1
    off = 0
    opts = [on, off]
    w = 150
    h = 150

    grid = np.random.choice(opts, w*h).reshape(w, h)

    fig, ax = plt.subplots()
    mat = ax.matshow(grid, cmap="GnBu")
    ani = animation.FuncAnimation(fig, update, interval=10)
    plt.show()
