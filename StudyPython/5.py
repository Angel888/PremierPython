#
# from flask import Flask
# import requests
# import pymysql
# app = Flask(__name__)
#
# @app.route("https://movie.douban.com/",methods="POST")
#
# res = requests.get("https://movie.douban.com/")
# contents=res.read()
#
#     db = pymysql.connect(host="localhost", user="root", password="1", db="test", port=3306)
# # 正则循环匹配
#     match=re.findall(r'剧情简介')
# # 加入数据库
# cur = db.cursor()
#
# sql_insert = """insert into user('name') values(4,'liu','1234')"""
#
# try:
#     cur.execute(sql_insert)
#     # 提交
#     db.commit()
# except Exception as e:
#     # 错误回滚
#     db.rollback()
# finally:
#     db.close()

import sys
print(sys.path)






















