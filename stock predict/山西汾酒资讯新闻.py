import re
import time
import datetime

import pymysql
import requests
from bs4 import BeautifulSoup
from pyquery import PyQuery as pq

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 "
                  "Safari/537.36"}


def get_article(url):
    req = requests.get(url, headers=headers)
    data = {}
    data['url'] = url
    data['title'] = ''
    data['time'] = ''
    data['article'] = ''

    content = req.text
    # time
    time_pat = '发表于 (.*?) '
    post_time = re.compile(time_pat).findall(content)[0]
    data['time'] = post_time

    # title
    soup = BeautifulSoup(content, 'lxml')
    title = soup.find('div', id='zwconttbt')
    title = title.get_text().strip()
    data['title'] = title
    article = ''
    # article
    if not soup.find('div', id='zw_body'):
        article = soup.find('div', id='zwconbody').get_text()
    else:
        article = soup.find('div', id='zw_body').get_text()
    article_pat = '(.*?)\[点击查看原文\]'
    if len(re.compile(article_pat).findall(article)) > 0:
        article = re.compile(article_pat).findall(article)[0]
    data['article'] = article
    return data


def save_data(d):
    db = pymysql.connect(
        host='39.107.231.30',
        user='root',
        password='Ipbd@mysql123',
        db='stock_trend',
        port=3306
    )
    cursor = db.cursor()
    a = "insert into article1(title, datetime, url, article) values('{}', '{}', '{}', '{}')" \
        .format(d['title'], d['time'], d['url'], d['article'].strip())
    print(a)
    cursor.execute(a)
    db.commit()
    cursor.close()
    db.close()


# 不获取当天的新闻
def get_url_1(url):
    # url = 'http://guba.eastmoney.com/list,600519,f_{}.html'.format(page)
    # url = 'http://guba.eastmoney.com/list,600809,1,f_2.html'
    req = requests.get(url, headers=headers)
    text = req.text
    doc = pq(text)
    lis = doc('#articlelistnew .articleh span:nth-child(3) a')
    l = []
    for li in lis.items():
        if li.attr('href').startswith('/news,'):
            news = 'http://guba.eastmoney.com' + li.attr('href')
            l.append(news)
    print(l)
    # print('scraping:' + news)
    # data = get_article(news)
    # today = datetime.date.today()
    # datetime1 = str(today.year) + '-' + str(today.month) + '-' + str(today.day)
    #
    # # if data['time'] == datetime1:
    # #     continue
    # save_data(data)
    # time.sleep(2)


# 只获取当天的新闻
def get_url_2(url):
    req = requests.get(url, headers=headers)
    text = req.text
    doc = pq(text)
    lis = doc('#articlelistnew .articleh span:nth-child(3) a')

    for li in lis.items():
        if li.attr('href').startswith('/news,'):
            news = 'http://guba.eastmoney.com' + li.attr('href')
            print('scraping:' + news)
            data = get_article(news)
            today = datetime.date.today()
            jintian = str(today)
            yesterday = str(today - datetime.timedelta(days=1))
            # if data['time'] == jintian:
            #     continue
            # if data['time'] != yesterday:
            #     break
            if data['url'] == 'http://guba.eastmoney.com/news,600809,975205092.html':
                save_data(data)
                break
            time.sleep(2)


