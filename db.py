# # pymysql 사용
# import pymysql
#
# # MySQL 데이터베이스 연결하는 구문 - 걍 외워야함 ㅇㅇ
# db = pymysql.connect(host='127.0.0.1', user='root', password='4254', db='user', charset='utf8')
# # db.cursor().execute(sql) 이지랄로 쓸꺼면 걍 안해도 됨
# cursor = db.cursor()
#
# # 걍 String 변수
# sql = "select * from Account"
#
# # SQL query
# cursor.execute(sql)
#
# # execute로 온 데이터 받기 -> 더 많음 메서드
# cursor.fetchall()  # 모든 행 가져오기
# cursor.fetchone()  # 하나의 행만 가져오기
# cursor.fetchmany(5)  # n개의 데이터 가져오기
#
# # 수정 사항 db에 저장 - < 아이디 비번 변경 시 실행 해야할듯
# db.commit()
#
# db.close()
import os

import dotenv
# =======================
# 간단한 로그인 만들어봅시다 ~


import pymysql
dotenv.load_dotenv()

db = pymysql.connect(host="localhost", user="root", password=os.environ.get("DB_PW"), db="user", charset='utf8')
cursor = db.cursor()

input_id = str(input("아이디 입력 >>>"))
input_pw = str(input("패스워드 입력 >>>"))
# 그냥 하면 SQL 인젝션 당한데오. ;;;;;
sql = "SELECT * FROM account Where NAME = %s AND PASSWORD = %s"

# 튜플로 뒤에 넣어주기
cursor.execute(sql, (input_id, input_pw))


# (1, 'ADMIN', '1214') 이렇게 출력 됨 ㅇㅇ
result = cursor.fetchone()



if result is not None:
    print("로그인 성공")
else:
    print("로그인 실패")

# 이렇게 해도 됨

# if result:
#     print("로그인 성공")
# else:
#     print("로그인 실패")


print(result)


db.close()
