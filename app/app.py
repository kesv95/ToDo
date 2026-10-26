
from flask import Flask, request, jsonify
from werkzeug.exceptions import HTTPException
from pathlib import Path

from database.learning_repository import init_db
from routes.weather_routes import weather_bp
from routes.learning_routes import learning_bp
from routes.log_routes import log_bp
from view_helpers import render_home
from log.logger_config import error_logger

app = Flask(__name__)


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


# 메인 페이지
@app.route("/")
def home():
    return render_home()


@app.after_request
def log_response_status(response):
    if response.status_code == 200 and request.path == "/":
        print("HTTPStatus 200")

    return response


# 서버 실행
if __name__ == "__main__":
    init_db()

    cert_path = Path(__file__).with_name("localhost.pem")
    key_path = Path(__file__).with_name("localhost-key.pem")

    app.run(
        debug=True,
        ssl_context=(str(cert_path), str(key_path))
    )
