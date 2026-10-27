
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
    95: "뇌우",
}


# 주요 도시의 정확한 좌표
# 좌표를 지정한 도시는 지오코딩 검색 결과에 의존하지 않는다.
CITY_COORDINATES = {
    "New York": {
        "name": "New York",
        "latitude": 40.7128,
        "longitude": -74.0060,
    },
    "Washington": {
        "name": "Washington",
        "latitude": 38.9072,
        "longitude": -77.0369,
    },
    "Chicago": {
        "name": "Chicago",
        "latitude": 41.8781,
        "longitude": -87.6298,
    },
    "London": {
        "name": "London",
        "latitude": 51.5072,
        "longitude": -0.1276,
    },
    "Paris": {
        "name": "Paris",
        "latitude": 48.8566,
        "longitude": 2.3522,
    },
    "Tokyo": {
        "name": "Tokyo",
        "latitude": 35.6762,
        "longitude": 139.6503,
    },
}


def get_weather(city):
    """도시 이름으로 현재 날씨 정보를 조회한다."""

    # 1. 주요 도시는 미리 지정한 좌표를 사용한다.
    location = CITY_COORDINATES.get(city)

    # 2. 좌표가 지정되지 않은 지역은 지오코딩 API로 검색한다.
    if location is None:
        geo_response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={
                "name": city,
                "count": 10,
                "language": "en",
                "format": "json",
            },
            timeout=10,
        )
        geo_response.raise_for_status()

        locations = geo_response.json().get("results", [])

        if not locations:
            return None, None

        # 검색어와 이름이 정확히 일치하는 결과를 우선한다.
        exact_matches = [
            item for item in locations
            if item.get("name", "").casefold() == city.casefold()
        ]

        location = (
            exact_matches[0]
            if exact_matches
            else locations[0]
        )

    # 3. 위도와 경도로 현재 날씨 조회
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
            "timezone": "auto",
        },
        timeout=10,
    )
    response.raise_for_status()

    current = response.json()["current"]

    # 4. 화면에 전달할 데이터 구성
    weather_data = {
        "temperature": current["temperature_2m"],
        "humidity": current["relative_humidity_2m"],
        "description": WEATHER_CODES.get(
            current["weather_code"],
            "기타 날씨",
        ),
        "wind": current["wind_speed_10m"],
    }

    return location["name"], weather_data
