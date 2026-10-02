"""Knowledge base: every intent the bot understands, stored as plain data.

The project brief calls a long if-elif ladder an anti-pattern and recommends a
dictionary instead. So *what* the bot knows lives here, and *how* it decides
lives in ``chatbot.py``. Adding a new intent means editing this file only.

Each intent has:

* ``patterns``           - phrases that trigger it (sanitized automatically)
* ``responses``          - reply templates; one is chosen at random
* ``personal_responses`` - optional replies used once the user's name is known
* ``match``              - how patterns are compared (default ``"keyword"``):
    - ``"keyword"`` - the phrase appears anywhere in the message, as whole words
    - ``"exact"``   - the whole message must equal the phrase
    - ``"prefix"``  - the message must start with the phrase

Templates may use ``{bot}``, ``{name}``, ``{time}`` and ``{date}``.
"""

from chatbot.preprocessor import sanitize

BOT_NAME = "Nova"

INTENTS: dict[str, dict] = {
    "greeting": {
        "patterns": [
            "hi", "hello", "hey", "hiya", "howdy", "greetings", "namaste", "yo",
            "hi there", "hello there", "hey there",
            "good morning", "good afternoon", "good evening",
        ],
        "responses": [
            "Hello! I'm {bot}. How can I help you today?",
            "Hi there! Nice to see you. Type 'help' to see what I can do.",
            "Hey! I'm {bot}, your rule-based assistant. What's on your mind?",
        ],
        "personal_responses": [
            "Hello again, {name}! What can I do for you?",
            "Hi {name}! Good to see you.",
        ],
    },
    "farewell": {
        "match": "exact",
        "patterns": [
            "bye", "bye bye", "goodbye", "good bye", "exit", "quit",
            "see you", "see you later", "see ya", "farewell",
        ],
        "responses": [
            "Goodbye! Thanks for chatting with me.",
            "See you later! Have a great day.",
        ],
        "personal_responses": [
            "Goodbye, {name}! Thanks for chatting with me.",
            "See you later, {name}! Have a great day.",
        ],
    },
    "how_are_you": {
        "patterns": [
            "how are you", "how are you doing", "how r u", "hows it going",
            "how do you do", "whats up", "how have you been",
        ],
        "responses": [
            "I'm running smoothly - all my rules are in order! How about you?",
            "Doing great, thanks for asking! How are you?",
        ],
    },
    "mood_positive": {
        "patterns": [
            "im good", "im fine", "im great", "im ok", "im okay", "im well",
            "i am good", "i am fine", "i am great", "i am ok", "i am okay",
            "i am well", "doing well", "doing good", "doing great", "not bad",
        ],
        "responses": [
            "Glad to hear it! What would you like to talk about?",
            "That's great! Let me know if there's anything I can do.",
        ],
    },
    "mood_negative": {
        "patterns": [
            "im sad", "im tired", "im bored", "im stressed", "im not good",
            "im not okay", "im not ok", "i am sad", "i am tired", "i am bored",
            "i am stressed", "i am not good", "not good", "not great",
            "feeling down",
        ],
        "responses": [
            "I'm sorry to hear that. Maybe a joke would help? Just say 'tell me a joke'.",
            "That sounds tough. Remember to take a break - you've earned it.",
        ],
    },
    "bot_identity": {
        "patterns": [
            "who are you", "what are you", "whats your name", "your name",
            "introduce yourself", "are you a bot", "are you human",
            "are you a robot",
        ],
        "responses": [
            "I'm {bot}, a rule-based chatbot. Every reply I give comes from "
            "explicit rules - no machine learning involved.",
            "My name is {bot}. I'm a rule-based AI: I match what you say "
            "against a knowledge base of predefined intents.",
        ],
    },
    "help": {
        "patterns": [
            "help", "what can you do", "commands", "options", "menu",
            "how does this work",
        ],
        "responses": [
            "Here's what I can do:\n"
            "  - Greet you:            'hi', 'good morning'\n"
            "  - Chat:                 'how are you?', 'who are you?'\n"
            "  - Remember your name:   'my name is Alex', 'what's my name?'\n"
            "  - Tell the time/date:   'what time is it?', 'what's the date?'\n"
            "  - Tell a joke:          'tell me a joke'\n"
            "  - Exit:                 'bye', 'exit' or 'quit'",
        ],
    },
    "thanks": {
        "patterns": [
            "thanks", "thank you", "thx", "ty", "thanks a lot",
            "appreciate it", "much appreciated",
        ],
        "responses": [
            "You're welcome!",
            "Happy to help!",
            "Anytime!",
        ],
        "personal_responses": [
            "You're welcome, {name}!",
            "Happy to help, {name}!",
        ],
    },
    "joke": {
        "patterns": [
            "joke", "jokes", "tell me a joke", "make me laugh",
            "something funny", "say something funny",
        ],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why was the if-statement so calm? It always had an else to fall back on.",
            "There are 10 types of people: those who understand binary and those who don't.",
            "A rule-based bot walks into a bar. The bartender asks what it'll have. "
            "It says: 'Sorry, I don't understand.'",
            "I told my computer I needed a break. It said: 'No problem - I'll go to sleep.'",
        ],
    },
    "time": {
        "patterns": [
            "what time is it", "whats the time", "what is the time",
            "current time", "time now", "tell me the time",
        ],
        "responses": [
            "It's {time} right now.",
            "The current time is {time}.",
        ],
    },
    "date": {
        "patterns": [
            "whats the date", "what is the date", "todays date",
            "what day is it", "what is today", "current date", "date today",
        ],
        "responses": [
            "Today is {date}.",
            "It's {date}.",
        ],
    },
    "name_intro": {
        "match": "prefix",
        "patterns": ["my name is", "call me", "i am called", "my names"],
        "responses": [
            "I didn't quite catch your name. Try 'my name is Alex'.",
        ],
        "personal_responses": [
            "Nice to meet you, {name}! I'll remember that.",
            "Got it - I'll call you {name}.",
        ],
    },
    "name_recall": {
        "patterns": [
            "whats my name", "what is my name", "who am i",
            "do you know my name", "do you remember my name",
        ],
        "responses": [
            "I don't know your name yet. Tell me with 'my name is ...'.",
        ],
        "personal_responses": [
            "Your name is {name}.",
            "You told me your name is {name}.",
        ],
    },
}

