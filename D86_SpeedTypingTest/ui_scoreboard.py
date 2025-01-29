"""Contains the scoreboard (ScoreboardFrame) of the application."""

import tkinter as tk

import data
import ui_core as uic

class ScoreboardFrame(tk.Frame):
    """Uses a table to display statistics about the best 5 test results"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._data_service = data.DataService()

        self._scoreboard_header = uic.SubHeading(self, "Scoreboard")
        self._scoreboard_header.pack()

        self._scoreboard = uic.Table(self, [], [])
        self._scoreboard.pack()

    def refresh_table(self):
        """Refreshes the content of the scoreboard (initial and after a run)."""
        table_header = ["Keys", "Words", "Date"]
        table_data = []

        for r in self._data_service.get_data()[:5]:
            table_data.append([
                f"({r.keys_correct} ✅ | {r.keys_wrong} ⛔) {r.keys} - {r.keys_accuracy} %",
                f"({r.words_correct} ✅ | {r.words_wrong} ⛔) {r.words} - {r.words_accuracy} %",
                r.date
            ])

        self._scoreboard.load_data(table_header, table_data)
