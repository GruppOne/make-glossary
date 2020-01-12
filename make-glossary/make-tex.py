import argparse
import json
import sys
from pathlib import Path

# TODO refactor to function
ARGUMENT_PARSER = argparse.ArgumentParser()

ARGUMENT_PARSER.add_argument(
    "-v", "--version", help="show program version and exit", action="store_true"
)

PARSED_ARGS = ARGUMENT_PARSER.parse_args()

if PARSED_ARGS.version:
    print("make-json.py version 1.0.1\nLicensed under the GPLv3.0")
    sys.exit()


def main() -> None:
    jsonFilePath = Path(".", "commons", "glossario.json")

    with jsonFilePath.open("r", encoding="utf-8") as jsonFile:
        glossary = json.load(jsonFile)

    texFilePath = Path(".", "esterni", "glossario", "glossario.tex")

    with texFilePath.open("r", encoding="utf-8") as texFile:
        contents = texFile.readlines()

    for letter, entries in glossary.items():
        if len(entries) != 0:
            contents.insert(-1, "  \\section{" + letter + "}\n")
            contents.insert(-1, "  \\begin{description}\n")

            for name, description in entries.items():
                contents.insert(-1, "    \\item[" + name + "] " + description + "\n")
            contents.insert(-1, "\t\\end{description}\n")

    with texFilePath.open("w", encoding="utf-8") as texFile:
        texFile.write("".join(contents))


if __name__ == "__main__":
    main()
