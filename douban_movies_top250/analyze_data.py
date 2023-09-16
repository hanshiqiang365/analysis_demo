#author:hanshiqiang365

import random
import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar3D
from pyecharts.faker import Faker
from pyecharts.charts import Bar, Grid, Line
from pyecharts.commons.utils import JsCode
from pyecharts.globals import ThemeType
from matplotlib import pyplot as plt


df=pd.read_excel('豆瓣电影top250.xlsx')#导入数据

color_js = """new echarts.graphic.LinearGradient(0, 0, 1, 0,
    [{offset: 0, color: '#009ad6'}, {offset: 1, color: '#ed1941'}], false)"""



a=df['评分'].values.tolist()[:20]
b=df['电影名'].values.tolist()[:20]
s=df['评论人数'].values.tolist()[:20]


#豆瓣Top250电影评价等级可视化
c = (
    Bar({"theme": ThemeType.MACARONS})
    .add_xaxis(b)
    .add_yaxis("评分",a,itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_js)))
    .set_global_opts(
        title_opts={"text": "dict配置", "subtext": "dict配置"}

        )
    .set_global_opts(title_opts=opts.TitleOpts(),
                     datazoom_opts=opts.DataZoomOpts(),#分段
                         xaxis_opts=opts.AxisOpts(name_rotate=60, name="电影名", axislabel_opts={"rotate": 35})#字体倾斜角度
                     )

        .render("豆瓣Top250电影评价等级可视化.html")
)

#豆瓣Top250电影评价人数可视化
c = (
    Bar({"theme": ThemeType.MACARONS})
    .add_xaxis(b)
    .add_yaxis("评论人数",s,itemstyle_opts=opts.ItemStyleOpts(color=JsCode(color_js)))
    .set_global_opts(
        title_opts={"text": "dict配置", "subtext": "dict配置"}

        )
    .set_global_opts(title_opts=opts.TitleOpts(),
                     datazoom_opts=opts.DataZoomOpts(),#分段
                         xaxis_opts=opts.AxisOpts(name_rotate=60, name="电影名", axislabel_opts={"rotate": 35})#字体倾斜角度
                     )

        .render("豆瓣Top250电影评价人数可视化.html")
)


#豆瓣Top250电影评价多Y轴数据分析

b=df['电影名'].values.tolist()[:250]
a=df['评分'].values.tolist()[:250]
s=df['评论人数'].values.tolist()[:250]

bar = (
    Bar()
    .add_xaxis(b)
    .add_yaxis(
        "评分",
        a,
        yaxis_index=0,
        color="#d14a61",
    )
    .add_yaxis(
        "评价人数",
        s,
        yaxis_index=1,
        color="#5793f3",
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            name="评价人数",
            type_="value",
            min_=0,
            max_=3000000,
            position="right",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#d14a61")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
        )
    )
    .extend_axis(
        yaxis=opts.AxisOpts(
            type_="value",
            name="评分",
            min_=0,
            max_=2000000,
            position="left",
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#675bba")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} "),
            splitline_opts=opts.SplitLineOpts(
                is_show=True, linestyle_opts=opts.LineStyleOpts(opacity=1)
            ),
        )
    )
    .set_global_opts(
        yaxis_opts=opts.AxisOpts(
            name="评分",
            min_=0,
            max_=10,
            position="right",
            offset=80,
            axisline_opts=opts.AxisLineOpts(
                linestyle_opts=opts.LineStyleOpts(color="#5793f3")
            ),
            axislabel_opts=opts.LabelOpts(formatter="{value} ml"),
        ),
        title_opts=opts.TitleOpts(title="豆瓣Top250多Y轴数据分析"),
        tooltip_opts=opts.TooltipOpts(trigger="axis", axis_pointer_type="cross"),
        datazoom_opts=opts.DataZoomOpts(),  # 分段
        xaxis_opts=opts.AxisOpts(name_rotate=60, name="电影名", axislabel_opts={"rotate": 35})  # 字体倾斜角度
    )
)

line = (
    Line()
    .add_xaxis(b)
    .add_yaxis(
        "平均评分",
        s,
        yaxis_index=2,
        color="#675bba",
        label_opts=opts.LabelOpts(is_show=False),
    )
)

bar.overlap(line)

bar.render('豆瓣Top250电影评价多Y轴数据分析.html')


#豆瓣Top250电影评价3D可视化分析图

a=df['评分'].values.tolist()[:10]
b=df['电影名'].values.tolist()[:10]
s=df['评论人数'].values.tolist()[:10]
data = [(i, j, random.randint(0, 10)) for i in range(10) for j in range(10)]
c = (
    Bar3D()
    .add(
        "",
        [[d[1], d[0], d[2]] for d in data],
        xaxis3d_opts=opts.Axis3DOpts(a),
        yaxis3d_opts=opts.Axis3DOpts(b),
        zaxis3d_opts=opts.Axis3DOpts(s),
    )
    .set_global_opts(
        visualmap_opts=opts.VisualMapOpts(max_=20),
        title_opts=opts.TitleOpts(title="豆瓣Top250电影评价3D可视化分析图"),
    )
    .render("豆瓣Top250电影评价3D可视化分析图.html")
)

