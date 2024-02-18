"""
Utility Functions for Concurrent Execution and Data Processing

This script is part of the Port Scanner project (https://github.com/fkkarakurt/portscanner) by Fatih Küçükkarakurt. 
It provides a set of helper functions designed to facilitate the simultaneous execution of tasks and 
processing of JSON data in Python applications. It uses Python's `multiprocessing.pool.ThreadPool` for parallel execution and 
`rich.console.Console` for advanced output formatting in the terminal.

Functions:
- displayProgress(iteration, total): Displays a progress bar in the terminal to visually indicate the progress of a given task. 
It dynamically updates as the task progresses.

- extractJsonData(filename): Reads and parses a JSON file, returning the data as a Python dictionary. 
It simplifies the process of working with JSON data by abstracting file handling and parsing logic.

- threadPoolExecuter(function, iterable, iterableLength): Executes a given function in parallel across multiple threads, 
utilizing a thread pool. It's designed to improve the efficiency of operations that can be executed concurrently, 
such as network requests or IO-bound tasks.

Features:
- Progress bar visualization for long-running tasks, enhancing user experience by providing 
real-time feedback on task completion status.

- Simplified JSON data extraction for quick and easy access to data stored in JSON files.

- Optimized concurrency model that automatically adjusts to the number of available CPU cores, 
maximizing resource utilization and performance.

Usage:
These utility functions are intended for developers looking to implement concurrent execution patterns in their 
Python applications or scripts, especially when dealing with IO-bound tasks or when needing to 
process large amounts of data efficiently.

Example:
```python
# Example of using threadPoolExecuter to perform tasks concurrently
def task(item):
    # Task implementation
    pass

items = range(10)  # Iterable of items to process
threadPoolExecuter(task, items, len(items))

Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Part of the Port Scanner project: https://github.com/fkkarakurt/portscanner
Created: 2022-10-24
Last Updated: 2024-02-18
"""

import json
from multiprocessing.pool import ThreadPool
import os

from rich.console import Console

console = Console()

def displayProgress(iteration, total):
    bar_max_width = 40
    bar_current_width = bar_max_width * iteration // total
    bar = "█" * bar_current_width + "-" * (bar_max_width - bar_current_width)
    progress = "%.2f" % (iteration / total * 100)
    console.print(f"|{bar}| {progress} %", end="\r", style="blue")
    if iteration == total:
        print()


def extractJsonData(filename):
    with open(filename, "r") as file:
        data = json.load(file)
    return data


def threadPoolExecuter(function, iterable, iterableLength):
    number_of_workers = os.cpu_count()
    print(f"\nRunning using {number_of_workers} workers.\n")
    with ThreadPool(number_of_workers) as pool:
        for loopIndex, _ in enumerate(pool.imap(function, iterable), 1):
            displayProgress(loopIndex, iterableLength)
