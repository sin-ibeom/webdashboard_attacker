import os

from Tools.scripts.fixcid import Number
from flask import Flask, render_template, request, session, url_for, redirect, jsonify

import SIB_attack
from SIB_search_main_id import *
from SIB_search_sub import *
from SIB_attack import *

# 아이디
# 섹션 아이디
# 양

MAIN_ID = 000000
SECTION_ID = 000000
QUANTITY = 0

current_dir = os.path.dirname(os.path.abspath(__file__))
app = Flask(__name__)
app.secret_key = 'SIB1214'


# 로그인 페이지
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if session.get("id") == "admin" and session.get("pw") == "1214":
        return redirect(url_for('dashboard'))


    info_data = {
        "id": request.form.get('id'),
        "pw": request.form.get('pw'),
    }

    if request.method == 'POST':
        info_data['id'] = request.form.get("id")
        info_data['pw'] = request.form.get("pw")

    if (info_data['id'] == "admin" and info_data['pw'] == "1214") or (session.get("id") == "admin" and session.get("pw") == "1214"):
        session["id"] = info_data['id']
        session["pw"] = info_data['pw']
        return redirect(url_for('dashboard'))
    elif not (info_data["id"] is None and info_data["pw"] is None):
        info_data["fail"] = "아이디 또는 비밀번호가 맞지 않습니다."
        if info_data["id"] == "" or info_data["pw"] == "":
            print(info_data["id"], info_data["pw"])
            info_data["fail"] = "아이디 또는 비밀번호를 입력하세요"

    return (render_template('login.html', info=info_data))


@app.route('/dashboard')
def dashboard():
    if session.get("id") == "admin" and session.get("pw") == "1214":
        print(session["id"])
        return render_template('dashboard.html')
    else:
        return redirect(url_for('login'))


@app.route('/get_data', methods=['POST', 'GET'])
def get_data():
    if request.method == 'POST':
        req_data = request.get_json()

    pattern = r"^https://padlet\.com/[\w-]+/[\w-]+$"
    if re.match(pattern, req_data["url"]):
        url = req_data["url"]

        result = extract_padlet_ids_final(url)

        sec_dict = run_search(result["wall_id"])

        session["MAIN_ID"] = result["wall_id"]

        return jsonify({
            "wall_hashid": result["wall_hashid"],
            "wall_id": result["wall_id"],
            "sec_json": sec_dict  # { "123": "title1", "345": "title2" }
        })
    else:
        return jsonify({"message": "[오류] 링크를 형식에 맞춰 적어주세요."})


@app.route('/attack', methods=['POST', 'GET'])
def start_attack():
    req_data = request.get_json()
    MAIN_ID = session.get("MAIN_ID", 0)
    QUANTITY = req_data["quantity"]
    if QUANTITY == "":
        QUANTITY = 1
    SECTION_ID = req_data["Sec111"]
    print("------------")
    print(MAIN_ID)
    print(QUANTITY)
    print(SECTION_ID)

    if (int(MAIN_ID) > 999 and int(QUANTITY) >= 1 and len(SECTION_ID) >= 1):
        if(int(QUANTITY) >= 50):
            QUANTITY = 50

        SIB.add_subject("신이범")
        SIB.add_body("고양이")
        SIB.add_attachment(
            "https://tenor.com/view/%EA%B3%A0%EC%96%91%EC%9D%B4-gif-11384361500077789531")
        SIB.set_quantity(int(QUANTITY))
        SIB.set_wall_id(int(MAIN_ID))
        for i in SECTION_ID:
            SIB.set_wall_sec(int(i))
            for msg in SIB.start():
                print(f"실시간 전송 상황: {msg}")

    else :
        return jsonify({"message" : "[오류] 정확한 값을 입력해주세요"})

    return jsonify({"message" : "[SIB] 공격 성공"})
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
