"""Правила для встроенных типов Anki с двумя полями.

Простая, Простая (с вводом ответа), Задание с пропусками:
два поля по порядку колонок, затем необязательный GUID и теги.
"""
import validators as common

BASIC = "Простая"
BASIC_TYPED = "Простая (с вводом ответа)"
CLOZE = "Задание с пропусками"
TWO_FIELD_COLUMNS = 3  # два поля + теги
CLOZE_MARK = "{{c"


def check_answer_not_empty(row):
    return "пустой ответ" if not row[1].strip() else None


def check_cloze_marker(row):
    if CLOZE_MARK in row[0]:
        return None
    return "в тексте нет пропуска вида {{c1::…}}"


BASIC_RULES = (
    common.check_question_not_empty,
    check_answer_not_empty,
    common.check_id_tag,
)

CLOZE_RULES = (
    common.check_question_not_empty,
    check_cloze_marker,
    common.check_id_tag,
)


def validate_basic_row(row, has_guid=False):
    """Простая и Простая (с вводом ответа): вопрос и ответ обязательны."""
    return common.run_rules(row, TWO_FIELD_COLUMNS, BASIC_RULES, has_guid)


def validate_cloze_row(row, has_guid=False):
    """Задание с пропусками: в тексте должен быть хотя бы один пропуск."""
    return common.run_rules(row, TWO_FIELD_COLUMNS, CLOZE_RULES, has_guid)
