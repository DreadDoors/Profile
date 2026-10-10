"""
MPHEAW - Engines/Number.py

The Number engine. It receives a list of whole numbers and the chosen options,
and returns the results. It assumes Choice.py already removed any junk; as a
safety net, if a non-number ever slips through, it raises UnexpectedTokenError
(defined in Engines/Error.py).

Active options:
    "Ascending Order"  -> list sorted low to high
    "Descending Order" -> list sorted high to low
    "Greatest Number"  -> the maximum
    "Smallest Number"  -> the minimum
"""

try:
    from Engines.Error import UnexpectedTokenError
except ImportError:
    from .Error import UnexpectedTokenError


class NumberEngine:
    def run(self, numbers, choices):
        # Safety net: the engine should only ever see whole numbers.
        for n in numbers:
            if not isinstance(n, int):
                raise UnexpectedTokenError(n)

        results = {}
        for choice in choices:
            if choice == "Ascending Order":
                results[choice] = sorted(numbers)
            elif choice == "Descending Order":
                results[choice] = sorted(numbers, reverse=True)
            elif choice == "Greatest Number":
                results[choice] = max(numbers)
            elif choice == "Smallest Number":
                results[choice] = min(numbers)
            # Unknown / not-yet-built options are ignored for now.
        return results
