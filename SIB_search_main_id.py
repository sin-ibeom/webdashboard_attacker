import requests
import json
import re


def extract_padlet_ids_final(padlet_url):
    padlet_url = re.sub(r'^https?://+:?//?', 'https://', padlet_url)
    padlet_url = re.sub(r'^(https?):/{3,}', r'\1://', padlet_url)

    # 봇 제한 방지 < 인터넷에서 따옴 >
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                      "(KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Referer": "https://padlet.com"
    }

    try:
        response = requests.get(padlet_url, headers=headers, timeout=10)
        html_content = response.text

        if response.status_code != 200:
            print(f"[실패] HTTP {response.status_code} — URL이 맞는지 먼저 확인하세요: {padlet_url}")
            return None

        wall_id = None
        data = {}
        start_keyword = "window.$pepinTraits"

        if start_keyword in html_content:
            start_idx = html_content.find(start_keyword)
            json_start_idx = html_content.find('{', start_idx)

            if json_start_idx != -1:
                brace_count = 0
                json_end_idx = -1
                for i in range(json_start_idx, len(html_content)):
                    if html_content[i] == '{':
                        brace_count += 1
                    elif html_content[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            json_end_idx = i + 1
                            break
                if json_end_idx != -1:
                    json_str = html_content[json_start_idx:json_end_idx]
                    data = json.loads(json_str)
                    wall_id = data.get("wallId")

        wall_hashid = (
            data.get("hashid")
            or data.get("wallHashid")
            or data.get("boardHashid")
        )

        if not wall_hashid:
            hashid_match = re.search(r'\b(board_[A-Za-z0-9]+)\b', html_content)
            wall_hashid = hashid_match.group(1) if hashid_match else None

        hash_match = re.search(r'padlet\.com/(?:[^/?#]+/)?([^/?#]+)', padlet_url)
        board_hashid = hash_match.group(1) if hash_match else None

        if wall_hashid or wall_id or board_hashid:
            return {"wall_id": wall_id, "wall_hashid": wall_hashid, "board_hashid": board_hashid}
        else:
            print("[실패] 데이터 추출에 실패했습니다.")
            return None

    except requests.exceptions.RequestException as e:
        print(f"[요청 에러] {str(e)}")
        return None
    except Exception as e:
        print(f"[에러 발생] {str(e)}")
        return None