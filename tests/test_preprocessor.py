import doctest
import unittest

from chatbot import preprocessor
from chatbot.preprocessor import ngrams, sanitize, tokenize


class SanitizeTests(unittest.TestCase):
    def test_lowercases(self):
        self.assertEqual(sanitize("HELLO"), "hello")

    def test_strips_outer_whitespace(self):
        self.assertEqual(sanitize("   hello \t\n"), "hello")

    def test_collapses_inner_whitespace(self):
        self.assertEqual(sanitize("how    are \t you"), "how are you")

    def test_removes_punctuation(self):
        self.assertEqual(sanitize("Hello!!! How are you?"), "hello how are you")

    def test_punctuation_between_words_becomes_space(self):
        self.assertEqual(sanitize("hi,there"), "hi there")

    def test_joins_contractions(self):
        self.assertEqual(sanitize("What's the time?"), "whats the time")
        self.assertEqual(sanitize("What’s up"), "whats up")

    def test_keeps_digits(self):
        self.assertEqual(sanitize("Project 1"), "project 1")

    def test_keeps_non_ascii_letters(self):
        self.assertEqual(sanitize("José"), "josé")

    def test_empty_and_blank_input(self):
        self.assertEqual(sanitize(""), "")
        self.assertEqual(sanitize("   "), "")
        self.assertEqual(sanitize("?!..."), "")

    def test_variants_normalize_to_same_value(self):
        variants = ["Hello", "hello", "HELLO", "  hello  ", "Hello!", "hello."]
        self.assertEqual({sanitize(v) for v in variants}, {"hello"})


class TokenizeTests(unittest.TestCase):
    def test_splits_words(self):
        self.assertEqual(tokenize("how are you"), ["how", "are", "you"])

    def test_empty(self):
        self.assertEqual(tokenize(""), [])


class NgramTests(unittest.TestCase):
    def test_unigrams(self):
        self.assertEqual(ngrams(["a", "b"], 1), ["a", "b"])

    def test_bigrams(self):
        self.assertEqual(ngrams(["a", "b", "c"], 2), ["a b", "b c"])

    def test_n_larger_than_input(self):
        self.assertEqual(ngrams(["a"], 3), [])

    def test_non_positive_n(self):
        self.assertEqual(ngrams(["a"], 0), [])


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(preprocessor))
    return tests


if __name__ == "__main__":
    unittest.main()
