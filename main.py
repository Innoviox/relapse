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
    YELLOW, RED = 'yellow', 'red'

class Piece:
    def __init__(self, master, typ):
        self.master = master
        self.typ = PieceType._value2member_map_[typ.upper()]
        self.color = Color.YELLOW if typ == typ.upper() else Color.RED

class Board(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self) # call superclass initializer

        self.board_frame = tk.Frame(self, borderwidth=5, relief=tk.RIDGE)
        
        self.pieces = []

        # initialize pieces
        for r_idx, row in enumerate(BOARD.split()):
            for c_idx, sq in enumerate(row):
                frame = tk.Frame(self.board_frame, width=10, height=10, borderwidth=1, relief=tk.GROOVE)
                label = tk.Label(frame, text=' ', font='TkFixedFont')
                
                if sq.upper() in SQUARES:
                    p = Piece(self, sq)
                    self.pieces.append(p)
                    label.config(text=p.typ.value, bg=p.color.value)

                frame.grid(row=r_idx, column=c_idx)
                label.pack()


        self.board_frame.pack()

if __name__ == "__main__":
    Board().mainloop()
