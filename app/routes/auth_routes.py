
from flask import Blueprint, session, redirect, url_for
from datetime import datetime

from extensions import oauth
from database.learning_repository import save_user, save_record
from services.learning_service import diagnose_learning

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login/google")
def google_login():
    redirect_uri = url_for(
        "auth.google_callback",
        _external=True
    )

    return oauth.google.authorize_redirect(
        redirect_uri,
        prompt="select_account"
    )


@auth_bp.route("/auth/google/callback")
def google_callback():
    """Google 로그인 완료 후 회원 및 대기 중인 진단을 처리한다."""

    token = oauth.google.authorize_access_token()
    userinfo = token["userinfo"]

    user_id = userinfo["sub"]
    name = userinfo.get("name", "")
    email = userinfo.get("email", "")

    # 로그인 전 임시 보관한 값은 세션을 초기화하기 전에 가져온다.
    pending_diagnosis = session.get("pending_diagnosis")

    # Google 로그인 사용자를 DB에 저장
    save_user(
        user_id=user_id,
        name=name,
        email=email
    )

    # 기존 세션을 초기화하고 로그인 사용자 정보 설정
    session.clear()
    session["user"] = {
        "id": user_id,
        "name": name,
        "email": email
    }

    # 로그인 전에 대기 중이던 두 번째 진단 처리
    if pending_diagnosis:
        study = pending_diagnosis["study"]
        plan = pending_diagnosis["plan"]
        review = pending_diagnosis["review"]
        category = pending_diagnosis["category"]

        score, diagnosis, advice = diagnose_learning(
            study=study,
            plan=plan,
            review=review
        )

        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        save_record(
            user_id=user_id,
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


@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))
