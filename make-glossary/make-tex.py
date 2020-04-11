import argparse
import json
import sys
import re
import typing
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


START_EXPRESSION = "INIZIO_SEZIONE_GENERATA_AUTOMATICAMENTE"
END_EXPRESSION = "FINE_SEZIONE_GENERATA_AUTOMATICAMENTE"


def findSectionStart(lines: typing.List[str]) -> int:
    matchedIndexes = [
        i for i, line in enumerate(lines) if re.search(START_EXPRESSION, line)
    ]
    assert len(matchedIndexes) == 1, "found too many start expressions"
    assert matchedIndexes[0] != 0, "this matched index does not make sense"

    return matchedIndexes[0]


def findSectionEnd(lines: typing.List[str]) -> int:
    matchedIndexes = [
        i for i, line in enumerate(lines) if re.search(END_EXPRESSION, line)
    ]
    assert len(matchedIndexes) == 1, "found too many end expressions"
    assert matchedIndexes[0] != 0, "this matched index does not make sense"

    return matchedIndexes[0]


def main() -> None:
    jsonFilePath = Path(".", "esterni", "glossario", "glossario.json")

    with jsonFilePath.open(
        "r", encoding="utf-8", errors="strict", newline="\n"
    ) as jsonFile:
        glossary = json.load(jsonFile)

    texFilePath = Path(".", "esterni", "glossario", "glossario.tex")

    with texFilePath.open(
        "r", encoding="utf-8", errors="strict", newline="\n"
    ) as texFile:
        wholeContents: typing.List[str] = texFile.readlines()

    sectionStart = findSectionStart(wholeContents)
    sectionEnd = findSectionEnd(wholeContents)

    preamble = wholeContents[: sectionStart + 1]
    # contents = wholeContents[sectionStart + 1 : sectionEnd]
    ending = wholeContents[sectionEnd:]

    contents: typing.List[str] = []

    for letter, entries in glossary.items():
        if len(entries) != 0:
            definitions = []

            for name, description in entries.items():
                if description:
                    definitions.append("  \\item[" + name + "] " + description + "\n")
                else:
                    print(f"ignored term {name}.")

            if definitions:
                contents.append("\\section{" + letter + "}\n")
                contents.append("\\begin{description}\n")

                contents.extend(definitions)

                contents.append("\\end{description}\n")
                contents.append("\\newpage\n")

    with texFilePath.open(
        "w", encoding="utf-8", errors="strict", newline="\n"
    ) as texFile:
        texFile.write("".join(preamble + contents + ending))


if __name__ == "__main__":
    main()
