import tushare as t1
import datetime

t1.set_token('e49133a4f8a2b65703286d82a69d668935bce6b67515e8a34b13759a')
ts = t1.pro_api()
alldays = ts.trade_cal()
# print(alldays)
tradingdays = alldays[alldays['is_open'] == 1]  # 所有开盘日
tradingdays_list = tradingdays['cal_date'].tolist()
# today = datetime.datetime.today().strftime('%Y%m%d')
today = datetime.datetime.today()
print(today)
print(today.hour)
print(today.month)
print(today.day)
print(str(today.year)+str(today.month)+str(today.day))

# if today.strftime('%Y%m%d') in tradingdays_list:
#     today_index = tradingdays_list.index(today.strftime('%Y%m%d'))
#     last_day = tradingdays_list[int(today_index) - 1]  # 上一次开盘日
#     print(today)
#     print(last_day)
#     print(tradingdays_list)


# import datetime
# print((datetime.datetime.today()+datetime.timedelta(days=1)).strftime('%Y%m%d'))
def is_openday(day):
    alldays = ts.trade_cal()
    tradingdays = alldays[alldays['is_open'] == 1]  # 所有开盘日
    tradingdays_list = tradingdays['cal_date'].tolist()
    if day in tradingdays_list:
        return True
    else:
        return False


# if is_openday(today.strftime('%Y%m%d')) == True:
if is_openday('20201108') == True:
    print('是')
else:
    print('不是')
