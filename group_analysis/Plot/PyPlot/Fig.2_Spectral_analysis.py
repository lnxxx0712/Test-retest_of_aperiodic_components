"""
This file runs the topography of the exponent and offset in the five states using FOOOF method.
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib import cm
import pandas as pd
import mne


# Import an EEG after montage
eeg_data_ref = mne.read_epochs('F:/...')

# Import exponent and offset value under each State
# Exponent
file_path_template = r'F:/topomap/exps_session{:02d}.xlsx'
sheet_names = ['Sheet1', 'Sheet2', 'Sheet3', 'Sheet4', 'Sheet5']
dfs = {}

for session in range(1, 4):
    for i, sheet_name in enumerate(sheet_names):
        file_path = file_path_template.format(session)
        df = pd.read_excel(file_path, sheet_name=sheet_name, names=None)
        key = f'exps{(session-1) * 5 + i + 1}'
        df_array = np.array(df.stack())
        dfs[key] = df_array

exps1_array = dfs['exps1']
exps2_array = dfs['exps2']
exps3_array = dfs['exps3']
# ...
exps15_array = dfs['exps15']

# Offset
file_path_template = r'F:/topomap/offs_session{:02d}.xlsx'
dfs = {}

for session in range(1, 4):
    for i, sheet_name in enumerate(sheet_names):
        file_path = file_path_template.format(session)
        df = pd.read_excel(file_path, sheet_name=sheet_name, names=None)
        key = f'offs{(session-1) * 5 + i + 1}'
        df_array = np.array(df.stack())
        dfs[key] = df_array

offs1_array = dfs['offs1']
offs2_array = dfs['offs2']
offs3_array = dfs['offs3']
# ...
offs15_array = dfs['offs15']

"""---------------------------------------------------------------"""

# Get min & max value
vmin1 = np.min([exps1_array, exps2_array, exps3_array, # ...,
                exps15_array])
vmax1 = np.max([exps1_array, exps2_array, exps3_array, # ...,
                exps15_array])

vmin2 = np.min([offs1_array, offs2_array, offs3_array, # ...,
                offs15_array])
vmax2 = np.max([offs1_array, offs2_array, offs3_array, # ...,
                offs15_array])

# Plot
fig, axs = plt.subplots(6, 5, figsize=(8, 8), constrained_layout=True,
                        gridspec_kw={'width_ratios': [1, 1, 1, 1, 0.8], 'height_ratios': [1, 1, 1, 1, 1, 1]})

im1, _ = mne.viz.plot_topomap(exps1_array, eeg_data_ref.info, cmap=cm.viridis, contours=4, show=False, axes=axs[0][0], vmin=vmin1, vmax=vmax1)
mne.viz.plot_topomap(exps2_array, eeg_data_ref.info, cmap=cm.viridis, contours=4, show=False, axes=axs[0][1], vmin=vmin1, vmax=vmax1)
mne.viz.plot_topomap(exps3_array, eeg_data_ref.info, cmap=cm.viridis, contours=4, show=False, axes=axs[0][2], vmin=vmin1, vmax=vmax1)
# ...
mne.viz.plot_topomap(exps15_array, eeg_data_ref.info, cmap=cm.viridis, contours=4, show=False, axes=axs[2][4], vmin=vmin1, vmax=vmax1)

im6, _ = mne.viz.plot_topomap(offs1_array, eeg_data_ref.info, cmap=cm.magma, contours=4, show=False, axes=axs[3][0], vmin=vmin2, vmax=vmax2)
mne.viz.plot_topomap(offs2_array, eeg_data_ref.info, cmap=cm.magma, contours=4, show=False, axes=axs[3][1], vmin=vmin2, vmax=vmax2)
mne.viz.plot_topomap(offs3_array, eeg_data_ref.info, cmap=cm.magma, contours=4, show=False, axes=axs[3][2], vmin=vmin2, vmax=vmax2)
# ...
mne.viz.plot_topomap(offs15_array, eeg_data_ref.info, cmap=cm.magma, contours=4, show=False, axes=axs[5][4], vmin=vmin2, vmax=vmax2)

fig.subplots_adjust(hspace=0.1, wspace=0.1)

plt.colorbar(im1, ax=[axs[0][4], axs[1][4], axs[2][4]], location='right', shrink=0.88)
plt.colorbar(im6, ax=[axs[3][4], axs[4][4], axs[5][4]], location='right', shrink=0.88)

# Text
font = {'family': 'Arial', 'weight': 'bold', 'size': 10}
axs[5][0].set_xlabel('EC', labelpad=20, font=font)
axs[5][1].set_xlabel('EO', labelpad=20, font=font)
axs[5][2].set_xlabel('MA', labelpad=20, font=font)
axs[5][3].set_xlabel('ME', labelpad=20, font=font)
axs[5][4].set_xlabel('MU', labelpad=20, font=font)

axs[0][0].set_ylabel('Exponent(session1)                       ', rotation=0, y=0.35, font=font)
axs[1][0].set_ylabel('Exponent(session2)                       ', rotation=0, y=0.35, font=font)
axs[2][0].set_ylabel('Exponent(session3)                       ', rotation=0, y=0.35, font=font)
axs[3][0].set_ylabel('Offset(session1)                       ', rotation=0, y=0.35, font=font)
axs[4][0].set_ylabel('Offset(session2)                       ', rotation=0, y=0.35, font=font)
axs[5][0].set_ylabel('Offset(session3)                       ', rotation=0, y=0.35, font=font)

plt.show()
