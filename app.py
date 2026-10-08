import streamlit as st
import itertools
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# ------------------- Page Config -------------------
st.set_page_config(
    page_title="Student Selection Combination System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ------------------- Custom CSS -------------------
st.markdown("""
<style>
.main {background-color: #f8f9ff;}
.stButton>button {background: linear-gradient(90deg, #6a11cb, #2575fc); color:white; border-radius:10px; height:45px; font-weight:bold;}
.metric-card {background:white; padding:15px; border-radius:12px; box-shadow: 0 4px 10px rgba(0,0,0,0.1);}
</style>
""", unsafe_allow_html=True)

st.title("🎓 Student Selection Combination System")
st.caption("DML Mini Project | Sandip University | Guide: J. Sonawane | Team: V.Poleshwar, S.Nandikeswar Reddy, L.Chandu, P.Yugandhar")
st.divider()

# ------------------- Load Data -------------------
@st.cache_data
def load_default_data():
    return pd.DataFrame([
        {"ID": 1, "Name": "V. Poleshwar", "CGPA": 8.5, "Skills": "Python, ML, DBMS", "Attendance": 88, "Projects": 3, "Year": "TY"},
        {"ID": 2, "Name": "S. Nandikeswar Reddy", "CGPA": 8.2, "Skills": "Java, DBMS, OS", "Year": "TY", "Attendance": 85, "Projects": 2},
        {"ID": 3, "Name": "L. Chandu", "CGPA": 7.8, "Skills": "Python, Web, React", "Year": "TY", "Attendance": 90, "Projects": 4},
        {"ID": 4, "Name": "P. Yugandhar", "CGPA": 9.0, "Skills": "ML, AI, Python", "Year": "TY", "Attendance": 92, "Projects": 5},
        {"ID": 5, "Name": "Rahul Kumar", "CGPA": 7.6, "Skills": "Python, C++, DSA", "Year": "TY", "Attendance": 78, "Projects": 2},
        {"ID": 6, "Name": "Amit Sharma", "CGPA": 8.0, "Skills": "DBMS, OS, CN", "Year": "TY", "Attendance": 82, "Projects": 3},
        {"ID": 7, "Name": "Priya Singh", "CGPA": 8.7, "Skills": "Web, Python, UI/UX", "Year": "TY", "Attendance": 91, "Projects": 4},
        {"ID": 8, "Name": "Rohit Verma", "CGPA": 7.9, "Skills": "Java, Spring", "Year": "TY", "Attendance": 80, "Projects": 2},
        {"ID": 9, "Name": "Anjali Desai", "CGPA": 8.9, "Skills": "Python, ML, Web", "Year": "TY", "Attendance": 95, "Projects": 5},
        {"ID": 10, "Name": "Karan Patel", "CGPA": 7.5, "Skills": "C, Python", "Year": "TY", "Attendance": 75, "Projects": 1},
    ])

if 'df' not in st.session_state:
    st.session_state.df = load_default_data()

# Sidebar - Upload
with st.sidebar:
    st.header("📁 Data Input")
    uploaded = st.file_uploader("Upload students.csv (optional)", type=['csv'])
    if uploaded:
        st.session_state.df = pd.read_csv(uploaded)
        st.success("CSV Loaded!")

    st.header("🎯 Selection Criteria (DML Filtering)")
    min_cgpa = st.slider("Min CGPA", 5.0, 10.0, 7.5, 0.1)
    min_att = st.slider("Min Attendance %", 50, 100, 75)
    team_size = st.number_input("Team Size (k for nCk)", 2, 6, 3)
    skill_req = st.text_input("Required Skill", placeholder="e.g. Python")
    top_n = st.slider("Show Top N Teams", 3, 20, 5)

    generate = st.button("🚀 Generate Best Combinations", use_container_width=True)

# Main Tabs
tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🧮 Combination Engine", "🏆 Results"])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Students", len(st.session_state.df))
    col2.metric("Avg CGPA", f"{st.session_state.df['CGPA'].mean():.2f}")
    col3.metric("Max CGPA", f"{st.session_state.df['CGPA'].max()}")
    col4.metric("Python Skilled", len(st.session_state.df[st.session_state.df['Skills'].str.contains('Python', case=False)]))

    c1, c2 = st.columns(2)
    with c1:
        fig = px.histogram(st.session_state.df, x="CGPA", nbins=10, title="CGPA Distribution", color_discrete_sequence=['#6a11cb'])
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig2 = px.scatter(st.session_state.df, x="Attendance", y="CGPA", size="Projects", color="Name", title="Attendance vs CGPA vs Projects")
        st.plotly_chart(fig2, use_container_width=True)

    st.dataframe(st.session_state.df, use_container_width=True)

