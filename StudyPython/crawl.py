from bs4 import BeautifulSoup
from urllib import parse
import requests
import csv
url = "http://bj.58.com/pinpaigongyu/pn/{page}/?minprice=2000_4000"
headers = {'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'}
page = 0
csv_file = open("rent.csv")
csv_writer = csv.writer(csv_file, delimeter=',')

while True:
    page += 1
    print("fetch: ", url.format(page=page))
    response = requests.get(url.format(page=page))
    html = BeautifulSoup(response.text)
    house_list = html.select(".list > li")

