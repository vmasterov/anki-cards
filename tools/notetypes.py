"""Выбор валидатора по типу заметки из шапки #notetype.

Новый тип подключается одной строкой в VALIDATORS, check.py не меняется.
"""
import rules_two_field as two_field
import validators

VALIDATORS = {
    validators.ALLINONE: validators.validate_row,
    two_field.BASIC: two_field.validate_basic_row,
    two_field.BASIC_TYPED: two_field.validate_basic_row,
    two_field.CLOZE: two_field.validate_cloze_row,
}


def validator_for(note_type: str):
    """Функция проверки строки или None, если тип не поддерживается."""
    return VALIDATORS.get(note_type)
