# Test-Retest Reliability of EEG Aperiodic Components

[![DOI](https://img.shields.io/badge/DOI-10.1007%2Fs10548--024--01067--x-blue)](https://doi.org/10.1007/s10548-024-01067-x)
[![Python](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

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

## 📊 Analysis Pipeline

The analysis workflow consists of the following steps:

### 1. Preprocessing
- filtering
- Downsampling
- Channel interpolation
- Independent Component Analysis (ICA) for artifact removal
- Average reference

### 2. Power Spectral Density (PSD) Estimation
- Welch's method
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


## ⭐ Support

If you find this repository useful, please consider:
- ⭐ Starring the repository
- 📖 Citing our paper
- 🔄 Sharing with colleagues

---

**Keywords**: EEG, Aperiodic Activity, Test-Retest Reliability, FOOOF, LMER, Power Spectrum, ICC, Neuroscience
