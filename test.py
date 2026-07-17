import os
import requests


def run_search_test(wall_id):
    headers = {
        "Authorization": os.environ.get('TOKEN', '0'),
        "Accept": "application/vnd.api+json",
    }

    url = f"https://padlet.com/api/5/wall_sections?wall_id={wall_id}"
    print(f"[요청 URL] {url}")

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"[오류] API 호출 실패 (상태 코드: {response.status_code})")
        print(response.text)
        return

    data = response.json()

    detected_sections = {}

    sections_data = data.get("data", [])

    for item in sections_data:
        sec_id = str(item.get("id"))
        sec_attributes = item.get("attributes", {})

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
    TEST_WALL_ID = "267289200"

    run_search_test(TEST_WALL_ID)