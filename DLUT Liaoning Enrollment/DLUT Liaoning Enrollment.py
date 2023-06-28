#coding:utf8
from selenium import webdriver
import time
import pymongo
from selenium.webdriver.common.by import By
import csv

class dlutSpider(object):
    def __init__(self):
        #21是辽宁
        self.url='http://www.creditsailing.com/school/major_score/21/{}.html'
        # self.options=webdriver.ChromeOptions() # 无头模式
        # self.options.add_argument('--headless')options=self.options
        self.browser=webdriver.Chrome() # 创建无界面参数的浏览器对象
        self.all=['2022/2877464','2021/1473887','2020/1473889','2019/1473891','2018/1473893']  #年份
        self.i='1'

    def get_html(self):
        self.browser.get(self.url.format(self.i))

    def get_data(self):
        self.get_html()
        # 执行js语句，拉动进度条件
        # self.browser.execute_script(
        #     'window.scrollTo(0,document.body.scrollHeight)'
        # )
        # 给页面元素加载时预留时间
        time.sleep(2)
        #用 xpath 提取每页中所有商品，最终形成一个大列表
        li_list=self.browser.find_elements(By.XPATH,'//*[@class="score"]/table/tbody/tr')
        datas=[]
        for li in li_list:
            #构建空字典
            item={}
            item['年份']=li.find_element(By.XPATH,'.//td[2]').text.strip()  
            item['科目']=li.find_element(By.XPATH,'.//td[3]').text.strip()
            item['专业']=li.find_element(By.XPATH,'.//td[5]').text.strip()
            item['最低分数']=li.find_element(By.XPATH,'.//td[6]').text.strip()
            item['最低位次']=li.find_element(By.XPATH,'.//td[7]').text.strip()
            # print(item) 
            datas.append(item)
        self.wri(datas=datas)

    def wri(self,datas):
        with open('test2.csv', 'a', newline='',encoding='utf-8') as f: 
            writer = csv.DictWriter(f,fieldnames=['年份','科目','专业','最低分数','最低位次'])
            writer.writeheader()
            writer.writerows(datas) 

    def run(self):
        for self.i in self.all:
            self.get_data()




if __name__ == '__main__':
    spider=dlutSpider()
    spider.run()