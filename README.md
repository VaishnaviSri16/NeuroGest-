# 🧠 NeuroGest
### Brain-Computer Interface Based Game Control System Using EEG Motor Imagery Classification

![Python](https://img.shields.io/badge/Python-3.8+-blue?style=flat-square&logo=python)
![Pygame](https://img.shields.io/badge/Pygame-2D%20Game-green?style=flat-square)
![SVM](https://img.shields.io/badge/Classifier-SVM%20(RBF)-orange?style=flat-square)
![Accuracy](https://img.shields.io/badge/Accuracy-85.6%25-brightgreen?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-purple?style=flat-square)

---

## 📌 Overview

**NeuroGest** is an end-to-end Brain-Computer Interface (BCI) system that enables **hands-free control of a 2D video game** using EEG-based motor imagery classification — no physical input device required.

Using the publicly available **PhysioNet EEG Motor Movement/Imagery Dataset**, NeuroGest extracts brainwave features and classifies three mental states in real time:

| Mental State | Game Command |
|---|---|
| 🧠 IDLE | No movement |
| 👈 LEFT motor imagery | Move player left |
| 👉 RIGHT motor imagery | Move player right |

> Built as a Final Year B.Tech Project — Institute of Technology and Management, Gida, Gorakhpur, UP, India (2026)

---

## ✨ Key Features

- 🔬 **EEG Feature Extraction** — Band power across 5 frequency bands: Delta, Theta, Alpha, Beta, Gamma
- 🤖 **SVM Classifier** — Radial Basis Function (RBF) kernel, 3-class classification
- 🎮 **Real-Time Pygame Integration** — Brain commands directly drive player movement
- 📊 **Live Brain Monitor Panel** — Displays EEG waveforms, confidence scores & predictions during gameplay
- 💻 **No Hardware Required** — Runs entirely on the PhysioNet dataset (no physical EEG device needed)

---

## 📊 Results

| Metric | Value |
|---|---|
| Classification Accuracy | **85.6%** |
| Mean Classification Confidence | **72.4%** |
| Game Score (over 90 epochs) | **642** |
| EEG Channels Used | 64 |
| Classes | 3 (IDLE, LEFT, RIGHT) |

---

## 🛠️ Tech Stack

| Component | Technology |
|---|---|
| Language | Python |
| ML Classifier | Scikit-learn (SVM - RBF kernel) |
| EEG Processing | MNE-Python / NumPy |
| Game Engine | Pygame |
| Dataset | PhysioNet EEG Motor Movement/Imagery Dataset |

---

## 🚀 Getting Started

### Prerequisites
```bash
pip install numpy scikit-learn pygame mne matplotlib
```

### Clone the Repository
```bash
git clone https://github.com/VaishnaviSri16/NeuroGest-.git
cd NeuroGest-
```

### Run the Project
```bash
python main.py
```

---

## 📁 Project Structure

```
NeuroGest/
├── data/               # PhysioNet EEG dataset files
├── preprocessing/      # EEG signal preprocessing scripts
├── features/           # Band power feature extraction
├── classifier/         # SVM model training & evaluation
├── game/               # Pygame 2D game environment
├── monitor/            # Brain Monitor panel (live EEG display)
├── main.py             # Entry point
└── README.md
```

---

## 🧪 How It Works

```
EEG Data (PhysioNet)
        ↓
Preprocessing (filtering, epoching)
        ↓
Feature Extraction (band power: δ θ α β γ)
        ↓
SVM Classifier (RBF kernel)
        ↓
Predicted Class → IDLE / LEFT / RIGHT
        ↓
Pygame Game Control + Brain Monitor Display
```

---

## 👩‍💻 Authors

| Name | Role |
|---|---|
| Suruchi Thakur | Final Year B.Tech, CSE |
| Vaishnavi Srivastava | Final Year B.Tech, CSE |

**Institution:** Institute of Technology and Management, Gida, Gorakhpur, Uttar Pradesh, India
**Batch:** B.Tech 2026

---

## 📄 Publication

This project was submitted as an IEEE-format research paper:

> *"NeuroGest: A Brain-Computer Interface-Based Game Control System Using EEG Motor Imagery Classification"*
> Department of Computer Science & Engineering, ITM Gida, Gorakhpur — 2026

---

## 🙏 Acknowledgements

- [PhysioNet](https://physionet.org/) for the EEG Motor Movement/Imagery Dataset
- [MNE-Python](https://mne.tools/) for EEG processing tools
- [Scikit-learn](https://scikit-learn.org/) for the SVM implementation

---

## 📜 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
