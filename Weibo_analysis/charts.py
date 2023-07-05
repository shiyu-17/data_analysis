# 绘制根据用户 基本信息绘制一些表，性别、年龄、省市分布 lsy
import numpy as np  # linear algebra
import pandas as pd  # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import silhouette_score
import warnings
import os
import datetime
import re
# from pyecharts import options as opts
# from pyecharts.charts import Map, Bar, Line, Scatter
# from matplotlib.pyplot import MultipleLocator
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
warnings.filterwarnings("ignore")


findday = re.compile(r'[0-9]{4}-[0-9]{1,2}-[0-9]{1,2}')


def calculate_age(birth):
    birth_d = datetime.datetime.strptime(birth, "%Y-%m-%d")
    today_d = datetime.datetime.now()
    age = today_d.year - birth_d.year
    return age


# 数据预处理
def preprocess_text(text):
    # 去除特殊字符、标点符号等
    text = re.sub(r"[^a-zA-Z0-9\u4e00-\u9fa5]", " ", text)
    # 将文本转换为小写
    text = text.lower()
    # 分词
    words = text.split()
    return " ".join(words)


def weibocontent_time_analysis():

    # 从CSV文件中读取DataFrame
    df = pd.read_csv('1861290354.csv')

    # 将 'publish_time' 列转换为日期时间类型
    df['publish_time'] = pd.to_datetime(df['publish_time'])

    # 设置 'publish_time' 列为索引
    df.set_index('publish_time', inplace=True)

    # 按时间段进行微博数量统计，可以选择不同的时间粒度，如天、周、月等
    resample_freq = 'D'  # 按天统计
    df_count = df.resample(resample_freq).size()

    # 绘制时间序列图
    plt.figure(figsize=(12, 6))
    plt.plot(df_count.index, df_count.values)
    plt.xlabel('Time')
    plt.ylabel('Number of Weibo')
    plt.title('Weibo Activity Over Time')
    plt.show()

    # 计算微博内容的热度（例如按月统计）
    resample_freq = 'M'  # 按月统计
    df_heatmap = df.resample(resample_freq).size().reset_index()
    df_heatmap.columns = ['Year-Month', 'Number of Weibo']

    # 使用热度图展示微博内容的变化
    heatmap_data = pd.pivot_table(df_heatmap, values='Number of Weibo', index='Year-Month')
    plt.figure(figsize=(10, 6))
    plt.imshow(heatmap_data, cmap='YlOrRd', aspect='auto')
    plt.colorbar(label='Number of Weibo')
    plt.xlabel('Month')
    plt.ylabel('Year')
    plt.title('Weibo Heatmap')
    plt.show()


def age_analysis(df):
    # 年龄
    age = []
    birth = []
    birth1 = []
    birthday = df['birthday']
    for i in range(1, 1001):
        day = re.findall(findday, str(birthday[i]))
        birth.append(day)
    for da in birth:
        if da:
            birth1.append(da)
    for bir in birth1:
        temp = calculate_age(bir[0])
        if temp > 90:
            temp -= 90
        age.append(temp)

    # 设置图形的显示风格
    plt.style.use('ggplot')
    # 绘图：乘客年龄的频数直方图
    plt.hist(age,  # 绘图数据
             bins=20,  # 指定直方图的条形数为20个
             color='steelblue',  # 指定填充色
             edgecolor='k',  # 指定直方图的边界色
             label='直方图')  # 为直方图呈现标签
    # 去除图形顶部边界和右边界的刻度
    plt.tick_params(top='off', right='off')
    plt.title('Age')
    # 显示图形
    plt.show()


def gender_analysis(df):
    # 性别
    plt.figure(1, figsize=(15, 5))
    sns.countplot(y='gender', data=df)
    plt.show()


def set_time(df):
    # 创建微博时间
    time = []
    birth = []
    birth1 = []
    birthday = df['created_at']
    for i in range(1, 1001):
        day = re.findall(findday, str(birthday[i]))
        birth.append(day)
    for da in birth:
        if da:
            birth1.append(da)
    for bir in birth1:
        temp = calculate_age(bir[0])
        time.append(temp)

    # 设置图形的显示风格
    plt.style.use('ggplot')
    # 绘图：乘客年龄的频数直方图
    plt.hist(time,  # 绘图数据
             bins=20,  # 指定直方图的条形数为20个
             color='steelblue',  # 指定填充色
             edgecolor='k',  # 指定直方图的边界色
             label='直方图')  # 为直方图呈现标签
    # 去除图形顶部边界和右边界的刻度
    plt.tick_params(top='off', right='off')
    plt.title('create time')
    # 显示图形
    plt.show()


def province():
    # 省市分布
    data = pd.read_csv('userinfo.csv', encoding='utf-8', usecols=['userid', 'location'])
    data = data.dropna(axis=0, how='any')

    g = data.groupby('location')
    data_region = g['userid'].count()

    region = data_region.index.tolist()
    count = data_region.values.tolist()

    new = []
    for i in region:
        if i[0:2] == '新疆':
            new.append(i[0:2] + '维吾尔自治区')
        elif i[0:2] == '西藏':
            new.append(i[0:2] + '自治区')
        elif i[0:3] == '内蒙古':
            new.append(i[0:3] + '自治区')
        elif i[0:2] == '广西':
            new.append(i[0:2] + '壮族自治区')
        elif i[0:2] == '宁夏':
            new.append(i[0:2] + '回族自治区')
        elif i[0:2] == '重庆' or i[0:2] == '北京' or i[0:2] == '天津' or i[0:2] == '上海':
            new.append(i[0:2] + '市')
        elif i[0:2] == '香港' or i[0:2] == '澳门':
            new.append(i[0:2] + '特别行政区')
        elif i[0:3] == '黑龙江':
            new.append(i[0:3] + '省')
        else:
            new.append(i[0:2] + '省')
    m = (
        map().add('', [list(z) for z in zip(new, count)], maptype='china').set_global_opts(
            title_opts=opts.TitleOpts(title='粉丝分布图'),
            visualmap_opts=opts.VisualMapOpts(max_=30)
        )
    )
    m.render_notebook()


if __name__ == '__main__':
    df = pd.read_csv('userinfo.csv')

    # 微博用户时间序列分析，绘制时间序列图，热图
    # weibocontent_time_analysis()

    # 年龄
    # age_analysis(df)

    # 性别
    # gender_analysis()

    # 微博注册时间
    # set_time(df)

    # 省市分布
    province()

    # print(df.isnull().sum())








