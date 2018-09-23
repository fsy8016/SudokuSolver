""" 
Solve Every Sudoku Puzzle
Sources:    http://norvig.com/sudoku.html
            http://www.scanraid.com/BasicStrategies.htm
            http://www.sudokudragon.com/sudokustrategy.htm
            http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
            http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/
Members Who worked on the Code:
    -Steve: modify the code from the first source to add BFS
    -Kao-Ying: alter code from first source to work on a 4x4 instead of 9x9 
"""

## Throughout this program we have:
##   r is a row,    e.g. 'A'
##   c is a column, e.g. '3'
##   s is a square, e.g. 'A3'
##   d is a digit,  e.g. '9'
##   u is a unit,   e.g. ['A1','B1','C1','D1','E1','F1','G1','H1','I1']
##   grid is a grid,e.g. 81 non-blank chars, e.g. starting with '.18...7...
##   values is a dict of possible values, e.g. {'A1':'12349', 'A2':'8', ...}

def cross(A, B):
    "Cross product of elements in A and elements in B."
    return [a+b for a in A for b in B]

digits   = '1234'
rows     = 'ABCD'
cols     = digits
squares  = cross(rows, cols)
unitlist = ([cross(rows, c) for c in cols] +
            [cross(r, cols) for r in rows] +
            [cross(rs, cs) for rs in ('AB','CD') for cs in ('12','34')])
units = dict((s, [u for u in unitlist if s in u])
             for s in squares)
peers = dict((s, set(sum(units[s],[]))-set([s]))
             for s in squares)
prevBoard = units

################ Unit Tests ################

def test():
    "A set of tests that must pass."
    assert len(squares) == 16
    assert len(unitlist) == 12
    assert all(len(units[s]) == 3 for s in squares)
    assert all(len(peers[s]) == 7 for s in squares)
    assert units['C2'] == [['A2', 'B2', 'C2', 'D2'],
                           ['C1', 'C2', 'C3', 'C4'],
                           ['C1', 'C2', 'D1', 'D2']]
    assert peers['C2'] == set(['A2', 'B2', 'D2',
                               'C1', 'C3', 'C4',
                               'D1'])
    print 'All tests pass.'

################ Parse a Grid ################

def parse_grid(grid):
    """Convert grid to a dict of possible values, {square: digits}, or
    return False if a contradiction is detected. This is the AC-3 part of our code.
    This also contains the final print of AC3"""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s,d in grid_values(grid).items():
        if d in digits and not assignAC3(values, s, d):
            return False ## (Fail if we can't assign d to square s.)
    displayAC3(values, units)
    return values
    
def basicParse_grid(grid):
    """No AC3 is done in this version of parse"""
    ## To start, every square can be any digit; then assign values from the grid.
    values = dict((s, digits) for s in squares)
    for s,d in grid_values(grid).items():
		if d == '.' or d == '0':
			values[s] = digits
		else:
			values[s] = d
    return values
    
def grid_values(grid):
    "Convert grid into a dict of {square: char} with '0' or '.' for empties."
    chars = [c for c in grid if c in digits or c in '0.']
    assert len(chars) == 16
    return dict(zip(squares, chars))

################ Constraint Propagation ################

def assign(values, s, d):
    """Eliminate all the other values (except d) from values[s] and propagate.
    Return values, except return False if a contradiction is detected."""
    other_values = values[s].replace(d, '')
    if all(eliminate(values, s, d2) for d2 in other_values):
        return values
    else:
        return False
        
def assignAC3(values, s, d):
    """Identical to the assign above, but is neccessary for printing the two different
    methods. Note that the logic of the AC3 eliminates given variables one at a time. Thus
    the domains of the squares are all 1234 except for one square. After the board
    is reduced, the other given variable is then applied to the board."""
    other_values = values[s].replace(d, '')
    if all(eliminateAC3(values, s, d2) for d2 in other_values):
        if solved(values) is False:
            displayAC3(values, prevBoard)
        return values
    else:
        return False

def basicAssign(values, s, d):
    """basicAssign only checks if d is a valid assignment on the board. If
    assign fails, we return false. Else, delete other values in the domain
    of this square"""
	## calls assign to see if the assignment is valid, but doesn't reduce the domains of other squares
    """ This prints the board with the tried value when false. We also print the board without
	the bad value to show how the DFS returns to the original board to attempt another value"""
    if not assign(values.copy(), s, d):
        valuescopy = values.copy()
        values[s] = str(d)
        display(valuescopy)
        display(values)
        return False
    else:
        values[s] = str(d)
    display(values)
    return values
    
