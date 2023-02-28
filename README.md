# sudoku_solver
A Sudoku solver written in python.

A Sudoku solver written in python. The sudoku_solver() function takes a 9 by 9 list where each cell is either an integer [1-9] or empty and returns a completed sudoku or an exception. The script starts by populating the list by applying two rules to each cell: inclusion (i.e. just one number is missing from the row/col/sqr) and exclusion (i.e. one number can go nowhere else in the row/col/sqr). These rules are sufficient to solve easy puzzles but for hard puzzles guesswork is required. 

When no further cells can be updated by inclusion / exclusion, recursion is used to make a guess. After each guess the inclusion / exclusion rules are re-applied. This process will return either a completed sudoku or an exception that can be used to rule out false guesses. If a single solution is found the scrip will return that solution as a 9 by 9 list. If the input is invalid or the sudoku has more than one solution an exception is raised.

This script solved a test set of >100 puzzles on the servers at codewars.com within the 12 second time limit. Challenge details can be found at: https://www.codewars.com/kata/5588bd9f28dbb06f43000085