with tab2:
    st.subheader("How Combination System Works (DML Concept)")
    st.code("""
    1. FILTERING (Data Preprocessing): eligible = CGPA >= X AND Attendance >= Y AND Skill contains Z
    2. COMBINATION (nCr): total_combos = n! / (k! * (n-k)!) -> using itertools.combinations
    3. SCORING (Ranking): Score = (0.5*Avg_CGPA) + (0.3*Avg_Attendance/10) + (0.2*Total_Projects)
    4. RANKING: Sort teams by Score DESC -> Select Top N
    """, language="python")

    if generate:
        # Step 1: Filtering
        df = st.session_state.df
        eligible = df[(df['CGPA'] >= min_cgpa) & (df['Attendance'] >= min_att)]
        if skill_req:
            eligible = eligible[eligible['Skills'].str.contains(skill_req, case=False, na=False)]

        eligible_list = eligible.to_dict('records')

        st.session_state['eligible'] = eligible_list
        st.session_state['eligible_df'] = eligible

        if len(eligible_list) < team_size:
            st.error(f"❌ Not enough students. Eligible: {len(eligible_list)}, Required: {team_size}")
        else:
            # Step 2: nCr Combinations
            n = len(eligible_list)
            k = team_size
            total_combos = np.math.factorial(n) // (np.math.factorial(k) * np.math.factorial(n-k)) if n>=k else 0

            st.info(f"✅ Eligible: {n} students | Total Combinations {n}C{k} = {total_combos} teams")

            all_combos = list(itertools.combinations(eligible_list, team_size))

            # Step 3: Scoring Function (Impressive)
            ranked = []
            for combo in all_combos:
                avg_cgpa = sum(s['CGPA'] for s in combo) / team_size
                avg_att = sum(s['Attendance'] for s in combo) / team_size
                total_proj = sum(s['Projects'] for s in combo)
                skill_diversity = len(set(",".join([s['Skills'] for s in combo]).split(",")))

                # Weighted Score - DML Concept
                score = (avg_cgpa * 0.5) + (avg_att/10 * 0.3) + (total_proj * 0.15) + (skill_diversity * 0.05)

                ranked.append({
                    "score": round(score, 3),
                    "avg_cgpa": round(avg_cgpa, 2),
                    "avg_att": round(avg_att, 1),
                    "total_proj": total_proj,
                    "team": combo
                })

            ranked.sort(key=lambda x: x['score'], reverse=True)
            st.session_state['ranked'] = ranked
            st.success(f"Generated {len(ranked)} ranked teams!")

with tab3:
    if 'ranked' in st.session_state:
        ranked = st.session_state['ranked']
        st.subheader(f"🏆 Top {top_n} Optimal Teams")

        for i, data in enumerate(ranked[:top_n], 1):
            score = data['score']
            with st.container(border=True):
                st.markdown(f"### Team #{i} | Score: {score} | Avg CGPA: {data['avg_cgpa']} | Attendance: {data['avg_att']}% | Projects: {data['total_proj']}")
                cols = st.columns(len(data['team']))
                for idx, member in enumerate(data['team']):
                    with cols[idx]:
                        st.markdown(f"""
                        **{member['Name']}**
                        - CGPA: {member['CGPA']}
                        - {member['Skills']}
                        - Att: {member['Attendance']}%
                        """)

        # Export
        export_data = []
        for r in ranked[:top_n]:
            export_data.append({
                "Team_Score": r['score'],
                "Avg_CGPA": r['avg_cgpa'],
                "Members": ", ".join([m['Name'] for m in r['team']]),
                "CGPAs": ", ".join([str(m['CGPA']) for m in r['team']])
            })
        df_export = pd.DataFrame(export_data)
        st.download_button("📥 Download Top Teams CSV", df_export.to_csv(index=False), "best_teams.csv", "text/csv")
    else:
        st.warning("Click Generate button in sidebar first.")

st.sidebar.divider()
st.sidebar.caption(f"Deployed on {datetime.now().strftime('%d-%m-%Y')} | DML Project")
