import tkinter as tk
from enum import Enum
'''
lowercase is yellow, uppercase is red
Ss: square, Tt: triangle, Cc: circle
H: home, E: entryway

todo: circles. thoughts:
A number means the square has a circle on the corresponding corner:
 1   2
 .---.
 |   |
 |   |
 .---.
 4   3
'''
BOARD = '\n'.join([
    '..............',
    '..............',
    'S............s',
    'S............t',
    'C...ehhHHE...c',
    'C...ehhHHE...c',
    'T............t',
    'S............s',
    '..............',
    '..............', 
])
SQUARES = 'SCT'

class PieceType(Enum):
    SQUARE, CIRCLE, TRIANGLE = SQUARES

class Color(Enum):
    YELLOW, RED = range(2)

class Piece:
    def __init__(self, master, typ):
        self.master = master
        self.typ = typ
        self.color = Color.YELLOW if typ == typ.upper() else Color.RED

class Board:
    def __init__(self):
        self.pieces = []

        # initialize pieces
        for row in BOARD:
            for sq in row:
                if sq.upper() in SQUARES:
                    self.pieces.append(Piece(self, sq))
