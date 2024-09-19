 # WatchDict

 

 `WatchDict` is a Python class that extends the standard dictionary to track changes and save/load its state to/from a JSON file. It supports lists and sets as values, with notifications on modifications. The class also integrates logging with configurable log levels and allows custom JSON indentation for readability.

 

 ## Features

 

 - **Change Detection**: Automatically detects changes in lists and sets, and logs modifications.

 - **State Persistence**: Saves the current state to a JSON file and loads it on startup.

 - **Logging**: Configurable logging with different log levels and customizable JSON indentation.

 - **Customizable File Handling**: Specify the JSON file name and indentation level.

 

 ## Installation

 

 You don’t need to install `WatchDict` separately if you have the source code. Simply include the `WatchDict` class in your project or copy the code into your script.

## Installation
```zsh
python -m pip install watchdict --break-system-packages
```
 

 ## Usage

 

 1. **Create an Instance of `WatchDict`**:

 

    ```python

    from watchdict import WatchDict

 

    # Create an instance with a specific file name, log level, and JSON indentation

    watch_dict = WatchDict(filename="my_state.json", log_level=logging.DEBUG, indent=2)

    ```

 

 2. **Working with Lists and Sets**:

 

    ```python

    # Working with lists

    watch_dict['test_list'] = []

    watch_dict['test_list'].append(1)

    

    # Working with sets

    watch_dict['test_set'] = set()

    watch_dict['test_set'].add(42)

    watch_dict['test_set'].remove(42)

    ```

 

 3. **Logging**:

 

    - The `log_level` parameter in the constructor determines the verbosity of logs. Common levels include `logging.DEBUG`, `logging.INFO`, `logging.WARNING`, etc.

    - If the log level is set to `logging.NOTSET` (0), no logs will be printed.

 

 4. **Saving and Loading State**:

 

    - The `save_state()` method is automatically called after modifications to save the current state.

    - The `load_state()` method is called when creating an instance to load the saved state from the JSON file.

 

 ## Parameters

 

 - `filename` (str): The name of the JSON file for saving and loading the state. Defaults to `"watchdict_state.json"`.

 - `log_level` (int): The logging level. Defaults to `logging.INFO`. Set to `logging.NOTSET` to disable logging.

 - `indent` (int): The number of spaces for JSON indentation. Defaults to `4`.

 

 ## Example

 

 Here is a complete example of how to use `WatchDict`:

 

 ```python

 import logging

 from watchdict import WatchDict

 

 # Create an instance of WatchDict

 watch_dict = WatchDict(filename="my_state.json", log_level=logging.DEBUG, indent=2)

 

 # Working with lists

 watch_dict['test_list'] = []

 watch_dict['test_list'].append(1)

 

 # Working with sets

 watch_dict['test_set'] = set()

 watch_dict['test_set'].add(42)

 watch_dict['test_set'].remove(42)

 ```

 

 ## Dependencies

 

 - Python 3.x

 

 ## Contributing

 

 Feel free to submit issues or pull requests. Contributions are welcome!

 

 ## License

 

 This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

