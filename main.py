"""Entry point for the rule-based chatbot.

Usage:
    python main.py            # start chatting
    python main.py --trace    # also show which rule produced each reply
"""

import argparse
import sys

from chatbot.cli import run


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Nova - a rule-based AI chatbot (DecodeLabs Project 1)."
    )
    parser.add_argument(
        "--trace",
        action="store_true",
        help="show the matched rule and intent for every reply",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> None:
    args = parse_args(argv)
    # Show "?" instead of crashing on characters the terminal can't display,
    # e.g. a non-Latin name when output is redirected on Windows.
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    run(trace=args.trace)


if __name__ == "__main__":
    main()
