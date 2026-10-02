import random
import unittest
from datetime import datetime

import main
from chatbot.chatbot import Chatbot
from chatbot.cli import BANNER, run
from chatbot.knowledge_base import BOT_NAME


class ScriptedConsole:
    """Feeds scripted lines to run() and records what it prints."""

    def __init__(self, lines: list):
        self._lines = iter(lines)
        self.prompts: list[str] = []
        self.output: list[str] = []

    def input(self, prompt: str) -> str:
        self.prompts.append(prompt)
        line = next(self._lines)
        if isinstance(line, BaseException):
            raise line
        return line

    def print(self, text: str = "") -> None:
        self.output.append(text)

    @property
    def bot_lines(self) -> list[str]:
        return [line for line in self.output if line.startswith(f"{BOT_NAME}: ")]


def run_script(lines: list, trace: bool = False) -> tuple[ScriptedConsole, Chatbot]:
    console = ScriptedConsole(lines)
    bot = Chatbot(rng=random.Random(0), clock=lambda: datetime(2026, 10, 2, 15, 5))
    run(trace=trace, bot=bot, input_fn=console.input, output_fn=console.print)
    return console, bot


class LoopTests(unittest.TestCase):
    def test_banner_is_shown_first(self):
        console, _ = run_script(["bye"])
        self.assertEqual(console.output[0], BANNER)

    def test_loop_runs_until_exit_command(self):
        console, bot = run_script(["hi", "how are you", "tell me a joke", "bye"])
        self.assertEqual(len(console.prompts), 4)
        self.assertEqual(len(console.bot_lines), 4)
        self.assertEqual(bot.session.turns, 4)

    def test_lines_after_exit_are_never_read(self):
        console, _ = run_script(["exit", "hello"])
        self.assertEqual(len(console.prompts), 1)

    def test_loop_survives_unknown_and_empty_input(self):
        console, _ = run_script(["", "asdfgh", "quit"])
        self.assertEqual(len(console.bot_lines), 3)

    def test_session_summary_is_printed(self):
        console, _ = run_script(["hi", "bye"])
        self.assertIn("Session ended after 2 message(s)", console.output[-1])


class CleanShutdownTests(unittest.TestCase):
    def test_ctrl_c_exits_cleanly(self):
        console, _ = run_script(["hi", KeyboardInterrupt()])
        self.assertEqual(len(console.bot_lines), 2)  # reply + goodbye
        self.assertIn("Session ended", console.output[-1])

    def test_end_of_input_exits_cleanly(self):
        console, _ = run_script([EOFError()])
        self.assertEqual(len(console.bot_lines), 1)


class TraceModeTests(unittest.TestCase):
    def test_trace_lines_shown_when_enabled(self):
        console, _ = run_script(["hello", "bye"], trace=True)
        traces = [line for line in console.output if "[trace]" in line]
        self.assertEqual(len(traces), 2)
        self.assertIn("intent=greeting", traces[0])
        self.assertIn("rule=exact", traces[1])

    def test_trace_hidden_by_default(self):
        console, _ = run_script(["hello", "bye"])
        self.assertFalse(any("[trace]" in line for line in console.output))


class MainArgsTests(unittest.TestCase):
    def test_trace_flag(self):
        self.assertTrue(main.parse_args(["--trace"]).trace)
        self.assertFalse(main.parse_args([]).trace)


if __name__ == "__main__":
    unittest.main()
