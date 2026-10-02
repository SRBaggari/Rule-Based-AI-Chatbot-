"""INPUT stage: sanitize and tokenize raw user text.

Every string that is compared - user input *and* knowledge-base patterns -
passes through :func:`sanitize`, so both sides are always in the same form.
"""

import re

# Apostrophes are removed outright so contractions stay one word ("what's" -> "whats").
_APOSTROPHES = re.compile(r"['‘’`]")
# Any other punctuation or symbol becomes a space ("hi,there" -> "hi there").
_PUNCTUATION = re.compile(r"[^\w\s]|_")


def sanitize(text: str) -> str:
    """Normalize case, punctuation and whitespace.

    >>> sanitize("  HeLLo,   World!!! ")
    'hello world'
    >>> sanitize("What's up?")
    'whats up'
    """
    text = text.lower().strip()
    text = _APOSTROPHES.sub("", text)
    text = _PUNCTUATION.sub(" ", text)
    return " ".join(text.split())


def tokenize(clean_text: str) -> list[str]:
    """Split sanitized text into words."""
    return clean_text.split()


def ngrams(tokens: list[str], n: int) -> list[str]:
    """Return every run of ``n`` consecutive tokens, joined by spaces.

    >>> ngrams(["how", "are", "you"], 2)
    ['how are', 'are you']
    """
    if n <= 0:
        return []
    return [" ".join(tokens[i:i + n]) for i in range(len(tokens) - n + 1)]
