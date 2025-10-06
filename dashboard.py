import streamlit as st
#import pandas as pd
from read_csv import read_csv

# run page -- streamlit run dashboard.py

st.write("Data Dashboard")

# test file printing with pandas to see what it should look like
# data = read_csv("data/Recalls_Data.csv")
# st.write(data)


# test our functions
data = read_csv("data/Recalls_Data.csv")
st.write(data)