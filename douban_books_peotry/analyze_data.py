#author:hanshiqiangh365

from matplotlib import pyplot as plt
import seaborn as sns
import random
import jieba
import wordcloud
import pandas as pd
import numpy as np
from PIL import Image


plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#读取数据
db_read = pd.read_excel(r"豆瓣读书-诗词图书.xlsx",index_col=0)

#数据清理
db_read = db_read.drop_duplicates()
# head = db_read.head()
# print(head)

#查看数据信息
db_read.info()

#将整个数组以评分来排序
desc_data = db_read.sort_values(by="评分",ascending=False)
#print(desc_data)

#豆瓣读书-数据可视化
#评分主要分布区域
sns.histplot(db_read["评分"])
#plt.show()
plt.savefig('豆瓣读书-诗词图书-评分分布分析.png')

#取出前一百条数据,体现星级分布
top_100 = desc_data.iloc[:100,:]
sns.catplot(x="星级",data = top_100,kind="count",height=10)
plt.xticks(rotation=90)
#plt.show()
plt.savefig('豆瓣读书-诗词图书-星级分布分析.png')

#豆瓣读书-图书简介词云分析
db_read = pd.read_excel(r"豆瓣读书-诗词图书.xlsx",index_col=0)

with open('豆瓣读书-诗词图书-简介.txt', 'w', encoding='utf-8') as f:  # 使用with open()新建对象f
    # 将列表中的数据循环写入到文本文件中
    for i in db_read["简介"]:
        f.write(str(i) + "\n")  # 写入数据

# 读取文本
with open("豆瓣读书-诗词图书-简介.txt",encoding="utf-8") as f:
    s = f.read()
#print(s)
ls = jieba.lcut(s) # 生成分词列表
text = ' '.join(ls) # 连接成字符串

stopwords = ["的","是","了"] # 去掉不需要显示的词

img = Image.open('heart.jpg')
img_array = np.array(img)
wc = wordcloud.WordCloud(font_path="msyh.ttc",
                         width = 1000,
                         height = 700,
                         background_color='white',
                         max_words=100,stopwords=s,mask=img_array)
# msyh.ttc电脑本地字体，写可以写成绝对路径
wc.generate(text) # 加载词云文本
wc.to_file("豆瓣读书-诗词图书-简介词云分析.png") # 保存词云文件
