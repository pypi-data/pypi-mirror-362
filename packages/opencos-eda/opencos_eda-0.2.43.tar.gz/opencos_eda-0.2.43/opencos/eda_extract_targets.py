#!/usr/bin/env python3

'''
Helper pymodule used by eda_deps_bash_completion.bash, extracts valid
targets from DEPS files
'''

import sys
import os
from pathlib import Path
import json

import yaml
import toml

from opencos.deps_helpers import get_all_targets

PATH_LPREFIX = str(Path('.')) + os.path.sep


def get_terminal_columns():
    """
    Retrieves the number of columns (width) of the terminal window.

    Returns:
        int: The number of columns in the terminal, or a default value (e.g., 80)
             if the terminal size cannot be determined.
    """
    try:
        size = os.get_terminal_size()
        return size.columns
    except OSError:
        # Handle cases where the terminal size cannot be determined (e.g., not in a TTY)
        return 80  # Default to 80 columns
    else:
        return 80


def print_columns_manual(data: list, num_columns: int = 4, auto_columns: bool = True) -> None:
    """Prints a list of strings in columns, manually aligning them."""
    if not data:
        print()
        return

    _spacing = 2

    # Calculate maximum width for each column
    max_lengths = [0] * num_columns
    max_item_len = 0
    for i, item in enumerate(data):
        col_index = i % num_columns
        max_lengths[col_index] = max(max_lengths[col_index], len(item))
        max_item_len = max(max_item_len, len(item))

    if auto_columns and num_columns > 1:
        window_cols = get_terminal_columns()
        max_line_len = 0
        for x in max_lengths:
            max_line_len += x + _spacing
        if max_line_len > window_cols:
            # subtract a column (already >= 2):
            return print_columns_manual(data=data, num_columns=num_columns-1, auto_columns=True)
        if max_line_len + max_item_len + _spacing < window_cols:
            # add 1 more column if we're guaranteed to have room.
            return print_columns_manual(data=data, num_columns=num_columns+1, auto_columns=True)
        # else continue

    # Print data in columns
    for i, item in enumerate(data):
        col_index = i % num_columns
        print(item.ljust(max_lengths[col_index] + _spacing), end="")  # Add padding
        if col_index == num_columns - 1 or i == len(data) - 1:
            print() # New line at the end of a row or end of data

def get_path_and_pattern(partial_path: str = '', base_path=str(Path('.'))) -> (str, str):
    '''Returns tuple of (partial_path, partial_target or filter)'''
    partial_target = ''
    if not partial_path or partial_path == str(Path('.')):
        partial_path = PATH_LPREFIX
    if not os.path.exists(partial_path):
        partial_path, partial_target = os.path.split(partial_path)
    if not partial_path:
        partial_path = PATH_LPREFIX

    return partial_path, partial_target



def run(partial_paths: list, base_path=str(Path('.'))) -> None:
    '''Returns None, prints DEPS keys into pretty columns, using arg

    partial_path as a string filter for target completions.
    '''

    targets_set = set()
    if not partial_paths:
        partial_paths = [PATH_LPREFIX] # run on current directory.

    for partial_path in partial_paths:
        partial_path, partial_target = get_path_and_pattern(
            partial_path=partial_path, base_path=base_path
        )
        try:
            keys = get_all_targets(
                dirs=[partial_path],
                base_path=base_path,
                filter_str=partial_target,
                error_on_empty_return=False,
                lstrip_path=True
            )
        except:
            keys = []
        for key in keys:
            targets_set.add(key)

    data = list(targets_set)
    data.sort()
    print_columns_manual(data=data, num_columns=4, auto_columns=True)


def main() -> None:
    '''Returns None, prints DEPS keys into pretty columns, uses sys.argv[1] for args:

    sys.args[1] -- optional partial path for target completions
    '''

    if len(sys.argv) > 1:
        partial_path = sys.argv[1]
    else:
        partial_path = ''
    run(partial_paths=[partial_path])


if __name__ == "__main__":
    main()
