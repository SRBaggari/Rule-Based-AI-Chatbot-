"""One test per requirement in the DecodeLabs Project 1 brief.

* Key requirements: greetings and exit commands, if-else logic, continuous loop.
* Specification ("The Logic Skeleton"): input loop, sanitization, dictionary
  knowledge base with 5+ intents, fallback, clean exit.
"""

import ast
import inspect
import textwrap
import unittest

from chatbot import chatbot as chatbot_module
from chatbot import cli
from chatbot.chatbot import FALLBACK_INTENT, Chatbot
from chatbot.knowledge_base import INTENTS
from chatbot.preprocessor import sanitize


def function_tree(func) -> ast.AST:
    return ast.parse(textwrap.dedent(inspect.getsource(func)))


class KeyRequirementTests(unittest.TestCase):
    def test_handles_greetings(self):
        for text in ("hi", "Hello!", "good morning"):
            with self.subTest(text=text):
                self.assertEqual(Chatbot().respond(text).intent, "greeting")

    def test_handles_exit_commands(self):
        for text in ("bye", "exit", "quit"):
            with self.subTest(text=text):
                self.assertTrue(Chatbot().respond(text).should_exit)

    def test_uses_if_else_logic_for_responses(self):
        tree = function_tree(chatbot_module.Chatbot.respond)
        chains = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.If) and node.orelse
        ]
        self.assertTrue(chains, "respond() should contain an if/elif/else chain")


class LogicSkeletonSpecTests(unittest.TestCase):
    def test_input_loop_is_a_continuous_while_cycle(self):
        tree = function_tree(cli.run)
        loops = [
            node for node in ast.walk(tree)
            if isinstance(node, ast.While)
            and isinstance(node.test, ast.Constant) and node.test.value is True
        ]
        self.assertEqual(len(loops), 1, "run() should contain one 'while True' loop")

    def test_sanitization_handles_case_and_whitespace(self):
        self.assertEqual(sanitize("   HeLLo   "), "hello")

    def test_knowledge_base_is_a_dictionary_with_five_plus_intents(self):
        self.assertIsInstance(INTENTS, dict)
        self.assertGreaterEqual(len(INTENTS), 5)

    def test_fallback_for_unknown_input(self):
        reply = Chatbot().respond("qwerty uiop")
        self.assertEqual(reply.intent, FALLBACK_INTENT)
        self.assertTrue(reply.text)

    def test_exit_strategy_is_a_clean_break(self):
        tree = function_tree(cli.run)
        self.assertTrue(any(isinstance(node, ast.Break) for node in ast.walk(tree)))

        prompts = []

        def scripted_input(prompt):
            prompts.append(prompt)
            return "exit"

        cli.run(input_fn=scripted_input, output_fn=lambda *_: None)
        self.assertEqual(len(prompts), 1)


if __name__ == "__main__":
    unittest.main()
