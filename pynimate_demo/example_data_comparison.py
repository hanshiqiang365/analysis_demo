#author:hanshiqiang365

from matplotlib import pyplot as plt
import pandas as pd
import pynimate as nim

df = pd.read_csv('example_data.csv').set_index('year')

cnv = nim.Canvas()
bar = nim.Barplot(df, "%Y", "2d")
bar.set_time(callback=lambda i, datafier: datafier.data.index[i].year)
cnv.add_plot(bar)
cnv.animate()
plt.show()

cnv.save("example_data_comparison", 24, "gif")
cnv.save("example_data_comparison", 24 ,"mp4")




