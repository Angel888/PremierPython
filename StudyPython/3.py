import re
import json
import requests
from flask import Flask
from flask import request
import pymysql
import time

app = Flask(__name__)


def get_info_from_zhihu(movie_name):
    """
    访问知乎，返回用户信息
    :param movie_name:
    :return:
    """
    headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    data = requests.get('https://www.zhihu.com/search?type=content&type=people&q=' + movie_name, headers=headers)
    print(movie_name)
    pattern = re.compile(
        r'ContentItem-main.*?href=\"(.*?)\".*?Avatar.*?src=\"(.*?)\".*?ContentItem-title.*?<em>(.*?)<\/em>.*?ContentItem-meta.*?Highlight\">(.*?)<\/div>')
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
    print(users)
    return users


def save_history(keyword):
    db = pymysql.connect(host='localhost', user='lin', password='linyi', db='grab', port=3306)
    cur = db.cursor()
    ip = request.remote_addr

    create_time = int(time.time())
    sql_insert = "insert into history values(null,'','%s','%s',%d)" % (ip, keyword, create_time)
    try:
        cur.execute(sql_insert)
        db.commit()
    except Exception as e:
        # print(e)
        db.rollback()
    finally:
        db.close()

@app.route('/')
def index():
    return "hello"

@app.route('/query')
def query():
    #TODO 1. 我们发现查询的很慢，想要加快速度，怎么办呢？ 由于用户信息变化不大，所以我们可以使用缓存，第二次查询速度会很快，请使用redis进行缓存
    #TODO 2. 我们想要查询我的历史查询记录,提示：根据当前ip来判断用户，查询数据库，列出所有的查询记录
    #TODO 3. 现在的用户信息太少了，我还想知道用户的粉丝数，关注数
    #TODO 4. 我们发现，在网页上查询的时候，用户很多，但是通过接口查询只有一两个，为什么呢？我想要更多，怎么办呢？
    #TODO 5. 这个是静态网页，很好查，我想查询豆瓣那样的动态网页，怎么办呢？
    # 第一步，获取参数中的电影名称
    movie_name = request.args['movie']

    # 第二步，+头像、简介、显示中文
    users = get_info_from_zhihu(movie_name)

    # 第三步，存储用户访问记录
    save_history(movie_name)

    # 第四步，返回电影信息
    return json.dumps(users)


if __name__ == '__main__':
    app.run()
