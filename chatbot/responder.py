"""OUTPUT stage: turn an intent into a reply.

The lookup ``INTENTS.get(intent, FALLBACK)`` resolves the intent and falls
back to a default reply in a single step, as the project brief recommends.
"""

import random
from datetime import datetime

from chatbot.knowledge_base import BOT_NAME, FALLBACK, INTENTS


def format_time(now: datetime) -> str:
    """Return ``now`` as a 12-hour clock time, e.g. ``"3:05 PM"``."""
    return f"{now:%I:%M %p}".lstrip("0")


def format_date(now: datetime) -> str:
    """Return ``now`` as a readable date, e.g. ``"Friday, 2 October 2026"``."""
    return f"{now:%A}, {now.day} {now:%B %Y}"


def render(
    entry: dict,
    *,
    name: str | None = None,
    now: datetime | None = None,
    rng: random.Random | None = None,
) -> str:
    """Pick a template from a knowledge-base entry and fill in its placeholders.

    If the user's name is known and the entry has personalised replies, one of
    those is used instead of the general ones.
    """
    rng = rng or random.Random()
    now = now or datetime.now()

    if name is not None and entry.get("personal_responses"):
        templates = entry["personal_responses"]
    else:
        templates = entry["responses"]

    return rng.choice(templates).format(
        bot=BOT_NAME,
        name=name or "friend",
        time=format_time(now),
        date=format_date(now),
    )


def build_response(intent: str | None, **options) -> str:
    """Return a reply for ``intent``, or a fallback reply if it is unknown."""
    return render(INTENTS.get(intent, FALLBACK), **options)
