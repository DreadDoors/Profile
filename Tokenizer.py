"""
MPHEAW - Modules/Tokenizer.py

A PURE helper: text in, tokens out. Knows nothing about engines or routing,
so it can be reused by every mode and tested on its own.

NUMBERS mode: split on ANY whitespace (spaces AND newlines). Commas are left
ATTACHED to their token on purpose -- cleaning commas is Input.py's job.

    "16\n65, 72, 62\n516 8\n18, Cat, 5"
        ->  ["16", "65,", "72,", "62", "516", "8", "18,", "Cat,", "5"]
"""


def tokenize(text, mode="numbers"):
    """Split raw text into a list of string tokens for the given mode."""
    if mode == "numbers":
        return _tokenize_numbers(text)
    raise ValueError(f"Tokenizer has no rule for mode: {mode!r}")


def _tokenize_numbers(text):
    # str.split() with no argument splits on runs of any whitespace and
    # drops empty pieces -- exactly the behaviour we want here.
    return text.split()
