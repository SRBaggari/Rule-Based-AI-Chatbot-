"""PROCESS stage: the decision logic that ties input, rules and output together.

The knowledge base (a dictionary) decides *what* to say. The short
if/elif/else chain in :meth:`Chatbot.respond` decides *what to do*:

    empty input  -> ask the user to type something
    no match     -> fallback reply
    farewell     -> say goodbye and signal the loop to exit
    name intro   -> remember the user's name
    anything else-> look up the reply for the matched intent

The chain stays the same size however many intents the knowledge base holds.
"""

import random
from dataclasses import dataclass
from datetime import datetime
from typing import Callable

from chatbot.intent_matcher import Match, extract_name, match_intent
from chatbot.knowledge_base import EMPTY_INPUT
from chatbot.preprocessor import sanitize
from chatbot.responder import build_response, render

FALLBACK_INTENT = "fallback"
EMPTY_INTENT = "empty"


@dataclass
class Session:
    """What the bot remembers during one conversation."""

    name: str | None = None
    turns: int = 0


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
        if clean:
            self.session.turns += 1

        if not clean:
            text = render(EMPTY_INPUT, rng=self._rng)
            return self._reply(EMPTY_INTENT, clean, None, text)
        elif match is None:
            text = self._say(FALLBACK_INTENT)
            return self._reply(FALLBACK_INTENT, clean, None, text)
        elif match.intent == "farewell":
            text = self._say("farewell", name=self.session.name)
            return self._reply("farewell", clean, match, text, should_exit=True)
        elif match.intent == "name_intro":
            name = extract_name(clean, match.phrase)
            if name is not None:
                self.session.name = name
            text = self._say("name_intro", name=name)
            return self._reply("name_intro", clean, match, text)
        else:
            text = self._say(match.intent, name=self.session.name)
            return self._reply(match.intent, clean, match, text)

    def goodbye(self) -> str:
        """Return a farewell for when the user leaves without typing 'bye'."""
        return self._say("farewell", name=self.session.name)

    def _say(self, intent: str, name: str | None = None) -> str:
        return build_response(intent, name=name, now=self._clock(), rng=self._rng)

    @staticmethod
    def _reply(
        intent: str,
        clean: str,
        match: Match | None,
        text: str,
        should_exit: bool = False,
    ) -> Reply:
        return Reply(
            text=text,
            intent=intent,
            clean_input=clean,
            matched=match.phrase if match else None,
            rule=match.rule if match else None,
            should_exit=should_exit,
        )
