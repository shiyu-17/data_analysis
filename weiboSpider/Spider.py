# -*- coding: utf-8 -*-
# 1000名微博用户信息，包括但不限于用户发表的微博或知乎内容、关注对象、粉丝
# 直接运行这个文件就可以

import pandas as pd
import UserIdSpider
import UserSpider
import UserInfoSpider


if __name__ == "__main__":
    id = '1776448504' #
    num = 10
    fansId = UserIdSpider.GetFansId(id, num)
    print(fansId)

    for i in range(0, num - 1):
        user_info = UserInfoSpider.getUserInfo(fansId[i])  # 1776448504
        obj = pd.Series(user_info)
        obj.to_csv('userinfo.csv', mode='a')
        UserSpider.WeiboUserScrapy(fansId[i], filter=0)
        # print(obj)
