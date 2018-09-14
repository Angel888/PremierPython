import requests
import urllib
import re
from bs4 import BeautifulSoup
import time
import pymysql

url = 'https://www.douban.com/search?cat=1002&q=fr'


def get_url_douban(self, headers):
    self.headers = {'Host': 'img3.doubanio.com'
                            'User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'
                                          'Accept': '=''*/*'
                                                    'Accept-Language', 'en-GB,en;q=0.5'
                                                                       'Accept-Encoding': 'gzip, deflate, br'
                                                                                          'Referer',
                    'https://www.douban.com/search?cat=1002&q=fr'
                    'Connection': 'keep-alive '}
    req = requests.get(url, self.headers)
    contents = req.read()

    db = pymysql.connect(host="localhost", user="root", password="1", db="test", port=3306)
    # 正则循环匹配
    match = re.findall(r'剧情简介')


# 加入数据库


def get_info_from_zhihu(movie_name):
    """
    访问知乎，返回用户信息
    :param movie_name:
    :return:
    """
    headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
    data = requests.get('https://www.zhihu.com/search?type=content&type=people&q=' + movie_name, headers=headers)

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

    return users


if __name__ == '__main__':
    users = get_info_from_zhihu("明日香哈哈")
    print(users)
