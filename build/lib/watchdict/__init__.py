import json
import os
import sys
from .trie import PrefixTree as build_trie
from typing import Any, Dict, SupportsIndex

# Initialize the debug flag
debug = True  # Set to True to enable logging, False to disable it

def log_change(message: str):
    """Log a message to stdout if debug is enabled."""
    if debug:
        print(message, file=sys.stdout)

def check_query(s):
    if not isinstance(s, str):
        return False
    return '*' in s or '$' in s or '>' in s or '<' in s or '|' in s or '&' in s

def ensure_path(path):
    if not os.path.exists(path) or not os.path.getsize(path):
        with open(path, '+w') as fp:
            fp.write('{\n}')
    return json.load(open(path, 'rb'))

def check(top, item, allow_search=False):
    if isinstance(item, list) or isinstance(item, set):
        return WatchableList(top, item, allow_search)
    if isinstance(item, dict):
        return WatchableDict(top, item, allow_search)
    return item

class WatchableList(list):
    def __init__(self, top, data, allow_search=False):
        self.top = top
        self.data = data
        super().__init__(data)
        if allow_search:
            self.search = build_trie(self)
        self.allow_search = allow_search

    def append(self, object: Any) -> None:
        self.data.append(object)
        super().append(object)
        self.top.commit()
        log_change(f"Appended: {object}")

    def sort(self, key=None, reverse=False):
        self.data.sort(key, reverse)
        super().sort(key, reverse)
        self.top.commit()
        log_change("Sorted list")

    def extend(self, iterable) -> None:
        self.data.extend(iterable)
        super().extend(iterable)
        log_change(f"Extended list with: {iterable}")

    def pop(self, index: SupportsIndex = -1) -> Any:
        value = self.data.pop(index)
        self.top.commit()
        log_change(f"Popped: {value}")
        return super().pop(index)

    def remove(self, value: Any) -> None:
        self.data.remove(value)
        self.top.commit()
        log_change(f"Removed: {value}")
        return super().remove(value)

    def insert(self, index: SupportsIndex, object: Any) -> None:
        self.data.insert(index, object)
        self.top.commit()
        log_change(f"Inserted: {object} at index {index}")
        return super().insert(index, object)

    def reverse(self) -> None:
        self.data.reverse()
        self.top.commit()
        log_change("Reversed list")
        return super().reverse()

    def __getitem__(self, item):
        if self.allow_search and check_query(item):
            return self.search.search(item)
        return check(self.top, self.data[item], self.allow_search)

class WatchableDict(dict):
    def __init__(self, top, data, allow_search=False):
        self.data = data
        self.top = top
        super().__init__(data)
        self.allow_search = allow_search
        if allow_search:
            self.val_search = build_trie(list(self.values()))
            self.key_search = build_trie(list(self.keys()))

    def __setitem__(self, key: Any, value: Any) -> None:
        self.data[key] = value
        self.top.commit()
        log_change(f"Set item: {key} = {value}")
        return super().__setitem__(key, value)

    def __delitem__(self, key: Any) -> None:
        value = self.data.pop(key)
        self.top.commit()
        log_change(f"Deleted item: {key} which had value {value}")
        return super().__delitem__(key)

    def __getitem__(self, item):
        if self.allow_search and check_query(item):
            res = self.val_search.search(item)
            return [{list(self.keys())[i[1]]: i[0]} for i in res]
        return check(self.top, self.data[item], self.allow_search)

class WatchDict(WatchableDict):
    def __init__(self, database, allow_search=False):
        """
        Allow search makes a searchable watchdict but this option may use more resources. but it's faster in searching.
        """
        super().__init__(self, ensure_path(database), allow_search)
        self.db = database

    def commit(self):
        with open(self.db, '+w') as fp:
            fp.write(json.dumps(self.data))
            log_change(f"Committed changes to {self.db}")
