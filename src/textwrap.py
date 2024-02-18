"""
Text Wrapping Utility

This utility function, `wrap_text`, is designed to wrap a given text or a list of texts into lines of a specified width, 
ensuring that the output fits within a certain column width without breaking words. It supports handling text, 
lists of text, and datetime objects by converting them into a string format that is suitable for display or logging purposes.

Parameters:
- value (str, list, datetime): The input to be wrapped. This can be a single string, a list of strings, or a datetime object.
- width (int): The maximum line width for the wrapped text. Defaults to 80 characters.

Returns:
- str: A new string that contains the original text wrapped to the specified width.

Features:
- Dynamically wraps text or lists of text to a specified width.
- Converts datetime objects to a string representation before wrapping.
- Ensures that words are not split in the middle when wrapping lines.

Usage:
This function is particularly useful for formatting output in console applications, log files, 
or any situation where maintaining a specific column width for text output is necessary. 
It enhances readability and presentation of data when dealing with variable length strings or data entries.

# Example usage with a string
print(wrap_text("This is a long string that will be wrapped to the specified width.", 50))

# Example usage with a list of text
print(wrap_text(["List", "of", "strings", "to", "be", "wrapped"], 20))

# Example usage with a datetime object
print(wrap_text(datetime.now(), 30))

Note:
This utility does not handle very long words that exceed the specified width; such words will remain unbroken.

Author: Fatih Küçükkarakurt <https://github.com/fkkarakurt>
Created: 2024-02-17
Last Updated: 2024-02-18
"""

import textwrap
from datetime import datetime

def wrap_text(value, width=80):
    """Splits text or a list of text into lines of a specified width."""
    # If the value is of datetime type, convert it to string
    if isinstance(value, datetime):
        text = value.strftime("%Y-%m-%d %H:%M:%S")
    elif isinstance(value, list):
        # Convert list items to a string
        text = ', '.join(map(str, value))  
    else:
        # Convert all other values to string
        text = str(value)  

    wrapped_text = '\n'.join(textwrap.wrap(text, width))
    return wrapped_text
