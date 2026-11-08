import argparse
import json
from pathlib import Path

from dotenv import load_dotenv

from .llm_client import generate_card
from .prompt_builder import build_prompt
from .validators import validate_card
from .display import print_card


ROOT_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT_DIR / "data"
RESULTS_DIR = ROOT_DIR / "results"


def process_product(input_path: Path) -> bool:
    """Обрабатывает один JSON-файл и сохраняет результат."""

    print(f"\n{'=' * 60}")
    print(f"Обработка: {input_path.name}")
    print(f"{'=' * 60}")

    try:
        product = json.loads(
            input_path.read_text(encoding="utf-8")
        )

        if not isinstance(product, dict):
            raise ValueError(
                "Корневой элемент входного JSON должен быть объектом."
            )

        prompt = build_prompt(product)
        raw_answer = generate_card(prompt)

        # Передаём исходный JSON для дополнительной проверки
        card = validate_card(raw_answer, product)

        RESULTS_DIR.mkdir(
            parents=True,
            exist_ok=True
        )

        output_path = (
            RESULTS_DIR / f"{input_path.stem}_card.json"
        )

        output_path.write_text(
            card.model_dump_json(indent=2),
            encoding="utf-8"
        )

        print(f"Карточка сохранена: {output_path}")
        print_card(card)

        return True

    except Exception as error:
        print(
            f"Ошибка при обработке {input_path.name}: {error}"
        )

        return False


def main():
    parser = argparse.ArgumentParser(
        description="Генератор SEO-карточек контрольно-измерительных приборов"
    )

    parser.add_argument(
        "product",
        help="Имя JSON-файла из data/ или all для обработки всех файлов"
    )

    args = parser.parse_args()

    load_dotenv(ROOT_DIR / ".env")

    if args.product == "all":
        input_files = sorted(
            DATA_DIR.glob("*.json")
        )

        if not input_files:
            raise FileNotFoundError(
                f"В папке {DATA_DIR} нет JSON-файлов."
            )

        print(f"Найдено файлов: {len(input_files)}")

        successful = 0
        failed = 0

        for input_path in input_files:
            if process_product(input_path):
                successful += 1
            else:
                failed += 1

        print("\nИТОГ:")
        print(f"Успешно обработано: {successful}")
        print(f"Ошибок: {failed}")

    else:
        # Разрешаем передавать только имя файла
        input_path = DATA_DIR / Path(args.product).name

        if (
            input_path.suffix.lower() != ".json"
            or not input_path.is_file()
        ):
            raise FileNotFoundError(
                f"Не найден входной JSON-файл: {input_path}"
            )

        process_product(input_path)


if __name__ == "__main__":
    main()
