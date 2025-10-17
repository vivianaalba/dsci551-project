import streamlit as st
from read_csv import read_csv
from filter_data import filter_data

# terminal command to run page locally
# streamlit run dashboard.py

# cache the dataset so it doesn’t reload each time you press a button
@st.cache_data
def load_data(format=None):
    if format == "table":
        return read_csv("data/toy_data_cereals.csv", table_format=True)
    else:
        return read_csv("data/toy_data_cereals.csv")

table_data = load_data("table")
data = load_data()

# VIEW ENTIRE DATA SET
# Streamlit expander toggles table visibility
# can also add different datasets here in the future when we work with join
st.write("## View Dataset")

with st.expander("View Data Table"):
    if table_data:
        st.table(table_data) # data loads as a full table
    else:
        st.error("Failed to load data.")

# FILTER DATA SET
st.write("## Filter Dataset by Column")

col = st.selectbox("Select column", list(data[0].keys()))
operator = st.selectbox("Select operator", ["==", "!=", ">", "<", ">=", "<="])
value = st.text_input("Enter value")

if st.button("Filter"):
    filtered = filter_data(data, col, operator, value)
    st.table([list(filtered[0].keys())] + [[row[h] for h in filtered[0].keys()] for row in filtered])