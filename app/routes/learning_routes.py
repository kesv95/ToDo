from flask import (
    Blueprint, request, redirect, url_for, session
)
from datetime import datetime

from database.learning_repository import save_record
from services.learning_service import diagnose_learning

learning_bp = Blueprint("learning", __name__)


@learning_bp.route("/diagnose", methods=["POST"])
def diagnose():
    """학습 정보를 진단하고 로그인 상태에 따라 저장한다."""

    user = session.get("user")

    # 비회원은 진단 결과를 1회만 저장할 수 있다.
    if not (user and user.get("id")):
        guest_records = session.get("guest_records", [])

        if guest_records:
            return redirect(url_for("home", guest_limit=1))

    try:
        category = int(request.form["category"])
        study = int(request.form["study"])
        plan = int(request.form["plan"])
        review = int(request.form["review"])

        if category < 1:
            return "입력값이 올바르지 않습니다.", 400

        if not all(
            1 <= value <= 4
            for value in (study, plan, review)
        ):
            return "입력값이 올바르지 않습니다.", 400

    except (ValueError, KeyError):
        return "올바른 학습 정보를 입력해 주세요.", 400

    score, diagnosis, advice = diagnose_learning(
        study=study,
        plan=plan,
        review=review
    )

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    record = {
        "category": category,
        "study": study,
        "plan": plan,
        "review": review,
        "score": score,
        "diagnosis": diagnosis,
        "advice": advice,
        "created_at": created_at
    }

    if user and user.get("id"):
        # 로그인 사용자: DB에 저장
        save_record(
            user_id=user["id"],
            category=category,
            study=study,
            plan=plan,
            review=review,
            score=score,
            diagnosis=diagnosis,
            advice=advice,
            created_at=created_at
        )
    else:
        # 비회원: 세션에 결과 1개만 저장
        session["guest_records"] = [record]
        session.permanent = True

    return redirect(url_for("home"))