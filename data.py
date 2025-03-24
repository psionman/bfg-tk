"""User data for BfG."""

import json

from constants import DATA_FILE


class DataStore():
    def __init__(self):
        self.data = {}

    def read(self) -> None:
        with open(DATA_FILE, 'r') as f_data:
            store = json.load(f_data)
        self.username = '' if 'username' not in store else store['username']
        self.data = store

    def write(self, store: dict) -> None:
        with open(DATA_FILE, 'w') as f_data:
            json.dump(f_data, store)
        self.data = store
