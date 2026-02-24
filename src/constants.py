from pathlib import Path

__all__ = [
    "DATA_DIR",
    "SESSIONS_DIR",
    "LOGS_DIR",
    "IGNORE_LIST",
    "BASE_DIR",
    "CONFIG_DIR",
]


BASE_DIR = Path(__file__).parent.parent

DATA_DIR = BASE_DIR / "data"
SRC_DIR = BASE_DIR / "src"

SESSIONS_DIR = DATA_DIR / "sessions"
LOGS_DIR = DATA_DIR / "logs"

IGNORE_LIST = DATA_DIR / "ignore_list.json"
CONFIG_DIR = SRC_DIR / "config"
