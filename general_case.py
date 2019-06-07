import json
import re
import time
import execjs
import requests
from lxml import etree
from __m__and_headers import m_js


def enter_index():
    session = requests.session()
    session.cookies.set("Alina", "e65b9544-eecf59-33470412-8781e218-74639483999a")
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
    js_ = "var document={getElementsByTagName:function(){return {length:7,Robots:true}}};var window={location:{href:'https://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport'}};var result={};var Image=function(){};var location={href:'https://flight.qunar.com/site/oneway_list.htm?searchDepartureAirport'};" + \
          res + \
          "function res(){return window._pt_};console.log(res());"
    # print(js)
    # -----------------------------------------------------------------------------------------------------
    ctx = execjs.compile(js_)
    pre = ctx.call("res")
    return pre, session


def get_qn668_qn48(pre, session):
    url = "https://flight.qunar.com/touch/api/domestic/wbdflightlist"
    params = {
        'departureCity': '重庆',
        'arrivalCity': '上海',
        'departureDate': '2019-06-14',
        'ex_track': '',
        '__m__': 'e50c65621f30075afbb33264d82a4644',
        'sort': '',
        '_v': '3'
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
        'f8427e': '576306c80fc54f9fa19751fbde9e6932'
    }
    res = session.get(url, headers=headers, params=params, verify=False)
    return session, res.cookies.get_dict()['QN668'], res.cookies.get_dict()['QN48']


def get_msg(pre, session, qn668, qn48):
    print(session.cookies)
    ctx = execjs.compile(m_js)
    __m__header = ctx.call('result_m_num', qn668, qn48)
    # print(__m__header)
    url = "https://flight.qunar.com/touch/api/domestic/wbdflightlist"
    params = {
        'departureCity': '重庆',
        'arrivalCity': '上海',
        'departureDate': '2019-06-14',
        'ex_track': '',
        '__m__': __m__header[0],
        'sort': '',
        '_v': '3',

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
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    headers = dict(headers, **__m__header[1])

    flight_res = session.get(url, headers=headers, params=params)
    # print(flight_res.text)
    t1000 = json.loads(flight_res.text)['t1000'][5:-3]
    function_name = re.findall('function (_\w+)', t1000)[0]

    right_js = "var window={open:true,navigator:{}};var Image=function(){};" + \
               t1000 + ";" + \
               "var res=" + flight_res.text + ";" + \
               "function result(){" + function_name + "(res);return res};"
    # print(right_js)
    ctx = execjs.compile(right_js)
    res = ctx.call('result')
    return res


if __name__ == '__main__':
    pre, session = enter_index()
    session, QN668, QN48 = get_qn668_qn48(pre, session)
    msg = get_msg(pre, session, QN668, QN48)
    print(msg)
