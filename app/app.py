from flask import Flask

from database.learning_repository import init_db
from routes.weather_routes import weather_bp
from routes.learning_routes import learning_bp
from view_helpers import render_home
from log.logger_config import action_logger
from routes.log_routes import log_bp
app = Flask(__name__)


# 라우트 등록
app.register_blueprint(weather_bp)
app.register_blueprint(learning_bp)
app.register_blueprint(log_bp)

# 메인 페이지
@app.route("/")
def home():
    return render_home()


# if __name__ == "__main__":
#     init_db()
#     app.run(debug=True)
if __name__ == "__main__":
    init_db()

    app.run(debug=True)