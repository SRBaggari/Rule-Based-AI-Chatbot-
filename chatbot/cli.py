"""The console interface: a continuous ``while`` loop that talks to the user.

This is the only module that reads input or prints output, so the rest of the
bot can be tested without a terminal.
"""

from collections.abc import Callable

from chatbot.chatbot import Chatbot, Reply
from chatbot.knowledge_base import BOT_NAME

BANNER = f"""\
==================================================
  {BOT_NAME} - Rule-Based AI Chatbot
  DecodeLabs AI Internship | Project 1
==================================================
Type 'help' to see what I can do, or 'bye' to exit.
"""


def format_trace(reply: Reply) -> str:
    """Describe how a reply was produced: Input -> Logic -> Output."""
    return (
        f"  [trace] input={reply.clean_input!r} -> "
        f"rule={reply.rule or 'none'} matched={reply.matched!r} -> "
        f"intent={reply.intent}"
    )


def run(
    trace: bool = False,
    bot: Chatbot | None = None,
    input_fn: Callable[[str], str] = input,
    output_fn: Callable[[str], None] = print,
) -> None:
    """Run the chat loop until the user exits."""
    bot = bot or Chatbot()
    output_fn(BANNER)

    while True:
        try:
            user_input = input_fn("You: ")
        except (KeyboardInterrupt, EOFError):
            # Ctrl+C or end of input: leave cleanly instead of crashing.
            output_fn("")
            output_fn(f"{BOT_NAME}: {bot.goodbye()}")
            break

        reply = bot.respond(user_input)
        if trace:
            output_fn(format_trace(reply))
        output_fn(f"{BOT_NAME}: {reply.text}")

        if reply.should_exit:
            break

    output_fn(f"\n(Session ended after {bot.session.turns} message(s).)")
