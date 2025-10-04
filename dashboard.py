import streamlit as st
import pandas as pd

# run page -- streamlit run dashboard.py

# test file printing
st.write("Data Dashboard")
data = pd.read_csv("data/Recalls_Data.csv")
st.write(data)