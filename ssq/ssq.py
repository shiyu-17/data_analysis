#coding:utf8
from selenium import webdriver
import time
import pymongo
from selenium.webdriver.common.by import By
import csv

class ssqSpider(object):
    def __init__(self):
        self.url='https://www.zhcw.com/kjxx/ssq/'
        # self.options=webdriver.ChromeOptions() # 无头模式
        # self.options.add_argument('--headless')options=self.options
        self.browser=webdriver.Chrome() # 创建无界面参数的浏览器对象
        self.i=2  #计录页数

    def get_html(self):
        self.browser.get(self.url)
        self.browser.find_element(By.XPATH,'//*[@class="wq-xlk01"]/div/strong[@class="N-t"]').click()
        self.browser.find_element(By.XPATH,'//*[@class="qscount"]').send_keys(1000)
        self.browser.find_element(By.XPATH,"//div[@class='xc-qs nr']/div[@class='btn-box']/div[@class='bt00']/div[@class='JG-an03']").click()


        #获得省份
    # def get_pro(self,url):
    #     js = 'window.open("{}");'.format(url)
    #     self.browser.execute_script(js)
    #     handles = (self.browser.window_handles)  # 获取当前窗口句柄集合（列表类型）
    #     for handle in handles:# 切换窗口
    #         if handle!=self.browser.current_window_handle:
    #             self.browser.switch_to.window(handle)
    #     #有些奖池没有一等奖信息
    #     tem = self.browser.find_elements(By.XPATH,"/html/body/div[2]/div[4]/div[2]/div[4]/dl[1]/dd").text.strip()
    #     self.browser.close()
    #     self.browser.switch_to.window(handles[0])
    #     return tem

        #把进度条件拉倒最底部+提取商品信息
    def get_data(self):
        # 执行js语句，拉动进度条件
        self.browser.execute_script(
            'window.scrollTo(0,document.body.scrollHeight)'
        )
        # 给页面元素加载时预留时间
        time.sleep(2)
        #用 xpath 提取每页中所有商品，最终形成一个大列表
        li_list=self.browser.find_elements(By.XPATH,'//tbody/tr')
        datas=[]
        for li in li_list:
            item={}  
            item['期号']=li.find_element(By.XPATH,'.//td[1]').text.strip('')
            item['开奖日期']=li.find_element(By.XPATH,'.//td[2]').text.strip('')
            item['开奖号码(红1)']=li.find_element(By.XPATH,'.//td[3]/span[1]').text.strip('')
            item['开奖号码(红2)']=li.find_element(By.XPATH,'.//td[3]/span[2]').text.strip('')
            item['开奖号码(红3)']=li.find_element(By.XPATH,'.//td[3]/span[3]').text.strip('')
            item['开奖号码(红4)']=li.find_element(By.XPATH,'.//td[3]/span[4]').text.strip('')
            item['开奖号码(红5)']=li.find_element(By.XPATH,'.//td[3]/span[5]').text.strip('')
            item['开奖号码(红6)']=li.find_element(By.XPATH,'.//td[3]/span[6]').text.strip('')
            item['开奖号码(蓝)']=li.find_element(By.XPATH,'.//td[4]').text.strip('')
            item['总销售额']=li.find_element(By.XPATH,'.//td[5]').text.strip('')
            item['奖池']=li.find_element(By.XPATH,'.//td[12]').text.strip('')
            # url = li.find_element(By.XPATH,'.//td[13]/a').get_attribute("href")
            # temp = self.get_pro(url)
            # item['一等奖省份']=temp
            # print(item)
            datas.append(item)
        # print(datas)
        self.wri(datas)

    def wri(self,datas):
        with open('ssq.csv', 'a', newline='',encoding='utf-8') as f: 
            writer = csv.DictWriter(f,fieldnames=['期号','开奖日期','开奖号码(红1)','开奖号码(红2)','开奖号码(红3)','开奖号码(红4)','开奖号码(红5)','开奖号码(红6)','开奖号码(蓝)','总销售额','奖池'])
            writer.writeheader()
            writer.writerows(datas) 

    def run(self):
        self.get_html()
        #循环执行点击“下一页”操作
        while True:
            #获取每一页要抓取的数据
            self.get_data()
            #判断是否是最一页
            if self.i<35:
                self.browser.find_element(By.XPATH,'//a[@title="{}"]'.format(self.i)).click()
                self.i+=1
                #预留元素加载时间
                time.sleep(1)
            else:
                break


if __name__ == '__main__':
    flag_only_one = True
    spider=ssqSpider()
    spider.run()