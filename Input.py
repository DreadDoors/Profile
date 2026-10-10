"""
MPHEAW - Engines/Input.py

The Input engine. It takes what the GUI collected (raw text, mode, chosen
options), runs it through the Tokenizer, then CLEANS each token -- stripping
stray commas (e.g. "65," -> "65", "Cat," -> "Cat"). It packs the cleaned
tokens into an InputResult for Choice.py to route.

It does NOT validate numbers or raise errors. Deciding what counts as a number
(and discarding junk like "Cat") is Choice.py's job; all error messages live in
Engines/Error.py.
"""

from dataclasses import dataclass, field

try:
    from Modules.Tokenizer import tokenize
except ImportError:
    from ..Modules.Tokenizer import tokenize


@dataclass
class InputRequest:
    """What the GUI sends in."""
    raw_text: str
    mode: str = "numbers"
    choices: list = field(default_factory=list)
    extra: dict = field(default_factory=dict)


@dataclass
class InputResult:
    """What Input.py hands to Choice.py."""
    mode: str
    choices: list
    tokens: list          # cleaned string tokens
    extra: dict = field(default_factory=dict)


class InputEngine:
    def process(self, request):
        raw_tokens = tokenize(request.raw_text, request.mode)
        cleaned = [self._clean(t) for t in raw_tokens]
        cleaned = [t for t in cleaned if t]   # drop anything that became empty
        return InputResult(request.mode, request.choices, cleaned, request.extra)

    @staticmethod
    def _clean(token):
        """Strip stray commas around a token."""
        return token.strip(",").strip()
