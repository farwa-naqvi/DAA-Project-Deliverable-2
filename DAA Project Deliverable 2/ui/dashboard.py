
import streamlit as st

from closest_pair_page import show_closest_pair_page

st.set_page_config(
    page_title="Divide and Conquer Project",
    page_icon="📊",
    layout="wide"
)

st.title("Divide and Conquer Algorithms")
st.write("Interactive demonstration of two Divide and Conquer algorithms.")

page = st.sidebar.selectbox(
    "Choose an Algorithm",
    ["Closest Pair of Points", "Integer Multiplication"]
)

if page == "Closest Pair of Points":
    show_closest_pair_page()

elif page == "Integer Multiplication":
    st.title("Integer Multiplication")
    st.info("Integer Multiplication page will be added soon.")
