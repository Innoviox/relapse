import tkinter as tk
from enum import Enum
from itertools import cycle
from PIL import Image, ImageTk

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
    'T............t',
    'C...ehhHHE...c',
    'C...ehhHHE...c',
    'T............t',
    'S............s',
    '..............',
    '..............', 
]
CIRCLES = [[3, 3], [5, 3], [3, 9], [5, 9]]
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

def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle = _create_circle

def _create_circle_arc(self, x, y, r, **kwargs):
    if "start" in kwargs and "end" in kwargs:
        kwargs["extent"] = kwargs["end"] - kwargs["start"]
        del kwargs["end"]
    return self.create_arc(x-r, y-r, x+r, y+r, **kwargs)
tk.Canvas.create_circle_arc = _create_circle_arc


def same_case(s1, s2): # utility method to test if two one-length strings are the same case
    return (s1 == s1.upper() and s2 == s2.upper()) or (s1 == s1.lower() and s2 == s2.lower())

def is_diagonal(dxy): # returns if a motion is diagonal or not
    return all(dxy)

class Board(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self) # call superclass initializer

        self.board_frame = tk.Frame(self, borderwidth=5, relief=tk.RIDGE)
        # self.board_canvas = tk.Canvas(self)
        
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


        # self.board_canvas.place(relx=1, x=-2, y=2, anchor=tk.NE)
        # self.black_circle = ImageTk.PhotoImage(Image.open('./black_circle.gif'))

        # for c in CIRCLES:
        #     i = self.board_canvas.create_circle(c[1] * 20 + 25, c[0] * 20 + 20, 5, fill="black")

    def clicked(self, event):
        label = event.widget
        t = label['text']

        if self.selected and label in self.highlighted:
            self.clear_highlighted()
            self.move_to(label)
        elif t.upper() in SQUARES and t == self.turn(t) and label['fg'] not in PLACEHOLDERS.values():
            self.clear_highlighted()
            self.highlight_possible(label)
            self.selected = label

    def move_to(self, label): # note: assumes selected has been set
        self.moved.append(self.get_pos(self.selected))

        def finish_move():
            label.config(text=self.selected['text'], bg=self.selected['bg'], fg='black')     
            self.selected['text'] = ' '
            self.reset(self.selected)
            self.selected = None
            self.tick_turn()
        
        if label['text'] == ' ': 
            finish_move()
        else: # bounce tile
            self.bounce(label['text'], finish_move)

    # a bit of a nasty way to handle bouncing
    def bounce(self, typ, callback):
        available = [i for i in map(self._get_label, self.board_frame.grid_slaves()) if i['text'] == typ and i['fg'] in PLACEHOLDERS.values()]
        for i in available:
            i.config(bg='green')
            i.unbind("<1>")
            i.bind("<1>", self.bounce_to(typ, callback, available))

    def bounce_to(self, typ, callback, available):
        def clicked(event):
            label = event.widget
            label.config(text=typ, fg='black')

            # rebind callbacks
            for i in available:
                i.config(bg=COLORS[typ])
                i.unbind("<1>")
                i.bind("<1>", self.clicked)
            
            callback()
        return clicked

    def tick_turn(self):
        self.turn = next(self.turns)

        if w := self.winner():
            print(["", "Yellow", "Red"][w], "wins!")

    def highlight_possible(self, label): # note: assumes clear_highlighted has already been called
        r, c = self.get_pos(label)
        
        for label in self.valid_moves(label['text'], (r, c)):
            self.highlight(label)

    def valid_moves(self, typ, pos):
        r, c = pos

        old_text = BOARD[r][c]

        moves = MOVEMENT[typ.upper()]
        if pos not in self.moved and (c in [0, len(BOARD[0]) - 1]):
            moves = list(moves) + [[i[0] * 2, i[1] * 2] for i in moves] # double movement on first turn
            # todo: can't move through pieces on a double move
            
        for (dx, dy) in moves:
            new_row, new_col = r + dy, c + dx

            if label := self.label_at(new_row, new_col):
                orig = BOARD[new_row][new_col]
                t = label['text']
                
                impossible = False
                if is_diagonal((dx, dy)):
                    for circ in CIRCLES:
                        a, b = circ[0] - r, circ[1] - c
                        if [a, b, dx, dy] in [ # some fun bashing. please dont ask me to justify these numbers
                            [0, -1, -1, 1],
                            [-1, -1, -1, -1],
                            [0, 0, 1, 1],
                            [-1, 0, 1, -1]
                            ]:
                            impossible = True
                if old_text.upper() == 'E' and orig == '.': # can't move out of entrance
                    impossible = True
                if orig.upper() == 'E' and not same_case(typ, orig): # can't move into alternate entrance
                    impossible = True
                if old_text.upper() == 'H' and orig.upper() != 'H': # can't move out of home 
                    impossible = True
                if old_text.upper() == 'H' and orig.upper() == 'H' and not same_case(old_text, orig): # can't move into other home
                    impossible = True
                if orig.upper() == 'H' and old_text.upper() == '.': # can't move into home from outside
                    impossible = True
                if old_text.upper() != 'E' and orig.upper() == 'E' and dy != 0: # can't move into entrance from outside
                    if (orig == orig.upper() and dx == 1) or \
                       (orig == orig.lower() and dx == -1) or \
                       dx == 0:
                        impossible = True
                # print(' '.join(map(str, ((dx, dy), old_text, orig, impossible))))
            
                if not impossible and (t == ' ' or label['fg'] in PLACEHOLDERS.values() or not same_case(typ, t)):
                    yield label
        # print()

    def winner(self): # returns 1 for yellow, 2 for red, None for none
        yellow, red = 0, 0
        for r_idx, row in enumerate(BOARD):
            for c_idx, sq in enumerate(row):
                if sq.upper() == 'H' and self.label_at(r_idx, c_idx)['text'] != ' ':
                    if sq == sq.upper():
                        yellow += 1
                    else:
                        red += 1
        if yellow == 4:
            return 1
        if red == 4:
            return 2

    # visual utility methods
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
        elif label['text'].upper() in SQUARES:
            label.config(bg=COLORS[label['text']], fg='black')

    def label_at(self, row, col):
        try:
            return self._get_label(self.board_frame.grid_slaves(row, col)[0])
        except (tk.TclError, IndexError): # went off grid
            return None

    def _get_label(self, frame):
        return frame.winfo_children()[0]

    def get_pos(self, label):
        info = label.master.grid_info()
        return info['row'], info['column']
            

if __name__ == "__main__":
    Board().mainloop()

# todo: lines/diagonals/circles on board
# done! todo: can click on placeholder
