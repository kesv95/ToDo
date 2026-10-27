
import os
from dotenv import load_dotenv

from flask import Flask, request, jsonify, render_template
from werkzeug.exceptions import HTTPException
from pathlib import Path

from database.learning_repository import init_db
from routes.weather_routes import weather_bp
from routes.learning_routes import learning_bp
from routes.log_routes import log_bp
from routes.auth_routes import auth_bp
from view_helpers import render_home
from log.logger_config import error_logger
from extensions import oauth


# 프로젝트 루트의 .env 파일 읽기
load_dotenv()


# Flask 앱 생성
app = Flask(__name__)


# Flask 세션 보안 키 설정
app.config["SECRET_KEY"] = os.getenv("FLASK_SECRET_KEY")

if not app.config["SECRET_KEY"]:
    raise RuntimeError(
        "FLASK_SECRET_KEY가 .env 파일에 설정되지 않았습니다."
    )


# Google OAuth 초기화
oauth.init_app(app)

oauth.register(
    name="google",
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url=(
        "https://accounts.google.com/.well-known/openid-configuration"
    ),
    client_kwargs={
        "scope": "openid email profile"
    },
)


# HTTP 오류 처리: 404, 400, 403, 405 등
@app.errorhandler(HTTPException)
def handle_http_error(error):
    """HTTP 오류를 로그 파일에 기록한다."""

    error_logger.warning(
        "HTTP 오류 | status=%s | path=%s | description=%s",
        error.code,
        request.path,
        error.description
    )

    # Flask의 원래 HTTP 오류 응답을 유지한다.
    return error


# 예상하지 못한 서버 내부 오류 처리
@app.errorhandler(Exception)
def handle_unexpected_error(error):
    """처리되지 않은 예외를 로그 파일에 기록한다."""

    error_logger.exception(
        "서버 내부 오류 | path=%s",
        request.path
    )

    return jsonify({
        "error": "Internal Server Error",
        "message": "서버 내부 오류가 발생했습니다."
    }), 500


# 블루프린트 등록
app.register_blueprint(weather_bp)
app.register_blueprint(learning_bp)
app.register_blueprint(log_bp)
app.register_blueprint(auth_bp)


# 메인 페이지
@app.route("/")
def home():
    return render_home()


# 응답 상태 로그
@app.after_request
def log_response_status(response):
    return response


# 자기소개 페이지
@app.route("/about")
def about():
    return render_template("about.html")


# 서버 실행
if __name__ == "__main__":
    init_db()

    cert_path = Path(__file__).with_name("localhost.pem")
    key_path = Path(__file__).with_name("localhost-key.pem")

    app.run(
        debug=False,
        ssl_context=(str(cert_path), str(key_path))
    )
