#!/usr/bin/env python3
"""Проверка CSV-колод перед импортом в Anki.

Использование:
    python3 tools/check.py                # все колоды в decks/
    python3 tools/check.py decks/git      # конкретная папка или файл
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import deck_index
import deck_io
import notetypes

ROOT = Path(__file__).resolve().parent.parent
DECKS = ROOT / "decks"


def check_file(path: Path, known: dict) -> list:
    headers, rows = deck_io.read_deck(path)
    validate = notetypes.validator_for(deck_io.note_type(headers))
    if validate is None:
        return [f"{path.name}: тип {deck_io.note_type(headers)!r} не проверяется"]
    problems = []
    has_guid = "guid column" in headers
    for index, row in enumerate(rows, start=1):
        for message in validate(row, has_guid):
            problems.append(f"{path.name}:{index} — {message}")
    for index, message in deck_index.find_duplicates(rows, known):
        problems.append(f"{path.name}:{index} — {message}")
    return problems


def resolve_targets(argument: str | None) -> list:
    target = Path(argument) if argument else DECKS
    if target.is_file():
        return [target]
    return list(deck_io.iter_decks(target))


def main() -> int:
    known, problems = deck_index.build(DECKS)
    targets = resolve_targets(sys.argv[1] if len(sys.argv) > 1 else None)
    if not targets:
        print("Колод не найдено.")
        return 0
    for path in targets:
        problems.extend(check_file(path, known))
    for problem in problems:
        print(problem)
    print(f"\nФайлов: {len(targets)}, проблем: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
