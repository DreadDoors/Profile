"""
MPHEAW - Engines/Error.py

The SINGLE home for all error definitions and messages. No other file holds
error message text. Engines detect a problem and RAISE one of these classes;
the GUI catches it and shows it via GUI/Popups/Dialogue_Box.py.

Each error carries a .title (popup window title) and .message (popup body).
"""


class MPHEAWError(Exception):
    """Base for every MPHEAW error."""
    title = "Error"
    message = "Something went wrong."

    def __init__(self, message=None, title=None):
        if message is not None:
            self.message = message
        if title is not None:
            self.title = title
        super().__init__(self.message)


class NoChoiceError(MPHEAWError):
    title = "No option selected"
    message = "Please select at least one option before pressing Next."


class NoNumbersError(MPHEAWError):
    title = "No numbers"
    message = "No whole numbers were found in your input."


class SingleNumberError(MPHEAWError):
    title = "Not enough numbers"
    message = "Only one number was given. Please enter at least two."


class OverloadError(MPHEAWError):
    title = "Too many numbers"

    def __init__(self, count, limit):
        super().__init__(
            message=f"Too many numbers ({count}). The current limit is {limit}."
        )


class UnexpectedTokenError(MPHEAWError):
    """Safety net: a non-number value reached the number engine."""
    title = "Unexpected value"

    def __init__(self, token):
        super().__init__(
            message=f"An unexpected non-number value reached the calculator: {token!r}."
        )
