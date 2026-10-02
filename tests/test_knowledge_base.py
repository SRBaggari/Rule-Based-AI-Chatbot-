import unittest

from chatbot import knowledge_base as kb
from chatbot.preprocessor import sanitize


class KnowledgeBaseStructureTests(unittest.TestCase):
    def test_is_a_dictionary_with_at_least_five_intents(self):
        self.assertIsInstance(kb.INTENTS, dict)
        self.assertGreaterEqual(len(kb.INTENTS), 5)

    def test_every_intent_has_responses(self):
        for intent, entry in kb.INTENTS.items():
            with self.subTest(intent=intent):
                self.assertTrue(entry["responses"])

    def test_every_intent_has_patterns(self):
        for intent, entry in kb.INTENTS.items():
            with self.subTest(intent=intent):
                self.assertTrue(entry["patterns"])

    def test_match_types_are_valid(self):
        for intent, entry in kb.INTENTS.items():
            with self.subTest(intent=intent):
                self.assertIn(entry.get("match", "keyword"), kb.MATCH_TYPES)

    def test_required_intents_exist(self):
        for intent in ("greeting", "farewell"):
            self.assertIn(intent, kb.INTENTS)

    def test_fallback_and_empty_responses_exist(self):
        self.assertTrue(kb.FALLBACK["responses"])
        self.assertTrue(kb.EMPTY_INPUT["responses"])

    def test_templates_only_use_known_placeholders(self):
        allowed = {"bot": "", "name": "", "time": "", "date": ""}
        entries = list(kb.INTENTS.values()) + [kb.FALLBACK, kb.EMPTY_INPUT]
        for entry in entries:
            for template in entry["responses"] + entry.get("personal_responses", []):
                with self.subTest(template=template):
                    template.format(**allowed)  # raises KeyError if unknown


class IndexTests(unittest.TestCase):
    def test_every_pattern_is_indexed_in_sanitized_form(self):
        indexes = {
            "keyword": kb.KEYWORD_INDEX,
            "exact": kb.EXACT_INDEX,
            "prefix": kb.PREFIX_INDEX,
        }
        for intent, entry in kb.INTENTS.items():
            index = indexes[entry.get("match", "keyword")]
            for pattern in entry["patterns"]:
                with self.subTest(pattern=pattern):
                    self.assertEqual(index[sanitize(pattern)], intent)

    def test_exit_commands_are_exact_matches(self):
        for command in ("bye", "exit", "quit", "goodbye"):
            self.assertEqual(kb.EXACT_INDEX[command], "farewell")
            self.assertNotIn(command, kb.KEYWORD_INDEX)

    def test_max_word_counts(self):
        self.assertEqual(
            kb.MAX_KEYWORD_WORDS, max(len(p.split()) for p in kb.KEYWORD_INDEX)
        )
        self.assertGreaterEqual(kb.MAX_PREFIX_WORDS, 1)


class BuildIndexesValidationTests(unittest.TestCase):
    def test_duplicate_pattern_across_intents_raises(self):
        intents = {
            "a": {"patterns": ["hello"], "responses": ["x"]},
            "b": {"patterns": ["Hello!"], "responses": ["y"]},
        }
        with self.assertRaises(ValueError):
            kb.build_indexes(intents)

    def test_unknown_match_type_raises(self):
        intents = {"a": {"match": "fuzzy", "patterns": ["x"], "responses": ["x"]}}
        with self.assertRaises(ValueError):
            kb.build_indexes(intents)

    def test_empty_pattern_raises(self):
        intents = {"a": {"patterns": ["!!!"], "responses": ["x"]}}
        with self.assertRaises(ValueError):
            kb.build_indexes(intents)


if __name__ == "__main__":
    unittest.main()
