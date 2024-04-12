import tkinter as tk
from threading import Thread
from functools import partial
import time
from sudoku import Sudoku


class Gui:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sudoku Solver")
        self.root.geometry("500x500")

        self.string_vars = [[tk.StringVar()
                             for i in range(9)] for j in range(9)]

        self.squares = [[tk.Entry(self.root, width=1, justify="center",
                                  textvariable=self.string_vars[j][i], font=("Helvetica", 20)) for i in range(9)] for j in range(9)]

        def callback(y, x, *_):
            # Get the current value of the StringVar
            n = self.string_vars[y][x].get()

            try:
                n = int(n)
            except ValueError:
                n = 0

            if n not in range(1, 10):
                n = 0
                self.string_vars[y][x].set("")
            # Call set_square_color with updated value
            self.set_square_color(y, x, n)

        # prepare board
        for i in range(9):
            self.root.rowconfigure(2 * i + 1, weight=1)
            self.root.columnconfigure(2 * i + 1, weight=1)
            for j in range(9):
                self.string_vars[i][j].trace_add(
                    mode="write", callback=partial(callback, i, j))
                self.squares[i][j].grid(row=(2 * j + 1),
                                        column=(2 * i + 1), sticky="news")
        for i in range(0, 19, 2):
            if i % 6 == 0:
                tk.Frame(self.root, height=10, bg="black").grid(
                    row=i, column=0, columnspan=19, sticky="we")
                tk.Frame(self.root, width=10, bg="black").grid(
                    column=i, row=0, rowspan=19, sticky="sn")
            else:
                tk.Frame(self.root, height=5, bg="black").grid(
                    row=i, column=0, columnspan=19, sticky="we")
                tk.Frame(self.root, width=5, bg="black").grid(
                    column=i, row=0, rowspan=19, sticky="sn")

        generate_grid_button = tk.Button(
            self.root, text="Generate", command=self.new_grid)
        generate_grid_button.grid(row=19, column=0, columnspan=8)

        solve_button = tk.Button(
            self.root, text="Solve", command=lambda: Thread(target=self.solve).start())
        solve_button.grid(row=19, column=8, columnspan=8)

        self.new_grid()
        self.root.mainloop()

    def new_sudoku(self):
        self.sudoku = Sudoku()

    def new_grid(self):
        self.new_sudoku()
        for x in range(9):
            for y in range(9):
                self.set_square(y, x, self.sudoku.grid[y][x], True)

    def set_square(self, y, x, n, new=False):
        if n == 0:
            self.string_vars[y][x].set("")
        else:
            self.string_vars[y][x].set(str(n))

        if n == 0:
            self.set_square_color(y, x, n)
        else:
            self.set_square_color(y, x, n, new)

    def set_square_color(self, y, x, n, new=False):
        if new:
            self.squares[y][x].config(bg="gray")
        elif n == self.sudoku.solution[y][x]:
            self.squares[y][x].config(bg="green2")
        elif n != 0:
            self.squares[y][x].config(bg="red")
        else:
            self.squares[y][x].config(bg="white")

    def get_grid(self):
        return [[0 if self.string_vars[j][i].get() == "" else int(self.string_vars[j][i].get()) for i in range(9)] for j in range(9)]

    def solve(self):

        grid = self.get_grid()

        def possible(y, x, n):
            for i in range(9):
                if n in (grid[i][x], grid[y][i]):
                    return False
            for i in range(3):
                for j in range(3):
                    if grid[(y // 3) * 3 + i][(x // 3) * 3 + j] == n:
                        return False
            return True

        self.solved = False

        def solve_helper():
            time.sleep(0.005)
            for x in range(9):
                for y in range(9):
                    if grid[y][x] == 0:
                        for n in range(1, 10):
                            if possible(y, x, n):
                                grid[y][x] = n
                                self.set_square(y, x, n)
                                solve_helper()
                        if self.solved:
                            return
                        grid[y][x] = 0
                        self.set_square(y, x, 0)
                        return
            self.solved = True

        solve_helper()
