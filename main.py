import tkinter as tk
from enum import Enum
from itertools import cycle

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
PLACEHOLDERS = {
    COLORS[SQUARES[0]]: 'pink',
    COLORS[SQUARES[0].lower()]: 'white'
}

def same_case(s1, s2): # utility method to test if two one-length strings are the same case
    return (s1 == s1.upper() and s2 == s2.upper()) or (s1 == s1.lower() and s2 == s2.lower())

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

        self.turns = cycle((str.upper, str.lower)) # yellow first, red second
        self.turn = next(self.turns)

        self.moved = []

        self.board_frame.pack()

    def clicked(self, event):
        label = event.widget
        t = label['text']

        if self.selected and label in self.highlighted:
            self.clear_highlighted()
            self.move_to(label)
            self.selected = None
            self.tick_turn()
        elif t.upper() in SQUARES and t == self.turn(t):
            self.clear_highlighted()
            self.highlight_possible(label)
            self.selected = label

    def move_to(self, label): # note: assumes selected has been set
        self.moved.append(self.get_pos(self.selected))
        print(self.selected['bg'])
        label.config(text=self.selected['text'], bg=self.selected['bg'], fg='black')
        print(label['bg'])
        self.selected['text'] = ' '
        self.reset(self.selected)

    def tick_turn(self):
        self.turn = next(self.turns)

    def highlight_possible(self, label): # note: assumes clear_highlighted has already been called
        r, c = self.get_pos(label)
        
        for label in self.valid_moves(label['text'], (r, c)):
            self.highlight(label)

    def valid_moves(self, typ, pos):
        r, c = pos

        moves = MOVEMENT[typ.upper()]
        if pos not in self.moved and (c in [0, len(BOARD[0]) - 1]):
            moves = list(moves) + [[i[0] * 2, i[1] * 2] for i in moves] # double movement on first turn
            # todo: can't move through pieces on a double move
            
        for (dx, dy) in moves:
            new_row, new_col = r + dy, c + dx

            if label := self.label_at(new_row, new_col):
                t = label['text']
                if t == ' ' or label['fg'] in PLACEHOLDERS.values() or not same_case(typ, t):
                    yield label

    def highlight(self, label):
        self.highlighted.append(label)
        label.config(bg='light blue')

    def clear_highlighted(self):
        for sq in self.highlighted:
            self.reset(sq)
        self.highlighted = []

    def reset(self, label): # reset to original color
        r, c = self.get_pos(label)
        original_text = BOARD[r][c]
        
        label.config(bg=COLORS[original_text])

        if original_text.upper() in SQUARES:
           label.config(text=original_text, fg=PLACEHOLDERS[label['bg']])

    def label_at(self, row, col):
        try:
            return self.board_frame.grid_slaves(row, col)[0].winfo_children()[0]
        except (tk.TclError, IndexError): # went off grid
            return None

    def get_pos(self, label):
        info = label.master.grid_info()
        return info['row'], info['column']
            

if __name__ == "__main__":
    Board().mainloop()

# todo: lines/diagonals/circles on board
