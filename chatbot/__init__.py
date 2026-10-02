"""Nova - a rule-based AI chatbot (DecodeLabs AI Internship, Project 1).

The package follows the Input -> Process -> Output (IPO) model:

* ``preprocessor``   - INPUT:   sanitize and tokenize raw user text
* ``intent_matcher`` - PROCESS: map clean text to an intent via dictionary lookups
* ``chatbot``        - PROCESS: if/elif/else decision logic and session state
* ``responder``      - OUTPUT:  turn an intent into a reply
* ``cli``            - the continuous ``while`` loop that talks to the user
"""

__version__ = "1.0.0"
