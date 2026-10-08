# 🎓 Student Selection Combination System - DML Project

> An intelligent system to generate optimal student teams using Combination Logic (nCr) + Ranking.

**College:** Sandip University | **Subject:** DML | **Guide:** J. Sonawane

### 🚀 Features
- Filter by CGPA, Attendance, Skills (Data Preprocessing)
- Generate all nCk combinations using `itertools.combinations`
- Weighted Scoring: 50% CGPA + 30% Attendance + 20% Projects
- Dashboard with Plotly Graphs
- CSV Upload & Export Top Teams
- Streamlit + GitHub Ready

### 🧮 Core Algorithm
`Total Combinations = n! / (k! * (n-k)!)`

### 🖥️ Run Locally
pip install -r requirements.txt
streamlit run app.py
# Open http://localhost:8501

### 🌐 Deploy on Streamlit Cloud
1. Push to GitHub
2. Go to share.streamlit.io -> Deploy app.py

### Team
V.Poleshwar, S.Nandikeswar Reddy, L.Chandu, P.Yugandhar
