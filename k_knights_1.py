from collections import deque
from matplotlib import patches, pyplot as plt

class CSP_Knights:
    def __init__(self, k, n):
        # Number of knights
        self.k = k
        # Size of the chessboard
        self.n = n
        # Variables: Knights
        self.X = [i for i in range(k)]
        # Domains: all possible squares on the board
        self.D = {i: [(x,y) for x in range(n) for y in range(n)] for i in range(k)}
        # Constraints: all knights are potentially in conflict with each other
        self.C = [(i,j) for i in range(k) for j in range (k) if i!=j]
    
    def is_threat(self, pos1, pos2):
        if pos1 == pos2:
            return True
        x1, y1 = pos1
        x2, y2 = pos2
        # return True if the given positions are in conflict with each other
        return (abs(x2 - x1) == 1 and abs(y2 - y1)== 2) or (abs(x2 - x1) == 2 and abs(y2 - y1) == 1)
    

class Solver:
    def __init__(self) -> None:
        self.count = 0
    
    def solve(self, csp: CSP_Knights):
        return self.backtrack(csp, {})
    
    def ac3(self, csp: CSP_Knights, var, assignment):
        # Maintaining Arc Consitency:
        # We want to check arc consistency only on the arcs terminating in var, e.g. (other_var, var)  
        # where other_var hasn't been assigned yet
        queue = deque(arc for arc in csp.C if arc[1] == var and arc[0] not in assignment)
        while queue:
            var1, var2 = queue.popleft()
            if self.revise(csp, var1, var2):
                # if a domain is reduced to zero, there's no solution
                if csp.D[var] == 0:
                    return False
                # propagate the inference to revised variables
                queue.extend(arc for arc in csp.C if arc[1] == var1 and arc[0] not in assignment)
        return True
    
    def revise(self, csp: CSP_Knights, var1, var2):
        revised = False
        for pos in csp.D[var1]:
            # if there's no value in the domain of var2 such that current value for var1 is consistent
            if all(csp.is_threat(pos, other_pos) for other_pos in csp.D[var2]):
                # then remove current value from the domain of var1
                csp.D[var1].remove(pos)
                revised = True
        return revised
    
    def select_unassigned_var(self, csp: CSP_Knights, assignment):
        # Minimum Remaining Values (MRV) heuristic
        # Choose the variable with the fewest remaining values in its domain
        unassigned_vars = [var for var in csp.X if var not in assignment]
        MRV_var = min(unassigned_vars, key=lambda var: len(csp.D[var]))
        return MRV_var
    
    def order_domain_values(self, csp: CSP_Knights, var, assignment):
        # calculate the impact of each value in the domain
        def count_conflicts(pos):
            count = 0
            for other_var in csp.X:
                if other_var not in assignment and other_var != var:
                    count += sum(csp.is_threat(pos, other_pos) for other_pos in csp.D[other_var])
            return count
        # sort the domain according to the Least Constraining Value heuristic
        return sorted(csp.D[var], key=count_conflicts)
    
    def backtrack(self, csp:CSP_Knights, assignment):
        self.count += 1
        print("Try #", self.count)
        # if all knights have been assigned, return the solution
        if len(assignment) == csp.k:
            return assignment
        # select the next unassigned variable
        var = self.select_unassigned_var(csp, assignment)
        # try all possible values for the selected variable
        for pos in self.order_domain_values(csp, var, assignment):
            # if the value is consistent with the current assignment
            if not self.is_consistent(pos, csp, assignment):
                continue
            # assign the value to the variable
            assignment[var] = pos
            # deep copy
            original_domains = {var: csp.D[var].copy() for var in csp.X}
            # reduce the domain of the variable to the single value
            csp.D[var] = [pos]
            # apply AC3 to reduce the domains of other variables
            if self.ac3(csp, var, assignment):
                result = self.backtrack(csp, assignment)
                # if a solution is found, return it
                if result:
                    return result
            # undo the assignment
            del assignment[var]
            # restore the original domains
            csp.D = original_domains
        # if no solution is found, return None
        return None
    
    def is_consistent(self, pos, csp: CSP_Knights, assignment):
        # a position is consistent if it's not in conflict with any other assigned knight
        return all(not csp.is_threat(pos, assignment[other_var]) for other_var in assignment)
    

class Drawer:
    @staticmethod
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
        for knight, (x, y) in solution.items():
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
