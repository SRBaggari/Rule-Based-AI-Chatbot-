"""PROCESS stage: map sanitized text to an intent.

Matching is exact and deterministic - every step is a dictionary ``.get()``
lookup, never a scan through an if-elif ladder. Rules are tried in order:

1. **Exact**   - the whole message is a command such as ``"bye"`` or ``"exit"``.
2. **Prefix**  - the message starts with a phrase such as ``"my name is"``.
3. **Keyword** - a known phrase appears in the message as whole words. Longer
   phrases are tried first, so ``"how are you"`` beats ``"hello"`` in
   ``"hello how are you"``.
"""

from dataclasses import dataclass

from chatbot.knowledge_base import (
    EXACT_INDEX,
    KEYWORD_INDEX,
    MAX_KEYWORD_WORDS,
    MAX_PREFIX_WORDS,
    PREFIX_INDEX,
)
from chatbot.preprocessor import ngrams, tokenize

# Words that can't be part of a name. They end the name ("my name is alex and
# i like python" -> "Alex") or reject it entirely ("call me later" -> no name).
_NOT_NAME_WORDS = frozenset({
    "and", "but", "so", "or", "because", "from", "im", "i", "please",
    "a", "an", "the", "not", "later", "back", "maybe", "now", "soon",
    "tomorrow", "again", "anytime",
})
_MAX_NAME_WORDS = 3


@dataclass(frozen=True)
class Match:
    """The result of a successful rule match."""

    intent: str
    phrase: str  # the pattern that fired, for traceability
    rule: str    # "exact", "prefix" or "keyword"


def match_intent(clean_text: str) -> Match | None:
    """Return the intent for ``clean_text`` (already sanitized), or ``None``."""
    if not clean_text:
        return None

    intent = EXACT_INDEX.get(clean_text)
    if intent is not None:
        return Match(intent, clean_text, "exact")

    tokens = tokenize(clean_text)

    for n in range(min(MAX_PREFIX_WORDS, len(tokens)), 0, -1):
        prefix = " ".join(tokens[:n])
        intent = PREFIX_INDEX.get(prefix)
        if intent is not None:
            return Match(intent, prefix, "prefix")

    for n in range(min(MAX_KEYWORD_WORDS, len(tokens)), 0, -1):
        for phrase in ngrams(tokens, n):
            intent = KEYWORD_INDEX.get(phrase)
            if intent is not None:
                return Match(intent, phrase, "keyword")

    return None


def extract_name(clean_text: str, prefix: str) -> str | None:
    """Pull a name out of a message like ``"my name is alex"``.

    Takes up to three words after ``prefix`` and returns them title-cased. It
    stops at the first word that can't be part of a name (a joining word, a
    number, ...). Returns ``None`` if no valid name follows the prefix.

    >>> extract_name("my name is alex", "my name is")
    'Alex'
    >>> extract_name("call me mary jane and say hi", "call me")
    'Mary Jane'
    >>> extract_name("call me later", "call me") is None
    True
    """
    words = tokenize(clean_text)[len(prefix.split()):]
    name_words: list[str] = []
    for word in words:
        if len(name_words) == _MAX_NAME_WORDS:
            break
        if word in _NOT_NAME_WORDS or not word.isalpha():
            break
        name_words.append(word)
    return " ".join(name_words).title() if name_words else None
