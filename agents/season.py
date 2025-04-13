from datetime import datetime

def get_season(state: dict) -> dict:
    """현재 월(month)을 기준으로 계절을 분류하여 상태에 추가합니다.

    분류 기준:
    - 3월 ~ 5월   : 봄
    - 6월 ~ 8월   : 여름
    - 9월 ~ 11월  : 가을
    - 12월, 1월, 2월 : 겨울
    """
    month = datetime.now().month  # 현재 월(1~12)을 가져옵니다

    # 월에 따라 계절을 분류합니다
    if 3 <= month <= 5:
        season = "봄"
    elif 6 <= month <= 8:
        season = "여름"
    elif 9 <= month <= 11:
        season = "가을"
    else:
        season = "겨울"  # 12월, 1월, 2월

    # 상태에 계절 정보를 추가해서 반환합니다
    return {**state, "season": season}
    