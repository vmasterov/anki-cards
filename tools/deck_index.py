"""Индекс вопросов по всем колодам: поиск дублей без отдельного реестра."""
from pathlib import Path

import deck_io


def own_id(row) -> str | None:
    """Тег-идентификатор карточки. Теги всегда в последней колонке."""
    return next((tag for tag in row[-1].split() if tag.startswith("id-")), None)


def normalize(question: str) -> str:
    """Грубая нормализация для сравнения: без тегов, регистра и пробелов."""
    text = question.lower()
    for token in ("<code>", "</code>", "<br>", "<b>", "</b>", "<pre>", "</pre>"):
        text = text.replace(token, "")
    return " ".join(text.split())


def build(root: Path) -> tuple[dict, list]:
    """Индекс {нормализованный вопрос: id} и ошибки повторных id."""
    index, owners, problems = {}, {}, []
    for path in deck_io.iter_decks(root):
        _, rows = deck_io.read_deck(path)
        location = f"{path.parent.name}/{path.name}"
        for row in rows:
            card_id = own_id(row)
            if card_id in owners:
                problems.append(f"{location} — id {card_id} уже занят в {owners[card_id]}")
            if card_id is not None:
                owners[card_id] = location
            index.setdefault(normalize(row[0]), card_id)
    return index, problems


def find_duplicates(rows, index: dict) -> list:
    """Дубли вопросов против всей базы и внутри самого файла.

    Совпадение по собственному id — это та же карточка, не дубль.
    """
    problems, seen = [], {}
    for number, row in enumerate(rows, start=1):
        key = normalize(row[0])
        if key in index and index[key] != own_id(row):
            problems.append((number, f"дубль карточки {index[key]}"))
        elif key in seen:
            problems.append((number, f"дубль строки {seen[key]} этого же файла"))
        else:
            seen[key] = number
    return problems
