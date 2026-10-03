"""Чтение CSV-колод Anki: служебная шапка + строки заметок."""
import csv
from pathlib import Path

HEADER_PREFIX = "#"
DELIMITER = ";"


def read_deck(path: Path):
    """Возвращает (headers: dict, rows: list[list[str]])."""
    headers, body = {}, []
    with path.open(encoding="utf-8") as handle:
        for line in handle:
            if line.startswith(HEADER_PREFIX):
                key, _, value = line[1:].rstrip("\n").partition(":")
                headers[key.strip()] = value.strip()
            elif line.strip():
                body.append(line)
    rows = [row for row in csv.reader(body, delimiter=DELIMITER) if row]
    return headers, rows


def note_type(headers: dict) -> str:
    return headers.get("notetype", "")


def iter_decks(root: Path):
    """Все CSV-файлы колод в порядке обхода."""
    yield from sorted(root.rglob("*.csv"))
