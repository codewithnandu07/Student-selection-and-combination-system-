import streamlit as st
import itertools
import pandas as pd
import math

st.set_page_config(page_title="Student Selection", layout="wide")
st.title("🎓 Student Selection - MANUAL NAMES")
st.write("DML Project | Sandip University")

if 'students' not in st.session_state:
    st.session_state.students = []

with st.sidebar:
    st.header("Add Student Manually")
    name = st.text_input("Name")
    cgpa = st.number_input("CGPA", 0.0, 10.0, 8.0)
    skills = st.text_input("Skills")
    att = st.number_input("Attendance", 0, 100, 85)
    proj = st.number_input("Projects", 0, 20, 2)

    if st.button("Add Student"):
        if name:
            st.session_state.students.append({"ID":len(st.session_state.students)+1,"Name":name,"CGPA":cgpa,"Skills":skills,"Attendance":att,"Projects":proj})
            st.success(f"Added {name}")

    if st.button("Clear All"):
        st.session_state.students = []
        st.rerun()

    st.divider()
    min_cgpa = st.slider("Min CGPA", 5.0, 10.0, 7.5)
    min_att = st.slider("Min Att", 50, 100, 75)
    team_size = st.number_input("Team Size k", 2, 6, 3)
    skill_filter = st.text_input("Skill Filter")
    top_n = st.slider("Top Teams", 1, 20, 5)
    gen = st.button("Generate")

if len(st.session_state.students)==0:
    st.warning("Add students from sidebar: Poleshwar, Nandikeswar, Chandu, Yugandhar")
else:
    df = pd.DataFrame(st.session_state.students)
    st.dataframe(df, use_container_width=True)

    if gen:
        eligible = [s for s in st.session_state.students if s['CGPA']>=min_cgpa and s['Attendance']>=min_att]
        if skill_filter:
            eligible = [s for s in eligible if skill_filter.lower() in s['Skills'].lower()]

        if len(eligible) < team_size:
            st.error(f"Not enough. Found {len(eligible)}")
        else:
            n=len(eligible)
            st.info(f"{n}C{team_size} = {math.comb(n, team_size)} teams")
            combos = list(itertools.combinations(eligible, team_size))
            ranked=[]
            for c in combos:
                score = sum(x['CGPA'] for x in c)/team_size*0.5 + sum(x['Attendance'] for x in c)/team_size/10*0.3 + sum(x['Projects'] for x in c)*0.2
                ranked.append((round(score,2), c))
            ranked.sort(key=lambda x: x[0], reverse=True)

            for i in range(min(top_n, len(ranked))):
                score, team = ranked[i]
                st.write(f"### Team {i+1} Score {score}")
                for m in team:
                    st.write(f"- {m['Name']} | {m['CGPA']} | {m['Skills']}")
