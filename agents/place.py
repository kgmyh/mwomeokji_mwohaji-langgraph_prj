import requests
from config import KAKAO_API_KEY

def search_place(state: dict) -> dict:
    """
    사용자의 지역 정보(location)와 검색 키워드(search_keyword)를 바탕으로
    Kakao Local API를 호출하여 근처 장소 정보를 가져오는 함수입니다.
    """

    # 상태에서 검색 키워드 및 지역 정보 추출
    location = state.get("location", "홍대")               # 예: "홍대"
    keyword = state.get("search_keyword", "추천")          # 예: "한식", "북카페"

    # 검색어는 '지역 + 키워드' 조합으로 구성. 공백으로 연결해 전형적인 키워드 검색의 **키워드 형식**으로 만듬.
    query = f"{location} {keyword}"
    print(">>> GPT 생성 키워드 검색:", query)  # 디버깅용 로그

    # Kakao Local Search API endpoint
    url = "https://dapi.kakao.com/v2/local/search/keyword.json"
    headers = {
        "Authorization": f"KakaoAK {KAKAO_API_KEY}"  # API 키 인증
    }
    params = {
        "query": query,   # 검색어
        "size": 5         # 최대 5개의 결과 요청
    }

    # API 요청 전송
    res = requests.get(url, headers=headers, params=params)
    res.raise_for_status()  # 요청 실패 시 예외 발생

    # 응답 결과 중 첫 번째 장소만 사용
    docs = res.json()["documents"]

    if docs:
        top = docs[0]  # 가장 관련성 높은 장소 (***************************랭킹이 가장 높은 것이므로. 여러 검색결과를 다 보여줄 거면 그에 맞게 고친다.)
        ### 카카오에서 주는 결과에는 더 많은 내용이 있으므로 그것들 넣어도 된다.
        place = {
            "name": top["place_name"],               # 장소 이름
            "address": top["road_address_name"],     # 도로명 주소
            "url": top["place_url"]                  # 지도 링크
        }
    else:
        # 검색 결과 없을 경우 기본 메시지
        place = {
            "name": "추천 장소 없음",
            "address": "",
            "url": ""
        }

    # 추천 장소 정보를 상태에 추가하여 반환
    return {**state, "recommended_place": place}
    