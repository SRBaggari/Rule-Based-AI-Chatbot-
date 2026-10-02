import random
import unittest
from datetime import datetime

from chatbot.knowledge_base import BOT_NAME, FALLBACK, INTENTS
from chatbot.responder import build_response, format_date, format_time, render

FIXED_NOW = datetime(2026, 10, 2, 15, 5)


def possible_replies(templates: list[str], name: str = "friend") -> set[str]:
    return {
        t.format(
            bot=BOT_NAME,
            name=name,
            time=format_time(FIXED_NOW),
            date=format_date(FIXED_NOW),
        )
        for t in templates
    }


class FormattingTests(unittest.TestCase):
    def test_format_time(self):
        self.assertEqual(format_time(FIXED_NOW), "3:05 PM")
        self.assertEqual(format_time(datetime(2026, 1, 1, 10, 30)), "10:30 AM")

    def test_format_date(self):
        self.assertEqual(format_date(FIXED_NOW), "Friday, 2 October 2026")


class BuildResponseTests(unittest.TestCase):
    def test_reply_comes_from_the_intents_templates(self):
        for intent, entry in INTENTS.items():
            with self.subTest(intent=intent):
                reply = build_response(intent, now=FIXED_NOW, rng=random.Random(0))
                self.assertIn(reply, possible_replies(entry["responses"]))

    def test_unknown_intent_uses_fallback(self):
        reply = build_response("no_such_intent", rng=random.Random(0))
        self.assertIn(reply, possible_replies(FALLBACK["responses"]))

    def test_none_intent_uses_fallback(self):
        reply = build_response(None, rng=random.Random(0))
        self.assertIn(reply, possible_replies(FALLBACK["responses"]))

    def test_time_placeholder_is_filled(self):
        reply = build_response("time", now=FIXED_NOW)
        self.assertIn("3:05 PM", reply)
        self.assertNotIn("{", reply)

    def test_date_placeholder_is_filled(self):
        self.assertIn("Friday, 2 October 2026", build_response("date", now=FIXED_NOW))

    def test_bot_name_placeholder_is_filled(self):
        self.assertIn(BOT_NAME, build_response("bot_identity"))

    def test_same_seed_gives_same_reply(self):
        first = build_response("joke", rng=random.Random(42))
        second = build_response("joke", rng=random.Random(42))
        self.assertEqual(first, second)


class PersonalisationTests(unittest.TestCase):
    def test_known_name_uses_personal_responses(self):
        reply = build_response("greeting", name="Alex")
        personal = INTENTS["greeting"]["personal_responses"]
        self.assertIn(reply, possible_replies(personal, "Alex"))
        self.assertIn("Alex", reply)

    def test_unknown_name_uses_general_responses(self):
        reply = build_response("greeting", now=FIXED_NOW)
        self.assertIn(reply, possible_replies(INTENTS["greeting"]["responses"]))

    def test_name_ignored_when_no_personal_responses(self):
        reply = build_response("joke", name="Alex")
        self.assertIn(reply, possible_replies(INTENTS["joke"]["responses"]))

    def test_render_works_on_any_entry(self):
        self.assertEqual(render({"responses": ["Hi {name}"]}, name="Sam"), "Hi Sam")


if __name__ == "__main__":
    unittest.main()
