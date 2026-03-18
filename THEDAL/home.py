import streamlit as st

st.set_page_config(page_title="THEDAL", layout="centered")

# -------- UI --------
st.markdown("""
    <h1 style='text-align:center; font-size:60px; margin-top:150px;'>
        🔎 THEDAL
    </h1>
""", unsafe_allow_html=True)

# -------- SEARCH --------
query = st.text_input("", placeholder="Search Smartly.....")

# -------- SEARCH ACTION --------
if query:
    st.session_state["query"] = query
    st.query_params["q"] = query   # ✅ persists after refresh
    st.switch_page("pages/Results.py")