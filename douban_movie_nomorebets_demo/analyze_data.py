#author:hanshiqiang365

import jieba
import stylecloud
import pandas as pd
from PIL import Image
from collections import Counter
from pyecharts.charts import Geo
from pyecharts.charts import Bar
from pyecharts.charts import Line
from pyecharts.charts import Pie
from pyecharts.charts import Calendar
from pyecharts.charts import WordCloud
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType,SymbolType,ChartType

#读取数据
df = pd.read_excel("孤注一掷.xlsx")
df.head()
df.info()

#print(df.info())

#影评评分等级分布分析
color_js = """new echarts.graphic.LinearGradient(0, 0, 1, 0,
    [{offset: 0, color: '#009ad6'}, {offset: 1, color: '#ed1941'}], false)"""

df_star = df.groupby('评分')['评论'].count()
df_star = df_star.sort_values(ascending=True)
x_data = [str(i) for i in list(df_star.index)]
y_data = df_star.values.tolist()
b1 = (
    Bar()
    .add_xaxis(x_data)
    .add_yaxis('',y_data,itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_js)))
    .reversal_axis()
    .set_series_opts(label_opts=opts.LabelOpts(position='right'))
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(name='评分等级'),
        xaxis_opts=opts.AxisOpts(name='人/次'),
        title_opts=opts.TitleOpts(title='评分等级分布',pos_left='45%',pos_top="5%"),
        legend_opts=opts.LegendOpts(type_="scroll", pos_left="85%",pos_top="28%",orient="vertical")
    )
)

df_star = df.groupby('评分')['评论'].count()
x_data = [str(i) for i in list(df_star.index)]
y_data = df_star.values.tolist()
p1 = (
    Pie(init_opts=opts.InitOpts(width='800px', height='600px'))
    .add(
    '',
    [list(z) for z in zip(x_data, y_data)],
    radius=['10%', '30%'],
    center=['65%', '60%'],
    label_opts=opts.LabelOpts(is_show=True),
    )
    .set_colors(["blue", "green", "#800000", "red", "#000000", "orange", "purple", "red", "#000000", "orange", "purple"])
    .set_series_opts(label_opts=opts.LabelOpts(formatter='评分{b}: {c} \n ({d}%)'),position="outside")
)

b1.overlap(p1)
b1.render('影评评分等级分布分析.html')


#每日评论量分析
df['评论时间'] = pd.to_datetime(df['评论时间'])
df_day = df.groupby(df['评论时间'].dt.day)['评论'].count()
day_x_data = [str(i) for i in list(df_day.index)]
day_y_data = df_day.values.tolist()
 
line1 = (
    Line(init_opts=opts.InitOpts(bg_color=JsCode(color_js)))
    .add_xaxis(xaxis_data=day_x_data)
    .add_yaxis(
        series_name="",
        y_axis=day_y_data,
        is_smooth=True,
        is_symbol_show=True,
        symbol="circle",
        symbol_size=6,
        linestyle_opts=opts.LineStyleOpts(color="#fff"),
        label_opts=opts.LabelOpts(is_show=True, position="top", color="white"),
        itemstyle_opts=opts.ItemStyleOpts(
            color="red", border_color="#fff", border_width=3
        ),
        tooltip_opts=opts.TooltipOpts(is_show=False),
        areastyle_opts=opts.AreaStyleOpts(color=JsCode(color_js), opacity=1),
    )
    .set_global_opts(
        title_opts=opts.TitleOpts(
            title="每日评论量分布",
            pos_top="5%",
            pos_left="center",
            title_textstyle_opts=opts.TextStyleOpts(color="#fff", font_size=16),
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            boundary_gap=True,
            axislabel_opts=opts.LabelOpts(margin=30, color="#ffffff63"),
            axisline_opts=opts.AxisLineOpts(is_show=False),
            axistick_opts=opts.AxisTickOpts(
                is_show=True,
                length=25,
                linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
            ),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
            ),
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            position="left",
            axislabel_opts=opts.LabelOpts(margin=20, color="#ffffff63"),
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(width=2, color="#fff")
            ),
            axistick_opts=opts.AxisTickOpts(
                is_show=True,
                length=15,
                linestyle_opts=opts.LineStyleOpts(color="#ffffff1f"),
            ),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(color="#ffffff1f")
            ),
        ),
        legend_opts=opts.LegendOpts(is_show=False),
    )
)

line1.render('每日评论量分布分析.html')