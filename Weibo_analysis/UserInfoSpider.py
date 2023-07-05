# -*- coding: utf-8 -*-
# 爬取用户的基本信息 lsy

import requests
import pandas as pd
from time import sleep
import json
import UserIdSpider
import UserSpider
import csv


headers = {
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
    'cookie': 'SINAGLOBAL=4945420457337.851.1687757054834; ULV=1687783573979:2:2:2:4484271402463.207.1687783573938:1687757054879; ALF=1690376071; SUB=_2A25JnfrXDeRhGeFK71cR8C3KwzyIHXVrYYafrDV8PUJbkNAGLVfkkW1NQ0JvEEY9SrsfJRjBmxnGao7QKaJXXaK1; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFTjbqqYaFYv30HRPYsfwDi5JpX5oz75NHD95QNShBfeh50Son7Ws4Dqcj-i--ciKLFiKLhi--NiKnpi-zfMN.t; XSRF-TOKEN=QlpOXAUR4uBBSzQig269ZHZn; WBPSESS=UrLW89wrdUSfYyBqvsO571XABSPBMZ50sC7VUf1twclrUpozKM59pcOrr6shrDF9RGHUUQipvQYQnBs90fWmPIPQUHCE0B2dlhi1wWtjf9YHKdNM4gq37FtATeYEJTA36KZRV9FoT9WuB0jGfgeyhQ=='
}


def parseUid(uid):
    response = requests.get(url=f'https://weibo.com/ajax/profile/info?custom={uid}', headers=headers)
    try:
        return response.json()['data']['user']['id']
    except:
        return None


def getUserInfo(uid):
    try:
        uid = int(uid)
    except:
        # 说明是 xiena 这样的英文串
        uid = parseUid(uid)
        if not uid:
            return None
    response = requests.get(url=f'https://weibo.com/ajax/profile/detail?uid={uid}', headers=headers)
    if response.status_code == 400:
        return {
            'errorMsg': '用户可能注销或者封号',
            'location': None,
            'user_link': f'https://weibo.com/{uid}'
        }
    resp_json = response.json().get('data', None)
    # print(resp_json)
    if not resp_json:
        return None
    sunshine_credit = resp_json.get('sunshine_credit', None)
    if sunshine_credit:
        sunshine_credit_level = sunshine_credit.get('level', None)
    else:
        sunshine_credit_level = None
    education = resp_json.get('education', None)
    if education:
        school = education.get('school', None)
    else:
        school = None

    location = resp_json.get('location', None)
    gender = resp_json.get('gender', None)

    birthday = resp_json.get('birthday', None)
    created_at = resp_json.get('created_at', None)
    description = resp_json.get('description', None)
    # 我关注的人中有多少人关注 ta
    followers = resp_json.get('followers', None)
    if followers:
        followers_num = followers.get('total_number', None)
    else:
        followers_num = None

    n = 10
    fans = UserIdSpider.GetFansId(str(uid), n)
    friends = UserIdSpider.GetFriendsId(str(uid), n)

    return {
        'userid': uid,
        'fans': fans,
        'friends': friends,
        'sunshine_credit_level': sunshine_credit_level,
        'school': school,
        'location': location,
        'gender': gender,
        'birthday': birthday,
        'created_at': created_at,
        'description': description,
        'followers_num': followers_num
    }


# def WriteUserInfo(user_info):


if __name__ == '__main__':
    # id = '1776448504'
    # num = 5
    # fansId = UserIdSpider.GetFansId(id, num)
    # print(fansId)

    temp = []
    fansid = pd.read_csv('fansid.csv', index_col=0)


    f = open('userinfo.csv', 'a', newline='', encoding='utf-8')
    writer = csv.DictWriter(f,fieldnames=['userid', 'fans', 'friends', 'sunshine_credit_level', 'school',
                                                'location', 'gender', 'birthday', 'created_at', 'description',
                                                'followers_num'])
    # writer.writeheader()

    for i in range(1000, 1200):
        user_info = getUserInfo(fansid.loc[i].values[0])  # 1776448504
        print(fansid.loc[i].values[0])
        temp.append(user_info)
        writer.writerows(temp)
        temp.pop()
        # UserSpider.WeiboUserScrapy(fansid.loc[i].values[0], filter=0)
        print(i)

    # with open('userinfo.csv', 'a', newline='', encoding='utf-8') as f:
    #     writer = csv.DictWriter(f, fieldnames=['userid', 'fans', 'friends', 'sunshine_credit_level', 'school',
    #                                            'location', 'gender', 'birthday', 'created_at', 'description',
    #                                            'followers_num'])
    #     writer.writeheader()
    #     writer.writerows(temp)



# https://weibo.cn/1776448504/fans   7433383273