# 对存储的用户微博内容进行聚类分析，生成词云 lsy
import pandas as pd
import numpy as np
import re
import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号
from wordcloud import WordCloud

# 读取CSV文件
df = pd.read_csv('weibo_content.csv', encoding='utf-8')

# 提取微博内容列
weibo_content = df['content']
weibo_content = weibo_content.str.replace("原图", "")
weibo_content = weibo_content.str.replace("转发", "")
weibo_content = weibo_content.str.replace("理由", "")
weibo_content = weibo_content.str.replace("内容", "")
weibo_content = weibo_content.str.replace("原始用户", "")
weibo_content = weibo_content.str.replace("微博", "")
weibo_content = weibo_content.str.replace("已被删除", "")
weibo_content = weibo_content.str.replace("链接", "")
weibo_content = weibo_content.str.replace("网页", "")
weibo_content = weibo_content.str.replace("组图", "")
weibo_content = weibo_content.str.replace("图片", "")

# 数据预处理
def preprocess_text(text):
    # 去除特殊字符、标点符号等
    text = re.sub(r"[^\u4e00-\u9fa5]", "", text)
    # 分词
    words = jieba.lcut(text)
    return " ".join(words)


# 应用数据预处理函数
preprocessed_weibo = weibo_content.apply(preprocess_text)


# 特征提取（使用TF-IDF向量化）
vectorizer = TfidfVectorizer()
features = vectorizer.fit_transform(preprocessed_weibo)

# 聚类分析
num_clusters = 3  # 设定聚类数量
kmeans = KMeans(n_clusters=num_clusters, random_state=42)
cluster_labels = kmeans.fit_predict(features)
# 5 0.10463013407376015
# 4 0.10139802806926465
# 4 0.09631543032124915



# 评估聚类结果
silhouette_avg = silhouette_score(features, cluster_labels)
print("聚类结果的轮廓系数：", silhouette_avg)

# 将聚类结果与微博内容关联
df['聚类标签'] = cluster_labels

# 绘制聚类结果统计图
cluster_counts = df['聚类标签'].value_counts()
plt.bar(cluster_counts.index, cluster_counts.values)
plt.xlabel('聚类标签')
plt.ylabel('微博数量')
plt.title('聚类结果统计')
plt.show()

# 提取每个聚类的关键词
feature_names = vectorizer.get_feature_names_out()
top_keywords = []

for i in range(num_clusters):
    cluster_samples = preprocessed_weibo[df['聚类标签'] == i]
    cluster_features = vectorizer.transform(cluster_samples)
    cluster_tf_idf = np.asarray(cluster_features.mean(axis=0)).ravel()
    top_keywords_idx = cluster_tf_idf.argsort()[::-1][:10]  # 提取权重最高的前10个特征索引
    keywords = [feature_names[idx] for idx in top_keywords_idx]
    top_keywords.append(keywords)

# 打印每个聚类的关键词
for i, keywords in enumerate(top_keywords):
    print(f"聚类 {i+1} 的关键词: {keywords}")

# 绘制聚类结果的词云图
for i in range(num_clusters):
    cluster_samples = preprocessed_weibo[df['聚类标签'] == i]
    cluster_text = ' '.join(cluster_samples)
    wordcloud = WordCloud(width=800, height=400, background_color='white', min_word_length=2, font_path='msyh.ttc').generate(cluster_text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.title(f"聚类 {i+1} 的词云图")
    plt.show()
