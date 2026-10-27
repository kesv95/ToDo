
from flask import Blueprint, request

from services.weather_service import get_weather
from view_helpers import render_home


weather_bp = Blueprint("weather", __name__)


# 화면에 표시할 도시 이름
CITY_NAMES = {
    "Gangwon": "강원",
    "Seoul": "서울",
    "Gyeonggi": "경기",
    "Sejong": "세종",
    "Daejeon": "대전",
    "Jeolla": "전라",
    "Gyeongsang": "경상",
    "Busan": "부산",
    "Jeju": "제주",
    "Hokkaido": "홋카이도",
    "Tokyo": "도쿄",
    "Nagoya": "나고야",
    "Osaka": "오사카",
    "Washington": "워싱턴",
    "New York": "뉴욕",
    "Chicago": "시카고",
    "Texas": "텍사스",
    "Edinburgh": "에든버러",
    "London": "런던",
    "Manchester": "맨체스터",
    "Paris": "파리",
    "Nice": "니스",
    "Marseille": "마르세유",
}


# 날씨 검색
@weather_bp.route("/weather", methods=["POST"])
def weather():
    """도시 이름을 받아 날씨 정보를 조회한다."""

    city = request.form.get("city", "").strip()

    if not city:
        return render_home(
            error="도시 이름을 입력해 주세요."
        )

    # 화면에는 선택한 도시의 한글 이름을 표시한다.
    city_name = CITY_NAMES.get(city, city)

    try:
        location_name, weather_data = get_weather(city)

        if not location_name or not weather_data:
            return render_home(
                city=city_name,
                error="도시를 찾을 수 없습니다."
            )

        return render_home(
            city=city_name,
            weather=weather_data
        )

    except Exception:
        return render_home(
            city=city_name,
            error=(
                "날씨 정보를 가져오지 못했습니다. "
                "인터넷 연결을 확인해 주세요."
            )
        )
