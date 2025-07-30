import argparse
import sys
from typing import TextIO

from unimoji import replace_with_desc

def unimojify(fp: TextIO):
    for line in fp:
        print(replace_with_desc(line), end="")


def main():
    if not sys.stdin.isatty():
        if "-h" not in sys.argv and "--help" not in sys.argv:
            fp = sys.stdin
            return unimojify(fp)

    parser = argparse.ArgumentParser(
        description=(
            "Replace emojis in file(s) or string"
            " with their :code: equivalents"
        )
    )
    parser.add_argument(
        "files",
        nargs="+",
        help=(
            "One or more files to process with unimoji,"
            " or '-' for stdin; also accepts piped stdin"
        ),
    )
    args = parser.parse_args()
    files = args.files
    for filename in files:
        if filename == "-":
            fp = sys.stdin
            unimojify(fp)
        else:
            with open(filename) as fp:
                unimojify(fp)


if __name__ == "__main__":
    main()
