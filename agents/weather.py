import os
import requests
from config import WEATHER_API_KEY


# 동기 코드 이므로 지연이 발생한다. 그래서 비동기적 코드로 작성하면 -> 툴로 바꿔 툴노드에 넣고 비동기적 코드로 바꾼다.
# 처음에는 결과를 봐야 하므로 동기적으로 만들지만 asysio를 이용해 비동기 코드로 작성한 뒤 tool_node 등록할 때 비동기적으로 등록한다. --> asynio 이용하는 비동기 코드로 바꿔줘라고 llm에 물어봐서 하자.
# 중요한 것은 버전 체크다. 그래서 구버전 코드여서 안되는 경우가 많다. 그래거 라이브러리 버전을 context에 잘 넣어줘야 한다.
def get_weather(state: dict) -> dict:
    """OpenWeather API를 통해 현재 날씨 정보를 가져와서 상태에 추가합니다.

    현재는 location이 '서울' 기준으로 고정되어 있으며,
    반환되는 날씨 상태는 'Clear', 'Clouds', 'Rain', 'Snow' 등입니다.
    """

    # OpenWeather API 호출 URL과 파라미터 설정
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": "Seoul",   ############################# 여기서 고정했는데 이것을 받아서 처리해야 함.
        "appid": WEATHER_API_KEY,
        "lang": "kr",
        "units": "metric"
    }

    # API 요청 전 로그 출력
    print(">>> OpenWeather API 호출 시작 (서울 기준)")

    # GET 요청을 통해 날씨 정보 요청
    response = requests.get(url, params=params)

    # 응답 코드가 실패일 경우 예외 발생
    response.raise_for_status()

    # 응답에서 날씨 상태 추출
    weather_data = response.json()
    weather = weather_data["weather"][0]["main"]  # 예: 'Clear', 'Rain', 'Clouds'

    # 상태에 날씨 정보 추가 후 반환
    return {**state, "weather": weather}
    