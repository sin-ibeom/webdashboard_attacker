import os
import requests


def run_search(wall_id):  # hashid 대신 wall_id를 받습니다.
    headers = {
        "Authorization": os.environ.get('TOKEN'),
        "Accept": "application/vnd.api+json",
    }

    # 성공했던 전용 API 호출
    url = f"https://padlet.com/api/5/wall_sections?wall_id={wall_id}"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"[오류] API 호출 실패 (상태 코드: {response.status_code})")
        return {}

    data = response.json()
    sec_list = {}

    for item in data.get("data", []):
        sec_id = str(item.get("id"))
        sec_attributes = item.get("attributes", {})
        sec_title = sec_attributes.get("title") or sec_attributes.get("name") or f"섹션 {sec_id}"
        sec_list[sec_id] = sec_title

    return sec_list