#-*-coding=utf-8-*-
__author__ = 'Jaco'
#获取破指定天数内的新高 比如破60日新高
import tushare as ts
import datetime, calendar
import csv
info=ts.get_stock_basics()

#将字符串转换成datetime类型  
def strtodatetime(datestr,format):      
    return datetime.datetime.strptime(datestr,format)  
#两个日期相隔多少天，例：20081003和20081001是相隔两天  
def datediff(beginDate,endDate):  
    format="%Y%m%d";  
    bd=strtodatetime(beginDate,format)  
    ed=strtodatetime(endDate,format)      
    oneday=datetime.timedelta(days=1)  
    count=0
    while bd!=ed:  
        ed=ed-oneday  
        count+=1
    return count 

#判断是不是新股,上市50天内算新股
def not_new_stock(stockID):
    df1 = ts.get_stock_basics()
    timeToMarket = str(df1.ix[stockID]['timeToMarket'])
    today = datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day).strftime("%Y%m%d")
    count = datediff(timeToMarket,today)
    if count > 50: 
        return True
    else: 
        return False

def loop_all_stocks():
    csvfile = file('/Users/apple/Downloads/higher_test.csv', 'wb')
    writer = csv.writer(csvfile)
    writer.writerow(['code', 'name'])
    for EachStockID in info.index:
         if is_break_high(EachStockID,60):
            if not_new_stock(EachStockID):
                #print "High price on",
                #print EachStockID,
                name = info.ix[EachStockID]['name'].decode('utf-8')
                data = [(EachStockID,name)]
                writer.writerows(data)
    csvfile.close()



def is_break_high(stockID,days):
    end_day=datetime.date(datetime.date.today().year,datetime.date.today().month,datetime.date.today().day)
    days=days*7/5
    #考虑到周六日非交易
    start_day=end_day-datetime.timedelta(days)

    start_day=start_day.strftime("%Y-%m-%d")
    end_day=end_day.strftime("%Y-%m-%d")
    df=ts.get_h_data(stockID,start=start_day,end=end_day)

    period_high=df['high'].max()
    #print period_high
    today_high=df.iloc[0]['high']
    #这里不能直接用 .values
    #如果用的df【：1】 就需要用.values
    #print today_high
    if today_high>=period_high:
        return True
    else:
        return False

loop_all_stocks()