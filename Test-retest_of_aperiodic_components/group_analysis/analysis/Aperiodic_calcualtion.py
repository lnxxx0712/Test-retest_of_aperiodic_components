"""
This file parameterizes EEG power spectra and get aperiodic exponent and offset.
"""

import os
import numpy as np
import pandas as pd
import statsmodels.api as sm

# MNE & associated code
import mne

# FOOOF, and custom helper & utility functions
from fooof import FOOOF


"""---Settings---"""
# Import custom code for this analysis
import sys
sys.path.append('/group_analysis/code')
from settings import DATA_PATH, RESULTS_PATH

# Set which average function to use
avg_func = np.mean

# Data settings
EXT = '.fif'

# FOOOF Settings
FREQ_RANGE = [3, 25]
PEAK_WIDTH_LIMITS = [1, 6]
MAX_N_PEAKS = 6
MIN_PEAK_HEIGHT = 0.05
PEAK_THRESHOLD = 1.5
APERIODIC_MODE = 'fixed'

# Params for FOOOF fit
epo_list = []
exp_list = []
off_list = []
r2_fooof_list = []
# err_fooof_list = []

# Params for LMER fit
intercept_list = []
slope_list = []
r2_lmer_list = []
# p_value_list = []

# Initialize subject order run log
# subj_list = []
ch_list = []
sub_list = []
session_list = []
skip_list = []

"""---Data loading---"""
# Get list of subject files
subj_files = os.listdir(os.path.join(RESULTS_PATH, 'Preprocess_300/01_EC'))
subj_files = [file for file in subj_files if EXT.lower() in file.lower()]
subj_files = sorted(subj_files)

# Loop across all subjects
for sub_ind, subj_file in enumerate(subj_files):

    # Get & check which subject is being run
    subj_label = subj_file.split('.')[0]
    print('\nCURRENTLY RUNNING SUBJECT: ', subj_label, '\n')

    # Import auto-reject results
    eeg_data_auto = mne.read_epochs(os.path.join(RESULTS_PATH, 'Preprocess_300/01_EC', subj_label + '.fif'))
    epochs = eeg_data_auto.__len__()

    """---Calculate PSD---"""
    # Set channel of interest
    # ch_ind = eeg_data_ref.ch_names.index('Cz')

    # PSD settings
    n_fft, n_overlap, n_per_seg = int(512), int(256), int(512)

    # Data settings
    fmin, fmax = (1, 50)

    # PSD calculation
    psds_epo, freqs_epo = mne.time_frequency.psd_welch(
        eeg_data_auto, fmin=fmin, fmax=fmax,
        n_fft=n_fft, n_overlap=n_overlap, n_per_seg=n_per_seg, verbose=False)

    # Average across all epochs & channels
    psds_avg_epo = avg_func(psds_epo, axis=0)
    # psds_avg_all = avg_func(psds_epo, axis=(0, 1))

    """---Aperiodic analysis---"""
    for i in range(len(psds_avg_epo)):

        ch_list.append(i)
        sub_list.append(sub_ind+1)
        epo_list.append(epochs)
        session_list.append(1/2/3)  # This depends on your data belonged to which session

        """---FOOOF---"""
        # Initialize FOOOF object
        # fg = FOOOFGroup(peak_width_limits=PEAK_WIDTH_LIMITS, max_n_peaks=MAX_N_PEAKS,
        #                 min_peak_height=MIN_PEAK_HEIGHT, peak_threshold=PEAK_THRESHOLD, aperiodic_mode=APERIODIC_MODE)
        fm = FOOOF(peak_width_limits=PEAK_WIDTH_LIMITS, max_n_peaks=MAX_N_PEAKS,
                                   min_peak_height=MIN_PEAK_HEIGHT, peak_threshold=PEAK_THRESHOLD,
                                   aperiodic_mode=APERIODIC_MODE)

        # Run FOOOF method
        # fg.fit(freqs_epo, psds_avg_epo, FREQ_RANGE, progress='tqdm')
        fm.fit(freqs_epo, psds_avg_epo[i], FREQ_RANGE)

        # Get FOOOF params and goodness-of-fit
        exp_list.append(fm.get_params('aperiodic_params', 'exponent'))
        off_list.append(fm.get_params('aperiodic_params', 'offset'))
        r2_fooof_list.append(fm.get_params('r_squared'))
        # err_list.append(fm.get_params('error'))

        """---LMER---"""
        # Convert PSD data to log-log space
        psds_avg_epo_log = np.log10(psds_avg_epo[i])

        # Set frequency range the same as fooof method
        freq_min = 3
        freq_max = 25
        mask = (freqs_epo >= freq_min) & (freqs_epo <= freq_max)

        # Run OLS regression
        Freqs_epo = np.log10(freqs_epo[mask])
        Freqs_epo = sm.add_constant(Freqs_epo)
        model = sm.OLS(np.log10(psds_avg_epo[i][mask]), Freqs_epo).fit()
        # print(model.summary())

        # Get LMER params and goodness-of-fit
        intercept_list.append(model.params[0])
        slope_list.append(-(model.params[1]))
        r2_lmer_list.append(model.rsquared_adj)
        # p_value_list.append(model.f_pvalue)


"""---Export parameters---"""

# convert list to dataframe and export
df = pd.DataFrame({'session': session_list, 'sub_list': sub_list, 'ch_list': ch_list,
                   'epo_list': epo_list, 'exp_list': exp_list, 'off_list': off_list,
                   'r2_fooof_list': r2_fooof_list, 'slope_list': slope_list,
                   'intercept_list': intercept_list, 'r2_lmer_list': r2_lmer_list})

df.to_excel('F:/...')

print("Aperiodic analysis successfully completed")
