def intent_unsupported_handler(state: dict) -> dict:
    """
    사용자의 입력이 'food'나 'activity'로 분류되지 않은 경우에 실행되는 에이전트입니다.

    의도가 'unknown'으로 판단되면 추천을 수행하지 않고,
    대신 사용자에게 정중한 안내 메시지를 전달합니다.
    """

    # 안내 메시지를 상태에 추가
    return {
        **state,
        "final_message": "죄송해요! 저는 음식이나 활동 추천만 도와드릴 수 있어요 😊"
    }
    