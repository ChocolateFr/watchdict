import json
import logging
from typing import Any, Dict

class WatchableList(list):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent = None
        self._parent_key = None

    def set_parent(self, parent, key):
        """Set the parent WatchDict and key to notify on change."""
        self._parent = parent
        self._parent_key = key

    def append(self, item):
        super().append(item)
        self._notify_change(f"Appended {item} to key: {self._parent_key}")

    def extend(self, iterable):
        super().extend(iterable)
        self._notify_change(f"Extended key: {self._parent_key} with {list(iterable)}")

    def __setitem__(self, index, value):
        super().__setitem__(index, value)
        self._notify_change(f"Set index {index} of key: {self._parent_key} to {value}")

    def _notify_change(self, message):
        if self._parent:
            self._parent._log(message)

class WatchableSet(set):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._parent = None
        self._parent_key = None

    def set_parent(self, parent, key):
        """Set the parent WatchDict and key to notify on change."""
        self._parent = parent
        self._parent_key = key

    def add(self, item):
        if item not in self:
            super().add(item)
            self._notify_change(f"Added {item} to key: {self._parent_key}")

    def remove(self, item):
        if item in self:
            super().remove(item)
            self._notify_change(f"Removed {item} from key: {self._parent_key}")

    def discard(self, item):
        if item in self:
            super().discard(item)
            self._notify_change(f"Discarded {item} from key: {self._parent_key}")

    def clear(self):
        if len(self) > 0:
            super().clear()
            self._notify_change(f"Cleared all items from key: {self._parent_key}")

    def _notify_change(self, message):
        if self._parent:
            self._parent._log(message)

class WatchDict(dict):
    def __init__(self, filename: str = "watchdict_state.json", log_level: int = logging.INFO, indent: int = 4):
        super().__init__()
        self._original = dict(self)
        self._filename = filename
        self._indent = indent
        self._setup_logger(log_level)
        self.load_state()

    def _setup_logger(self, log_level: int):
        """Set up logging configuration."""
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(log_level)
        handler = logging.StreamHandler()
        handler.setLevel(log_level)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        if not self._logger.hasHandlers():
            self._logger.addHandler(handler)

    def _log(self, message: str):
        """Log a message based on the log level."""
        if self._logger.level > logging.NOTSET:
            self._logger.info(message)

    def __setitem__(self, key, value):
        if isinstance(value, list):
            value = WatchableList(value)
            value.set_parent(self, key)
        elif isinstance(value, set):
            value = WatchableSet(value)
            value.set_parent(self, key)
        
        super().__setitem__(key, value)
        self._mark_as_modified(key)
        self.save_state()

    def _mark_as_modified(self, key):
        """Helper function to mark the key as modified."""
        self._log(f"Modified key: {key} (in-place change detected)")

    def __delitem__(self, key):
        if key in self:
            self._log(f"Deleted key: {key}, value: {self[key]}")
            super().__delitem__(key)
            del self._original[key]
            self.save_state()

    def clear(self):
        for key in list(self.keys()):
            self._log(f"Deleted key: {key}, value: {self[key]}")
        super().clear()
        self._original.clear()
        self.save_state()

    def pop(self, key, *args):
        value = super().pop(key, *args)
        self._log(f"Popped key: {key}, value: {value}")
        if key in self._original:
            del self._original[key]
        self.save_state()
        return value

    def update(self, *args, **kwargs):
        updated_dict = dict(*args, **kwargs)
        for key, value in updated_dict.items():
            self[key] = value
        self.save_state()

    def setdefault(self, key, default=None):
        if key not in self:
            self._log(f"Set default for key: {key}, value: {default}")
        return super().setdefault(key, default)

    def reset_change_tracking(self):
        """Resets the original state to the current state."""
        self._original = dict(self)

    def save_state(self):
        """Save the current state to a JSON file with custom indent."""
        with open(self._filename, 'w') as file:
            json.dump(self._to_serializable(), file, indent=self._indent)
        self._log("State saved to file.")

    def load_state(self):
        """Load the state from a JSON file."""
        try:
            with open(self._filename, 'r') as file:
                data = json.load(file)
                self.update(self._from_serializable(data))
            self._log("State loaded from file.")
        except FileNotFoundError:
            self._log("No saved state found. Starting with an empty dictionary.")

    def _to_serializable(self):
        """Convert the dictionary to a serializable format."""
        serializable_dict = {}
        for key, value in self.items():
            if isinstance(value, (WatchableList, WatchableSet)):
                serializable_dict[key] = list(value) if isinstance(value, WatchableList) else list(value)
            else:
                serializable_dict[key] = value
        return serializable_dict

    def _from_serializable(self, data):
        """Convert data from a serializable format to the dictionary."""
        deserialized_dict = {}
        for key, value in data.items():
            if isinstance(value, list) and any(isinstance(i, list) for i in value):
                deserialized_dict[key] = WatchableList(value)
            elif isinstance(value, list):
                deserialized_dict[key] = WatchableSet(value)
            else:
                deserialized_dict[key] = value
        return deserialized_dict

