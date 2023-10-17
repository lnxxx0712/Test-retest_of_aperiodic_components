"""
This file runs pre-processing.
Here, we separate the processes of preprocessing and parameterizing the EEG power spectra
to adjust unexpected errors in time.
"""

import os
from os.path import join as pjoin
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# MNE & associated code
import mne
from mne.preprocessing import read_ica

from autoreject import AutoReject, read_auto_reject
from eeg_positions import get_elec_coords

# Import custom code for this analysis
import sys
sys.path.append('/group_analysis/code')
from settings import DATA_PATH, RESULTS_PATH


"""---settings---"""
# Preprocessing options
run_ica = True
preprocess = True
RUN_AUTOREJECT = True

# Set File type
EXT = '.set'

# Initialize subject order run log
subj_list = []
epoch_label_AR = []
epoch_label = []

# Get list of subject files
subj_files = os.listdir(os.path.join(DATA_PATH, 'session01_EC'))
subj_files = [file for file in subj_files if EXT.lower() in file.lower()]
subj_files = sorted(subj_files)

# Loop across all subjects
for sub_ind, subj_file in enumerate(subj_files):
    # Get & check which subject is being run
    subj_label = subj_file.split('.')[0]
    subj_list.append(subj_label)
    print('\nCURRENTLY RUNNING SUBJECT: ', subj_label, '\n')

    if preprocess:

        """---Load data---"""
        eeg_data = mne.io.read_raw_eeglab(os.path.join(DATA_PATH, 'session01_EC', subj_file), preload=True)

        # Get sampling rate
        srate = int(eeg_data.info['sfreq'])
        # print(srate)

        # Check if there are any channels marked bad
        print(eeg_data.info['bads'])

        """---Set montage---"""
        # Set channel montage
        chs = get_elec_coords(system="1005", as_mne_montage=True)
        # chs.plot()  # 2D
        # fig = chs.plot(kind='3d', show=False)  # 3D
        # fig = fig.gca().view_init(azim=70, elev=15)  # set view angle for tutorial
        # plt.show()

        eeg_data.set_montage(chs, match_case=False, verbose=False)
        # Check channel positions
        # eeg_data.plot_sensors(show_names=True)
        # plt.show()

        """---Pre-processing---"""
        # Filtering
        eeg_data_filter = eeg_data.copy().filter(l_freq=0.1, h_freq=50, fir_design='firwin')
        eeg_data_filter.notch_filter(freqs=50)

        # Resampling
        eeg_data_resample = eeg_data_filter.copy().resample(sfreq=250)

        # import bad channels
        bad_channel = pd.read_excel(r'F:/...',
                                    sheet_name=1, usecols=[sub_ind], names=None)
        bad_channel_array = np.array(bad_channel.stack())
        bad_channel_list = bad_channel_array.tolist()
        eeg_data_resample.info['bads'].extend(bad_channel_list)
        # print(eeg_data_resample.info['bads'])

        # Interpolating bad channels
        eeg_data_inter = eeg_data_resample.copy().interpolate_bads(reset_bads=True)

        # Create 2s-epoch without original events
        events = mne.make_fixed_length_events(eeg_data_inter, id=2, start=0.5, duration=2.0)

        # annotate bad epochs by eye
        # fig = eeg_data_inter.plot()
        # fig.fake_keypress('a')  # Simulates user pressing 'a' on the keyboard.
        # plt.show()

        eeg_data_epoch = mne.Epochs(eeg_data_inter, events, tmin=-0.5, tmax=1.5,
                                     preload=True, reject_by_annotation=True)

        # eeg_data_epoch.save(pjoin(RESULTS_PATH, 'epoch/01_EC', subj_label + '-epo.fif'), overwrite=True)

        # """---read epochs---"""
        # eeg_data_epoch = mne.read_epochs(os.path.join(RESULTS_PATH, 'epoch/01_Me', subj_label + '-epo.fif'))

        # ICA
        if run_ica:
            ica = mne.preprocessing.ICA(n_components=0.99, random_state=48, method='fastica', max_iter=800)
            reject = {'eeg': 10e-3}  # 100μV
            ica.fit(eeg_data_epoch, decim=None, reject=reject)
            eeg_data_epoch.load_data()
            ica.plot_components()
            # picks = list(range(0, 30))
            # ica.plot_properties(eeg_data_inter)
            ica.plot_sources(eeg_data_epoch, show_scrollbars=True, title='select the components need to be removed')
            plt.show(block=True)
            eeg_data_ica = ica.apply(eeg_data_epoch)

            # Save out ICA solution
            ica.save(pjoin(RESULTS_PATH, 'ICA/01_EC', subj_label + '-ica.fif'), overwrite=True)
        else:
            ica = read_ica(os.path.join(RESULTS_PATH, 'ICA/01_EC', subj_label + '-ica.fif'))
            eeg_data_ica = ica.apply(eeg_data_epoch)

        # Set reference
        eeg_data_ref = eeg_data_ica.copy().set_eeg_reference(ref_channels='average',
                                               projection=False, verbose=False)

        # """---Retaining different recording lengths---"""
        # eeg_data_ref = eeg_data_ref[:30]  # first 1min
        # eeg_data_ref = eeg_data_ref[:60]  # first 2min
        # eeg_data_ref = eeg_data_ref[:90]  # first 3min
        # eeg_data_ref = eeg_data_ref[:120]  # first 4min

        # Auto-rejection
        eeg_data_auto = eeg_data_ref.copy()
        ## PRE-PROCESSING: AUTO-REJECT
        if RUN_AUTOREJECT:

            print('\nAUTOREJECT: CALCULATING SOLUTION\n')

            # Initialize and run autoreject across epochs
            ar = AutoReject(n_jobs=4, verbose=False)
            ar.fit(eeg_data_auto)

            # Save out AR solution
            ar.save(pjoin(RESULTS_PATH, 'AR_300/01_EC', subj_label + '-ar.hdf5'), overwrite=True)

        # Otherwise: load & apply previously saved AR solution
        else:
            print('\nAUTOREJECT: USING PRECOMPUTED\n')
            ar = read_auto_reject(pjoin(RESULTS_PATH, 'AR_300/01_EC', subj_label + '-ar.hdf5'))
            ar.verbose = 'tqdm'

        # Apply autoreject to the original epochs object it was learnt on
        eeg_data_auto, rej_log = ar.transform(eeg_data_auto, return_log=True)
        # epochs = eeg_data_auto.__len__()
        # if epochs == 0:
        #     epoch_label_AR.append(sub_ind)
        #     continue
        eeg_data_auto.save(pjoin(RESULTS_PATH, 'Preprocess_300/01_EC', subj_label + '-epo.fif'), overwrite=True)


print("Preprocess successfully completed")
