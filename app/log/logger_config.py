
import logging
from pathlib import Path
from logging.handlers import RotatingFileHandler

# 현재 log 폴더
LOG_DIR = Path(__file__).resolve().parent
LOG_DIR.mkdir(parents=True, exist_ok=True)


def create_file_handler(filename, level=logging.INFO):
    """로그 파일 핸들러 생성."""
    handler = RotatingFileHandler(
        LOG_DIR / filename,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    handler.setLevel(level)
    handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(levelname)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    )
    return handler


# 1. 사용자 행동 로그
action_logger = logging.getLogger("action_logger")
action_logger.setLevel(logging.INFO)
action_logger.propagate = False

if not action_logger.handlers:
    action_logger.addHandler(create_file_handler("action.log"))


# 2. HTTP 요청 로그
access_logger = logging.getLogger("werkzeug")
access_logger.setLevel(logging.INFO)

if not access_logger.handlers:
    access_logger.addHandler(create_file_handler("access.log"))


# 3. 애플리케이션 에러 로그
error_logger = logging.getLogger("app_error")
error_logger.setLevel(logging.WARNING)
error_logger.propagate = False

if not error_logger.handlers:
    error_logger.addHandler(create_file_handler("error.log"))
