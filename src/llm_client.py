
import os

from groq import Groq


def generate_card(prompt: str) -> str:
    """Отправляет промпт в Groq и возвращает текстовый ответ модели."""

    api_key = os.getenv("GROQ_API_KEY")

    if not api_key:
        raise RuntimeError(
            "Не найден GROQ_API_KEY. Создай файл .env в корне проекта "
            "на основе .env.example и добавь свой API-ключ."
        )

    model = os.getenv(
        "GROQ_MODEL",
        "openai/gpt-oss-20b"
    )

    client = Groq(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.2,
        max_completion_tokens=4096,
        reasoning_effort="low",
        include_reasoning=False,
        response_format={"type": "json_object"}
    )

    if not response.choices:
        raise RuntimeError(
            "Groq вернул ответ без вариантов генерации."
        )

    choice = response.choices[0]
    content = choice.message.content

    if not content or not content.strip():
        raise RuntimeError(
            f"Groq вернул пустой ответ. "
            f"Finish reason: {choice.finish_reason}"
        )

    if choice.finish_reason != "stop":
        raise RuntimeError(
            "Генерация завершилась нештатно: "
            f"{choice.finish_reason}. "
            "Попробуй увеличить max_completion_tokens."
        )

    return content
