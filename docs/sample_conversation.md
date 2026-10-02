# Sample Conversation

A real session recorded with `python main.py`. Replies are picked at random
from each intent's templates, so wording can differ between runs.

```text
==================================================
  Nova - Rule-Based AI Chatbot
  DecodeLabs AI Internship | Project 1
==================================================
Type 'help' to see what I can do, or 'bye' to exit.

You: Hello!
Nova: Hello! I'm Nova. How can I help you today?
You: how are you?
Nova: I'm running smoothly - all my rules are in order! How about you?
You: I am good
Nova: Glad to hear it! What would you like to talk about?
You: my name is Alex
Nova: Nice to meet you, Alex! I'll remember that.
You: what time is it?
Nova: It's 3:02 PM right now.
You: what is the date today
Nova: Today is Friday, 2 October 2026.
You: tell me a joke
Nova: There are 10 types of people: those who understand binary and those who don't.
You: what is my name
Nova: Your name is Alex.
You: who are you
Nova: My name is Nova. I'm a rule-based AI: I match what you say against a knowledge base of predefined intents.
You:
Nova: You didn't type anything. Say 'hi', or type 'help' to get started.
You: what is the capital of France
Nova: Sorry, I don't understand that yet. Type 'help' to see what I can do.
You: help
Nova: Here's what I can do:
  - Greet you:            'hi', 'good morning'
  - Chat:                 'how are you?', 'who are you?'
  - Remember your name:   'my name is Alex', 'what's my name?'
  - Tell the time/date:   'what time is it?', 'what's the date?'
  - Tell a joke:          'tell me a joke'
  - Exit:                 'bye', 'exit' or 'quit'
You: thanks
Nova: Happy to help, Alex!
You: bye
Nova: Goodbye, Alex! Thanks for chatting with me.

(Session ended after 13 message(s).)
```

## Trace mode

`python main.py --trace` shows which rule produced each reply, so every
answer can be traced from input to output:

```text
You: Hi there
  [trace] input='hi there' -> rule=keyword matched='hi there' -> intent=greeting
Nova: Hey! I'm Nova, your rule-based assistant. What's on your mind?
You: I will not quit
  [trace] input='i will not quit' -> rule=none matched=None -> intent=fallback
Nova: Hmm, that's not in my rulebook. Try 'help' for ideas.
You: exit
  [trace] input='exit' -> rule=exact matched='exit' -> intent=farewell
Nova: See you later! Have a great day.

(Session ended after 3 message(s).)
```

"I will not quit" contains the word *quit* but does not end the session,
because exit commands must match the whole message.
