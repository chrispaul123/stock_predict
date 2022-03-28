import time
import numpy
from flask import Flask, render_template, jsonify
import config
import os
from db import db
import tushare as t1
import datetime
from models import ARTICLE1
from math import exp, log

t1.set_token('e49133a4f8a2b65703286d82a69d668935bce6b67515e8a34b13759a')
ts = t1.pro_api()

app = Flask(__name__, template_folder='templates', static_folder='resources', static_url_path='/')
app.config.from_object(config)
app.config['SECRET_KEY'] = os.urandom(24)

db.init_app(app)


# 判断是否是开盘日
def is_openday(day):
    alldays = ts.trade_cal()
    tradingdays = alldays[alldays['is_open'] == 1]  # 所有开盘日
    tradingdays_list = tradingdays['cal_date'].tolist()
    if day in tradingdays_list:
        return True
    else:
        return False


# model,仅做参考,没有用到
def index1():
    today = datetime.datetime.today()
    # 如果在1点前，判断前一天是否开盘
    if today.hour < 1:
        yesterday = (today - datetime.timedelta(days=1)).strftime('%Y%m%d')
        # 如果昨天是开盘日，就用30天的数据,不是的话,用31天的数据
        if is_openday(yesterday):
            return page2()
        else:
            return page1()
    # 在1点后,判断今天是否开盘
    else:
        if is_openday(today.strftime('%Y%m%d')):
            if today.hour >= 15:
                return page2()
            else:
                return page1()
        else:
            return page1()


# 给出31天数据
def page1():
    df = ts.daily(ts_code='600809.SH')
    # 查询最近30天的股票信息
    df1 = df[:30]
    json_data = []
    
    x_axis = []
    for index, col in df1.iterrows():
        d = {'open': col.open, 'close': col.close, 'high': col.high, 'low': col.low,
             'date': col.trade_date[4:6] + '月' + col.trade_date[6:8] + '日'}
        x_axis.append(col.trade_date[4:6] + '月' + col.trade_date[6:8] + '日')
        json_data.append(d)
    json_data.reverse()
    x_axis.reverse()
    print('横坐标：', x_axis)

    # 获取-3到29天的收盘价
    # df2 = df[1:33]
    df2 = df[0:33]
    shoupanjia = list(df2['close'])
    shoupanjia.reverse()
    # 计算真实收益率
    shouyilv = []
    for k, v in enumerate(shoupanjia):
        if k == 0:
            continue
        shouyilv.append(log(shoupanjia[k] / shoupanjia[k - 1]))

    # 最近33天开盘的日期
    df3 = df[0:32]
    dates = list(df3['trade_date'])
    dates.reverse()
    # 最近30天开盘的所对应的新闻日期
    previous_dates = []
    today = datetime.datetime.today()
    dates.append(str(today.year)+str(today.month)+str(today.day))

    # 每日要获取的新闻的区间为上次开盘日到本次开盘日的前一天
    for k, v in enumerate(dates):
        if k == 0:
            continue
        l = []
        # 本次开盘的日期
        date1 = v[0:4] + '-' + v[4:6] + '-' + v[6:8]
        # 上次开盘的日期
        date2 = dates[k - 1][0:4] + '-' + dates[k - 1][4:6] + '-' + dates[k - 1][6:8]

        # 从本次开盘日开始每次向前推一天，直到上次开盘日后停止，把这段时间放入列表
        for i in range(1, 16):
            date = (datetime.datetime(int(v[0:4]), int(v[4:6]), int(v[6:8])) - datetime.timedelta(days=i)).strftime(
                '%Y-%m-%d')
            l.append(date)
            # 向前倒退到上次开盘时停止
            if date == date2:
                break
        previous_dates.append(l)
    # previous_dates.append(['2020-11-09'])
    print('新闻日期：', previous_dates)

    # 存放30天对应的新闻
    news_list = []
    for date in previous_dates:
        # 存放每一次开盘日对应的新闻
        daily_news = []
        for d in date:
            news = ARTICLE1.query.filter(ARTICLE1.datetime == d).all()
            for new in news:
                if new.motion:
                    daily_news.append(new.motion)
        news_list.append(daily_news)
    print('新闻情感值：', news_list)
    news_num = []
    motion_list = []
    for news in news_list:
        news_num.append(len(news))
        motion_sum = 0
        if len(news) > 0:
            for new in news:
                motion_sum += (new - 0.7784)
            motion_list.append(motion_sum / len(news))
        else:
            motion_list.append(0.0)
    print('新闻数量：', news_num)
    # print('预测收益率：', motion_list)
    # 最近30天的预测收益率
    return_num = []
    for i in range(31):
        num = -0.0592 * shouyilv[i] - 0.1415 * shouyilv[i + 1] + 0.00935 * motion_list[i] - 0.00905 * motion_list[
            i + 1] - 0.00325
        return_num.append(num)
    print('预测收益率：', return_num)
    # df4 = df[1:31]
    df4 = df[0:31]
    true_price = list(df4['close'])
    true_price.reverse()

    json_data.append({'open': '待定', 'close': '待定', 'high': '待定', 'low': '待定', 'date': str(today.month)+'月'+str(today.day)+'日', 'predict': 0})
    predict = []
    for i in range(31):
        p = exp(return_num[i]) * true_price[i]
        predict.append(p)
        json_data[i]['predict'] = round(p, 2)
    # predict.append(235.2442957255163)


    # ----------------计算1-30天的motion值---------------------
    df5 = df[0:31]
    dates2 = list(df5['trade_date'])
    dates2.reverse()
    today_dates = []
    for k, v in enumerate(dates2):
        if k == 0:
            continue
        l = []
        # 本次开盘的日期
        date1 = v[0:4] + '-' + v[4:6] + '-' + v[6:8]
        # 上次开盘的日期
        date2 = dates2[k - 1][0:4] + '-' + dates2[k - 1][4:6] + '-' + dates2[k - 1][6:8]
        # 从本次开盘向前倒退，到上次开盘日截止
        for i in range(0, 16):
            date = (datetime.datetime(int(v[0:4]), int(v[4:6]), int(v[6:8])) - datetime.timedelta(days=i)).strftime(
                '%Y-%m-%d')
            # 向前倒退到上次开盘时停止
            if date == date2:
                break
            l.append(date)
        today_dates.append(l)
    print('今日Motion日期：', today_dates)
    # 存放1到30天对应的新闻motion值
    news_list1 = []
    for date in today_dates:
        # 存放每一次开盘日对应的新闻
        daily_news = []
        for d in date:
            news = ARTICLE1.query.filter(ARTICLE1.datetime == d).all()
            for new in news:
                if new.motion:
                    daily_news.append(new.motion)
        news_list1.append(daily_news)

    motion_list1 = []
    for news in news_list1:
        motion_sum = 0
        if len(news) > 0:
            for new in news:
                motion_sum += (new - 0.7784)
            motion_list1.append(motion_sum / len(news))
        else:
            motion_list1.append(0.0)
    # 进行归一化，把数据控制在-1到1内
    zuida = max(motion_list1)
    zuixiao = min(motion_list1)
    junzhi = (zuixiao + zuida) / 2
    for k, v in enumerate(motion_list1):
        motion_list1[k] = 2 * (v - junzhi) / (zuida - zuixiao)
    print(motion_list1)
    total_list = []
    for i in range(30):
        if i == 0:
            total_list.append(motion_list1[0])
        else:
            total_list.append(total_list[i - 1] + motion_list1[i])
    print(len(total_list))


    x_axis.append(str(today.month)+'月'+str(today.day)+'日')
    print('最终数据：', json_data)
    # index6是31天数据，有预测点
    # index7是30天数据，无预测点
    return render_template('index6.html', json_data=json_data, predict=predict, dates=x_axis)


