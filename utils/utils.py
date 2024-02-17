import json
from multiprocessing.pool import ThreadPool
import os

from rich.console import Console

console = Console()

def displayProgress(iteration, total):
    bar_max_width = 45
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
