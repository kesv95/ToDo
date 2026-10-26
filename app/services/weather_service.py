
import requests


# 날씨 코드별 한글 설명
WEATHER_CODES = {
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


def get_weather(city):
    """도시 이름을 이용해 현재 날씨 정보를 조회한다."""

    # 1. 도시 이름으로 위치 검색
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
        return None, None

    location = locations[0]

    # 2. 위도와 경도로 현재 날씨 조회
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

    # 3. 화면에 전달할 데이터 구성
    weather_data = {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "description": WEATHER_CODES.get(
            current["weather_code"],
            "기타 날씨"
        ),
        "wind": current["wind_speed_10m"]
    }

    return location["name"], weather_data
