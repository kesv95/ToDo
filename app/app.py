from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from pathlib import Path
from datetime import datetime
import requests

app = Flask(__name__)

DB_PATH = Path(__file__).resolve().parent / "learning.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS learning_records (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category INTEGER NOT NULL,
                study INTEGER NOT NULL,
                plan INTEGER NOT NULL,
                review INTEGER NOT NULL,
                score INTEGER NOT NULL,
                diagnosis TEXT NOT NULL,
                advice TEXT NOT NULL,
                created_at TEXT NOT NULL
            )
        """)


def get_records():
    with get_db() as conn:
        return conn.execute("""
            SELECT *
            FROM learning_records
            ORDER BY id DESC
            LIMIT 10
        """).fetchall()


def render_home(**kwargs):
    return render_template(
        "index.html",
        records=get_records(),
        **kwargs
    )


@app.route("/")
def home():
    return render_home()


@app.route("/diagnose", methods=["POST"])
def diagnose():
    try:
        category = int(request.form["category"])
        study = int(request.form["study"])
        plan = int(request.form["plan"])
        review = int(request.form["review"])

        if not all(1 <= value <= 4
                   for value in (study, plan, review)):
            return "입력값이 올바르지 않습니다.", 400

    except (ValueError, KeyError):
        return "올바른 학습 정보를 입력해 주세요.", 400

    score = study + plan + review

    if score >= 10:
        diagnosis = "우수한 학습 습관입니다!"
        advice = "현재의 공부 습관을 유지하고 심화 학습에 도전하세요."
    elif score >= 7:
        diagnosis = "양호하지만 개선할 부분이 있어요."
        advice = "공부 계획을 세우고 배운 내용을 꾸준히 복습하세요."
    else:
        diagnosis = "학습 습관을 조금씩 만들어 보세요."
        advice = "하루 20분부터 시작해 작은 목표를 실천하세요."

    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with get_db() as conn:
        conn.execute("""
            INSERT INTO learning_records
            (category, study, plan, review,
             score, diagnosis, advice, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            category, study, plan, review, score,
            diagnosis, advice, created_at
        ))

    return redirect(url_for("home"))


@app.route("/weather", methods=["POST"])
def weather():
    city = request.form.get("city", "").strip()

    if not city:
        return render_home(error="도시 이름을 입력해 주세요.")

    try:
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 1,
                "language": "ko",
                "format": "json"
            },
            timeout=10
        )
        geo_response.raise_for_status()
        locations = geo_response.json().get("results", [])

        if not locations:
            return render_home(
                city=city,
                error="도시를 찾을 수 없습니다."
            )

        location = locations[0]

        response = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": location["latitude"],
                "longitude": location["longitude"],
                "current": (
                    "temperature_2m,"
                    "relative_humidity_2m,"
                    "weather_code,"
                    "wind_speed_10m"
                ),
                "timezone": "auto"
            },
            timeout=10
        )
        response.raise_for_status()
        current = response.json()["current"]

        codes = {
            0: "맑음",
            1: "대체로 맑음",
            2: "부분적으로 흐림",
            3: "흐림",
            45: "안개",
            48: "짙은 안개",
            51: "약한 이슬비",
            53: "이슬비",
            55: "강한 이슬비",
            61: "약한 비",
            63: "비",
            65: "강한 비",
            71: "약한 눈",
            73: "눈",
            75: "강한 눈",
            80: "소나기",
            81: "강한 소나기",
            82: "매우 강한 소나기",
            95: "뇌우"
        }

        weather_data = {
            "temperature": current["temperature_2m"],
            "humidity": current["relative_humidity_2m"],
            "description": codes.get(
                current["weather_code"], "기타 날씨"
            ),
            "wind": current["wind_speed_10m"]
        }

        return render_home(
            city=location["name"],
            weather=weather_data
        )

    except (requests.RequestException, KeyError, ValueError):
        return render_home(
            city=city,
            error="날씨 정보를 가져오지 못했습니다. 인터넷 연결을 확인해 주세요."
        )


if __name__ == "__main__":
    init_db()
    app.run(debug=True)