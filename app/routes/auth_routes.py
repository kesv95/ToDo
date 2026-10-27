from flask import Blueprint, session, redirect, url_for
from extensions import oauth
from database.learning_repository import save_user


auth_bp = Blueprint("auth", __name__)


# Google 로그인 시작
@auth_bp.route("/login/google")
def google_login():
    redirect_uri = url_for("auth.google_callback", _external=True)

    return oauth.google.authorize_redirect(
        redirect_uri,
        prompt="select_account"
    )


# Google 로그인 콜백
@auth_bp.route("/auth/google/callback")
def google_callback():
    token = oauth.google.authorize_access_token()
    userinfo = token["userinfo"]

    user_id = userinfo["sub"]
    name = userinfo.get("name", "")
    email = userinfo.get("email", "")

    # DB에 사용자 정보 등록 또는 갱신
    save_user(
        user_id=user_id,
        name=name,
        email=email
    )

    # 로그인 세션 저장
    session.clear()
    session["user"] = {
        "id": user_id,
        "name": name,
        "email": email,
    }

    return redirect(url_for("home"))


# 로그아웃
@auth_bp.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))