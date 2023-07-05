#-*- codeing = utf-8 -*-
import pandas as pd
from bs4 import BeautifulSoup     #网页解析，获取数据
import re       #正则表达式，进行文字匹配
import urllib.request, urllib.error      #制定URL，获取网页数据
import xlwt     #进行excel操作
import sqlite3  #进行SQLite数据库操作


findId = re.compile(r'{"users":\[{"id":(.*?),')  # 创建正则表达式对象，表示规则（字符串的模式）


def GetFansId(tarid, num):
    baseurl = "https://weibo.com/ajax/friendships/friends?relate=fans&page="
    # "https://weibo.com/u/page/follow/1776448504?relate=fans"
    last1url = "&uid="
    targetid = tarid
    last2url = "&type=fans&newFollowerCount=0"
    lasturl = last1url + targetid + last2url
    # 1.爬取网页
    j = 0
    i = 1
    uid = []
    for n in range(1, num):  # 调用获取页面信息的函数
        i = i + 1
        if n % 100 == 0:
            j = j + 1
            i = 1
        url = baseurl + str(i) + lasturl + str(j)
        html = askURL(url)  # 保存获取到的网页源码
        # print(url)
        # print(n)
        # print(html)

        userid = re.findall(findId, html)
        if userid:
            uid.append(userid[0])
        else:
            break
            # uid.append(0)

    return uid


def GetFriendsId(tarid, num):
    baseurl = "https://weibo.com/ajax/friendships/friends?page="
    # https://weibo.com/ajax/friendships/friends?page=2&uid=1776448504
    last1url = "&uid="
    targetid = tarid
    lasturl = last1url + targetid
    # 1.爬取网页
    uid = []
    for i in range(1, num):  # 调用获取页面信息的函数
        url = baseurl + str(i) + lasturl
        html = askURL(url)  # 保存获取到的网页源码
        # print(i)
        # print(html)

        userid = re.findall(findId, html)
        if userid:
            uid.append(userid[0])
        else:
            break
            # uid.append(0)

    return uid




# # 爬取网页
# def getData(baseurl, lasturl,num):
#     uid = []
#     for i in range(1, num):       # 调用获取页面信息的函数
#         url = baseurl + str(i) + lasturl
#         html = askURL(url)      # 保存获取到的网页源码
#         print(i)
#         print(html)
#
#         userid = re.findall(findId, html)
#         uid.append(userid)
#
#     return uid


# 得到指定一个URL的网页内容
def askURL(url):
    head = {                # 模拟浏览器头部信息，向豆瓣服务器发送消息
        'authority': 'weibo.com',
        'x-requested-with': 'XMLHttpRequest',
        'sec-ch-ua-mobile': '?0',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'content-type': 'application/x-www-form-urlencoded',
        'accept': '*/*',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'cors',
        'sec-fetch-dest': 'empty',
        'referer': 'https://weibo.com/1192329374/KnnG78Yf3?filter=hot&root_comment_id=0&type=comment',
        'accept-language': 'zh-CN,zh;q=0.9,en-CN;q=0.8,en;q=0.7,es-MX;q=0.6,es;q=0.5',
        'cookie': 'SINAGLOBAL=4945420457337.851.1687757054834; ULV=1687783573979:2:2:2:4484271402463.207.1687783573938:1687757054879; ALF=1690376071; SUB=_2A25JnfrXDeRhGeFK71cR8C3KwzyIHXVrYYafrDV8PUJbkNAGLVfkkW1NQ0JvEEY9SrsfJRjBmxnGao7QKaJXXaK1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFTjbqqYaFYv30HRPYsfwDi5JpX5oz75NHD95QNShBfeh50Son7Ws4Dqcj-i--ciKLFiKLhi--NiKnpi-zfMN.t; XSRF-TOKEN=3wXZ3Udcf5PS1NibWJIkYAsy; WBPSESS=UrLW89wrdUSfYyBqvsO571XABSPBMZ50sC7VUf1twclrUpozKM59pcOrr6shrDF9RGHUUQipvQYQnBs90fWmPH4dYnWJDd508b3_3UfO8aZG2mdK3-SNragyhGd2Hkz5WQB26U54IWn6HTakTkxPVw=='
    }

    request = urllib.request.Request(url, headers=head)
    html = ""
    try:


        response = urllib.request.urlopen(request)
        html = response.read().decode("utf-8")
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html


if __name__ == "__main__":          # 当程序执行时
# 调用函数
    targetId = "1776448504" # 1776448504 7623977576
    num = 5000
    fansId = GetFansId(targetId, 5)
    print(fansId)

    # friendsId = GetFriendsId(targetId, num)

    print("爬取完毕！")