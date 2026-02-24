import json
from src.constants import BASE_DIR


def load_json(filename: str) -> dict:
    with open(BASE_DIR / filename, "r", encoding="utf-8") as f:
        return json.load(f)


MESSAGES = load_json("messages.json")
