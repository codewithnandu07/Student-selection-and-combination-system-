# 🎓 Student Selection Combination System - DML

**Sandip University | Data Mining Lab Project**
**Live App:** https://xbejuglurnzbkuawg7oatg.streamlit.app/

### Problem
Manual team selection for projects is time-consuming. This system automates it.

### DML Concepts Used
1. **Filtering & Preprocessing:** CGPA >= 7.5, Attendance >= 75%, Skills filtering
2. **Combination Generation (nCr):** `nCr = n! / (k!(n-k)!)` using `itertools.combinations`
3. **Ranking:** Score = 0.5*CGPA + 0.3*Attendance + 0.2*Projects

### Features
- Manual student entry (no CSV needed)
- Eligible student filtering
- nCr team generation (e.g. 10C3 = 120 teams)
- Top N best teams ranking
- Download results

### Libraries
- streamlit
- pandas

### How to Use
1. Add students manually from sidebar (e.g. V.Poleshwar, S.Nandikeswar Reddy, L.Chandu, P.Yugandhar)
2. Set Criteria: Min CGPA, Attendance, Team Size k
3. Click Generate Combinations
4. View Top Teams

### Team Members
- V. Poleshwar
- S. Nandikeswar Reddy
- L. Chandu
- P. Yugandhar
