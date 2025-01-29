"""Contains the entry point (StartPage) of the application."""

import datetime as dt
import tkinter as tk

import data
import ui_core as uic
import ui_scoreboard as uis
import ui_test as uit

class StartPage(tk.Tk):
    """Represents the main window, which shows a score board, the test or a result."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        default_pady = 5
        self.title('Speed typing tester')

        self.minsize(600, 200)
        self.grid_columnconfigure(0, weight=1)

        self._header = uic.Heading(self, 'Speed typing tester')
        self._header.grid(row=0, column=0, pady=default_pady)

        self._scoreboard = uis.ScoreboardFrame(self)
        self._scoreboard.grid(row=1, column=0, pady=default_pady)
        self._scoreboard.refresh_table()

        self._test_start = uit.StartTestFrame(self, self.start_test)
        self._test_start.grid(row=2, column=0, pady=default_pady)

        self._test_run = uit.RunTestFrame(self, self.finished_test)
        self._test_run.grid(row=3, column=0, pady=default_pady)
        self._test_run.grid_remove()

        self._test_result = uit.TestResultFrame(self, self.close_test_result)
        self._test_result.grid(row=4, column=0, pady=default_pady)
        self._test_result.grid_remove()

        self.mainloop()

    def start_test(self):
        """Event handler for start test button"""
        self._scoreboard.grid_remove()
        self._test_start.grid_remove()

        self._test_run.reset()
        self._test_run.grid()

    def finished_test(self):
        """This callback is used if a test run is finished 
        and the window switches to the test result."""
        words, w_words, keys, w_keys = self._test_run.get_result()

        summary = data.TestSummaryModel(
            dt.datetime.now().strftime("%Y-%m-%d"),
            words, w_words, keys, w_keys
        )
        self._test_result.load(summary)

        self._test_run.grid_remove()
        self._test_result.grid()

    def close_test_result(self):
        """Used to switch from test result to scoreboard"""
        self._scoreboard.refresh_table()

        self._test_result.grid_remove()
        self._scoreboard.grid()
        self._test_start.grid()
