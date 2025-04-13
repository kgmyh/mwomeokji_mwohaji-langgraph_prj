from datetime import datetime

def get_time_slot(state: dict) -> dict:
    """현재 시각을 기준으로 시간대를 분류하여 상태에 추가합니다.

    시간대는 다음과 같이 분류됩니다:
    - 05:00 ~ 11:00 -> '아침'
    - 11:00 ~ 16:00 -> '점심'
    - 16:00 ~ 22:00 -> '저녁'
    - 22:00 ~ 05:00 -> '야간'
    """
    hour = datetime.now().hour  # 현재 시간의 시(hour) 정보를 가져옵니다.

    # 시간에 따라 적절한 시간대를 반환합니다.
    if 5 <= hour < 11:
        return {**state, "time_slot": "아침"}
    elif 11 <= hour < 16:
        return {**state, "time_slot": "점심"}
    elif 16 <= hour < 22:
        return {**state, "time_slot": "저녁"}
    else:
        return {**state, "time_slot": "야간"}  # 22시 이후 또는 5시 이전은 야간으로 처리
        