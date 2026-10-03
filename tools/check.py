#!/usr/bin/env python3
"""Проверка CSV-колод перед импортом в Anki.

Использование:
    python3 tools/check.py                # все колоды в decks/
    python3 tools/check.py decks/git      # конкретная папка или файл
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import deck_io
import registry
import validators

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "registry.csv"


def check_file(path: Path, known: dict) -> list:
    headers, rows = deck_io.read_deck(path)
    if deck_io.note_type(headers) != validators.ALLINONE:
        return [f"{path.name}: тип {deck_io.note_type(headers)!r} не проверяется"]
    problems = []
    for index, row in enumerate(rows, start=1):
        for message in validators.validate_row(row):
            problems.append(f"{path.name}:{index} — {message}")
    for index, message in registry.find_duplicates(rows, known):
        problems.append(f"{path.name}:{index} — {message}")
    return problems


def resolve_targets(argument: str | None) -> list:
    target = Path(argument) if argument else ROOT / "decks"
    if target.is_file():
        return [target]
    return list(deck_io.iter_decks(target))


def main() -> int:
    known = registry.load(REGISTRY_PATH)
    targets = resolve_targets(sys.argv[1] if len(sys.argv) > 1 else None)
    if not targets:
        print("Колод не найдено.")
        return 0
    problems = []
    for path in targets:
        problems.extend(check_file(path, known))
    for problem in problems:
        print(problem)
    print(f"\nФайлов: {len(targets)}, проблем: {len(problems)}")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
