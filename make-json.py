import argparse
import json
import re
import sys
from pathlib import Path

ARGUMENT_PARSER = argparse.ArgumentParser()

# TODO define a path argument so as to call this script with
# python ./make-json.py ../path-to-target-folder
ARGUMENT_PARSER.add_argument(
    "-v", "--version", help="show program version and exit", action="store_true"
)

PARSED_ARGS = ARGUMENT_PARSER.parse_args()

if PARSED_ARGS.version:
    print("make-json.py version 1.0.1\nLicensed under the GPLv3.0")
    sys.exit()

jsonFilePath = Path(".", "commons", "glossario.json")

if not jsonFilePath.exists():
    jsonFilePath.touch()
    jsonFile = jsonFilePath.open("a", encoding="utf-8")
    jsonFile.write("{\n")
    for letter in [chr(i) for i in range(ord("A"), ord("Z") + 1)]:
        jsonFile.write(f'  "{letter}": ' + "{ }")
        if letter != "Z":
            jsonFile.write(",")
        jsonFile.write("\n")
    jsonFile.write("}\n")
    jsonFile.close()

with jsonFilePath.open("r", encoding="utf-8") as jsonFile:
    glossary = json.load(jsonFile)

for file in Path(".").glob("**/*.tex"):
    with file.open("r", encoding="utf-8") as openedFile:
        for lineNumber, line in enumerate(openedFile):
            for match in re.finditer(r"\\glossario\{(?P<entry>.*?)\}", line):
                entry = match.group("entry")
                initial = entry[0].upper()

                if len(entry) < 2:
                    print(f"skipping entry {entry}, too short")
                    continue

                # cannot use the str.capitalize() function because it lowers every
                # other letter
                capitalizedEntry = initial + entry[1:]

                try:
                    if capitalizedEntry not in glossary[initial]:
                        glossary[initial][capitalizedEntry] = ""

                except KeyError:
                    print("This entry is not a suitable dictionary key.")
                    print(f"File: {file}")
                    print(f"Line number: {lineNumber}")
                    print(f"Line: {line}")
                    print(f"Entry: {capitalizedEntry}")


with jsonFilePath.open("w", encoding="utf-8", newline="\n") as jsonFile:
    json.dump(glossary, jsonFile, indent=2, sort_keys=True)
