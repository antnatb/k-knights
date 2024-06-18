## README

### Overview

This repository contains two implementations for solving the problem of placing \( k \) knights on an \( n \times n \) chessboard such that no two knights threaten each other.
The implementations utilize Constraint Satisfaction Problems (CSP) and backtracking algorithms to find a solution. Additionally, the repository provides functionality for visualizing 
the solution on a chessboard.

### File Descriptions

1. **`k_knights_1.py`**:
    - This file contains the first implementation of the CSP solver for the knights problem, where the variables are the knights.
    - Classes:
        - `CSP_Knights`: Represents the CSP for placing knights on the board. It defines the variables, domains, and constraints.
        - `Solver`: Implements the backtracking algorithm.
        - `Drawer`: Provides methods for visualizing the chessboard and the solution.

2. **`k_knights_2.py`**:
    - This file contains the second implementation of the CSP solver for the knights problem, where the variables are the squares of the chessboard.
    The classes have the same names and functionality as the first implementation

3. **`main.py`**:
    - The main script for running tests on the two implementations.
    - Functions:
        - `custom_test()`: Allows the user to run custom tests by specifying the number of knights and the board size.
        - `default_test()`: Runs a series of default test cases to compare the performance of the two implementations.
        - `test(k, n)`: Runs a single test case with \( k \) knights on an \( n \times n \) board.

4. **`test.py`**:
    - A script that contains utility functions for running the tests. It is used by `main.py` to execute the custom and default tests.

### How to Run

#### Running Custom Tests

Follow these steps:

1. Clone the repository:
   ```bash
   git clone <repository_url>
   cd <repository_name>
   ```

2. Run the `main.py` script:
   ```bash
   python main.py
   ```

3. When prompted, enter `custom` to run custom tests or `default` to run the default tests.

4. If you're running a custom test, follow the prompts to enter the number of knights and the board size.

### Results

The default tests will run the series of cases described in the relation, that is cases where k=c for a given n, measuring the time taken by each implementation to find a solution.
The results will be displayed in the console, and the solutions will be visualized on a chessboard.
For n>8, implementation 2 will take a **very long** time.

### Notes

- The implementations may take a significant amount of time for larger board sizes and higher numbers of knights due to the complexity of the problem.
- Ensure you have the required libraries installed before running the scripts:
  ```bash
  pip install matplotlib
  ```
