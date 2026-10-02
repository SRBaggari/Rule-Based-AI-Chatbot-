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
_BOT = BOT_NAME.lower()

INTENTS: dict[str, dict] = {
    # --- Conversation basics -------------------------------------------------
    "greeting": {
        "patterns": [
            "hi", "hii", "hello", "hey", "heya", "hiya", "howdy", "greetings",
            "namaste", "yo", "sup", "hi there", "hello there", "hey there",
            "good morning", "good afternoon", "good evening", "good day", _BOT,
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
        # Exact match only, so a sentence like "I will not quit" never ends the chat.
        "match": "exact",
        "patterns": [
            "bye", "bye bye", "goodbye", "good bye", "exit", "quit", "stop",
            "see you", "see you later", "see you soon", "see ya", "farewell",
            "later", "catch you later", "talk to you later", "ttyl",
            "good night", "goodnight", "ok bye", "okay bye", "bye for now",
            "bye then", "thanks bye", "thank you bye", "ok goodbye",
            "i have to go", "i need to go", "i gotta go", "gotta go",
            "im leaving", "im done", "thats all",
            f"bye {_BOT}", f"goodbye {_BOT}", f"see you {_BOT}",
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
    "exit_hint": {
        # An exit word inside a longer sentence: explain how to leave instead.
        "patterns": ["bye", "goodbye", "exit", "quit"],
        "responses": [
            "If you'd like to leave, just type 'bye' on its own.",
        ],
    },
    "help": {
        "patterns": [
            "help", "what can you do", "what do you do", "what can i ask",
            "what can i say", "what do you know", "commands", "options", "menu",
            "how does this work", "how do i use this", "show commands",
        ],
        "responses": [
            "Here's what I understand:\n"
            "  - Greetings:      'hi', 'good morning'\n"
            "  - Small talk:     'how are you?', 'I'm good', 'sorry'\n"
            "  - About me:       'who are you?', 'who made you?', 'how do you work?'\n"
            "  - Your name:      'my name is Alex', 'what's my name?'\n"
            "  - Time and date:  'what time is it?', 'what's the date?'\n"
            "  - Fun:            'tell me a joke'\n"
            "  - Exit:           'bye', 'exit' or 'quit'",
        ],
    },
    "thanks": {
        "patterns": [
            "thanks", "thank you", "thank u", "thx", "ty", "cheers",
            "thanks a lot", "many thanks", "appreciate it", "much appreciated",
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
    "acknowledgement": {
        "patterns": [
            "ok", "okay", "alright", "cool", "nice", "great", "sure", "yes",
            "yeah", "no", "nope", "got it", "i see", "makes sense",
        ],
        "responses": [
            "Okay! Anything else I can help with?",
            "Got it. What would you like to do next?",
        ],
    },
    # --- Small talk ----------------------------------------------------------
    "how_are_you": {
        "patterns": [
            "how are you", "how are you doing", "how are u", "how r u",
            "how r you", "how you doing", "hows it going", "how is it going",
            "how do you do", "whats up", "how have you been", "how are things",
            "hows your day", "how is your day", "are you ok", "are you okay",
        ],
        "responses": [
            "I'm running smoothly - all my rules are in order! How about you?",
            "Doing great, thanks for asking! How are you?",
        ],
    },
    "mood_positive": {
        "patterns": [
            "im good", "im fine", "im great", "im ok", "im okay", "im well",
            "im happy", "im fantastic", "i am good", "i am fine", "i am great",
            "i am ok", "i am okay", "i am well", "i am happy", "doing well",
            "doing good", "doing great", "not bad", "all good", "pretty good",
        ],
        "responses": [
            "Glad to hear it! What would you like to talk about?",
            "That's great! Let me know if there's anything I can do.",
        ],
    },
    "mood_negative": {
        "patterns": [
            "im sad", "im tired", "im bored", "im stressed", "im upset",
            "im unhappy", "im lonely", "im not good", "im not okay", "im not ok",
            "im not well", "i am sad", "i am tired", "i am bored",
            "i am stressed", "i am upset", "i am not good", "i am not well",
            "not good", "not great", "not so good", "feeling down", "bad day",
        ],
        "responses": [
            "I'm sorry to hear that. Maybe a joke would help? "
            "Just say 'tell me a joke'.",
            "That sounds tough. Remember to take a break - you've earned it.",
        ],
    },
    "compliment": {
        "patterns": [
            "you are smart", "youre smart", "you are awesome", "youre awesome",
            "you are great", "youre great", "you are cool", "youre cool",
            "good bot", "nice bot", "good job", "nice job", "well done",
            "i like you",
        ],
        "responses": [
            "Thank you! My rules and I appreciate it.",
            "That's kind of you to say!",
        ],
    },
    "criticism": {
        "patterns": [
            "you are stupid", "youre stupid", "you are dumb", "youre dumb",
            "you are useless", "youre useless", "you suck", "bad bot",
            "stupid bot",
        ],
        "responses": [
            "Sorry I couldn't help. I only know my predefined rules - "
            "type 'help' to see what I understand.",
        ],
    },
    "apology": {
        "patterns": ["sorry", "my bad", "i apologize", "apologies"],
        "responses": [
            "No problem at all!",
            "No worries!",
        ],
    },
    "laughter": {
        "patterns": ["lol", "haha", "hahaha", "lmao", "that was funny", "so funny"],
        "responses": [
            "Glad that made you smile!",
            "Ha! Want another one? Say 'tell me a joke'.",
        ],
    },
    "joke": {
        "patterns": [
            "joke", "jokes", "tell me a joke", "another joke", "one more joke",
            "tell me another one", "make me laugh", "something funny",
            "say something funny",
        ],
        "responses": [
            "Why do programmers prefer dark mode? Because light attracts bugs.",
            "Why was the if-statement so calm? It always had an else to fall back on.",
            "There are 10 types of people: those who understand binary "
            "and those who don't.",
            "A rule-based bot walks into a bar. The bartender asks what it'll have. "
            "It says: 'Sorry, I don't understand.'",
            "I told my computer I needed a break. "
            "It said: 'No problem - I'll go to sleep.'",
            "How many programmers does it take to change a light bulb? "
            "None - that's a hardware problem.",
            "Why don't programmers like nature? It has too many bugs.",
        ],
    },
    # --- About the bot -------------------------------------------------------
    "bot_identity": {
        "patterns": [
            "who are you", "what are you", "whats your name", "your name",
            "introduce yourself", "tell me about yourself", "are you a bot",
            "are you human", "are you a robot", "are you real",
            "what should i call you",
        ],
        "responses": [
            "I'm {bot}, a rule-based chatbot. Every reply I give comes from "
            "explicit rules - no machine learning involved.",
            "My name is {bot}. I'm a rule-based AI: I match what you say "
            "against a knowledge base of predefined intents.",
        ],
    },
    "creator": {
        "patterns": [
            "who made you", "who created you", "who built you", "who wrote you",
            "who programmed you", "who developed you", "who is your creator",
        ],
        "responses": [
            "I was built by srbaggari as Project 1 of the DecodeLabs "
            "Artificial Intelligence Internship.",
        ],
    },
    "bot_age": {
        "patterns": [
            "how old are you", "your age", "whats your age", "when were you born",
        ],
        "responses": [
            "I'm brand new - I was created in 2026 as an internship project.",
        ],
    },
    "how_it_works": {
        "patterns": [
            "how do you work", "how do you understand me", "rule based",
            "what is ai", "what is artificial intelligence", "are you smart",
            "are you intelligent", "do you learn", "can you learn",
        ],
        "responses": [
            "I'm a rule-based AI. I clean up your message, look up its words "
            "in a dictionary of known phrases, and reply with the answer linked "
            "to that phrase. I don't learn - every rule was written by hand.",
            "AI is about making machines act intelligently. I do it the "
            "classic way: with explicit if-then rules instead of machine "
            "learning, so every answer I give can be traced to a rule.",
        ],
    },
    # --- Utilities -----------------------------------------------------------
    "time": {
        "patterns": [
            "what time is it", "whats the time", "what is the time",
            "current time", "time now", "tell me the time", "time please",
            "do you know the time",
        ],
        "responses": [
            "It's {time} right now.",
            "The current time is {time}.",
        ],
    },
    "date": {
        "patterns": [
            "whats the date", "what is the date", "todays date", "what date is it",
            "what day is it", "which day is it", "what is today", "current date",
            "date today", "date please",
        ],
        "responses": [
            "Today is {date}.",
            "It's {date}.",
        ],
    },
    "weather": {
        "patterns": [
            "weather", "is it raining", "will it rain", "temperature",
            "how hot is it", "how cold is it",
        ],
        "responses": [
            "I can't check the weather - I don't connect to the internet, "
            "I only know my rules. Try a weather app!",
        ],
    },
    # --- Name memory ---------------------------------------------------------
    "name_intro": {
        "match": "prefix",
        "patterns": [
            "my name is", "my names", "call me", "you can call me", "i am called",
        ],
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
            "whats my name", "what is my name", "who am i", "say my name",
            "do you know my name", "do you remember my name",
            "do you know who i am",
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

# Used instead of FALLBACK when the user has been misunderstood several times in a row.
FALLBACK_REPEATED: dict = {
    "responses": [
        "I'm still not following, sorry. I only understand predefined phrases.\n"
        "  Try one of these: 'hello', 'how are you?', 'what time is it?', "
        "'tell me a joke', or 'help' for the full list.",
    ],
}

EMPTY_INPUT: dict = {
    "responses": [
        "You didn't type anything. Say 'hi', or type 'help' to get started.",
    ],
}

SYMBOLS_ONLY: dict = {
    "responses": [
        "I can only read words, not symbols. Try 'hi', or type 'help'.",
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
