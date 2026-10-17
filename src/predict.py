import base64
import mimetypes
from pathlib import Path

from langchain_core.messages import HumanMessage, SystemMessage

from src.model import model_yes_no, model_number


PROJECT_ROOT = Path(__file__).resolve().parent.parent
IMAGE_DIR = PROJECT_ROOT / "img"


SYSTEM_PROMPT = """
You are an assistant that analyzes financial charts.

Carefully inspect the provided chart image and answer the
user's question using the visible information in the chart.

Follow these rules:
- Use the chart and the question as your primary evidence.
- Do not invent exact prices or values that cannot be inferred.
- For yes/no questions, select the most defensible answer.
- For numerical questions, return the requested numerical value.
- Do not include explanations outside the required output schema.
"""

IMAGE_ALIASES = {
    "Ayar_9khordad_7tir.png": "Ayar_1405_9khordad_7tir.png",
    "hamkaran_1tir.png": "hamkaran_1405_1tir.png",
    "khasapa_18khordad_26khordad.png": (
        "khasapa_1405_18khordad_26khordad.png"
    ),
    "vebmelat_2mehr_3Aban.png": (
        "vebmelat_1404_2mehr_3Aban.png"
    ),
}


def resolve_image_path(image_file: str) -> Path:
    actual_name = IMAGE_ALIASES.get(image_file, image_file)
    image_path = IMAGE_DIR / actual_name

    if not image_path.is_file():
        raise FileNotFoundError(
            f"Image not found for '{image_file}'. "
            f"Expected path: {image_path}"
        )

    return image_path


def encode_image(image_path: Path) -> str:
    with image_path.open("rb") as image_file:
        return base64.b64encode(image_file.read()).decode("utf-8")


def build_messages(question: str, image_file: str) -> list:
    image_path = resolve_image_path(image_file)

    if not image_path.is_file():
        raise FileNotFoundError(
            f"Image not found: {image_path}"
        )

    image_base64 = encode_image(image_path)

    mime_type, _ = mimetypes.guess_type(str(image_path))
    if mime_type not in {"image/png", "image/jpeg", "image/webp"}:
        raise ValueError(
            f"Unsupported image format: {image_path.suffix}"
        )

    image_url = (
        f"data:{mime_type};base64,{image_base64}"
    )

    return [
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(
            content=[
                {
                    "type": "text",
                    "text": question,
                },
                {
                    "type": "image_url",
                    "image_url": {
                        "url": image_url,
                    },
                },
            ]
        ),
    ]


def get_answer(question: str, image_file: str, answer_type: str):
    messages = build_messages(question, image_file)

    if answer_type == "yes_no":
        result = model_yes_no.invoke(messages)
    elif answer_type == "number":
        result = model_number.invoke(messages)
    else:
        raise ValueError(
            f"Unsupported answer type: {answer_type}"
        )

    return result.answer
