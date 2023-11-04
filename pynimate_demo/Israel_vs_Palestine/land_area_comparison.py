#author:hanshiqiang365

from matplotlib import pyplot as plt
from matplotlib.font_manager import FontProperties
import pandas as pd
import pynimate as nim

font = FontProperties(fname='../simhei.ttf')
plt.rcParams['font.family'] = font.get_name()

df = pd.read_csv('land_area_data.csv',encoding='utf-8').set_index('Year')

cnv = nim.Canvas(facecolor="#001219")
bar = nim.Barplot(df, "%Y", "90d", rounded_edges=True, grid=False)
bar.set_title("以色列和巴勒斯坦历年国土面积（平方公里）变化", color="w", weight=600)
bar.set_time(callback=lambda i, datafier: datafier.data.index[i].year)
cnv.add_plot(bar)
cnv.animate()

plt.show()

cnv.save("land_area_comparison", 24, "gif")

#cnv.save("land_area_comparison", 24 ,"mp4")




