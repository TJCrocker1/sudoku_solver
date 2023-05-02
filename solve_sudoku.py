# ------------------------------------------------ main script ---------------------------------------------------------
# import the necessary packages
from reader import extract_digit
from reader import find_puzzle
from keras.utils import img_to_array
from keras.models import load_model
from solver import solve
import numpy as np
import argparse
import imutils
import cv2

# ----------------------------------------------------------------------------------------------------------------------
# read in arguments
# ----------------------------------------------------------------------------------------------------------------------
ap = argparse.ArgumentParser()
ap.add_argument("-m", "--model", required=True, help="path to trained digit classifier")
ap.add_argument("-i", "--image", required=True, help="path to input Sudoku puzzle image")
ap.add_argument("-d", "--debug", required=False, type=int, help="print intermediate steps in puzzle recognition")
args = vars(ap.parse_args())

# ----------------------------------------------------------------------------------------------------------------------
# read puzzle from image, classify digits in cells then print solution:
# ----------------------------------------------------------------------------------------------------------------------
# load the digit classifier from disk
print("[INFO] loading digit classifier...")
model = load_model(args["model"])

# read the image
image = cv2.imread(args["image"])
image = imutils.resize(image, width=600)

# find the puzzle in the image and the size of each cell
(puzzleImage, warped) = find_puzzle(image, debug=args["debug"] > 0)
stepR = warped.shape[0] // 9
stepC = warped.shape[1] // 9

# build the sudoku board:
puzzle = [[0 for i in range(0, 9)] for j in range(0, 9)]
for c in range(0, 9):
    for r in range(0, 9):

        # find cell and extract digit:
        cell = warped[(r*stepR):((r+1)*stepR), (c*stepC):((c+1)*stepC)]
        digit = extract_digit(cell, debug=args["debug"] > 0)

        # if the cell has a digit apply the classifier and save the result:
        if digit is not None:
            roi = cv2.resize(digit, (28, 28))
            roi = roi.astype("float") / 255.0
            roi = img_to_array(roi)
            roi = np.expand_dims(roi, axis=0)
            puzzle[r][c] = model.predict(roi).argmax(axis=1)[0]
            print(puzzle[r][c])

# solve and print
solved_puzzle = solve(puzzle)
[print(r) for r in solved_puzzle]