### aion/cli.py
import argparse
from .files import read_file
from .text import summarize_text
from .code import explain_code

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--read", help="Read file content")
    parser.add_argument("--summarize", help="Summarize input text")
    parser.add_argument("--explain", help="Explain code snippet")
    args = parser.parse_args()

    if args.read:
        print(read_file(args.read))
    elif args.summarize:
        print(summarize_text(args.summarize))
    elif args.explain:
        print(explain_code(args.explain))
