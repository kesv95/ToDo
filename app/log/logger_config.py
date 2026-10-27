
import logging
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler

# Vercel에서는 코드 디렉터리에 로그 파일을 쓰지 않고 콘솔에 출력
IS_VERCEL = os.getenv("VERCEL") == "1"

LOG_FORMAT = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)


def create_file_handler(filename, level=logging.INFO):
    """로컬 환경용 로그 파일 핸들러 생성."""
    log_dir = Path(__file__).resolve().parent
    log_dir.mkdir(parents=True, exist_ok=True)

    handler = RotatingFileHandler(
        log_dir / filename,
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8"
    )
    handler.setLevel(level)
    handler.setFormatter(LOG_FORMAT)
    return handler


def configure_logger(name, level=logging.INFO, propagate=False):
    """환경에 맞는 로그 핸들러를 설정."""
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = propagate

    if not logger.handlers:
        if IS_VERCEL:
            handler = logging.StreamHandler()
            handler.setLevel(level)
            handler.setFormatter(LOG_FORMAT)
        else:
            handler = create_file_handler(
                f"{name}.log",
                level
            )

        logger.addHandler(handler)

    return logger


# 1. 사용자 행동 로그
action_logger = configure_logger("action_logger")

# 2. HTTP 요청 로그
access_logger = configure_logger("werkzeug")

# 3. 애플리케이션 에러 로그
error_logger = configure_logger(
    "app_error",
    level=logging.WARNING
)
