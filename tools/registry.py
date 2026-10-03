"""Реестр вопросов: защита от дублей между партиями."""
import csv
from pathlib import Path

FIELDNAMES = ("id", "deck", "type", "question")


def load(path: Path) -> dict:
    """{нормализованный вопрос: id} из реестра."""
    if not path.exists():
        return {}
    with path.open(encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter=";")
        return {normalize(row["question"]): row["id"] for row in reader}


def normalize(question: str) -> str:
    """Грубая нормализация для сравнения: без тегов, регистра и пробелов."""
    text = question.lower()
    for token in ("<code>", "</code>", "<br>", "<b>", "</b>"):
        text = text.replace(token, "")
    return " ".join(text.split())


def own_id(row) -> str | None:
    """Тег-идентификатор карточки. Теги всегда в последней колонке."""
    return next((tag for tag in row[-1].split() if tag.startswith("id-")), None)


def find_duplicates(rows, known: dict) -> list:
    """Дубли против реестра и внутри самой партии.

    Совпадение с реестром по собственному id — это та же карточка, не дубль.
    """
    problems, seen = [], {}
    for index, row in enumerate(rows, start=1):
        key = normalize(row[0])
        if key in known and known[key] != own_id(row):
            problems.append((index, f"дубль карточки {known[key]} из реестра"))
        elif key in seen:
            problems.append((index, f"дубль строки {seen[key]} этой же партии"))
        else:
            seen[key] = index
    return problems
