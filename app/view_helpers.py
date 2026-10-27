from flask import render_template, session

from database.learning_repository import get_records


def render_home(**kwargs):
    """로그인 상태에 따라 학습 기록을 조회한다."""
    user = session.get("user")

    if user and user.get("id"):
        records = get_records(user_id=user["id"])
    else:
        records = session.get("guest_records", [])

    return render_template(
        "index.html",
        records=records,
        user=user,
        **kwargs
    )