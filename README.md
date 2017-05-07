# Sliding-tile-puzzle-solver
A python graphical  sliding puzzle solver. For puzzles from 3x3 to 12x12 or more if it fits on your screen 
It is python 3.6 and tkinter, not use recursive fuctions not IA, plain, simple pyton code that I made when 
i was learning python.
There are two python scripts, one, panel_puzzle.py, is the solver library that you can use standalone, the oter script, puzzle.py is the main program and the graphical interface.
A 3x3 puzzle take about 6ms, a 10x10 take 700ms in my old 2008 pc.
You can try your own permutation with Tablero.inicia(list) the lis must contain all numbers from 0 to (row x columns) and a -1 that represents the empty tile. 
Example:
from panel_puzzle import Tablero
game = Tablero(4, 4)
perm = [10, 7, 14, 2, 0, 1, 6, 12, 4, 8, 9, 11, 5, 3, 13, -1]
game.inicia(perm)
game.print('start panel')
game.resuelve()
game.print('I win')
