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
    avoid: str | None = None,
) -> str:
    """Pick a template from a knowledge-base entry and fill in its placeholders.

    If the user's name is known and the entry has personalised replies, one of
    those is used instead of the general ones. ``avoid`` is the previous reply:
    when there is another option, the bot won't say the same thing twice in a row.
    """
    rng = rng or random.Random()
    now = now or datetime.now()

    if name is not None and entry.get("personal_responses"):
        templates = entry["personal_responses"]
    else:
        templates = entry["responses"]

    replies = [
        template.format(
            bot=BOT_NAME,
            name=name or "friend",
            time=format_time(now),
            date=format_date(now),
        )
        for template in templates
    ]
    if avoid in replies and len(replies) > 1:
        replies.remove(avoid)
    return rng.choice(replies)


def build_response(
    intent: str | None,
    *,
    name: str | None = None,
    now: datetime | None = None,
    rng: random.Random | None = None,
    avoid: str | None = None,
) -> str:
    """Return a reply for ``intent``, or a fallback reply if it is unknown."""
    entry = INTENTS.get(intent, FALLBACK)
    return render(entry, name=name, now=now, rng=rng, avoid=avoid)
