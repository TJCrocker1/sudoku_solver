#------------------------------------------------- sudoku reader -------------------------------------------------------
from imutils.perspective import four_point_transform
from skimage.segmentation import clear_border
import numpy as np
import imutils
import cv2

# ----------------------------------------------------------------------------------------------------------------------
# find_puzzle takes and image and extracts the part with the sudoku puzzle
# ----------------------------------------------------------------------------------------------------------------------
def find_puzzle(image, debug=False):

    # convert the image to grayscale and blur it slightly
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 3)
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 11, 2)
    thresh = cv2.bitwise_not(thresh)
    if debug:
        cv2.imshow("Puzzle Thresh", thresh)
        cv2.waitKey(0)

    # find contours in the thresholded image and sort them by size
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)

    # look for the largest contour with four points: (raise exception if none is found)
    for i in range(0, len(cnts)):
        peri = cv2.arcLength(cnts[i], True)
        approx = cv2.approxPolyDP(cnts[i], 0.02 * peri, True)
        if len(approx) == 4:
            puzzleCnt = approx
            break
        if i == len(cnts-1):
            raise Exception(("Could not find Sudoku puzzle outline. "
                             "Try debugging your thresholding and contour steps."))

    if debug:
        output = image.copy()
        cv2.drawContours(output, [puzzleCnt], -1, (0, 255, 0), 2)
        cv2.imshow("Puzzle Outline", output)
        cv2.waitKey(0)

    # apply a four-point transform to make the puzzle square:
    puzzle = four_point_transform(image, puzzleCnt.reshape(4, 2))
    warped = four_point_transform(gray, puzzleCnt.reshape(4, 2))
    if debug:
        cv2.imshow("Puzzle Transform", puzzle)
        cv2.waitKey(0)

    return (puzzle, warped)

# ----------------------------------------------------------------------------------------------------------------------
# extract_digit returns only the pixles that make up digit in cell, if empty returns None
# ----------------------------------------------------------------------------------------------------------------------
def extract_digit(cell, debug = False):

    # threshold and clear the borders:
    thresh = cv2.threshold(cell, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    thresh = clear_border(thresh)
    if debug: cv2.imshow("Cell Thresh", thresh); cv2.waitKey(0)

    # find contours if any are present: (return None if empty)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    if len(cnts) == 0: return None

    # make a mask of the largest contour:
    c = max(cnts, key=cv2.contourArea)
    mask = np.zeros(thresh.shape, dtype="uint8")
    cv2.drawContours(mask, [c], -1, 255, -1)

    # check the mask fills more the 3\% of the cell: (if less it's likely noise)
    (h, w) = thresh.shape
    percentFilled = cv2.countNonZero(mask) / float(w * h)
    if percentFilled < 0.03: return None

    # apply the mask to the thresholded cell:
    digit = cv2.bitwise_and(thresh, thresh, mask=mask)
    if debug:
        cv2.imshow("Digit", digit)
        cv2.waitKey(0)

    return digit
