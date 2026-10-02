"""PROCESS stage: the decision logic that ties input, rules and output together.

The knowledge base (a dictionary) decides *what* to say. The short
if/elif/else chain in :meth:`Chatbot.respond` decides *what to do*:

    empty input   -> ask the user to type something
    no match      -> fallback reply (with examples after repeated misses)
    farewell      -> say goodbye and signal the loop to exit
    name intro    -> remember the user's name
    anything else -> look up the reply for the matched intent

The chain stays the same size however many intents the knowledge base holds.
"""

import random
from collections.abc import Callable
from dataclasses import dataclass
from datetime import datetime

from chatbot.intent_matcher import extract_name, match_intent
from chatbot.knowledge_base import EMPTY_INPUT, FALLBACK_REPEATED, SYMBOLS_ONLY
from chatbot.preprocessor import sanitize
from chatbot.responder import build_response, render

FALLBACK_INTENT = "fallback"
EMPTY_INTENT = "empty"
MISSES_BEFORE_EXAMPLES = 2


@dataclass
class Session:
    """What the bot remembers during one conversation."""

    name: str | None = None
    turns: int = 0              # messages that contained words
    misses: int = 0             # unrecognised messages in a row
    last_reply: str | None = None


@dataclass(frozen=True)
class Reply:
    """The bot's answer plus the trace of how it was produced."""

    text: str
    intent: str
    clean_input: str
    matched: str | None = None
    rule: str | None = None
    should_exit: bool = False


class Chatbot:
    """A rule-based chatbot. Holds session state; performs no I/O."""

    def __init__(
        self,
        rng: random.Random | None = None,
        clock: Callable[[], datetime] = datetime.now,
    ) -> None:
        self.session = Session()
        self._rng = rng or random.Random()
        self._clock = clock

    def respond(self, raw_input: str) -> Reply:
        """Return the reply to one message from the user."""
        clean = sanitize(raw_input)
        match = match_intent(clean)
        should_exit = False

        if not clean:
            # A blank line and a line of only symbols ("?!") get different hints.
            entry = SYMBOLS_ONLY if raw_input.strip() else EMPTY_INPUT
            intent, text = EMPTY_INTENT, self._render(entry)
        elif match is None:
            self.session.misses += 1
            if self.session.misses >= MISSES_BEFORE_EXAMPLES:
                intent, text = FALLBACK_INTENT, self._render(FALLBACK_REPEATED)
            else:
                intent, text = FALLBACK_INTENT, self._say(FALLBACK_INTENT)
        elif match.intent == "farewell":
            intent, text = "farewell", self._say("farewell", self.session.name)
            should_exit = True
        elif match.intent == "name_intro":
            name = extract_name(clean, match.phrase)
            if name is not None:
                self.session.name = name
            intent, text = "name_intro", self._say("name_intro", name)
        else:
            intent, text = match.intent, self._say(match.intent, self.session.name)

        if clean:
            self.session.turns += 1
        if match is not None:
            self.session.misses = 0
        self.session.last_reply = text

        return Reply(
            text=text,
            intent=intent,
            clean_input=clean,
            matched=match.phrase if match else None,
            rule=match.rule if match else None,
            should_exit=should_exit,
        )

    def goodbye(self) -> str:
        """Return a farewell for when the user leaves without typing 'bye'."""
        return self._say("farewell", self.session.name)

    def _say(self, intent: str, name: str | None = None) -> str:
        """Reply for an intent; unknown intents fall back to a default reply."""
        return build_response(
            intent,
            name=name,
            now=self._clock(),
            rng=self._rng,
            avoid=self.session.last_reply,
        )

    def _render(self, entry: dict) -> str:
        """Reply for a special entry that isn't an intent (empty input, etc.)."""
        return render(entry, rng=self._rng, avoid=self.session.last_reply)
