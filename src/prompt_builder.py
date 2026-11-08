
from pathlib import Path
import json


ROOT_DIR = Path(__file__).resolve().parents[1]

PROMPT_PATH = (
    ROOT_DIR / "prompts" / "product_card_prompt.txt"
)


def build_prompt(product: dict) -> str:
    """
    Читает шаблон промпта и подставляет
    в него JSON с характеристиками товара.
    """

    template = PROMPT_PATH.read_text(
        encoding="utf-8"
    )

    product_json = json.dumps(
        product,
        ensure_ascii=False,
        indent=2
    )

    return template.replace(
        "{{PRODUCT_JSON}}",
        product_json
    )
