
from flask import Blueprint, request, redirect, url_for
from datetime import datetime

from database.learning_repository import save_record
from services.learning_service import diagnose_learning


learning_bp = Blueprint("learning", __name__)


@learning_bp.route("/diagnose", methods=["POST"])
def diagnose():
    """학습 정보를 받아 진단 결과를 저장한다."""

    try:
        category = int(request.form["category"])
        study = int(request.form["study"])
        plan = int(request.form["plan"])
        review = int(request.form["review"])

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

    save_record(
        category=category,
        study=study,
        plan=plan,
        review=review,
        score=score,
        diagnosis=diagnosis,
        advice=advice,
        created_at=created_at
    )

    return redirect(url_for("home"))
