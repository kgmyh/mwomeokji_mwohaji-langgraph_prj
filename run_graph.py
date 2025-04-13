from langgraph.graph import StateGraph, END
from typing_extensions import TypedDict

# 각 단계에서 사용할 에이전트 함수들 불러오기
from agents.intent import classify_intent
from agents.time import get_time_slot
from agents.season import get_season
from agents.weather import get_weather
from agents.food import recommend_food
from agents.activity import recommend_activity
from agents.keyword import generate_search_keyword
from agents.place import search_place
from agents.summary import summarize_message
from agents.intent_unsupported import intent_unsupported_handler

# 상태(State) 타입 정의
# LangGraph에서 상태는 모든 노드 간에 주고받는 정보를 의미하며,
# 어떤 정보를 다룰지 명확히 정의해 줍니다.
class State(TypedDict):
    user_input: str                # 사용자의 입력 문장
    location: str                  # 지역 정보 (예: "홍대")
    time_slot: str                 # 시간대 (예: "아침", "점심", "야간")
    season: str                    # 계절 (예: "봄", "가을")
    weather: str                   # 날씨 상태 (예: "Rain", "Clear")
    intent: str                    # 분류된 의도 ("food", "activity", "unknown")
    recommended_items: list        # 추천 음식 또는 활동 리스트
    search_keyword: str            # 장소 검색용 키워드
    recommended_place: dict        # 장소 추천 결과 (name, address, url)
    final_message: str             # GPT가 생성한 최종 안내 메시지

# LangGraph builder 생성
builder = StateGraph(State)

# 각 노드에 이름을 붙여 LangGraph에 등록
builder.add_node("classify_intent", classify_intent)
builder.add_node("get_time_slot", get_time_slot)
builder.add_node("get_season", get_season)
builder.add_node("get_weather", get_weather)
builder.add_node("recommend_food", recommend_food)
builder.add_node("recommend_activity", recommend_activity)
builder.add_node("generate_search_keyword", generate_search_keyword)
builder.add_node("search_place", search_place)
builder.add_node("summarize_message", summarize_message)
builder.add_node("intent_unsupported", intent_unsupported_handler)

# 의도(intent)에 따라 음식 추천 / 활동 추천 / 종료 노드를 분기하는 함수
def route_intent(state: State) -> str:
    intent = state.get("intent", "")
    if intent == "food":
        return "recommend_food"
    elif intent == "activity":
        return "recommend_activity"
    return "intent_unsupported"  # intent가 unknown이면 graceful 종료로 분기

# 흐름 연결
builder.set_entry_point("classify_intent")
builder.add_edge("classify_intent", "get_time_slot")
builder.add_edge("get_time_slot", "get_season")
builder.add_edge("get_season", "get_weather")

# 분기 처리: intent에 따라 추천 경로 달라짐
builder.add_conditional_edges("get_weather", route_intent, {
    "recommend_food": "recommend_food",
    "recommend_activity": "recommend_activity",
    "intent_unsupported": "intent_unsupported"
})

# 공통 후처리 흐름
builder.add_edge("recommend_food", "generate_search_keyword")
builder.add_edge("recommend_activity", "generate_search_keyword")
builder.add_edge("generate_search_keyword", "search_place")
builder.add_edge("search_place", "summarize_message")

# 종료 처리
builder.add_edge("summarize_message", END)
builder.add_edge("intent_unsupported", END)

# 그래프 최종 컴파일
graph = builder.compile()

