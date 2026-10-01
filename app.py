import streamlit as st
import pandas as pd
import itertools
import math
import os

st.set_page_config(page_title="DML - Student Selection System", layout="wide")
st.title("🎓 Student Selection System - DML")
st.caption("Discrete Mathematics and Logic - Combination + Set Theory + Truth Table")
st.divider()

tab1, tab2 = st.tabs(["📊 PART A: Combinations & Set Theory", "🔐 PART B: Logic & Truth Table"])

# ================= TAB 1 =================
with tab1:
    st.latex(r"C(n,r) = \frac{n!}{r!(n-r)!} \quad P(n,r) = \frac{n!}{(n-r)!} \quad |P(S)| = 2^n")
    
    st.subheader("Step 1: Create Set S (Add Students Manually)")
    with st.form("add"):
        c1, c2 = st.columns([3,1])
        with c1:
            name = st.text_input("Enter Student Name", placeholder="e.g. Aditya")
        with c2:
            st.write("")
            st.write("")
            btn = st.form_submit_button("➕ Add to Set S")
        if btn:
            if name.strip() == "":
                st.error("Enter name!")
            else:
                df_new = pd.DataFrame([{"Name": name.strip()}])
                if os.path.exists("dml_students.csv"):
                    df_old = pd.read_csv("dml_students.csv")
                    if name.strip().lower() in [x.lower() for x in df_old["Name"].values]:
                        st.warning("Already exists!")
                    else:
                        pd.concat([df_old, df_new]).to_csv("dml_students.csv", index=False)
                        st.rerun()
                else:
                    df_new.to_csv("dml_students.csv", index=False)
                    st.rerun()

    if not os.path.exists("dml_students.csv"):
        st.info("Add at least 2 students to start.")
        st.stop()
    
    df = pd.read_csv("dml_students.csv")
    students = df["Name"].tolist()
    n = len(students)
    st.success(f"Set S = {{ {', '.join(students)} }} |  |S| = {n}")
    st.dataframe(df, use_container_width=True)

    if st.button("🗑️ Clear Set S"):
        os.remove("dml_students.csv")
        st.rerun()

    st.divider()
    st.subheader("Step 2: Student Selection (Combination System)")
    
    r = st.slider("Select r (team size)", 1, n, min(2, n))
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("n = Total", n)
    with col2:
        st.metric(f"C({n},{r}) Combinations", math.comb(n, r) if r<=n else 0)
    with col3:
        st.metric(f"P({n},{r}) Permutations", math.perm(n, r) if r<=n else 0)

    c1, c2 = st.columns(2)
    with c1:
        if st.button("Generate C(n,r) Combinations", use_container_width=True):
            combos = list(itertools.combinations(students, r))
            df_c = pd.DataFrame([{"No.": i+1, f"Team C({n},{r})": ", ".join(c)} for i, c in enumerate(combos)])
            st.dataframe(df_c, use_container_width=True)
            st.download_button("📥 Download C(n,r)", df_c.to_csv(index=False).encode(), "combinations.csv")
    
    with c2:
        if st.button("Generate P(n,r) Permutations", use_container_width=True):
            perms = list(itertools.permutations(students, r))
            df_p = pd.DataFrame([{"No.": i+1, f"Order P({n},{r})": " -> ".join(p)} for i, p in enumerate(perms[:100])])
            st.dataframe(df_p, use_container_width=True)
            st.caption(f"Showing 100 of {len(perms)} permutations")

# ================= TAB 2 =================
with tab2:
    st.subheader("🔐 PART B: Logic & Truth Table for Student Selection")
    st.write("**Rule:** If Student has (CGPA >= 7 AND Attendance >= 75%) THEN Selected")

    st.latex(r"p: CGPA >= 7 \quad q: Attendance >= 75 \quad Result = p \land q")

    # Manual logic input
    st.write("### Add Student for
