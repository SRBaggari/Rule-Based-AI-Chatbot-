import random
import unittest
from datetime import datetime

from chatbot.chatbot import EMPTY_INTENT, FALLBACK_INTENT, Chatbot
from chatbot.knowledge_base import EMPTY_INPUT, FALLBACK, INTENTS


def make_bot() -> Chatbot:
    return Chatbot(rng=random.Random(0), clock=lambda: datetime(2026, 10, 2, 15, 5))


class DecisionBranchTests(unittest.TestCase):
    """One test per branch of the if/elif/else chain in Chatbot.respond()."""

    def setUp(self):
        self.bot = make_bot()

    def test_empty_input_branch(self):
        for text in ("", "   ", "?!"):
            with self.subTest(text=text):
                reply = self.bot.respond(text)
                self.assertEqual(reply.intent, EMPTY_INTENT)
                self.assertIn(reply.text, EMPTY_INPUT["responses"])
                self.assertFalse(reply.should_exit)

    def test_fallback_branch(self):
        reply = self.bot.respond("purple elephants dance")
        self.assertEqual(reply.intent, FALLBACK_INTENT)
        self.assertIn(reply.text, FALLBACK["responses"])
        self.assertIsNone(reply.matched)
        self.assertFalse(reply.should_exit)

    def test_farewell_branch_signals_exit(self):
        reply = self.bot.respond("Bye!")
        self.assertEqual(reply.intent, "farewell")
        self.assertTrue(reply.should_exit)

    def test_name_intro_branch_stores_name(self):
        reply = self.bot.respond("My name is Alex")
        self.assertEqual(reply.intent, "name_intro")
        self.assertEqual(self.bot.session.name, "Alex")
        self.assertIn("Alex", reply.text)

    def test_name_intro_without_name(self):
        reply = self.bot.respond("my name is")
        self.assertIsNone(self.bot.session.name)
        self.assertIn(reply.text, INTENTS["name_intro"]["responses"])

    def test_matched_intent_branch(self):
        reply = self.bot.respond("tell me a joke")
        self.assertEqual(reply.intent, "joke")
        self.assertIn(reply.text, INTENTS["joke"]["responses"])
        self.assertFalse(reply.should_exit)


class OnlyFarewellExitsTests(unittest.TestCase):
    def test_no_other_intent_sets_should_exit(self):
        bot = make_bot()
        for intent, entry in INTENTS.items():
            if intent == "farewell":
                continue
            for pattern in entry["patterns"]:
                with self.subTest(pattern=pattern):
                    self.assertFalse(bot.respond(pattern).should_exit)


class SessionTests(unittest.TestCase):
    def setUp(self):
        self.bot = make_bot()

    def test_name_is_remembered(self):
        self.bot.respond("call me Sam")
        self.assertIn("Sam", self.bot.respond("what's my name?").text)

    def test_name_recall_before_intro(self):
        reply = self.bot.respond("what is my name")
        self.assertIn(reply.text, INTENTS["name_recall"]["responses"])

    def test_greeting_is_personalised_once_name_known(self):
        self.bot.respond("my name is Alex")
        self.assertIn("Alex", self.bot.respond("hello").text)

    def test_farewell_is_personalised_once_name_known(self):
        self.bot.respond("my name is Alex")
        self.assertIn("Alex", self.bot.respond("bye").text)

    def test_name_can_be_changed(self):
        self.bot.respond("my name is Alex")
        self.bot.respond("call me Sam")
        self.assertEqual(self.bot.session.name, "Sam")

    def test_turns_count_non_empty_messages(self):
        for text in ("hi", "", "joke", "   ", "bye"):
            self.bot.respond(text)
        self.assertEqual(self.bot.session.turns, 3)

    def test_sessions_are_independent(self):
        self.bot.respond("my name is Alex")
        self.assertIsNone(make_bot().session.name)

    def test_goodbye_uses_name(self):
        self.bot.respond("my name is Alex")
        self.assertIn("Alex", self.bot.goodbye())


class TraceTests(unittest.TestCase):
    def test_reply_records_how_it_was_produced(self):
        reply = make_bot().respond("  Hello There!! ")
        self.assertEqual(reply.clean_input, "hello there")
        self.assertEqual(reply.matched, "hello there")
        self.assertEqual(reply.rule, "keyword")

    def test_dynamic_time_reply(self):
        self.assertIn("3:05 PM", make_bot().respond("what time is it?").text)


if __name__ == "__main__":
    unittest.main()
