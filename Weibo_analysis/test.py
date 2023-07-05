import pandas as pd
import matplotlib.pyplot as plt

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