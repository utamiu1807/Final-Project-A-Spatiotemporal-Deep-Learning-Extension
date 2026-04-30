readme = """
# Vision Zero Chicago — Predictive Traffic Safety Analytics

This project builds a multimodal traffic-safety analytics pipeline for Chicago.

Components:
- LightGBM-Poisson crash forecasting
- ConvLSTM spatiotemporal forecasting
- Speed-camera mismatch analysis
- Computer vision pedestrian–vehicle exposure detection
- Public traffic-safety sentiment analysis
- Equity audit of predicted hotspots

Policy Partner:
Chicago Department of Transportation (CDOT)

Author:
Utami
Heinz College — Carnegie Mellon University
"""

vision-zero-chicago/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── notebooks/
│   ├── 01_EDA.ipynb
│   ├── 02_LGBM_Model.ipynb
│   ├── 03_ConvLSTM.ipynb
│   ├── 04_SpeedCameraFusion.ipynb
│   ├── 05_ComputerVision.ipynb
│   ├── 06_SentimentAnalysis.ipynb
│   └── 07_Dashboard.ipynb
│
├── data/
│   ├── raw/
│   ├── processed/
│   ├── cameras/
│   └── clips/
│
├── outputs/
│   ├── figures/
│   ├── maps/
│   ├── tables/
│   ├── reports/
│   └── cv/
│
├── dashboard/
│   └── app.py
│
├── src/
│   ├── models/
│   ├── features/
│   ├── evaluation/
│   ├── visualization/
│   └── utils/
│
└── docs/
    ├── methodology.md
    ├── findings.md
    └── policy_implications.md
