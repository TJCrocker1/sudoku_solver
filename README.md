# sudoku_solver
A Sudoku solver written in python.

A Sudoku solver written in python. solver.py provides a sudoku solving algorithm that takes a 9 by 9 list where each cell is either an integer [1-9] or empty (0) and returns a completed sudoku. The script starts by applying two rules to each cell: inclusion (i.e. just one number is missing from the row/col/sqr) and exclusion (i.e. only one number is left for that cell). These rules are sufficient to solve easy puzzles but for hard puzzles guesswork is required.

When no further cells can be updated by inclusion / exclusion, recursion is used to make a guess. After each guess the inclusion / exclusion rules are re-applied. This process will return either a completed sudoku or an exception that can be used to rule out false guesses. If a single solution is found the scrip will return that solution as a 9 by 9 list. If the input is invalid or the sudoku has more than one solution an exception is raised.

This script solved a large set of puzzles on the servers at codewars.com within the 12 second time limit. Challenge details can be found at: https://www.codewars.com/kata/5588bd9f28dbb06f43000085

The project has been updated with a computer vision module that extracts unsolved puzzles from images following the tutorial outlined at https://pyimagesearch.com/2020/08/10/opencv-sudoku-solver-and-ocr/. classifier.py and train_classifier.py contain a DNN and the script to train it on the MNIST data set using tensorflow. This model is supported by a computer vision script (reader.py) that extracts puzzles from an image using a procedure based on OpenCV. 

Usage: 
solve_sudoku.py -m [path to digit classifier] -i [path to sudoku image] -d [debug (1 or 0)] 
train_classifier -m [path to save digit classifier]
