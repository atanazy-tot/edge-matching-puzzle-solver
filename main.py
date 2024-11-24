from data.tiles import TILES
from puzzle_solver import EdgeMatchingPuzzleSolver

def main():
    # Create solver instance
    solver = EdgeMatchingPuzzleSolver(TILES)
    
    # Solve the puzzle
    solution = solver.solve()
    
    if solution:
        print("Solution found!")
        # Print the solution in a grid format
        grid = [[None] * solver.grid_size for _ in range(solver.grid_size)]
        for (t, r, c, a), value in solution.items():
            if value > 0.5:  # Account for floating-point precision
                grid[r][c] = f"T{t}R{a*90}"
        
        # Print the grid
        for row in grid:
            print(" | ".join(f"{cell:>6}" for cell in row))
    else:
        print("No solution found!")

if __name__ == "__main__":
    main() 