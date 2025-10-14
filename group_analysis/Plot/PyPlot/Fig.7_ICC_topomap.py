"""
This file runs the topography of ICC values for the aperiodic exponent and offset.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import mne

# Import an EEG after montage
eeg_data_ref = mne.read_epochs('F:/...')

file_paths = [
    'EC', 'EO', 'MA', 'ME', 'MU'
]

# Exponent
exp_dataframes = []

for file_path in file_paths:
    # Here, I separately saved the long & short interval ICCs
    long_file = r'F:/ICC/exp/ICC_{}_300_long.xlsx'.format(file_path)
    short_file = r'F:/ICC/exp/ICC_{}_300_short.xlsx'.format(file_path)

    df_long = pd.read_excel(long_file, sheet_name='Sheet1', names=None)
    df_long = df_long.loc[df_long['indicator'] == 'exp_list', 'icc'].values
    exp_dataframes.append(df_long)

    df_short = pd.read_excel(short_file, sheet_name='Sheet1', names=None)
    df_short = df_short.loc[df_short['indicator'] == 'exp_list', 'icc'].values
    exp_dataframes.append(df_short)

exps1 = exp_dataframes[0]
exps2 = exp_dataframes[1]
exps3 = exp_dataframes[2]
# ...
exps10 = exp_dataframes[9]

# Offset
off_dataframes = []

for file_path in file_paths:
    long_file = r'F:/ICC/off/ICC_{}_300_long.xlsx'.format(file_path)
    short_file = r'F:/ICC/off/ICC_{}_300_short.xlsx'.format(file_path)

    df_long = pd.read_excel(long_file, sheet_name='Sheet1', names=None)
    df_long = df_long.loc[df_long['indicator'] == 'off_list', 'icc'].values
    off_dataframes.append(df_long)

    df_short = pd.read_excel(short_file, sheet_name='Sheet1', names=None)
    df_short = df_short.loc[df_short['indicator'] == 'off_list', 'icc'].values
    off_dataframes.append(df_short)

offs1 = off_dataframes[0]
offs2 = off_dataframes[1]
offs3 = off_dataframes[2]
# ...
offs10 = off_dataframes[9]

# 计算所有数据的取值范围
vmin1 = np.min([exps1, exps2, exps3, # ...
                exps10])
vmax1 = np.max([exps1, exps2, exps3, # ...
                exps10])

vmin2 = np.min([offs1, offs2, offs3, # ...
                offs10])
vmax2 = np.max([offs1, offs2, offs3, # ...
                offs10])

# Plot
fig, axs = plt.subplots(4, 5, figsize=(8, 8), constrained_layout=True,
                        gridspec_kw={'width_ratios': [1, 1, 1, 1, 0.8], 'height_ratios': [1, 1, 1, 1]})

im1, _ = mne.viz.plot_topomap(exps1, eeg_data_ref.info, cmap=cm.viridis, contours=4, show=False, axes=axs[0][0], vmin=vmin1, vmax=vmax1)
mne.viz.plot_topomap(exps2, eeg_data_ref.info, cmap=cm.viridis, contours=4, show=False, axes=axs[0][1], vmin=vmin1, vmax=vmax1)
mne.viz.plot_topomap(exps3, eeg_data_ref.info, cmap=cm.viridis, contours=4, show=False, axes=axs[0][2], vmin=vmin1, vmax=vmax1)
# ...
mne.viz.plot_topomap(exps10, eeg_data_ref.info, cmap=cm.viridis, contours=4, show=False, axes=axs[1][4], vmin=vmin1, vmax=vmax1)


im6, _ = mne.viz.plot_topomap(offs1, eeg_data_ref.info, cmap=cm.magma, contours=4, show=False, axes=axs[2][0], vmin=vmin2, vmax=vmax2)
mne.viz.plot_topomap(offs2, eeg_data_ref.info, cmap=cm.magma, contours=4, show=False, axes=axs[2][1], vmin=vmin2, vmax=vmax2)
mne.viz.plot_topomap(offs3, eeg_data_ref.info, cmap=cm.magma, contours=4, show=False, axes=axs[2][2], vmin=vmin2, vmax=vmax2)
# ...
mne.viz.plot_topomap(offs10, eeg_data_ref.info, cmap=cm.magma, contours=4, show=False, axes=axs[3][4], vmin=vmin2, vmax=vmax2)

fig.subplots_adjust(hspace=0.1, wspace=0.1)

plt.colorbar(im1, ax=[axs[0][4], axs[1][4]], location='right', shrink=0.88)
plt.colorbar(im6, ax=[axs[2][4], axs[3][4]], location='right', shrink=0.88)

# Text
font = {'weight': 'bold', 'size': 10}
axs[3][0].set_xlabel('EC', labelpad=20, font=font)
axs[3][1].set_xlabel('EO', labelpad=20, font=font)
axs[3][2].set_xlabel('Ma', labelpad=20, font=font)
axs[3][3].set_xlabel('Me', labelpad=20, font=font)
axs[3][4].set_xlabel('Mu', labelpad=20, font=font)
axs[0][0].set_ylabel('Exponent(long)                       ', rotation=0, y=0.35, font=font)
axs[1][0].set_ylabel('Exponent(short)                       ', rotation=0, y=0.35, font=font)
axs[2][0].set_ylabel('Offset(long)                       ', rotation=0, y=0.35, font=font)
axs[3][0].set_ylabel('Offset(short)                       ', rotation=0, y=0.35, font=font)

plt.show()
