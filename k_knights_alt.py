from collections import deque
import random
from matplotlib import patches
import matplotlib.pyplot as plt


class CSP_knights:
    def __init__(self, k:int, n:int):
        if k > n*n:
            raise ValueError('Number of knights cannot be greater than the number of squares on the board')
        self.k = k
        self.n = n
        # Variables: Each cell (i, j) can be either 0 or 1 (no knight or knight)
        self.X = [(i,j) for i in range(n) for j in range(n)]
        random.shuffle(self.X)
        # Domains: [1, 0] for each cell
        self.D = {var: [1,0] for var in self.X}
        # Constraints: knights must not threaten each other
        self.C = self.create_constraints()

    def create_constraints(self):
        constraints = []
        for square in self.D:
            for other_square in self.D:
                if square != other_square and self.is_threat(square, other_square):
                    constraints.append((square, other_square))
        return constraints
    
    def is_threat(self, square, other_square):
        x1, y1 = square
        x2, y2 = other_square
        return ((abs(x2 - x1) == 2 and abs(y2 - y1) == 1) or
                (abs(x2 - x1) == 1 and abs(y2 - y1) == 2))
    

class Solver:
    def __init__(self) -> None:
        self.count = 0
    def solve(self, csp: CSP_knights):
        return self.backtrack(csp, {})
    
    def revise(self, csp: CSP_knights, var1, var2):
        revised = False
        for val in csp.D[var1]:
            if val and csp.D[var2] == [1]:
                revised = True
                csp.D[var1].remove(val)
        return revised
        
    
    def ac3(self, csp: CSP_knights, var, assignment):
        # Maintaining Arc Consistency (MAC)
        # Only arcs (var1, var2) are added to the queue where
        # var1 is an unassigned variable and
        # var2 is the just assigned variable
        arcs = [arc for arc in csp.C if arc[1] == var and arc[0] not in assignment]
        queue = deque(arcs)
        while queue:
            var1, var2 = queue.popleft()
            self.revise(csp, var1, var2)
            """ if self.revise(csp, var1, var2):
                for var3 in csp.X:
                    if var3 != var1:
                        if (var3, var1) in csp.C:
                            queue.append((var3, var1)) """
        return True


    def backtrack(self, csp: CSP_knights, assignment):
        # this counter keeps track of how many backtrack() functions are called
        self.count += 1
        print("trying...", self.count)
        # this block is useful when all knights have already been assigned
        # there's no more need to backtrack, all other cells are empty 
        if sum(assignment.values()) == csp.k:
            unassigned_vars = [var for var in csp.X if var not in assignment]
            for var in unassigned_vars:
                assignment[var] = 0
            return assignment
        # if all variables have been assigned and there's exactly k knights, return the solution
        if len(assignment) == csp.n**2:
            if sum(assignment.values()) == csp.k:
                return assignment
            else:
                return None
        # select the next variable to assign
        var = self.select_unassigned_variable(csp, assignment) # little bit of inference here as well
        if var is None:
            return None
        for value in csp.D[var]:
            if sum(assignment.values()) + value > csp.k:
                continue  # Skip if adding this value exceeds the limit of k knights
            if self.is_consistent(csp, var, value, assignment):
                assignment[var] = value
                # deep copy
                original_domain = {var: csp.D[var][:] for var in csp.D}
                csp.D[var] = [value]
                if self.ac3(csp, var, assignment):
                    result = self.backtrack(csp, assignment)
                    if result:
                        return result
                del assignment[var]
                csp.D = original_domain
        return None

    
    def select_unassigned_variable(self, csp: CSP_knights, assignment):
        unassigned_vars = [var for var in csp.X if var not in assignment]
        # check if it's possible to place k knights
        if sum(assignment.values()) + len(unassigned_vars) < csp.k:
            return None
        # Apply MRV heuristic
        return min(unassigned_vars, key=lambda var: len(csp.D[var]))

    def is_consistent(self, csp: CSP_knights, var, value, assignment):
        if value:
            for other_var in assignment:
                if csp.is_threat(var, other_var) and assignment[other_var]:
                    return False
        return True

class Drawer:
    def draw_chessboard(solution, n):
        # Create a figure and axis
        fig, ax = plt.subplots()

        # Calculate the font size based on the board size
        fontsize = 200 / n  # Adjust this scaling factor as needed

        # Create the chessboard
        for i in range(n):
            for j in range(n):
                color = 'white' if (i + j) % 2 == 0 else 'gray'
                rect = patches.Rectangle((i, j), 1, 1, linewidth=1, edgecolor='black', facecolor=color)
                ax.add_patch(rect)

        # Add knights
        for (x, y), value in solution.items():
            if value == 1:
                # Draw a knight
                ax.text(x + 0.5, y + 0.5, '♞', fontsize=fontsize, ha='center', va='center')


        # Set limits and show
        plt.xlim(0, n)
        plt.ylim(0, n)
        plt.gca().set_aspect('equal', adjustable='box')
        plt.gca().invert_yaxis()  # Invert y axis to match the traditional chessboard view
        plt.xticks([])
        plt.yticks([])
        plt.show()


#test
csp = CSP_knights(61, 11)
solver = Solver()
solution = solver.solve(csp)
if solution:
    drawer = Drawer
    drawer.draw_chessboard(solution, csp.n)
else:
    print ("No solution")