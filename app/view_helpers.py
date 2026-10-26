
from flask import render_template

from database.learning_repository import get_records


def render_home(**kwargs):
    """공통 메인 페이지 렌더링 함수."""

    return render_template(
        "index.html",
        records=get_records(),
        **kwargs
    )
