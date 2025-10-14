# Test-Retest Reliability of EEG Aperiodic Components

[![DOI](https://img.shields.io/badge/DOI-10.1007%2Fs10548--024--01067--x-blue)](https://doi.org/10.1007/s10548-024-01067-x)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

This repository provides the complete code implementation and visualization pipeline for the paper:

**Li, N., Yang, J., Long, C., & Lei, X. (2024). Test-Retest Reliability of EEG Aperiodic Components in Resting and Mental Task States. *Brain Topography*, 37(6), 961–971.**

## 📋 Overview

This repository contains:
- ✅ Complete Python implementation of the analysis pipeline
- ✅ Code for all figures and visualizations in the paper
- ✅ Preprocessing scripts for scalp EEG data
- ✅ Aperiodic activity extraction methods (FOOOF and LMER)
- ✅ Test-retest reliability (ICC) calculation procedures

**Note:** The original raw EEG data is **NOT** included in this repository.

## 🔬 About the Study

This study systematically investigates the test-retest reliability of EEG aperiodic components across different data durations, experimental states (resting and mental tasks), and extraction methods (FOOOF and LMER) at both short (90-min) and long (one-month) intervals.

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Required Packages
```bash
pip install numpy scipy matplotlib
pip install mne mne-icalabel
pip install fooof
pip install statsmodels
pip install autoreject
pip install pandas seaborn
```

## 📊 Analysis Pipeline

The analysis workflow consists of the following steps:

### 1. Preprocessing
- High-pass (0.1 Hz) and low-pass (50 Hz) filtering
- Downsampling to 250 Hz
- Channel interpolation for noisy electrodes
- Independent Component Analysis (ICA) for artifact removal
- Common average reference
- Automatic epoch rejection

### 2. Power Spectral Density (PSD) Estimation
- Welch's method (window: 512 ms, overlap: 256 ms)
- Frequency range: 1-40 Hz

### 3. Aperiodic Component Extraction
Two methods are implemented:

#### FOOOF Method
- Separates periodic and aperiodic components
- Extracts exponent and offset parameters

#### LMER Method
- Fits linear regression to log-log PSD
- Estimates slope (exponent) and intercept (offset)

### 4. Reliability Analysis
- Intraclass Correlation Coefficient (ICC) calculation
- ICC(2,k) model for random effects


## 📖 Acknowledgments

The FOOOF-based aperiodic activity analysis is modified from the work by Richard Höchenberger. For detailed theoretical background and implementation details, please visit:

🔗 **[pybrain_mne Repository](https://github.com/hoechenberger/pybrain_mne)**

## 📧 Contact

For questions regarding:
- **Analysis code or methodology**: Contact Na Li (first author)
- **Original data access or usage rights**: Contact Professor Xu Lei, Southwest University

## 🤝 Contributing

We welcome contributions! If you encounter any issues or have suggestions:
- Open an issue on GitHub
- Submit a pull request
- Contact the authors directly

## 📚 Citation

If this repository helps your research, please cite our work:

```bibtex
@article{li2024test,
  title={Test-Retest Reliability of EEG Aperiodic Components in Resting and Mental Task States},
  author={Li, Na and Yang, Jingqi and Long, Changquan and Lei, Xu},
  journal={Brain Topography},
  volume={37},
  number={6},
  pages={961--971},
  year={2024},
  publisher={Springer},
  doi={10.1007/s10548-024-01067-x}
}
```

## ⭐ Support

If you find this repository useful, please consider:
- ⭐ Starring the repository
- 📖 Citing our paper
- 🔄 Sharing with colleagues

---

**Keywords**: EEG, Aperiodic Activity, Test-Retest Reliability, FOOOF, LMER, Power Spectrum, ICC, Neuroscience

**Study Registration**: Approved by the Review Board of Southwest University (H19050)
