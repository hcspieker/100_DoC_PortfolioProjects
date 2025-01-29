"""Contains ui core components that are used in other modules.

This contains the following classes:
- Heading
- SubHeading
- BoldLabel
- Label
- Button
- Table
- WordTable

And the following global Constants:
- FONT_NAME

"""

import random
import tkinter as tk

from typing import Callable

FONT_NAME = "Segoe UI"

class Heading(tk.Label):
    """Represents a heading with defined formatting, which is based on a tkinter Label."""
    def __init__(self, root, text: str, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.config(font=(FONT_NAME, 12, "bold", "underline"))
        self.config(text=text)

class SubHeading(tk.Label):
    """Represents a subheading with defined formatting, which is based on a tkinter Label."""
    def __init__(self, root, text: str, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.config(font=(FONT_NAME, 11, "bold"))
        self.config(text=text)

class BoldLabel(tk.Label):
    """Represents a bold label with defined formatting, which is based on a tkinter Label."""
    def __init__(self, root, text: str, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.config(font=(FONT_NAME, 9, "bold"))
        self.config(text=text)

class Label(tk.Label):
    """Represents a standard label with defined formatting, which is based on a tkinter Label."""
    def __init__(self, root, text: str, *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.config(font=(FONT_NAME, 9))
        self.config(text=text)

class Button(tk.Button):
    """Represents a Button with defined formatting, which is based on a tkinter Button."""
    def __init__(self, root, text: str, button_command: Callable[[], None], *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self.config(font=(FONT_NAME, 9))
        self.config(text=text)
        self.config(command=button_command)

class Table(tk.Frame):
    """This class defines a table structure, built on a frame, where labels represent the cells."""
    def __init__(self, root, header:list[str], content: list[list[str]], *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.spacing = 2

        self.load_data(header, content)

    def load_data(self, header:list[str], content: list[list[str]]):
        """Removes the existing entries from the table and draws a new one

        Args:
            header (list[str]): list of headers
            content (list[list[str]]): rows which include cells
        """
        for child in self.winfo_children():
            child.destroy()

        for i, cell in enumerate(header):
            header_label = BoldLabel(self, cell, background="white")
            header_label.grid(
                row=0, column=i,
                pady=self.spacing, padx=self.spacing,
                sticky=tk.W+tk.E
            )

        for i, row in enumerate(content):
            for j, cell in enumerate(row):
                cell_label = Label(self, cell, background="white")
                cell_label.grid(
                    row=i+1, column=j,
                    padx=self.spacing, pady=self.spacing,
                    sticky=tk.W+tk.E
                )

class WordTable(tk.Frame):
    """Custom widget, which displays words during a speed test 
    with different formatting: green for correct words, 
    red for mistakes, and blue for the current word."""
    def __init__(
            self, root,
            words: list[str], amount_of_rows:int=3, amount_of_columns=6,
            **kwargs
        ):
        super().__init__(root, **kwargs)

        self._words = words
        self._rows = amount_of_rows
        self._columns = amount_of_columns
        self._grid = []
        self._current_word = None
        self._current_word_index = None

        for i in range(amount_of_rows):
            row = []
            for j in range(amount_of_columns):
                cell = BoldLabel(self, "dummy", foreground="gray")
                cell.grid(row=i, column=j, sticky=tk.W)
                row.append(cell)
            self._grid.append(row)

    def reset_table(self):
        """Resets the content and formatting of the table after a speed test run.
        """
        random.shuffle(self._words)
        self._current_word = None
        self._current_word_index = None

        for row in self._grid:
            for cell in row:
                word = self._words.pop(0)
                self._words.append(word)
                cell.config(text=word)
                cell.config(foreground="gray")
        self._grid[0][0].config(foreground="blue")

    def get_current(self) -> str:
        """Gets the current selected word from the table

        Returns:
            str: current word
        """
        if self._current_word is None:
            self._current_word = self._grid[0][0].cget("text")
            self._current_word_index = (0, 0)
        return self._current_word

    def mark_current_word(self, is_correct: bool):
        """Marks the current word and moves to the next. 
        If the current word was typed correctly, it will be 
        formatted in green otherwise red. The next 
        word will be highlighted in blue

        Args:
            is_correct (bool): indicator if the spelling was correct
        """
        r,c = self._current_word_index
        current_label = self._grid[r][c]

        if is_correct:
            current_label.config(foreground="green")
        else:
            current_label.config(foreground="red")

        if (c+1) < self._columns:
            c = c + 1
        elif r == 0:
            r = 1
            c = 0
        else:
            c = 0
            for i in range(self._columns):
                first = self._grid[0][i]
                second = self._grid[1][i]
                third = self._grid[2][i]

                first.config(text=second.cget("text"))
                first.config(foreground=second.cget("foreground"))

                second.config(text=third.cget("text"))
                second.config(foreground=third.cget("foreground"))

                new_word = self._words.pop(0)
                self._words.append(new_word)
                third.config(text=new_word)

        current_cell = self._grid[r][c]
        current_cell.config(foreground="blue")

        self._current_word = current_cell.cget("text")
        self._current_word_index = (r, c)
