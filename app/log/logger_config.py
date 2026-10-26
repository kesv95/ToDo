
import logging
from pathlib import Path


# 현재 파일이 있는 log 폴더
LOG_DIR = Path(__file__).resolve().parent

# 로그 파일 경로
ACTION_LOG_PATH = LOG_DIR / "action.log"


# 사용자 행동 로그 설정
action_logger = logging.getLogger("action_logger")
action_logger.setLevel(logging.INFO)
action_logger.propagate = False


# 핸들러 중복 등록 방지
if not action_logger.handlers:
    file_handler = logging.FileHandler(
        ACTION_LOG_PATH,
        encoding="utf-8"
    )

    file_handler.setFormatter(
        logging.Formatter(
            "%(asctime)s | %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )
    )

    action_logger.addHandler(file_handler)
