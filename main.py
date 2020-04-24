import tkinter as tk

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

class Piece:
    def __init__(self, master, typ):
        ...

class Board:
    def __init__(self):
        self.board = 