# Used by ``INTENTS.get(intent, FALLBACK)`` when no rule matches.
FALLBACK: dict = {
    "responses": [
        "Sorry, I don't understand that yet. Type 'help' to see what I can do.",
        "Hmm, that's not in my rulebook. Try 'help' for ideas.",
    ],
}

EMPTY_INPUT: dict = {
    "responses": [
        "You didn't type anything. Say 'hi', or type 'help' to get started.",
    ],
}

MATCH_TYPES = ("keyword", "exact", "prefix")


def build_indexes(intents: dict[str, dict]) -> dict[str, dict[str, str]]:
    """Build one ``pattern -> intent`` lookup dictionary per match type.

    Patterns are sanitized here, so they are compared in exactly the same form
    as user input. Raises ``ValueError`` for an unknown match type, an empty
    pattern, or a pattern claimed by two intents.
    """
    indexes: dict[str, dict[str, str]] = {kind: {} for kind in MATCH_TYPES}
    for intent, entry in intents.items():
        kind = entry.get("match", "keyword")
        if kind not in indexes:
            raise ValueError(f"Intent {intent!r} has unknown match type {kind!r}")
        for pattern in entry.get("patterns", []):
            clean = sanitize(pattern)
            if not clean:
                raise ValueError(f"Intent {intent!r} has an empty pattern")
            owner = indexes[kind].get(clean)
            if owner is not None and owner != intent:
                raise ValueError(
                    f"Pattern {clean!r} is used by both {owner!r} and {intent!r}"
                )
            indexes[kind][clean] = intent
    return indexes


_INDEXES = build_indexes(INTENTS)
KEYWORD_INDEX: dict[str, str] = _INDEXES["keyword"]
EXACT_INDEX: dict[str, str] = _INDEXES["exact"]
PREFIX_INDEX: dict[str, str] = _INDEXES["prefix"]

# Longest pattern length in words, so the matcher knows which n-grams to try.
MAX_KEYWORD_WORDS = max(len(p.split()) for p in KEYWORD_INDEX)
MAX_PREFIX_WORDS = max(len(p.split()) for p in PREFIX_INDEX)
