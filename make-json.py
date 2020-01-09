import re
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
    print("make-json.py version 1.0.1\nLicensed under the GPLv3.0")
    exit()

jsonFilePath = Path('.', 'commons', 'glossario.json')

if not jsonFilePath.exists():
    jsonFilePath.touch()
    jsonFile = jsonFilePath.open('a', encoding='utf-8')
    jsonFile.write('{\n')
    for letter in [chr(i) for i in range(ord('A'), ord('Z') + 1)]:
        jsonFile.write(f'\t"{letter}": ' + "{ }")
        if letter != 'Z':
            jsonFile.write(',')
        jsonFile.write('\n')
    jsonFile.write('}\n')
    jsonFile.close()

with jsonFilePath.open('r', encoding='utf-8') as jsonFile:
    glossary = json.load(jsonFile)

for file in Path('.').glob('**/*.tex'):
    with file.open('r', encoding='utf-8') as openedFile:
        for line in openedFile:
            for match in re.finditer(r'\\glossario\{.*?\}', line):
                entry = match.group()[11:-1]
                initial = entry[0].upper()
                if entry not in glossary[initial]:
                    glossary[initial][entry] = ''

with jsonFilePath.open('w', encoding='utf-8') as jsonFile:
    json.dump(glossary, jsonFile, indent=4, sort_keys=True)
