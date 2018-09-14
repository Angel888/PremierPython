import re
import json
import requests
from flask import Flask
from flask import request
import pymysql
app = Flask(__name__)



def get_info_from_zhihu(movie_name):
    """
    访问知乎，返回用户信息
    :param movie_name:
    :return:
    """
    headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    data = requests.get('https://www.zhihu.com/search?type=content&type=people&q=' + movie_name, headers=headers)

    pattern = re.compile(r'ContentItem-main.*?href=\"(.*?)\".*?Avatar.*?src=\"(.*?)\".*?ContentItem-title.*?<em>(.*?)<\/em>.*?ContentItem-meta.*?Highlight\">(.*?)<\/div>')
    result = pattern.findall(data.text)
    users = []
    for homepage, avatar, name, desc in result:
        homepage = "http:" + homepage
        users.append({
            "name": name,
            "homepage": homepage,
            "avatar": avatar,
            "desc": desc
        })

    return users


def save_history():
    db = pymysql.connect(host='localhost', user='root', password='1', db='mysql', port= 3306)
    cur = db.cursor()
    sql_insert = "insert into q1(username,ip) values(127.0.0.1, root)"
    try:
        cur.execute(sql_insert)
        db.commit()
    except Exception as e:
        db.rollback()
    finally:
        db.close()


@app.route('/query')
def query():
    # 第一步，获取参数中的电影名称
    movie_name = request.args['movie']

    # 第二步，+头像、简介、显示中文
    users = get_info_from_zhihu(movie_name)

    # 第三步，存储用户访问记录
    save_history()

    # 第四步，返回电影信息
    return json.dumps(users)


if __name__ == '__main__':
    app.run()
