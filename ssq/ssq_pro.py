#coding:utf8
from selenium import webdriver
import time
import pymongo
from selenium.webdriver.common.by import By
import csv

class ssqSpider(object):
    def __init__(self):
        self.url='https://kaijiang.zhcw.com/zhcw/html/ssq/ydjzc_new_42.html'
        # self.options=webdriver.ChromeOptions() # 无头模式
        # self.options.add_argument('--headless')options=self.options
        self.browser=webdriver.Chrome() # 创建无界面参数的浏览器对象
        self.i=1  #计录个数

    def get_html(self):
        self.browser.get(self.url)

        #把进度条件拉倒最底部+提取商品信息
    def get_data(self):
        # 执行js语句，拉动进度条件
        self.browser.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        # 给页面元素加载时预留时间
        time.sleep(1)
        li_list=self.browser.find_elements(By.XPATH,'//*[@class="xltb"]/table/tbody/tr')

        temp = li_list[0].find_element(By.XPATH,'.//td[1]').text.strip()
        datas=[]
        for li in li_list[0:-1]:
            #构建空字典
            item={}
            if li.find_elements(By.XPATH,'.//td[@rowspan]'):
                temp = li.find_element(By.XPATH,'.//td[1]').text.strip()
                item['期号']=temp
                item['省份']=li.find_element(By.XPATH,'.//td[4]').text.strip()
                self.i += 1
            else:    
                item['期号']=temp
                item['省份']=li.find_element(By.XPATH,'.//td[1]').text.strip()
            datas.append(item)
        self.wri(datas)

    def wri(self,datas):
        with open('test_more.csv', 'a', newline='',encoding='utf-8') as f: 
            writer = csv.DictWriter(f,fieldnames=['期号','省份'])
            writer.writeheader()
            writer.writerows(datas)

    def run(self):
        #搜索出想要抓取商品的页面
        self.get_html()
        #循环执行点击“下一页”操作
        while True:
            #获取每一页要抓取的数据
            self.get_data()
            #判断是否是最一页
            if self.i<1000:
                self.browser.find_element(By.LINK_TEXT,'下一页').click()
                #预留元素加载时间
                time.sleep(1)
            else:
                break


if __name__ == '__main__':
    spider=ssqSpider()
    spider.run()