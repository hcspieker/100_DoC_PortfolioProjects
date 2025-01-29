"""Contains the logic to save and load test summaries.

This contains the following classes:
- TestSummaryModel
- DataService

"""

import os.path
import pandas as pd

class TestSummaryModel:
    """Data model which stores information about a speed typing test.
    """
    def __init__(
            self,
            date: str,
            words: int, words_wrong: int,
            keys: int, keys_wrong: int
        ):
        self.date = date

        self.words = words
        self.words_wrong = words_wrong
        self.words_correct = words - words_wrong
        self.words_accuracy = round(self.words_correct * 100 / self.words, 2)

        self.keys = keys
        self.keys_wrong = keys_wrong
        self.keys_correct = keys - keys_wrong
        self.keys_accuracy = round(self.keys_correct * 100 / self.keys, 2)

class DataService:
    """This service is used to connect to data.csv which holds the past test results.
    """
    def __init__(self):
        self._data_file = "data.csv"

    def get_data(self) -> list[TestSummaryModel]:
        """Loads the past test results from data.csv, 
        orders the list (correct keys (descending); wrong keys (ascending)) 
        and converts the entries to TestSummaryModel.

        Returns:
            list[TestSummaryModel]: List of previous speed typing tests
        """
        result = []
        if not os.path.exists(self._data_file):
            return result

        df = pd.read_csv(self._data_file).sort_values(
            ["keys_correct", "keys_wrong"],
            ascending=[False,True])

        for _, row in df.iterrows():
            date = row["date"]
            words = row["words"]
            words_wrong = row["words_wrong"]
            keys = row["keys"]
            keys_wrong = row["keys_wrong"]

            result.append(TestSummaryModel(date, words, words_wrong, keys, keys_wrong))
        return result

    def save_entry(self, new_entry: TestSummaryModel):
        """Loads all existing entries from data.csv, 
        extends the list with the new entry and saves the result.

        Args:
            new_entry (TestSummaryModel): test result to add
        """
        new_row = pd.DataFrame({
            "date": [new_entry.date],
            "words": [new_entry.words],
            "words_wrong": [new_entry.words_wrong],
            "keys": [new_entry.keys],
            "keys_wrong": [new_entry.keys_wrong],
            "keys_correct": [new_entry.keys_correct]
        })

        if os.path.exists(self._data_file):
            df = pd.concat([pd.read_csv(self._data_file), new_row], ignore_index=True)
        else:
            df = new_row

        df.to_csv(self._data_file, index=False)