def eliminate(values, s, d):
    """Eliminate d from values[s]; propagate when values or places <= 2.
    Return values, except return False if a contradiction is detected."""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminate(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assign(values, dplaces[0], d):
                return False
    return values
    
def eliminateAC3(values, s, d):
    """Same as eliminate above, but we need it to print"""
    if d not in values[s]:
        return values ## Already eliminated
    values[s] = values[s].replace(d,'')
    ## (1) If a square s is reduced to one value d2, then eliminate d2 from the peers.
    if len(values[s]) == 0:
        return False ## Contradiction: removed last value
    elif len(values[s]) == 1:
        d2 = values[s]
        if not all(eliminateAC3(values, s2, d2) for s2 in peers[s]):
            return False
    ## (2) If a unit u is reduced to only one place for a value d, then put it there.
    for u in units[s]:
        dplaces = [s for s in u if d in values[s]]
        if len(dplaces) == 0:
            return False ## Contradiction: no place for this value
        elif len(dplaces) == 1:
            # d can only be in one place in unit; assign it there
            if not assignAC3(values, dplaces[0], d):
                return False
    return values

################ Display as 2-D grid ################

def display(values):
    "Display these values as a 2-D grid."
    width = 5
    for r in rows:
        print ''.join(('') + (values[r+c].center(width) if len(values[r+c]) == 1
                    else '_'.center(width)) for c in cols)
    time.sleep(.5)
    if solved(values) is False:
        print
    else:
        print "Board has been solved"
        print ''
        time.sleep(3)
    
def displayAC3(values, old):
    "Display these values as a 2-D grid. Shows domains instead of blanks."
    width = 5
    if (old == values):
        return
    global prevBoard
    prevBoard = values.copy()
    time.sleep(1.5)
    for r in rows:
        print ''.join(values[r+c].center(width)
                      for c in cols)
    if solved(values) is False:
        print
    else:
        print "Board has been solved by AC3"
        print ''
        time.sleep(3)

################ Search ################

def solve(grid): return search(parse_grid(grid))

#Adding more basic search in
def solveBasic(grid): return searchBasic(basicParse_grid(grid))

def search(values):
    "By the time the program reaches this point, the board is solved"
    if values is False:
        return False ## Failed earlier
    return values ## Solved!
	
def searchBasic(values):
    "Using depth-first search, try values until solution is found."
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in squares):
        return values ## Solved!
    ## Chose the unfilled square s with the fewest possibilities
    n,s = min((len(values[s]), s) for s in squares if len(values[s]) > 1)
    return some(searchBasic(basicAssign(values.copy(), s, d))
                for d in values[s])

################ Utilities ################

def some(seq):
    "Return some element of seq that is true."
    for e in seq:
        if e: return e
    return False

def from_file(filename, sep='\n'):
    "Parse a file into a list of strings, separated by sep."
    return file(filename).read().strip().split(sep)

def shuffled(seq):
    "Return a randomly shuffled copy of the input sequence."
    seq = list(seq)
    random.shuffle(seq)
    return seq

################ System test ################

import time, random

def solve_all(grids, name='', showif=0.0):
    """Attempt to solve a sequence of grids. Report results.
    When showif is a number of seconds, display puzzles that take longer.
    When showif is None, don't display any puzzles."""
    
    def time_solve(grid):
        start = time.clock()
        values = solve(grid)
        t = time.clock()-start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print '(%.2f seconds)\n' % t
        return (t, solved(values))
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 100:
		for timecomp in times:
			print timecomp

		print "AC-3 Solved %d of %d %s puzzles (avg %.5f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times)/N, N/sum(times), max(times))

def solve_allBasic(grids, name='', showif=0.0):
    """basicSearch (DFS) version of solve all"""
    def time_solve(grid):
        start = time.clock()
        values = solveBasic(grid)
        t = time.clock()-start
        ## Display puzzles that take long enough
        if showif is not None and t > showif:
            display(grid_values(grid))
            if values: display(values)
            print '(%.2f seconds)\n' % t
        return (t, solved(values))
    times, results = zip(*[time_solve(grid) for grid in grids])
    N = len(grids)
    if N > 100:
		for timecomp in times:
			print timecomp

		print "DFS Basic Solved %d of %d %s puzzles (avg %.5f secs (%d Hz), max %.2f secs)." % (
            sum(results), N, name, sum(times)/N, N/sum(times), max(times))

def solved(values):
    "A puzzle is solved if each unit is a permutation of the digits 1 to 9."
    def unitsolved(unit): return set(values[s] for s in unit) == set(digits)
    return values is not False and all(unitsolved(unit) for unit in unitlist)

################ Execute test ################     
if __name__ == '__main__':
    solve_all(from_file("sudo4x4_test_board.txt"), "AC3 Tests", None)
    solve_allBasic(from_file("sudo4x4_test_board.txt"), "Uninformed DFS", None)

## References used:
## http://www.scanraid.com/BasicStrategies.htm
## http://www.sudokudragon.com/sudokustrategy.htm
## http://www.krazydad.com/blog/2005/09/29/an-index-of-sudoku-strategies/
## http://www2.warwick.ac.uk/fac/sci/moac/currentstudents/peter_cock/python/sudoku/