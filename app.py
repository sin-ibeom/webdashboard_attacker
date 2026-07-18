import os
import pymysql
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
app.secret_key = os.environ.get("SECRET_KEY")

# 인코딩 에러 조심하기.
# with open("message.json", "r") as f:
#     msg = json.load(f)

with open("message.json", "r", encoding="UTF-8") as f:
    msg = json.load(f)


# 로그인 페이지
@app.route('/')
def index():
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    db = pymysql.connect(host="localhost", user="root", passwd=os.environ.get("DB_PW"), db="user")
    cursor = db.cursor()
    sql = "select * from account WHERE NAME = %s and PASSWORD = %s"
    cursor.execute(sql, (session.get("id"), session.get("pw")))
    _l = cursor.fetchone()

    # 로그인 한적이 있는지 검증
    if _l:
        return redirect(url_for('dashboard'))


    info_data = {
        "id": request.form.get('id'),
        "pw": request.form.get('pw')
    }

    if request.method == 'POST':
        info_data['id'] = request.form.get("id")
        info_data['pw'] = request.form.get("pw")

    _lo = cursor.execute(sql, (info_data['id'], info_data['pw']))
    # 튜플로 -> (ID, NAME(ID), PW, RANK)
    if _lo:
        session["id"] = info_data['id']
        session["pw"] = info_data['pw']
        return redirect(url_for('dashboard'))
    elif not (info_data["id"] is None and info_data["pw"] is None):
        info_data["fail"] = msg.get("fail_login")
        if info_data["id"] == "" or info_data["pw"] == "":
            print(info_data["id"], info_data["pw"])
            info_data["fail"] = msg.get("void_login")

    return render_template('login.html', info=info_data)


@app.route('/dashboard')
def dashboard():
    db = pymysql.connect(host="localhost", user="root", passwd=os.environ.get("DB_PW"), db="user")
    cursor = db.cursor()
    sql = "select * from account WHERE NAME = %s and PASSWORD = %s"

    if cursor.execute(sql, (session.get("id"), session.get("pw"))):
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
        return jsonify({"message": msg.get("err_link")})


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
            for mss in SIB.start():
                print(f"실시간 전송 상황: {mss}")

    else :
        return jsonify({"message" : msg.get("err_quantity")})

    return jsonify({"message" : msg.get("success_attack")})
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/get_message', methods=['GET', 'POST'])
def get_message():
    return jsonify(msg)

if __name__ == '__main__':
    app.run(debug=True, port=8080, host='0.0.0.0')
