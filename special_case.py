import json
import time
import requests
import re
from lxml import etree
import execjs


def enter_index():
    session = requests.session()
    session.cookies.set("Alina", "f76fbeae-c9da90-444fa331-678abc76-b1eb02b555e6")
    session.cookies.set("QN48", "0c46cea0-baed-4819-a003-883a1c8b4c0f")
    # print(session.cookies)
    url = "https://flight.qunar.com/site/oneway_list.htm"
    params = {
        'searchDepartureAirport': '重庆',
        'searchArrivalAirport': '上海',
        'searchDepartureTime': '2019-06-14',
        'searchArrivalTime': '2019-06-10',
        'nextNDays': '0',
        'startSearch': 'true',
        'fromCode': 'CKG',
        'toCode': 'SHA',
        'from': 'qunarindex',
        'lowestPrice': 'null',
        't': str(int(time.time() * 1000))
    }
    headers = {
        'Host': 'flight.qunar.com',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    res = session.get(url, headers=headers, params=params, verify=False)

    html = etree.HTML(res.text)
    res = html.xpath('//script[1]/text()')[0]
    # -----------------------------------------------------------------------------------------------------
    js_ = "var document={getElementsByTagName:function(){return {length:7,Robots:true}}};var window={location:{href:'https://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport'}};var result={};var Image=function(){};var location = {href: 'https://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport=%E9%87%8D%E5%BA%86&searchArrivalAirport=%E4%B8%8A%E6%B5%B7&searchDepartureTime=2019-06-14&searchArrivalTime=2019-06-12&nextNDays=0&startSearch=true&fromCode=CKG&toCode=SHA&from=qunarindex&lowestPrice=null'};" + \
          res + \
          "function res(){return window._pt_};console.log(res());"
    # print(js)
    # -----------------------------------------------------------------------------------------------------
    ctx = execjs.compile(js_)
    pre = ctx.call("res")
    print(pre)
    return pre, session


# -----------------------------------------------------------------------------------------------------
def get_msg(pre, session):
    url = "https://flight.qunar.com/touch/api/domestic/wbdflightlist"
    params = {
        'departureCity': '重庆',
        'arrivalCity': '上海',
        'departureDate': '2019-06-14',
        'ex_track': '',
        '__m__': '44ced61f87db4b6564a783535d33ba2b',
        'sort': '',
        '_v': '4'
    }
    headers = {
        'Host': 'flight.qunar.com',
        'Connection': 'keep-alive',
        'pre': pre,
        'w': '0',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/javascript, text/html, application/xml, text/xml, */*',
        'X-Requested-With': 'XMLHttpRequest',
        'Referer': 'https://flight.qunar.com/site/oneway_list.htm',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'f8427e': '367999bdaa9329d2660a6be8f519a6f1'
    }
    res = session.get(url, headers=headers, params=params, verify=False)
    print(res.text)
    t1000 = json.loads(res.text)['t1000'][5:-3]
    function_name = re.findall('function (_\w+)', t1000)[0]

    right_js = "var window={open:true,navigator:{}};var Image=function(){};" + \
               t1000 + ";" + \
               "var res=" + res.text + ";" + \
               "function result(){" + function_name + "(res);return res};"
    # print(right_js)
    ctx = execjs.compile(right_js)
    res = ctx.call('result')
    # print(res)
    return res


if __name__ == '__main__':
    pre, session = enter_index()
    msg = get_msg(pre, session)
    print(msg)