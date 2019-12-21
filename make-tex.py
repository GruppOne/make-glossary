from pathlib import Path
import json
import argparse

argumentParser = argparse.ArgumentParser()

argumentParser.add_argument(
    "-v", "--version",
    help="sow program version and exit",
    action="store_true")

args = argumentParser.parse_args()

if args.version:
    print("make-json.py version 1.0.0\nLicensed under the GPLv3.0")
    exit()

jsonFilePath = Path('.', 'commons', 'glossario.json')
with jsonFilePath.open('r') as jsonFile:
    glossary = json.load(jsonFile)

texFilePath = Path('.', 'esterni', 'glossario', 'glossario.tex')
with texFilePath.open('r') as texFile:
    contents = texFile.readlines()

for letter, entries in glossary.items():
    if len(entries) != 0:
        contents.insert(-1, "\t\\section{" + letter + "}\n")
        contents.insert(-1, "\t\\begin{description}\n")
        for name, description in entries.items():
            contents.insert(-1, "\t\t\\item[" +
                            name +
                            "] " +
                            description +
                            "\n")
        contents.insert(-1, "\t\\end{description}\n")

with texFilePath.open('w') as texFile:
    texFile.write("".join(contents))
