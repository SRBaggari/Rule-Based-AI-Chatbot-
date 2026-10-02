import doctest
import unittest

from chatbot import intent_matcher
from chatbot.intent_matcher import Match, extract_name, match_intent
from chatbot.knowledge_base import INTENTS
from chatbot.preprocessor import sanitize


def intent_of(text: str) -> str | None:
    match = match_intent(sanitize(text))
    return match.intent if match else None


class EveryPatternTests(unittest.TestCase):
    def test_each_pattern_matches_its_own_intent(self):
        for intent, entry in INTENTS.items():
            for pattern in entry["patterns"]:
                with self.subTest(intent=intent, pattern=pattern):
                    self.assertEqual(intent_of(pattern), intent)


class MatchingRuleTests(unittest.TestCase):
    def test_case_and_punctuation_do_not_matter(self):
        self.assertEqual(intent_of("  HELLO!!! "), "greeting")
        self.assertEqual(intent_of("What's the TIME?"), "time")

    def test_keyword_inside_sentence(self):
        self.assertEqual(intent_of("could you tell me a joke please"), "joke")

    def test_whole_words_only(self):
        # "hi" must not match inside "this" or "high".
        self.assertIsNone(intent_of("this is high"))

    def test_longest_phrase_wins(self):
        self.assertEqual(intent_of("hello how are you"), "how_are_you")

    def test_negative_mood_not_mistaken_for_positive(self):
        self.assertEqual(intent_of("I'm not good"), "mood_negative")

    def test_unknown_input_returns_none(self):
        self.assertIsNone(intent_of("purple elephants dance"))

    def test_empty_input_returns_none(self):
        self.assertIsNone(match_intent(""))

    def test_match_records_rule_and_phrase(self):
        self.assertEqual(
            match_intent("well hello there"),
            Match("greeting", "hello there", "keyword"),
        )


class ExitMatchingTests(unittest.TestCase):
    def test_exit_commands(self):
        for text in ("bye", "Exit", "QUIT", "goodbye!", "See you later"):
            with self.subTest(text=text):
                self.assertEqual(intent_of(text), "farewell")

    def test_exit_word_inside_sentence_does_not_exit(self):
        for text in ("I will not quit", "how do I exit vim", "bye bye birdie song"):
            with self.subTest(text=text):
                self.assertNotEqual(intent_of(text), "farewell")

    def test_exit_rule_is_exact(self):
        self.assertEqual(match_intent("bye").rule, "exact")


class NameTests(unittest.TestCase):
    def test_name_intro_is_prefix_match(self):
        match = match_intent(sanitize("My name is Alex"))
        self.assertEqual(match, Match("name_intro", "my name is", "prefix"))

    def test_name_phrase_in_middle_is_not_intro(self):
        self.assertNotEqual(intent_of("what is my name is a question"), "name_intro")

    def test_extract_simple_name(self):
        self.assertEqual(extract_name("my name is alex", "my name is"), "Alex")

    def test_extract_multi_word_name(self):
        self.assertEqual(extract_name("call me mary jane", "call me"), "Mary Jane")

    def test_extract_stops_at_joining_word(self):
        self.assertEqual(
            extract_name("my name is alex and i like python", "my name is"), "Alex"
        )

    def test_extract_caps_name_length(self):
        self.assertEqual(
            extract_name("call me a b c d e", "call me"), "A B C"
        )

    def test_extract_missing_name(self):
        self.assertIsNone(extract_name("my name is", "my name is"))


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(intent_matcher))
    return tests


if __name__ == "__main__":
    unittest.main()