if __name__ == '__main__':
    # 不获取当天的新闻
    # for url in ['http://guba.eastmoney.com/news,600519,895828758.html', 'http://guba.eastmoney.com/news,600519,895828686.html', 'http://guba.eastmoney.com/news,600519,895827645.html', 'http://guba.eastmoney.com/news,600519,895826522.html', 'http://guba.eastmoney.com/news,600519,895824074.html', 'http://guba.eastmoney.com/news,600519,895823771.html', 'http://guba.eastmoney.com/news,600519,895823684.html', 'http://guba.eastmoney.com/news,600519,895822819.html', 'http://guba.eastmoney.com/news,600519,895820250.html', 'http://guba.eastmoney.com/news,600519,895818906.html', 'http://guba.eastmoney.com/news,600519,895817815.html', 'http://guba.eastmoney.com/news,600519,895816324.html', 'http://guba.eastmoney.com/news,600519,895812532.html', 'http://guba.eastmoney.com/news,600519,895811426.html', 'http://guba.eastmoney.com/news,600519,895810502.html', 'http://guba.eastmoney.com/news,600519,895801095.html', 'http://guba.eastmoney.com/news,600519,895798891.html', 'http://guba.eastmoney.com/news,600519,895797663.html', 'http://guba.eastmoney.com/news,600519,895795144.html', 'http://guba.eastmoney.com/news,600519,895785241.html', 'http://guba.eastmoney.com/news,600519,895782911.html', 'http://guba.eastmoney.com/news,600519,895779124.html', 'http://guba.eastmoney.com/news,600519,895778868.html', 'http://guba.eastmoney.com/news,600519,895777419.html', 'http://guba.eastmoney.com/news,600519,895776155.html', 'http://guba.eastmoney.com/news,600519,895775279.html', 'http://guba.eastmoney.com/news,600519,895773855.html', 'http://guba.eastmoney.com/news,600519,895773616.html', 'http://guba.eastmoney.com/news,600519,895766827.html', 'http://guba.eastmoney.com/news,600519,895766830.html', 'http://guba.eastmoney.com/news,600519,895758472.html', 'http://guba.eastmoney.com/news,600519,895754941.html', 'http://guba.eastmoney.com/news,600519,895753582.html', 'http://guba.eastmoney.com/news,600519,895752727.html', 'http://guba.eastmoney.com/news,600519,895752127.html', 'http://guba.eastmoney.com/news,600519,895750324.html', 'http://guba.eastmoney.com/news,600519,895748939.html', 'http://guba.eastmoney.com/news,600519,895728123.html', 'http://guba.eastmoney.com/news,600519,895711855.html', 'http://guba.eastmoney.com/news,600519,895708565.html', 'http://guba.eastmoney.com/news,600519,895698053.html', 'http://guba.eastmoney.com/news,600519,895696929.html', 'http://guba.eastmoney.com/news,600519,895685682.html', 'http://guba.eastmoney.com/news,600519,895682896.html', 'http://guba.eastmoney.com/news,600519,895680116.html', 'http://guba.eastmoney.com/news,600519,895679652.html', 'http://guba.eastmoney.com/news,600519,895671941.html', 'http://guba.eastmoney.com/news,600519,895660801.html', 'http://guba.eastmoney.com/news,600519,895658950.html', 'http://guba.eastmoney.com/news,600519,895656736.html', 'http://guba.eastmoney.com/news,600519,895655569.html', 'http://guba.eastmoney.com/news,600519,895635374.html', 'http://guba.eastmoney.com/news,600519,895606248.html', 'http://guba.eastmoney.com/news,600519,895586217.html', 'http://guba.eastmoney.com/news,600519,895583731.html', 'http://guba.eastmoney.com/news,600519,895572511.html', 'http://guba.eastmoney.com/news,600519,895572103.html', 'http://guba.eastmoney.com/news,600519,895568435.html', 'http://guba.eastmoney.com/news,600519,895525745.html', 'http://guba.eastmoney.com/news,600519,895437613.html', 'http://guba.eastmoney.com/news,600519,895437386.html', 'http://guba.eastmoney.com/news,600519,895399739.html', 'http://guba.eastmoney.com/news,600519,895392910.html', 'http://guba.eastmoney.com/news,600519,895764113.html', 'http://guba.eastmoney.com/news,600519,895306594.html', 'http://guba.eastmoney.com/news,600519,895205567.html', 'http://guba.eastmoney.com/news,600519,895189928.html', 'http://guba.eastmoney.com/news,600519,895186332.html', 'http://guba.eastmoney.com/news,600519,895183036.html', 'http://guba.eastmoney.com/news,600519,895181170.html', 'http://guba.eastmoney.com/news,600519,895140767.html', 'http://guba.eastmoney.com/news,600519,895137572.html', 'http://guba.eastmoney.com/news,600519,895134757.html', 'http://guba.eastmoney.com/news,600519,895117206.html', 'http://guba.eastmoney.com/news,600519,895102894.html', 'http://guba.eastmoney.com/news,600519,894969535.html', 'http://guba.eastmoney.com/news,600519,894886385.html', 'http://guba.eastmoney.com/news,600519,894882050.html', 'http://guba.eastmoney.com/news,600519,894782467.html', 'http://guba.eastmoney.com/news,600519,894778923.html']:
    #     print('scraping:' + url)
    #     dict = get_article(url)
    #     save_data(dict)
    #     time.sleep(2)

    # 获取一页的所有新闻
    # for i in range(30, 32):
    #     url = 'http://guba.eastmoney.com/list,600519,1,f_{}.html'.format(i)
    #     print('scraping index_page: {}'.format(url))
    #     get_url_1(url)

    # 仅获取当天的新闻
    get_url_2('http://guba.eastmoney.com/list,600809,1,f_1.html')

    # dict = get_article('http://guba.eastmoney.com/news,600519,973268970.html')
    # save_data(dict)
