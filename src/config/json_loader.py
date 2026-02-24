import json
from dataclasses import dataclass

from src.constants import BASE_DIR


@dataclass
class Message:
    start_message: str
    access_denied: str
    join_request: str
    message_deleted: str
    message_edited: str

    @classmethod
    def create(cls, filename: str = "messages.json") -> "Message":
        messages = cls.load_json(filename)
        return cls(
            start_message=messages.get("start_message"),
            access_denied=messages.get("access_denied"),
            join_request=messages.get("join_request"),
            message_deleted=messages.get("message_deleted"),
            message_edited=messages.get("message_edited"),
        )

    @staticmethod
    def load_json(filename: str = "messages.json") -> dict:
        with open(BASE_DIR / filename, "r", encoding="utf-8") as f:
            return json.load(f)
