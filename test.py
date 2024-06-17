import k_knights_1 as k1
import k_knights_2 as k2
import time

def custom_test():
    while True:
        impl = input('Enter the implementation to test (1 or 2): ')
        if impl not in ['1', '2']:
            print('Invalid input')
            return
        k = int(input('Enter the number of knights: '))
        n = int(input('Enter the size of the board: '))
        if impl == '1':
            csp = k1.CSP_Knights(k, n)
            solver = k1.Solver()
            drawer = k1.Drawer()
            solution = solver.solve(csp)
            if solution:
                drawer.draw_chessboard(solution, n)
            else:
                print('No solution found')
        elif impl == '2':
            csp = k2.CSP_knights(k, n)
            solver = k2.Solver()
            drawer = k2.Drawer()
            solution = solver.solve(csp)
            if solution:
                drawer.draw_chessboard(solution, n)
            else:
                print('No solution found')
        repeat = input('Do you want to run another test? (y/n): ')
        if repeat.lower() != 'y':
            print('Exiting...')
            break

def default_test():
    print('Running default test...')
    print('This could take a while...')
    test(16, 6)
    test(20, 7)
    test(24, 8)
    test(32, 9)
    test(40, 10)

def test(k, n):
    measurements = 3
    print( "Test case:", k, "knights on a", n, "x", n, "board")
    csp1 = k1.CSP_Knights(k, n)
    solver1 = k1.Solver()
    drawer1 = k1.Drawer()
    start = time.time()
    solution1 = solver1.solve(csp1)
    end = time.time()
    print('Time taken by implementation 1:', round(end-start, 3), 'seconds')
    drawer1.draw_chessboard(solution1, n)
    solver2 = k2.Solver()
    drawer2 = k2.Drawer()
    total_time = 0
    for i in range(measurements):
        csp2 = k2.CSP_knights(k, n)
        start = time.time()
        solution2 = solver2.solve(csp2)
        end = time.time()
        total_time += end-start
    print('Average time taken by implementation 2:', round(total_time/3, 3), 'seconds')
    drawer2.draw_chessboard(solution2, n)
    
        
    