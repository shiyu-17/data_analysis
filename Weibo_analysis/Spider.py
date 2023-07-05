# -*- coding: utf-8 -*-
# 微博爬虫主入口

import pandas as pd
import UserIdSpider
import UserSpider
import UserInfoSpider
import csv

# if __name__ == "__main__":
#     id = '1776448504'  # 选择博主，爬取其粉丝信息
#     num = 10  # 选择爬取粉丝数量
#     fansId = UserIdSpider.GetFansId(id, num)
#     print(fansId)
#
#     for i in range(0, num - 1):
#         user_info = UserInfoSpider.getUserInfo(fansId[i])  # 获取用户基本信息
#         obj = pd.Series(user_info)
#         obj.to_csv('userinfo.csv', mode='a')
#         UserSpider.WeiboUserScrapy(fansId[i], filter=0) # 获取用户微博内容
#         # print(obj)


if __name__ == "__main__":
    id = '1776448504' # 选择博主，爬取其粉丝信息
    num = 1000 # 选择爬取粉丝数量
    fansId = UserIdSpider.GetFansId(id, num)
    # print(fansId)

    temp = []

    for i in range(0, num - 1):
        user_info = UserInfoSpider.getUserInfo(fansId[i])  # 获取用户基本信息
        temp.append(user_info)
        # obj.to_csv('userinfo.csv', mode='a')
        # UserSpider.WeiboUserScrapy(fansId[i], filter=0) # 获取用户微博内容

    with open('userinfo.csv', 'a', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=['userid', 'fans', 'friends', 'sunshine_credit_level', 'school', 'location', 'gender', 'birthday', 'created_at', 'description', 'followers_num'])
        writer.writeheader()
        writer.writerows(temp)