
import textwrap

from .models import ProductCard


def print_card(card: ProductCard, width: int = 80) -> None:
    """Красиво выводит сгенерированную карточку товара в консоль."""

    separator = "=" * width
    line = "-" * width

    def print_wrapped(text: str) -> None:
        """Переносит длинный текст, сохраняя абзацы."""
        paragraphs = text.splitlines()

        for paragraph in paragraphs:
            if paragraph.strip():
                print(
                    textwrap.fill(
                        paragraph,
                        width=width,
                        break_long_words=False,
                        break_on_hyphens=False
                    )
                )
            else:
                print()

    print(f"\n{separator}")
    print("СГЕНЕРИРОВАННАЯ КАРТОЧКА ТОВАРА")
    print(separator)

    print("\nSEO-ЗАГОЛОВОК:")
    print_wrapped(card.seo_title)

    print(f"\n{line}")
    print("SEO-ОПИСАНИЕ:")
    print(line)
    print_wrapped(card.seo_description)

    print(f"\n{line}")
    print("ХАРАКТЕРИСТИКИ:")

    for characteristic in card.characteristics:
        print(f"  • {characteristic.name}: {characteristic.value}")

    print(f"\n{line}")
    print("ПОИСКОВЫЕ ЗАПРОСЫ:")

    for query in card.search_queries:
        print(f"  • {query}")

    print(f"\n{line}")
    print("КОММЕРЧЕСКИЙ БЛОК:")
    print_wrapped(card.commercial_block)

    print(f"\n{line}")
    print("НЕДОСТАЮЩАЯ ИНФОРМАЦИЯ:")

    if card.missing_information:
        for item in card.missing_information:
            print(f"  • {item}")
    else:
        print("  Нет")

    print(f"\n{line}")
    print("ПРЕДУПРЕЖДЕНИЯ:")

    if card.warnings:
        for warning in card.warnings:
            print(f"  • {warning}")
    else:
        print("  Нет")

    print(f"\nНужно больше данных: {card.needs_more_data}")
    print(separator)
