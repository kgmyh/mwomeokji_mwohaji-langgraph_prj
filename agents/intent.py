from langchain_openai import ChatOpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL
import json

# GPT 기반 의도 분류 에이전트 설정
# 사용자의 입력 문장을 기반으로 food / activity / unknown 중 하나로 분류합니다.
llm = ChatOpenAI(
    model=OPENAI_MODEL,                    # 사용할 OpenAI 모델 (예: gpt-4o)
    api_key=OPENAI_API_KEY,               # 환경변수에서 불러온 OpenAI API 키
    temperature=0.3,                      # 창의성 제어 (낮을수록 일관성 ↑)
    model_kwargs={                        # OpenAI에 전달할 추가 옵션
        "response_format": {"type": "json_object"}  # 반드시 JSON 객체로 응답 (openai 1.6 형식이 바뀜. type: text, type: json_object 형식으로 지정해야 함. (이전방식(랭체인에는 이전방식으로 해도됨 경고만 뜨고 알아서 처리함): response_format='text' 식 이었다.))
    }
)

def classify_intent(state: dict) -> dict:
    """사용자의 입력 문장을 기반으로 GPT를 호출하여 food, activity, unknown 중 하나의 intent를 분류합니다."""
    user_input = state.get("user_input", "")  # 사용자의 입력 문장 추출

    # GPT에게 의도를 분류하도록 요청할 프롬프트 
    prompt = f"""
당신은 사용자의 자연어 입력을 food / activity / unknown 중 하나로 분류하는 AI입니다.

입력: "{user_input}"

분류 기준:
- 음식 관련 표현 → "food" (예: 배고파, 뭐 먹지, 야식 추천해줘 등)
- 활동 관련 표현 → "activity" (예: 심심해, 뭐 하지, 놀고 싶어 등)
- 증상, 감정, 질문, 애매한 표현 → "unknown"

조금 애매한 표현이라도 의미가 보이면 food 또는 activity로 분류하세요.

출력은 반드시 다음 중 하나의 JSON 배열 또는 객체로 작성하세요:
- 배열: ["food"]
- 객체: {{ "intent": ["food"] }}
"""

    # GPT 호출
    response = llm.invoke([{"role": "user", "content": prompt.strip()}])

    # GPT의 응답 원문을 출력 (디버깅용)
    intent_raw = response.content.strip()
    print(">>> GPT intent 응답:", intent_raw)

    try:
        # 응답을 JSON으로 파싱
        parsed = json.loads(intent_raw)

        # case 1: 응답이 배열 형태일 경우 (예: ["food"])
        if isinstance(parsed, list) and parsed and parsed[0] in ["food", "activity"]:
            return {**state, "intent": parsed[0]}

        # case 2: 응답이 딕셔너리 형태일 경우 (예: {"intent": ["activity"]})
        if isinstance(parsed, dict):
            if "intent" in parsed:
                inner = parsed["intent"]
                if isinstance(inner, list) and inner and inner[0] in ["food", "activity"]:  #value가 list이면.
                    return {**state, "intent": inner[0]}
            # fallback: GPT가 "food": [] 또는 "activity": [] 형식으로 응답했을 경우
            for key in ["food", "activity"]:
                if key in parsed:
                    return {**state, "intent": key}

    except Exception as e:
        print(">>> intent 분류 파싱 실패:", str(e))

    # 모든 조건 실패 시 unknown으로 처리
    return {**state, "intent": "unknown"}
    