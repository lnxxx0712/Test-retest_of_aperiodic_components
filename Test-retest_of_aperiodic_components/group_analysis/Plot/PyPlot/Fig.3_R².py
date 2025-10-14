"""
This file runs the distribution of goodness-of-fit(R²) with FOOOF and LMER
"""


import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


colors = ["#6BAED6", "#74C476"]
sns.set_palette(sns.color_palette(colors))

data = pd.read_excel(r"F:\...")
sns.violinplot(x="state", y="goodness", hue="method", data=data, palette="Blues", scale="count")

plt.title("Violin Plot Example")
plt.xlabel("State")
plt.ylabel("Goodness-of-fit")
plt.xticks([-0.1, 0.9, 1.9, 2.9, 3.9], ["EC", "EO", "MA", "ME", "MU"], fontproperties='Arial', size=12, weight='bold')
plt.yticks(fontproperties='Arial', size=12, weight='bold')
plt.show()



