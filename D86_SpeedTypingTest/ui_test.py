"""Contains components used to run a test or display the summary.

This contains the following classes:
- StartTestFrame
- RunTestFrame
- TestResultFrame

"""

import tkinter as tk
from typing import Callable, Tuple

import data
import ui_core as uic

class StartTestFrame(tk.Frame):
    """Simple frame which includes only a button to switch to a typing test."""
    def __init__(self, root, starting_test: Callable[[], None], *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self._start_button = uic.Button(self, "Start a new test", starting_test)
        self._start_button.pack()

class RunTestFrame(tk.Frame):
    """This Component is used to execute a speed typing test."""
    def __init__(self, root, finished_test: Callable[[], None], *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        default_pady = 5
        self._finished = finished_test
        self._started = False
        self._timer_start_value = 60
        self._timer = self._timer_start_value
        self._timer_job = None

        self._count_keys = 0
        self._count_words = 0
        self._count_words_wrong = 0
        self._count_keys_wrong = 0

        self.grid_columnconfigure(0, weight=1)

        with open("words.txt", "r", encoding="utf-8") as file:
            self.words = [x.strip() for x in file.readlines()]

        self._header = uic.SubHeading(self, "Typing test")
        self._header.grid(row=0, column=0, pady=(default_pady, 0))

        self._description = uic.Label(
            self,
            "Begin typing to start the test. " + 
            f"Each run lasts {str(self._timer_start_value)} seconds, after which you'll" +
            " receive a detailed summary, including the total" + 
            " characters and words typed, along with a breakdown" + 
            " of errors and correctly typed words/characters.",
            wraplength=350
        )
        self._description.grid(row=1, column=0, pady=(0, default_pady))

        self._timer_label = uic.SubHeading(self, self._timer_start_value)
        self._timer_label.grid(row=2, column=0, pady=2*default_pady)

        self._word_table = uic.WordTable(self, self.words)
        self._word_table.grid(row=3, column=0, pady=default_pady)

        self._input_text = tk.StringVar(value="")
        self._input = tk.Entry(
            self,
            textvariable=self._input_text,
            justify="center",
            background="blue",
            foreground="white"
        )
        self._input.bind("<KeyRelease>", self.pressed)
        self._input.grid(row=4, column=0, sticky=tk.W+tk.E, pady=default_pady)

    def pressed(self, event: tk.Event):
        """This event triggers when a key is pressed. 
        If the test isn't started, a new run begins. 
        It checks the input for errors and moves to the next word if needed."""
        if self._input.cget("state") != "normal":
            return

        if not self._started:
            self._started = True
            self.countdown()

        input_text = self._input_text.get().strip()
        current_word = self._word_table.get_current()

        self._count_keys = self._count_keys + 1

        if event.char == " ":
            if input_text == current_word:
                self._word_table.mark_current_word(True)
            else:
                self._word_table.mark_current_word(False)
                self._count_words_wrong = self._count_words_wrong + 1
            self._count_words = self._count_words + 1
            self._input.config(background="blue")
            self._input_text.set("")
        elif current_word.startswith(input_text):
            self._input.config(background="green")
        else:
            self._input.config(background="red")

            if len(event.keysym) == 1:
                self._count_keys_wrong = self._count_keys_wrong + 1

    def countdown(self):
        """Updates the countdown and switches to test summary if the time is exceeded."""
        self._timer = self._timer - 1
        self._timer_label.config(text=str(self._timer))

        if self._timer > 0:
            self._timer_job = self.after(1000, self.countdown)
        else:
            self._input.config(state="disabled")
            self._input_text.set("")
            self._finished()

    def get_result(self) -> Tuple[int, int, int, int]:
        """Returns the result of the last test run."""
        return (
            self._count_words,
            self._count_words_wrong,
            self._count_keys,
            self._count_keys_wrong
        )

    def reset(self):
        """Resets the component to be ready for the next speed typing test."""
        self._count_keys = 0
        self._count_words = 0
        self._count_words_wrong = 0
        self._count_keys_wrong = 0

        self._timer = self._timer_start_value
        self._timer_label.config(text=str(self._timer))
        self._started = False
        self._input_text.set("")
        self._input.config(state="normal")
        self._input.config(background="blue")
        self._word_table.reset_table()

class TestResultFrame(tk.Frame):
    """Displays the test result in a table"""
    def __init__(self, root, close_results_callback: Callable[[], None], *args, **kwargs):
        super().__init__(root, *args, **kwargs)

        self._data_service = data.DataService()
        self._summary = None

        self._close_results = close_results_callback

    def load(self, summary: data.TestSummaryModel):
        """Loads the submitted test results into a table.

        Args:
            summary (data.TestSummaryModel): test result
        """
        for child in self.winfo_children():
            child.destroy()

        if summary is None:
            return

        self._summary = summary
        uic.SubHeading(self, "Typing test summary").grid(row=0, column=0, columnspan=3)

        uic.BoldLabel(self, "Keys").grid(row=1, column=1, pady=(10,0))
        uic.BoldLabel(self, "Words").grid(row=1, column=2, pady=(10,0))

        uic.BoldLabel(self, "Total").grid(row=2, column=0)
        uic.Label(self, str(summary.keys)).grid(row=2, column=1)
        uic.Label(self, str(summary.words)).grid(row=2, column=2)

        uic.BoldLabel(self, "Correct").grid(row=3, column=0)
        uic.Label(self, str(summary.keys_correct)).grid(row=3, column=1)
        uic.Label(self, str(summary.words_correct)).grid(row=3, column=2)

        uic.BoldLabel(self, "Mistakes").grid(row=4, column=0)
        uic.Label(self, str(summary.keys_wrong)).grid(row=4, column=1)
        uic.Label(self, str(summary.words_wrong)).grid(row=4, column=2)

        uic.BoldLabel(self, "Accuracy").grid(row=5, column=0)
        uic.Label(self, f"{str(summary.keys_accuracy)} %").grid(row=5, column=1)
        uic.Label(self, f"{str(summary.words_accuracy)} %").grid(row=5, column=2)

        uic.Button(self, "Forget results", self._close_results).grid(
            row=6, column=0,
            sticky=tk.W, pady=10
        )
        uic.Button(self, "Save run", self.save_run).grid(row=6, column=2, sticky=tk.E, pady=10)

    def save_run(self):
        """Saves the test results using the data service"""
        self._data_service.save_entry(self._summary)
        self._close_results()
