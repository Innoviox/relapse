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
# ugly setting up of constants
BOARD = [
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
]
SQUARES = 'SCT'
ENTRY, HOME = 'EH'
COLORS = {
    '.': 'white', ' ': 'white',
    ENTRY.lower(): 'red',
    ENTRY.upper(): 'yellow',
    HOME.lower(): 'dark green',
    HOME.upper(): 'light green'
}
for i in SQUARES:
    COLORS[i.upper()] = 'yellow'
    COLORS[i.lower()] = 'red'

MOVEMENT = {
    SQUARES[0]:  ((1, 0), (-1, 0), (0, 1), (0, -1)),
    SQUARES[-1]: ((1, 1), (1, -1), (-1, 1), (-1, -1))
}
MOVEMENT[SQUARES[1]] = MOVEMENT[SQUARES[0]] + MOVEMENT[SQUARES[-1]]

class Board(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self) # call superclass initializer

        self.board_frame = tk.Frame(self, borderwidth=5, relief=tk.RIDGE)
        
        for r_idx, row in enumerate(BOARD):
            for c_idx, sq in enumerate(row):
                frame = tk.Frame(self.board_frame, width=10, height=10, borderwidth=1, relief=tk.GROOVE)
                label = tk.Label(frame, text=' ', font='TkFixedFont')
                
                if sq.upper() in SQUARES:
                    label.config(text=sq)

                label.config(bg=COLORS[sq])

                label.bind("<1>", self.clicked) # bind to left-click

                frame.grid(row=r_idx, column=c_idx)
                label.pack()

        self.highlighted = []
        self.selected = None

        self.board_frame.pack()

    def clicked(self, event):
        label = event.widget

        if self.selected:
            ...
        elif label['text'].upper() in SQUARES:
            self.clear_highlighted()
            self.highlight_possible(label)

    def highlight_possible(self, label): # note: assumes clear_highlighted has already been called
        info = label.master.grid_info()
        r, c = info['row'], info['column']
        
        for label in self.valid_moves(label['text'], (r, c)):
            try:
                self.highlight(label)
            except (tk.TclError, IndexError): # went off grid
                pass

    def valid_moves(self, typ, pos):
        r, c = pos
        for (dx, dy) in MOVEMENT[typ.upper()]:
            new_row, new_col = r + dy, c + dx

            lbl = self.label_at

    def highlight(self, label):
        self.highlighted.append(label)
        label.config(bg='light blue')

    def clear_highlighted(self):
        for sq in self.highlighted:
            sq.config(bg=COLORS[sq['text']])
        self.highlighted = []

    def label_at(self, row, col):
        return self.board_frame.grid_slaves(row, col)[0].winfo_children()[0]
            

if __name__ == "__main__":
    Board().mainloop()

# todo: lines/diagonals/circles on board