# 给出30天数据
def page2():
    time0 = time.time()
    df = ts.daily(ts_code='600809.SH')
    # 查询最近30天的股票信息
    df1 = df[:30]
    json_data = []
    x_axis = []
    for index, col in df1.iterrows():
        d = {'open': col.open, 'close': col.close, 'high': col.high, 'low': col.low,
             'date': col.trade_date[4:6] + '月' + col.trade_date[6:8] + '日'}
        x_axis.append(col.trade_date[4:6] + '月' + col.trade_date[6:8] + '日')
        json_data.append(d)
    json_data.reverse()
    x_axis.reverse()
    print('横坐标：', x_axis)

    # 获取-3到29天的收盘价
    df2 = df[1:33]
    shoupanjia = list(df2['close'])
    shoupanjia.reverse()
    # 计算真实收益率
    shouyilv = []
    for k, v in enumerate(shoupanjia):
        if k == 0:
            continue
        shouyilv.append(log(shoupanjia[k] / shoupanjia[k - 1]))

    # 获取-2到30天开盘的日期
    df3 = df[0:32]
    dates = list(df3['trade_date'])
    dates.reverse()
    # 最近31天开盘的所对应的新闻日期
    previous_dates = []
    # 每日要获取的新闻的区间为上次开盘日到本次开盘日的前一天
    for k, v in enumerate(dates):
        if k == 0:
            continue
        l = []
        # 本次开盘的日期
        date1 = v[0:4] + '-' + v[4:6] + '-' + v[6:8]
        # 上次开盘的日期
        date2 = dates[k - 1][0:4] + '-' + dates[k - 1][4:6] + '-' + dates[k - 1][6:8]

        # 从本次开盘日开始每次向前推一天，直到上次开盘日后停止，把这段时间放入列表
        for i in range(1, 16):
            date = (datetime.datetime(int(v[0:4]), int(v[4:6]), int(v[6:8])) - datetime.timedelta(days=i)).strftime(
                '%Y-%m-%d')
            l.append(date)
            # 向前倒退到上次开盘时停止
            if date == date2:
                break
        previous_dates.append(l)

    print('新闻日期：', previous_dates)

    # 存放-2到29天对应的新闻
    news_list = []
    for date in previous_dates:
        # 存放每一次开盘日对应的新闻
        daily_news = []
        for d in date:
            news = ARTICLE1.query.filter(ARTICLE1.datetime == d).all()
            for new in news:
                if new.motion:
                    daily_news.append(new.motion)
        news_list.append(daily_news)
    print('新闻情感值：', news_list)
    news_num = []
    motion_list = []
    for news in news_list:
        news_num.append(len(news))
        motion_sum = 0
        if len(news) > 0:
            for new in news:
                motion_sum += (new - 0.7784)
            motion_list.append(motion_sum / len(news))
        else:
            motion_list.append(0.0)
    print('新闻数量：', news_num)
    print('motion值：', motion_list)
    # 最近30天的预测收益率
    return_num = []
    for i in range(30):
        num = -0.0592 * shouyilv[i] + -0.1415 * shouyilv[i + 1] + 0.00935 * motion_list[i] - 0.00905 * motion_list[
            i + 1] - 0.00325
        return_num.append(num)

    df4 = df[1:31]
    true_price = list(df4['close'])
    true_price.reverse()

    predict = []
    for i in range(30):
        p = exp(return_num[i]) * true_price[i]
        predict.append(p)
        json_data[i]['predict'] = round(p, 2)

    # ----------------计算1-30天的motion值---------------------
    # 获取-1到30天的日期
    df5 = df[0:31]
    dates2 = list(df5['trade_date'])
    dates2.reverse()
    today_dates = []
    for k, v in enumerate(dates2):
        if k == 0:
            continue
        l = []
        # 本次开盘的日期
        date1 = v[0:4] + '-' + v[4:6] + '-' + v[6:8]
        # 上次开盘的日期
        date2 = dates2[k - 1][0:4] + '-' + dates2[k - 1][4:6] + '-' + dates2[k - 1][6:8]
        # 从本次开盘向前倒退，到上次开盘日截止
        for i in range(0, 16):
            date = (datetime.datetime(int(v[0:4]), int(v[4:6]), int(v[6:8])) - datetime.timedelta(days=i)).strftime(
                '%Y-%m-%d')
            # 向前倒退到上次开盘时停止
            if date == date2:
                break
            l.append(date)
        today_dates.append(l)
    print('今日Motion日期：', today_dates)
    # 存放1到30天对应的新闻motion值
    news_list1 = []
    for date in today_dates:
        # 存放每一次开盘日对应的新闻
        daily_news = []
        for d in date:
            news = ARTICLE1.query.filter(ARTICLE1.datetime == d).all()
            for new in news:
                if new.motion:
                    daily_news.append(new.motion)
        news_list1.append(daily_news)

    motion_list1 = []
    for news in news_list1:
        motion_sum = 0
        if len(news) > 0:
            for new in news:
                motion_sum += (new - 0.7784)
            motion_list1.append(motion_sum / len(news))
        else:
            motion_list1.append(0.0)
    # 进行归一化，把数据控制在-1到1内
    zuida = max(motion_list1)
    zuixiao = min(motion_list1)
    junzhi = (zuixiao + zuida)/2
    for k, v in enumerate(motion_list1):
        motion_list1[k] = 2*(v-junzhi)/(zuida - zuixiao)
    print(motion_list1)
    total_list = []
    for i in range(30):
        if i == 0:
            total_list.append(motion_list1[0])
        else:
            total_list.append(total_list[i-1]+motion_list1[i])
    print(len(total_list))
    print('最终数据：', json_data)
    # index6是31天数据，有预测点
    # index7是30天数据，无预测点
    print(time.time() - time0)
    return render_template('index8.html', json_data=json_data, predict=predict, dates=x_axis,motion_list=motion_list1,total_list=total_list)


# @app.route('/')
# def index():
#     today = datetime.datetime.today()
#     # 如果在1点前，判断前一天是否开盘
#     if today.hour < 1:
#         yesterday = (today - datetime.timedelta(days=1)).strftime('%Y%m%d')
#         # 如果昨天是开盘日，就用30天的数据,不是的话,用31天的数据
#         if is_openday(yesterday):
#             return page2()
#         else:
#             return page1()
#     # 在1点后,判断今天是否开盘
#     else:
#         if is_openday(today.strftime('%Y%m%d')):
#             if today.hour >= 15:
#
#                 return page2()
#             else:
#                 return page1()
#         else:
#             return page1()

@app.route('/')
def index():
    return page2()


if __name__ == '__main__':
    app.run()
