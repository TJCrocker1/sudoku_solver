# ------------------------------------------------ sudoku solver -------------------------------------------------------
import math
import copy
import numpy as np

# ----------------------------------------------------------------------------------------------------------------------
# sudoku solver returns completed puzzle where only one solution exists
# ----------------------------------------------------------------------------------------------------------------------
def solve(puzzle):
    global nsol
    global solution

    nsol, solution = 0, []
    local_puzzle = init(puzzle)

    # check puzzle is valid:
    if not valid(local_puzzle): raise Exception("Invalid puzzle!")

    # check a single solution exists: (solve puzzle as side effect)
    if not solvable(local_puzzle):
        raise Exception("Could not find a solution!")
    else:
        return [[solution[r][c][0] for c in range(9)] for r in range(9)]


# ----------------------------------------------------------------------------------------------------------------------
# solvable solves puzzle as side effect and returns true - raises exception if more than one solution
# ----------------------------------------------------------------------------------------------------------------------
def solvable(puzzle):
    global nsol
    global solution
    local_puzzle = copy.deepcopy(puzzle)
    unknown_cells = [(r, c) for r in range(9) for c in range(9) if len(local_puzzle[r][c]) > 1]
    while True:
        stuck = True

        # appy inclusion / exclusion rules: (if successful stuck = False)
        for cell in unknown_cells:
            r, c = cell[0], cell[1]
            old = copy.deepcopy(local_puzzle[r][c])
            local_puzzle[r][c] = apply_rules(local_puzzle, r, c)
            if local_puzzle[r][c] != old:
                stuck = False
                if local_puzzle[r][c] == []: return False
                if len(local_puzzle[r][c]) == 1: unknown_cells.remove((r, c))

        # if complete make checks and save solution:
        if len(unknown_cells) == 0:
            if local_puzzle != solution: nsol += 1
            if nsol == 1:
                solution = local_puzzle
                return True
            else:
                raise Exception("More than one solution has been found!")

        # if incomplete and stuck start guessing:
        if stuck:
            test_puzzle = copy.deepcopy(local_puzzle)
            l = min([len(local_puzzle[cell[0]][cell[1]]) for cell in unknown_cells])
            guess = next((cell for cell in unknown_cells if len(local_puzzle[cell[0]][cell[1]]) == l), None)
            r, c = guess[0], guess[1]

            # a non-solvable guess can be excluded:
            for n in local_puzzle[r][c]:
                test_puzzle[r][c] = [n]
                if not solvable(test_puzzle):
                    local_puzzle[r][c].remove(n)
                    if len(local_puzzle[r][c]) == 1: unknown_cells.remove((r, c))
                    break

# ----------------------------------------------------------------------------------------------------------------------
# apply_rules updates possibilities in a cell based on inclusion/exclusion rules
# ----------------------------------------------------------------------------------------------------------------------
def apply_rules(puzzle, r, c):

    # update possibilities in cell [r,c] by exclusion:
    row = puzzle[r]
    col = [p[c] for p in puzzle]
    cmin, rmin = 3 * math.floor(c / 3), 3 * math.floor(r / 3)
    sqr = [puzzle[r][c] for c in range(cmin, cmin + 3) for r in range(rmin, rmin + 3)]
    known_numbers = [i[0] for i in row + col + sqr if len(i) == 1]
    puzzle[r][c] = [i for i in puzzle[r][c] if i not in known_numbers]

    # check for single possibility in cell [r,c] by inclusion:
    for n in puzzle[r][c]:
        in_sqr = sum([n in i for i in sqr])
        in_col = sum([n in i for i in col])
        in_row = sum([n in i for i in row])
        if any([s == 1 for s in [in_sqr, in_col, in_row]]):
            puzzle[r][c] = [n]
            break

    return puzzle[r][c]


# ----------------------------------------------------------------------------------------------------------------------
# valid checks the input is legal - right dimensions and no errors
# ----------------------------------------------------------------------------------------------------------------------
def valid(puzzle):

    # check dimensions:
    valid_nums = all(puzzle[r][c][0] in range(1, 10) for r in range(9) for c in range(9))
    valid_dims = len(puzzle) == 9 and all([len(r) == 9 for r in puzzle])
    if not valid_dims or not valid_nums: return False

    # check row col and sqr errors:
    for i in range(9):

        row = puzzle[i]
        row = [r[0] for r in row if len(r) == 1]
        if sorted(row) != list(np.unique(row)): return False

        col = [p[i] for p in puzzle]
        col = [c[0] for c in col if len(c) == 1]
        if sorted(col) != list(np.unique(col)): return False

        cmin, rmin = math.floor(i / 3) * 3, (i % 3) * 3
        sqr = [puzzle[r][c] for c in range(cmin, cmin + 3) for r in range(rmin, rmin + 3)]
        sqr = [s[0] for s in sqr if len(s) == 1]
        if sorted(sqr) != list(np.unique(sqr)): return False

    return True


# ----------------------------------------------------------------------------------------------------------------------
# init populates empty cells with numbers [1-9]
# ----------------------------------------------------------------------------------------------------------------------
def init(puzzle):
    local_puzzle = copy.deepcopy(puzzle)
    for r in range(9):
        for c in range(9):
            if local_puzzle[r][c] == 0:
                local_puzzle[r][c] = list(range(1, 10))
            else:
                local_puzzle[r][c] = [local_puzzle[r][c]]
    return local_puzzle

# ----------------------------------------------------------------------------------------------------------------------
# test
# ----------------------------------------------------------------------------------------------------------------------

#empty_puzzle = [[0 for i in range(0,9)] for j in range(0,9)]
#print(empty_puzzle)

#puzzle = [
#    [0, 0, 6, 1, 0, 0, 0, 0, 8],
#    [0, 8, 0, 0, 9, 0, 0, 3, 0],
#    [2, 0, 0, 0, 0, 5, 4, 0, 0],
#    [4, 0, 0, 0, 0, 1, 8, 0, 0],
#    [0, 3, 0, 0, 7, 0, 0, 4, 0],
#    [0, 0, 7, 9, 0, 0, 0, 0, 3],
#    [0, 0, 8, 4, 0, 0, 0, 0, 6],
#    [0, 2, 0, 0, 5, 0, 0, 8, 0],
#    [1, 0, 0, 0, 0, 2, 5, 0, 0]
#]

#puzzle = [
#    [8, 0, 0, 0, 5, 0, 0, 0, 3],
#    [0, 5, 0, 6, 0, 1, 0, 8, 0],
#    [0, 0, 4, 0, 8, 0, 7, 0, 0],
#    [0, 8, 0, 7, 0, 5, 0, 3, 0],
#    [1, 0, 9, 0, 6, 0, 4, 0, 5],
#    [0, 7, 0, 1, 0, 2, 0, 9, 0],
#    [0, 0, 7, 0, 1, 0, 6, 0, 0],
#    [0, 1, 0, 2, 0, 9, 0, 4, 0],
#    [9, 0, 0, 0, 7, 0, 0, 0, 8]
#]


#solved_puzzle = solve(puzzle)
#[print(i) for i in solved_puzzle]


#print(solved_puzzle)
