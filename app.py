import streamlit as st
import itertools
import pandas as pd
import math
import plotly.express as px

st.set_page_config(page_title="Student Selection System", page_icon="🎓", layout="wide")
st.title("🎓 Student Selection Combination System - MANUAL ENTRY")
st.caption("DML Project | Sandip University")

# --- Session State for Manual Students ---
if 'df' not in st.session_state:
    st.session_state.df = pd.DataFrame(columns=["ID", "Name", "CGPA", "Skills", "Attendance", "Projects"])

# --- Sidebar: Add Student Manually ---
with st.sidebar:
    st.header("➕ Add Student Manually")
    with st.form("add_student", clear_on_submit=True):
        name = st.text_input("Student Name *", placeholder="e.g. Poleshwar")
        cgpa = st.number_input("CGPA *", 0.0, 10.0, 8.0, 0.1)
        skills = st.text_input("Skills *", placeholder="e.g. Python, ML")
        attendance = st.number_input("Attendance %", 0, 100, 85)
        projects = st.number_input("No. of Projects", 0, 20, 2)
        submitted = st.form_submit_button("Add Student", use_container_width=True)

        if submitted:
            if name.strip() == "" or skills.strip() == "":
                st.error("Name and Skills required!")
            else:
                new_id = len(st.session_state.df) + 1
                new_row = {"ID": new_id, "Name": name.strip(), "CGPA": cgpa, "Skills": skills.strip(), "Attendance": attendance, "Projects": projects}
                st.session_state.df = pd.concat([st.session_state.df, pd.DataFrame([new_row])], ignore_index=True)
                st.success(f"Added {name}")

    st.divider()
    if st.button("🗑️ Clear All Students", use_container_width=True):
        st.session_state.df = pd.DataFrame(columns=["ID", "Name", "CGPA", "Skills", "Attendance", "Projects"])
        st.rerun()

    st.divider()
    st.header("🎯 Selection Criteria")
    min_cgpa = st.slider("Min CGPA", 5.0, 10.0, 7.5, 0.1)
    min_att = st.slider("Min Attendance %", 50, 100, 75)
    team_size = st.number_input("Team Size (k for nCk)", 2, 6, 3)
    skill_req = st.text_input("Filter by Skill (optional)", placeholder="e.g. Python")
    top_n = st.slider("Show Top N Teams", 3, 20, 5)
    generate = st.button("🚀 Generate Combinations", use_container_width=True)

# --- Main Tabs ---
tab1, tab2, tab3 = st.tabs(["📋 My Students", "🧮 Combination Engine", "🏆 Results"])

with tab1:
    df = st.session_state.df
    if df.empty:
        st.warning("No students yet. Add students from left sidebar -> Add Student")
        st.info("Example: Add V.Poleshwar, S.Nandikeswar Reddy, L.Chandu, P.Yugandhar one by one")
    else:
        # FIX for pyarrow error - force string types
        df_display = df.copy()
        df_display['Skills'] = df_display['Skills'].astype(str)
        df_display['Name'] = df_display['Name'].astype(str)

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Added", len(df_display))
        col2.metric("Avg CGPA", f"{df_display['CGPA'].mean():.2f}" if len(df_display)>0 else "0")
        col3.metric("Total Combinations Possible", f"{math.comb(len(df_display), team_size) if len(df_display)>=team_size else 0}")

        st.dataframe(df_display, use_container_width=True)

        if len(df_display) >= 2:
            c1, c2 = st.columns(2)
            with c1:
                fig = px.bar(df_display, x="Name", y="CGPA", title="CGPA of Manually Added Students", color="CGPA")
                st.plotly_chart(fig, use_container_width=True)
            with c2:
                fig2 = px.scatter(df_display, x="Attendance", y="CGPA", size="Projects", color="Name", hover_name="Name", title="Your Students Graph")
                st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.code("""
    MANUAL ENTRY -> FILTER (CGPA/Attendance/Skill) -> nCr COMBINATIONS -> RANKING
    Score = 0.5*CGPA + 0.3*Attendance/10 + 0.2*Projects
    """)

    if generate:
        df = st.session_state.df.copy()
        if df.empty:
            st.error("Add students first!")
        else:
            df['Skills'] = df['Skills'].fillna("").astype(str)
            df['Name'] = df['Name'].fillna("").astype(str)

            # Safe filtering (no pyarrow error)
            eligible = df[(df['CGPA'] >= min_cgpa) & (df['Attendance'] >= min_att)].copy()
            if skill_req.strip()!= "":
                skill_lower = skill_req.lower()
                eligible = eligible[eligible['Skills'].apply(lambda x: skill_lower in str(x).lower())]

            eligible_list = eligible.to_dict('records')

            if len(eligible_list) < team_size:
                st.error(f"Not enough eligible. Found {len(eligible_list)}, need {team_size}")
            else:
                n = len(eligible_list)
                total_combos = math.comb(n, team_size)
                st.info(f"Eligible: {n} | Total {n}C{team_size} = {total_combos} teams")

                all_combos = list(itertools.combinations(eligible_list, team_size))
                ranked = []
                for combo in all_combos:
                    avg_cgpa = sum(s['CGPA'] for s in combo) / team_size
                    avg_att = sum(s['Attendance'] for s in combo) / team_size
                    total_proj = sum(s['Projects'] for s in combo)
                    score = (avg_cgpa * 0.5) + (avg_att/10 * 0.3) + (total_proj * 0.2)
                    ranked.append({"score": round(score, 3), "avg_cgpa": round(avg_cgpa, 2), "avg_att": round(avg_att, 1), "team": combo})

                ranked.sort(key=lambda x: x['score'], reverse=True)
                st.session_state['ranked'] = ranked
                st.success("Done! Go to Results tab")

with tab3:
    if 'ranked' in st.session_state:
        st.subheader(f"Top {top_n} Teams from YOUR Manual Names")
        for i, data in enumerate(st.session_state['ranked'][:top_n], 1):
            with st.container(border=True):
                st.markdown(f"### Team #{i} | Score {data['score']} | Avg CGPA {data['avg_cgpa']}")
                cols = st.columns(len(data['team']))
                for idx, m in enumerate(data['team']):
                    with cols[idx]:
                        st.write(f"**{m['Name']}**\n\nCGPA: {m['CGPA']}\n\n{m['Skills']}\n\nAtt: {m['Attendance']}%")
    else:
        st.warning("Generate combinations first")
