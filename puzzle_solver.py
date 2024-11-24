from ortools.linear_solver import pywraplp
import numpy as np
from typing import List, Tuple, Dict

class EdgeMatchingPuzzleSolver:
    def __init__(self, tiles: List[List[int]], color_count: int = 6, rotation_count: int = 4):
        """
        Initialize the Edge Matching Puzzle Solver.
        
        Args:
            tiles: List of tiles, where each tile is [top, right, bottom, left] colors
            color_count: Number of different colors (default: 6)
            rotation_count: Number of possible rotations (default: 4)
        """
        self.tiles = tiles
        self.tile_count = len(tiles)
        self.grid_size = int(np.sqrt(self.tile_count))
        self.color_count = color_count
        self.rotation_count = rotation_count
        
        # Generate color matrices
        self.CT, self.CR, self.CB, self.CL = self._generate_color_matrix()
        
        # Create solver
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        
    def _generate_color_matrix(self) -> Tuple[List, List, List, List]:
        """
        Generate color matrices for the puzzle that will be used as input for optimization.
        Returns CT (top), CR (right), CB (bottom), CL (left) matrices.
        """
        # Initialize matrices
        C_matrices = [[[[0]*self.color_count for _ in range(self.rotation_count)] 
                      for _ in range(self.tile_count)] for _ in range(4)]
        CT, CR, CB, CL = C_matrices
        
        # Fill matrices
        for i, tile in enumerate(self.tiles):
            for j, color in enumerate(tile):
                # For each rotation, update the color positions
                CT[i][0][tile[0]] = CR[i][1][tile[3]] = CB[i][2][tile[2]] = CL[i][3][tile[1]] = 1
                CR[i][0][tile[1]] = CT[i][1][tile[0]] = CL[i][2][tile[3]] = CB[i][3][tile[2]] = 1
                CB[i][0][tile[2]] = CL[i][1][tile[1]] = CT[i][2][tile[0]] = CR[i][3][tile[3]] = 1
                CL[i][0][tile[3]] = CB[i][1][tile[2]] = CR[i][2][tile[1]] = CT[i][3][tile[0]] = 1
                
        return CT, CR, CB, CL
    
    def solve(self) -> Dict:
        """
        Solve the edge matching puzzle using integer linear programming.
        Returns the solution as a dictionary mapping (tile, row, col, rotation) to 1.0
        """
        # Create variables
        x = {}  # Main decision variables (tile placement and rotation)
        h = {}  # Horizontal mismatch variables
        v = {}  # Vertical mismatch variables
        
        # Initialize decision variables
        for t in range(self.tile_count):
            for r in range(self.grid_size):
                for c in range(self.grid_size):
                    for a in range(self.rotation_count):
                        x[t,r,c,a] = self.solver.IntVar(0, 1, f'x_{t}_{r}_{c}_{a}')
        
        # Initialize mismatch variables
        for r in range(self.grid_size):
            for c in range(self.grid_size - 1):
                h[r,c] = self.solver.IntVar(0, 1, f'h_{r}_{c}')
        
        for r in range(self.grid_size - 1):
            for c in range(self.grid_size):
                v[r,c] = self.solver.IntVar(0, 1, f'v_{r}_{c}')
        
        # Add constraints
        self._add_placement_constraints(x)
        self._add_color_matching_constraints(x, h, v)
        
        # Set objective
        objective = self.solver.Objective()
        for r in range(self.grid_size):
            for c in range(self.grid_size - 1):
                objective.SetCoefficient(h[r,c], 1)
        for r in range(self.grid_size - 1):
            for c in range(self.grid_size):
                objective.SetCoefficient(v[r,c], 1)
        objective.SetMinimization()
        
        # Solve
        status = self.solver.Solve()
        
        if status == pywraplp.Solver.OPTIMAL:
            return {(t,r,c,a): x[t,r,c,a].solution_value() 
                    for (t,r,c,a) in x if x[t,r,c,a].solution_value() > 0.5}
        return None

    def _add_placement_constraints(self, x):
        """Add constraints ensuring each tile is placed exactly once and each position has exactly one tile."""
        # Each tile must be placed exactly once
        for t in range(self.tile_count):
            constraint = self.solver.Constraint(1, 1)
            for r in range(self.grid_size):
                for c in range(self.grid_size):
                    for a in range(self.rotation_count):
                        constraint.SetCoefficient(x[t,r,c,a], 1)
        
        # Each position must have exactly one tile
        for r in range(self.grid_size):
            for c in range(self.grid_size):
                constraint = self.solver.Constraint(1, 1)
                for t in range(self.tile_count):
                    for a in range(self.rotation_count):
                        constraint.SetCoefficient(x[t,r,c,a], 1)

    def _add_color_matching_constraints(self, x, h, v):
        """Add constraints for matching colors between adjacent tiles."""
        # Horizontal color matching
        for r in range(self.grid_size):
            for c in range(self.grid_size - 1):
                for l in range(self.color_count):
                    # Right color of left tile minus left color of right tile
                    constraint1 = self.solver.Constraint(-self.solver.infinity(), 0)
                    constraint2 = self.solver.Constraint(-self.solver.infinity(), 0)
                    
                    for t in range(self.tile_count):
                        for a in range(self.rotation_count):
                            constraint1.SetCoefficient(x[t,r,c,a], self.CR[t][a][l])
                            constraint1.SetCoefficient(x[t,r,c+1,a], -self.CL[t][a][l])
                            
                            constraint2.SetCoefficient(x[t,r,c,a], -self.CR[t][a][l])
                            constraint2.SetCoefficient(x[t,r,c+1,a], self.CL[t][a][l])
                    
                    constraint1.SetCoefficient(h[r,c], 1)
                    constraint2.SetCoefficient(h[r,c], 1) 