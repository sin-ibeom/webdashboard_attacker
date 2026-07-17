import os
import requests


def run_search_test(wall_id):
    # 환경 변수에 TOKEN이 설정되어 있어야 합니다.
    # 테스트 목적이라면 'YOUR_ACTUAL_TOKEN_HERE'에 실제 API 토큰을 입력하세요.
    headers = {
        "Authorization": os.environ.get('TOKEN', 'YOUR_ACTUAL_TOKEN_HERE'),
        "Accept": "application/vnd.api+json",
    }

    # 💡 핵심: 포스트 조회(wishes) 대신, 게시판 고유 ID(숫자)를 이용해 섹션 목록 전체를 다이렉트로 조회합니다.
    url = f"https://padlet.com/api/5/wall_sections?wall_id={wall_id}"
    print(f"[요청 URL] {url}")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"[오류] API 호출 실패 (상태 코드: {response.status_code})")
        print(response.text)
        return

    data = response.json()

    # API 응답 구조를 파싱하여 { "섹션ID": "섹션이름" } 매핑
    detected_sections = {}

    # JSON:API 표준 구조 ('data' 배열 순회)
    sections_data = data.get("data", [])

    for item in sections_data:
        sec_id = str(item.get("id"))
        sec_attributes = item.get("attributes", {})

        # 'title' 또는 'name' 값 추출
        sec_title = (
                sec_attributes.get("title") or
                sec_attributes.get("name") or
                f"이름 없는 섹션 ({sec_id})"
        )
        detected_sections[sec_id] = sec_title

    print("\n================ [최종 수집된 섹션 목록] ================")
    if not detected_sections:
        print("감지된 섹션이 없습니다. (게시판에 섹션 분류 기능이 활성화되어 있지 않을 수 있습니다.)")
    else:
        for s_id, s_title in detected_sections.items():
            print(f"✔️ 섹션 ID: {s_id:12} | 섹션 제목: {s_title}")
    print("========================================================\n")

    return detected_sections


if __name__ == "__main__":
    # 💡 주의: 이 API는 wall_hashid("board_xxx")가 아닌, 메인 숫자 ID("267289200")를 매개변수로 받습니다.
    # 전송해주신 JSON 데이터 상의 wall_id 값인 '267289200'을 대입해 보세요.
    TEST_WALL_ID = "267289200"

    run_search_test(TEST_WALL_ID)