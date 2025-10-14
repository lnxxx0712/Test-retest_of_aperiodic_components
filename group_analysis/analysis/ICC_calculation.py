"""
This file runs the ICC calculation function.
"""

import pingouin as pg
import pandas as pd
import numpy as np


ratings_cols = ['exp_list', 'slope_list']  # exp means using FOOOF method and slope means using LMER method

def calculate_iccs(state, data):
    results = {'indicator': [], 'ch': [], 'icc': []}
    iccs = []

    for ind_col in ratings_cols:
        for ch in range(61):
            sub_data = data[data['ch_list'] == ch]
            icc_res = pg.intraclass_corr(data=sub_data, targets='sub_list', raters='stage', ratings=ind_col)
            icc_value = icc_res.loc[icc_res['Type'] == 'ICC2', 'ICC'].values[0]
            results['indicator'].append(ind_col)
            results['ch'].append(ch)
            results['icc'].append(icc_value)
            iccs.append(icc_value)

        iccs_mean = np.mean(iccs)
        # iccs_ci = pg.compute_bootci(iccs, func=np.mean, n_boot=5000, decimals=6)
        print('state:', state)
        print('ratings:', ind_col)
        print('Mean ICC:', iccs_mean)
        # print('95% confidence interval:', iccs_ci)
        iccs = []

    df = pd.DataFrame.from_dict(results)
    df.to_excel(fr'F:/.../{state}_long.xlsx', index=False)

    mean_iccs = df.groupby('indicator', sort=False)['icc'].mean()
    sem_iccs = df.groupby('indicator', sort=False)['icc'].sem()

    return mean_iccs.values, sem_iccs.values

# Dataframe
datasets = [
    {'name': 'EC', 'output_folder': 'ICC_EC'},
    {'name': 'EO', 'output_folder': 'ICC_EO'},
    {'name': 'MA', 'output_folder': 'ICC_MA'},
    {'name': 'ME', 'output_folder': 'ICC_ME'},
    {'name': 'MU', 'output_folder': 'ICC_MU'}
]


for dataset in datasets:
    # 处理long session状态下的数据
    data_long = pd.read_excel(fr'F:/.../{dataset["name"]}/{dataset["name"]}.xlsx', sheet_name='Sheet1')
    mean_iccs_long, sem_iccs_long = calculate_iccs(dataset["name"], data_long)



