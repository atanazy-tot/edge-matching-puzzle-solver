# Edge Matching Puzzle Solver

This project implements a solution to the Edge Matching Puzzle (also known as "Monkey Puzzle") using Integer Linear Programming (ILP) with Google's OR-Tools.

## Problem Description

The Edge Matching Puzzle is a logical puzzle where players must arrange a set of tiles on a grid such that the colors on adjacent edges match. Each tile has a color on each of its four sides, and can be rotated by 0°, 90°, 180°, or 270°.

### Example Tile

![Example Tile](./images/example_tile.png)

# Mathematical Formulation

### Decision Variables

We define three binary decision variables:

1. $x_{t,r,c,a}$ - Binary variable that equals 1 if tile $t$ is placed at position $(r,c)$ and rotated by $a$ degrees. Otherwise, it equals 0.
2. $h_{r,c}$ - Binary variable that equals 1 if the right edge at position $(r,c)$ is mismatched. Otherwise, it equals 0.
3. $v_{r,c}$ - Binary variable that equals 1 if the bottom edge at position $(r,c)$ is mismatched. Otherwise, it equals 0.

### Color Matrices

We use four matrices to represent the colors of each tile's edges for all possible rotations:
- $CT_{t,a,l}$ - Equals 1 if tile $t$ rotated by $a$ degrees has color $l$ on its top edge
- $CR_{t,a,l}$ - Equals 1 if tile $t$ rotated by $a$ degrees has color $l$ on its right edge
- $CB_{t,a,l}$ - Equals 1 if tile $t$ rotated by $a$ degrees has color $l$ on its bottom edge
- $CL_{t,a,l}$ - Equals 1 if tile $t$ rotated by $a$ degrees has color $l$ on its left edge

### Constraints

1. **Tile Placement Constraint**: Each tile must be placed exactly once on the grid:

   $\sum_{r=0}^{n-1} \sum_{c=0}^{n-1} \sum_{a=0}^{3} x_{t,r,c,a} = 1 \quad \forall t \in \{0, 1, ..., T-1\}$

2. **Grid Occupation Constraint**: Each grid position must contain exactly one tile:

   $\sum_{t=0}^{T-1} \sum_{a=0}^{3} x_{t,r,c,a} = 1 \quad \forall r \in \{0, 1, ..., n-1\}, c \in \{0, 1, ..., n-1\}$

3. **Color Matching Constraints**: For horizontally adjacent tiles:

   $\sum_{t=0}^{T-1} \sum_{a=0}^{3} CR_{t,a,l} x_{t,r,c,a} - \sum_{t=0}^{T-1} \sum_{a=0}^{3} CL_{t,a,l} x_{t,r,c+1,a} \leq h_{r,c}$

   $-\sum_{t=0}^{T-1} \sum_{a=0}^{3} CR_{t,a,l} x_{t,r,c,a} + \sum_{t=0}^{T-1} \sum_{a=0}^{3} CL_{t,a,l} x_{t,r,c+1,a} \leq h_{r,c}$

   For vertically adjacent tiles:

   $\sum_{t=0}^{T-1} \sum_{a=0}^{3} CB_{t,a,l} x_{t,r,c,a} - \sum_{t=0}^{T-1} \sum_{a=0}^{3} CT_{t,a,l} x_{t,r+1,c,a} \leq v_{r,c}$

   $-\sum_{t=0}^{T-1} \sum_{a=0}^{3} CB_{t,a,l} x_{t,r,c,a} + \sum_{t=0}^{T-1} \sum_{a=0}^{3} CT_{t,a,l} x_{t,r+1,c,a} \leq v_{r,c}$

   These constraints apply for all valid positions $(r,c)$ and all colors $l$.

### Objective Function

The goal is to minimize the number of mismatched edges:

$\min \sum_{r=0}^{n-1}\sum_{c=0}^{n-2} h_{r,c} + \sum_{r=0}^{n-2}\sum_{c=0}^{n-1} v_{r,c}$

## Implementation Details

### Dependencies
- Python 3.x
- OR-Tools (`ortools`)
- NumPy (`numpy`)
- Typing support (`typing`)

### Key Components

1. **EdgeMatchingPuzzleSolver Class**: Main solver class that:
   - Handles puzzle initialization
   - Generates color matrices
   - Sets up the ILP model
   - Solves the optimization problem

2. **Color Matrix Generation**: 
   - Converts tile definitions into four matrices (CT, CR, CB, CL)
   - Handles all possible rotations automatically
   - Enables efficient constraint generation

## Usage

### 1. Define Your Tiles

Create a `tiles.py` file in your data directory:

```python:edge_matching_puzzle/data/tiles.py
TILES = [
    [1, 2, 3, 4],  # Tile 0: [top, right, bottom, left]
    [2, 3, 4, 1],  # Tile 1
    # ... more tiles ...
]
```

### 2. Solve the Puzzle

```python
from puzzle_solver import EdgeMatchingPuzzleSolver
from data.tiles import TILES

# Create solver instance
solver = EdgeMatchingPuzzleSolver(
    tiles=TILES,
    color_count=6,  # Number of different colors
    rotation_count=4  # Number of possible rotations
)

# Solve the puzzle
solution = solver.solve()

# Process the solution
if solution:
    grid_size = int(len(TILES) ** 0.5)
    grid = [[None] * grid_size for _ in range(grid_size)]
    
    for (t, r, c, a), value in solution.items():
        if value > 0.5:  # Account for floating-point precision
            grid[r][c] = f"T{t}R{a*90}"  # Tile number and rotation
            
    # Print the solution
    for row in grid:
        print(" | ".join(f"{cell:>6}" for cell in row))
```

## Output Format

The solution is returned as a dictionary with:
- Keys: Tuples of `(tile_index, row, column, rotation)`
- Values: Binary values (1.0 for placed tiles)

Example output:
```
T0R0  | T1R90 | T2R180
T3R90 | T4R0  | T5R270
T6R0  | T7R90 | T8R180
```
Where:
- `T#` represents the tile number
- `R#` represents the rotation in degrees

## License

[Your chosen license]