from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
import json

# GPT 기반 음식 추천 에이전트 구성
llm = ChatOpenAI(
    model=OPENAI_MODEL,                     # 사용할 GPT 모델 이름
    api_key=OPENAI_API_KEY,                # .env에서 불러온 API 키
    temperature=0.5,                       # 결과 다양성 조절
    model_kwargs={
        "response_format": {"type": "json_object"}  # JSON 형식 강제
    }
)


# 프롬프트에 `관련된 음식 또는 어울리는 음식으로 추천해도 좋습니다.` 이 들어가니까 결과가 좋아졌다고 한다.
def recommend_food(state: dict) -> dict:
    """
    사용자의 입력과 계절, 날씨, 시간대 정보를 기반으로
    GPT를 통해 음식 추천을 생성하는 함수입니다.
    """

    # 상태에서 필요한 정보 추출
    user_input = state.get("user_input", "")
    season = state.get("season", "봄")
    weather = state.get("weather", "Clear")
    time_slot = state.get("time_slot", "점심")

    # GPT에게 보낼 프롬프트 정의 (f-string 내부 문자열은 안전하게 작성)
    prompt = f"""당신은 음식 추천 AI입니다.

사용자 입력: "{user_input}"
현재 조건:
- 계절: {season}
- 날씨: {weather}
- 시간대: {time_slot}

이 조건에 어울리는 음식 2가지를 추천해 주세요.

사용자가 특정 음식을 언급한 경우(예: "피자")에는 그 음식을 포함하거나,
관련된 음식 또는 어울리는 음식으로 추천해도 좋습니다.

결과는 반드시 JSON 배열 형식으로 출력하세요.
예: ["피자", "떡볶이"]
"""  # f-string 끝

    # GPT 호출 실행
    response = llm.invoke([{"role": "user", "content": prompt.strip()}])

    # 응답 내용을 JSON으로 파싱
    items = json.loads(response.content)

    #### 응답의 모든 가능성에 대해 처리 해야 한다.
    # 응답이 딕셔너리일 경우 → 값만 추출
    if isinstance(items, dict):
        items = [i for sub in items.values() for i in (sub if isinstance(sub, list) else [sub])]
    elif not isinstance(items, list):
        items = [str(items)]  # 리스트가 아니면 리스트로 감싸기

    # 추천 음식 리스트를 상태에 추가하여 반환
    return {**state, "recommended_items": items}
    