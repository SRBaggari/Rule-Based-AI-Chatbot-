# Sample Conversation

A real session recorded from the chatbot. Replies are picked at random from
each intent's templates, so wording can differ between runs.

```text
==================================================
  Nova - Rule-Based AI Chatbot
  DecodeLabs AI Internship | Project 1
==================================================
Hi! I'm Nova. I reply using predefined rules, not machine learning.

  Try:  'hello'   'how are you?'   'what time is it?'
        'tell me a joke'   'my name is Alex'

Type 'help' to see everything I understand, or 'bye' to exit.

You: Hello!
Nova: Hey! I'm Nova, your rule-based assistant. What's on your mind?
You: how are u?
Nova: Doing great, thanks for asking! How are you?
You: I'm good
Nova: Glad to hear it! What would you like to talk about?
You: who made you?
Nova: I was built by srbaggari as Project 1 of the DecodeLabs Artificial Intelligence Internship.
You: my name is Alex
Nova: Nice to meet you, Alex! I'll remember that.
You: what time is it?
Nova: The current time is 3:16 PM.
You: what's the date today
Nova: Today is Friday, 2 October 2026.
You: tell me a joke
Nova: Why do programmers prefer dark mode? Because light attracts bugs.
You: lol
Nova: Glad that made you smile!
You: what's my name
Nova: You told me your name is Alex.
You:
Nova: You didn't type anything. Say 'hi', or type 'help' to get started.
You: asdf
Nova: Hmm, that's not in my rulebook. Try 'help' for ideas.
You: what is the capital of France
Nova: I'm still not following, sorry. I only understand predefined phrases.
  Try one of these: 'hello', 'how are you?', 'what time is it?', 'tell me a joke', or 'help' for the full list.
You: help
Nova: Here's what I understand:
  - Greetings:      'hi', 'good morning'
  - Small talk:     'how are you?', 'I'm good', 'sorry'
  - About me:       'who are you?', 'who made you?', 'how do you work?'
  - Your name:      'my name is Alex', 'what's my name?'
  - Time and date:  'what time is it?', 'what's the date?'
  - Fun:            'tell me a joke'
  - Exit:           'bye', 'exit' or 'quit'
You: thanks
Nova: You're welcome, Alex!
You: ok bye
Nova: Goodbye, Alex! Thanks for chatting with me.

(Session ended after 15 messages.)
```

## Trace mode

`python main.py --trace` shows which rule produced each reply, so every
answer can be traced from input to output:

```text
You: Hi there
  [trace] input='hi there' -> rule=keyword matched='hi there' -> intent=greeting
Nova: Hey! I'm Nova, your rule-based assistant. What's on your mind?
You: I will not quit
  [trace] input='i will not quit' -> rule=keyword matched='quit' -> intent=exit_hint
Nova: If you'd like to leave, just type 'bye' on its own.
You: call me later
  [trace] input='call me later' -> rule=prefix matched='call me' -> intent=name_intro
Nova: I didn't quite catch your name. Try 'my name is Alex'.
You: ?
  [trace] input='' -> rule=none matched=None -> intent=empty
Nova: I can only read words, not symbols. Try 'hi', or type 'help'.
You: exit
  [trace] input='exit' -> rule=exact matched='exit' -> intent=farewell
Nova: See you later! Have a great day.

(Session ended after 4 messages.)
```

- *"I will not quit"* contains the word *quit*, but exit commands must match the
  whole message, so the bot explains how to leave instead of exiting.
- *"call me later"* starts like a name introduction, but *"later"* is not
  accepted as a name.
