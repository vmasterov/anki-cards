"""Правила проверки карточек. Каждое правило — отдельная функция."""

ALLINONE = "AllInOne (kprim, mc, sc)"
ALLINONE_COLUMNS = 12
QTYPE_KPRIM, QTYPE_MC, QTYPE_SC = "0", "1", "2"
OPTION_SLICE = slice(3, 8)
ANSWERS_INDEX = 8
TAGS_INDEX = 11


def check_column_count(row, expected=ALLINONE_COLUMNS):
    if len(row) != expected:
        return f"колонок {len(row)}, ожидалось {expected}"
    return None


def check_qtype(row):
    if row[2] not in (QTYPE_KPRIM, QTYPE_MC, QTYPE_SC):
        return f"недопустимый QType: {row[2]!r}"
    return None


def check_answer_mask(row):
    options = [cell for cell in row[OPTION_SLICE] if cell.strip()]
    mask = row[ANSWERS_INDEX].split()
    if len(mask) != len(options):
        return f"маска {len(mask)} значений, вариантов {len(options)}"
    if any(value not in ("0", "1") for value in mask):
        return "маска содержит не только 0 и 1"
    correct = mask.count("1")
    if correct == 0:
        return "нет правильного варианта"
    if row[2] == QTYPE_SC and correct != 1:
        return f"sc требует ровно один правильный, найдено {correct}"
    if row[2] == QTYPE_MC and correct < 2:
        return "mc требует минимум два правильных варианта"
    if row[2] == QTYPE_KPRIM and len(options) != 4:
        return f"kprim требует ровно 4 утверждения, найдено {len(options)}"
    return None


def check_question_not_empty(row):
    return "пустой вопрос" if not row[0].strip() else None


def check_id_tag(row):
    tags = row[TAGS_INDEX].split()
    if not any(tag.startswith("id-") for tag in tags):
        return "нет тега-идентификатора id-*"
    return None


ALLINONE_RULES = (
    check_column_count,
    check_qtype,
    check_answer_mask,
    check_question_not_empty,
    check_id_tag,
)


def validate_row(row, rules=ALLINONE_RULES):
    """Список сообщений об ошибках для одной строки."""
    if (problem := check_column_count(row)) is not None:
        return [problem]
    return [message for rule in rules
            if (message := rule(row)) is not None]
