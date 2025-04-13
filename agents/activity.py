from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
import json

# GPT 기반 활동 추천 에이전트 구성
llm = ChatOpenAI(
    model=OPENAI_MODEL,                    # 사용할 GPT 모델 이름
    api_key=OPENAI_API_KEY,               # OpenAI API 키 (환경변수에서 불러옴)
    temperature=0.5,                      # 창의성 제어 (중간값)
    model_kwargs={                        # 응답 형식 명시
        "response_format": {"type": "json_object"}
    }
)

def recommend_activity(state: dict) -> dict:
    """
    GPT를 사용하여 사용자의 상황과 입력을 기반으로
    추천할 활동 2가지를 생성하는 함수입니다.
    """

    # 입력 상태에서 정보 추출
    user_input = state.get("user_input", "")
    season = state.get("season", "봄")
    weather = state.get("weather", "Clear")
    time_slot = state.get("time_slot", "점심")

    # GPT에게 활동 추천을 요청할 프롬프트 작성
    prompt = f"""당신은 활동 추천 AI입니다.

사용자 입력: "{user_input}"
현재 조건:
- 계절: {season}
- 날씨: {weather}
- 시간대: {time_slot}

이 조건과 입력에 어울리는 활동 2가지를 추천해 주세요.
실내 활동이 포함되면 더 좋습니다.

결과는 반드시 JSON 배열 형식으로 출력하세요.
예: ["북카페 가기", "실내 보드게임"]
"""  # 안전한 f-string

    # GPT 호출
    response = llm.invoke([{"role": "user", "content": prompt.strip()}])

    # GPT 응답 파싱
    items = json.loads(response.content)

    # dict 형태 응답 → 값만 리스트로 추출
    if isinstance(items, dict):
        items = [i for sub in items.values() for i in (sub if isinstance(sub, list) else [sub])]
    elif not isinstance(items, list):
        items = [str(items)]  # 단일 문자열을 리스트로 감싸기

    # 추천 활동을 상태에 추가하여 반환
    return {**state, "recommended_items": items}
    