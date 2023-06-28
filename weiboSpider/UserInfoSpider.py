# -*- coding: utf-8 -*-
# 1000名微博用户信息，包括但不限于用户发表的微博或知乎内容、关注对象、粉丝

import requests
import pandas as pd
from time import sleep
import json
import UserIdSpider
import UserSpider


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
    'cookie': '_T_WM=95b5ced721d7c8d4320874cf8584c615; SUB=_2A25JnfrXDeRhGeFK71cR8C3KwzyIHXVrYYafrDV6PUJbkdCOLRT9kW1NQ0JvEBamhPIB5UEq7wSWOq3i2IGzu_ra; SCF=ArZLcHguBxrAmLd-wxqYhYTysa105uwtFjF95A9lhmr3Ko8uC_TD-93kkgDxctcxZqw4BW9fyE6TD8I0zBU3-Ww.; SSOLoginState=1687784071; MLOGIN=1; M_WEIBOCN_PARAMS=luicode%3D10000011%26lfid%3D1076031776448504'
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
    id = '1776448504'
    num = 5
    fansId = UserIdSpider.GetFansId(id, num)
    print(fansId)

    for i in range(0, num - 1):
        user_info = getUserInfo(fansId[i])  # 1776448504
        obj = pd.Series(user_info)
        obj.to_csv('userinfo.csv', mode='a')
        UserSpider.WeiboUserScrapy(fansId[i], filter=0)
        print(obj)



# https://weibo.cn/1776448504/fans