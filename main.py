"""Entry point for the rule-based chatbot.

Usage:
    python main.py            # start chatting
    python main.py --trace    # also show which rule produced each reply
"""

import argparse

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
    run(trace=args.trace)


if __name__ == "__main__":
    main()
