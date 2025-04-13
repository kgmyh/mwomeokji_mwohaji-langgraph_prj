from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

# GPT 기반 최종 요약 메시지 생성 에이전트 구성
llm = ChatOpenAI(
    model=OPENAI_MODEL,                     # 사용할 GPT 모델 이름
    api_key=OPENAI_API_KEY,                 # OpenAI API 키
    temperature=0.7                         # 창의성 높임 (*********감성적 문장 유도)
)

def summarize_message(state: dict) -> dict:
    """
    추천된 음식/활동, 장소, 시간대 정보를 바탕으로
    사용자에게 보여줄 감성적인 요약 문장을 생성하는 함수입니다.
    """

    # 추천 항목 리스트에서 첫 항목 추출
    items = state.get("recommended_items", ["추천 항목 없음"])
    if isinstance(items, dict):
        items = list(items.values())
    elif not isinstance(items, list):
        items = [str(items)]
    item = items[0]  # 요약 문장에 사용할 대표 항목

    # 상태에서 필요한 정보 추출
    season = state.get("season", "")
    weather = state.get("weather", "")
    time_slot = state.get("time_slot", "")
    intent = state.get("intent", "food")
    place = state.get("recommended_place", {})

    # 장소 정보 추출
    place_name = place.get("name", "추천 장소")
    place_address = place.get("address", "")
    place_url = place.get("url", "")

    # food 또는 activity에 따라 안내 메시지 스타일 조정
    category = "음식" if intent == "food" else "활동"

    # GPT 프롬프트 구성 **************** 네가지 구성이 안나눠져 있다. 좀 더 튜닝해야 할 필요 있다. ******************
    prompt = f"""
사용자의 의도는 '{category}'입니다.
현재는 {season}이고, 날씨는 {weather}, 시간대는 {time_slot}입니다.
추천 {category}: {item}
추천 장소: {place_name} ({place_address})
지도 링크: {place_url}

이 정보를 바탕으로 사용자에게 감성적이고 따뜻한 문장으로 한 문단의 추천 메시지를 작성해 주세요.
"""

    # GPT 호출
    response = llm.invoke([
        {"role": "system", "content": "너는 음식 또는 활동을 추천하는 친절한 AI야."},
        {"role": "user", "content": prompt.strip()}
    ])

    # 최종 문장을 상태에 추가하여 반환
    return {**state, "final_message": response.content.strip()}
    