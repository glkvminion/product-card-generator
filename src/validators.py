
import re
from typing import Any

from .models import ProductCard


def flatten_source_values(value: Any) -> list[str]:
    """Собирает строковые представления значений исходного JSON."""
    result = []

    if isinstance(value, dict):
        for nested_value in value.values():
            result.extend(flatten_source_values(nested_value))

    elif isinstance(value, list):
        for nested_value in value:
            result.extend(flatten_source_values(nested_value))

    elif value is not None:
        result.append(str(value))

    return result


def extract_numbers(text: str) -> set[str]:
    """Извлекает числовые значения из текста."""
    return {
        token.replace(",", ".")
        for token in re.findall(r"\d+(?:[.,]\d+)?", text)
    }


def validate_card(
    raw_text: str,
    product: dict | None = None
) -> ProductCard:
    """
    Проверяет структуру ответа, ограничения SEO-полей
    и потенциально неподтверждённые числовые значения.
    """

    try:
        card = ProductCard.model_validate_json(raw_text)

    except Exception as error:
        raise ValueError(
            f"Ответ модели не соответствует ожидаемому JSON: {error}"
        ) from error

    # Проверка длины SEO-заголовка
    title_length = len(card.seo_title.strip())

    if title_length > 70:
        raise ValueError(
            f"SEO-заголовок длиннее 70 символов: {title_length}"
        )

    # Проверка длины SEO-описания
    description_length = len(card.seo_description.strip())

    if (
        not card.needs_more_data
        and not 800 <= description_length <= 1200
    ):
        raise ValueError(
            "SEO-описание должно содержать 800–1200 символов, "
            f"сейчас: {description_length}"
        )

    # Проверка числовых значений характеристик
    if product is not None:
        source_text = " ".join(flatten_source_values(product))
        source_numbers = extract_numbers(source_text)

        for characteristic in card.characteristics:
            numbers_in_value = extract_numbers(characteristic.value)
            unsupported = numbers_in_value - source_numbers

            if unsupported:
                warning = (
                    f"В характеристике «{characteristic.name}» "
                    f"обнаружены числа, которых нет в исходных данных: "
                    f"{', '.join(sorted(unsupported))}."
                )

                if warning not in card.warnings:
                    card.warnings.append(warning)

    return card
