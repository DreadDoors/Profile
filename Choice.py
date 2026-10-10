"""
MPHEAW - Engines/Choice.py

The router. It takes the cleaned tokens from Input.py, decides which engine to
use (numbers for now), separates real numbers from junk like "Cat" (the junk is
silently dropped), checks the basics, then sends the clean numbers to the right
engine.

It raises errors from Engines/Error.py when something is wrong; it never holds
error message text of its own.
"""

try:
    from Engines.Number import NumberEngine
    from Engines.Error import (
        NoChoiceError,
        NoNumbersError,
        SingleNumberError,
        OverloadError,
    )
except ImportError:
    from .Number import NumberEngine
    from .Error import (
        NoChoiceError,
        NoNumbersError,
        SingleNumberError,
        OverloadError,
    )

MAX_NUMBERS = 100_000


class ChoiceEngine:
    def __init__(self):
        self.number_engine = NumberEngine()

    def route(self, input_result):
        if input_result.mode == "numbers":
            return self._route_numbers(input_result)
        # Other modes are not built yet.
        raise NoChoiceError(
            message=f"Mode '{input_result.mode}' is not available yet.",
            title="Unavailable mode",
        )

    def _route_numbers(self, input_result):
        if not input_result.choices:
            raise NoChoiceError()

        numbers, ignored = self._split_numbers(input_result.tokens)

        if len(numbers) == 0:
            raise NoNumbersError()
        if len(numbers) == 1:
            raise SingleNumberError()
        if len(numbers) > MAX_NUMBERS:
            raise OverloadError(len(numbers), MAX_NUMBERS)

        results = self.number_engine.run(numbers, input_result.choices)
        return {"results": results, "numbers": numbers, "ignored": ignored}

    @staticmethod
    def _split_numbers(tokens):
        """Return (whole_numbers, ignored_tokens). Junk is dropped here."""
        numbers, ignored = [], []
        for token in tokens:
            body = token[1:] if token.startswith("-") else token
            if body.isdigit():
                numbers.append(int(token))
            else:
                ignored.append(token)
        return numbers, ignored
