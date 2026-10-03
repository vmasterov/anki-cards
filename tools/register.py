#!/usr/bin/env python3
"""Добавление карточек из CSV-колод в registry.csv.

Использование:
    python3 tools/register.py decks/js-basics   # папка или файл
Уже занесённые id пропускаются, поэтому повторный запуск безопасен.
"""
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import deck_io
import registry

ROOT = Path(__file__).resolve().parent.parent
REGISTRY_PATH = ROOT / "registry.csv"


def collect_entries(path: Path):
    headers, rows = deck_io.read_deck(path)
    deck = headers.get("deck", "")
    for row in rows:
        yield (registry.own_id(row), deck, path.stem, row[0])


def resolve_targets(argument: str) -> list:
    target = Path(argument)
    return [target] if target.is_file() else list(deck_io.iter_decks(target))


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__)
        return 1
    known_ids = set(registry.load(REGISTRY_PATH).values())
    added = 0
    with REGISTRY_PATH.open("a", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, delimiter=";")
        for path in resolve_targets(sys.argv[1]):
            for entry in collect_entries(path):
                if entry[0] is None or entry[0] in known_ids:
                    continue
                writer.writerow(entry)
                known_ids.add(entry[0])
                added += 1
    print(f"Добавлено в реестр: {added}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
