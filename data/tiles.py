"""
Data file containing the tile definitions for the edge matching puzzle.
Each tile is represented as [top, right, bottom, left] colors.
"""

# Original colors are 1-6, but we subtract 1 to use 0-5 as indices
TILES = [
    [1, 2, 3, 5],  # tile 0
    [5, 4, 6, 2],  # tile 1
    [1, 5, 3, 4],  # tile 2
    [2, 1, 6, 5],  # tile 3
    [3, 1, 6, 2],  # tile 4
    [6, 5, 4, 1],  # tile 5
    [3, 4, 2, 5],  # tile 6
    [6, 2, 3, 4],  # tile 7
    [6, 3, 4, 5],  # tile 8
    [4, 1, 2, 3],  # tile 9
    [2, 5, 4, 1],  # tile 10
    [3, 1, 6, 5],  # tile 11
    [4, 6, 1, 2],  # tile 12
    [2, 3, 5, 6],  # tile 13
    [4, 1, 6, 3],  # tile 14
    [6, 3, 2, 1]   # tile 15
]

# Store original tiles
ORIGINAL_TILES = TILES.copy()
# Convert colors to 0-based indexing
TILES = [[color - 1 for color in tile] for tile in ORIGINAL_TILES] 