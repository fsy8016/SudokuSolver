# SudokuSolver
A Python implementation using breadth-first search and depth-first search to take in and solve Sudoku boards

Sources:    
    http://norvig.com/sudoku.html
    http://www.scanraid.com/BasicStrategies.htm
    http://www.sudokudragon.com/sudokustrategy.htm
    http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
    http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/

Requirements:

    All files must be in the current directory
        Program Files:
            -Sudoku.py
            -sudoku4x4.py 
        
        Test Files:
            - top95.txt
            - Basic.txt
            - sudo4x4_test_board.txt

Assumption:
    -Board format is correct
    -Board is a valid sudoku board, meaing there is only one solution
    
Constraints Used:
    -A square may not have the same value as another square in its row,
    column, or in its block. Blocks being the N, sqrt(N) by sqrt(N) partitions
    in a sudoku board. (In a 9x9, the blocks are the 9 3x3 partitions).

Inputs:
    Board Format: Going across each row in the board list the numbers on one line
                    with a blank either being a "0" or "." (choose one formant).
                    Each line in the test file is a board.

Execution:
    Edit the "solve_all" and "solve_allbfs" to include the file name of the test file.
    Then run the code with "python sudoku4x4" or "python Sudoku" depending on the size of
    the board you are testing.
    
Error Handling:
    - Board with incorrect format like two 1's on a line in the board will show up as fail,
      in the number count of the number of test cases solved in the output
      
    - In Test file,board length is not of correct size will give an error message
    
Side Notes:
    "speed of the algorithm is determined by whether it can avoid the deadly combination of value choices"-norvig
