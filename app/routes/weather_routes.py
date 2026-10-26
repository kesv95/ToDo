
from flask import Blueprint, request

from services.weather_service import get_weather
from view_helpers import render_home


weather_bp = Blueprint("weather", __name__)


# 날씨 검색
@weather_bp.route("/weather", methods=["POST"])
def weather():
    """도시 이름을 받아 날씨 정보를 조회한다."""

    city = request.form.get("city", "").strip()

    if not city:
        return render_home(
            error="도시 이름을 입력해 주세요."
        )

    try:
        location_name, weather_data = get_weather(city)

        if not location_name or not weather_data:
            return render_home(
                city=city,
                error="도시를 찾을 수 없습니다."
            )

        return render_home(
            city=location_name,
            weather=weather_data
        )

    except Exception:
        return render_home(
            city=city,
            error=(
                "날씨 정보를 가져오지 못했습니다. "
                "인터넷 연결을 확인해 주세요."
            )
        )
