import streamlit as st
from paginate_table import paginate_table
from read_csv import read_csv
from filter_data import filter_data
from sort_data import sort_data
from aggregate import group_by_aggregate

# data file path 
# path = "data/toy_data_cereals.csv" # toy data
path = "data/FoodImports.csv" # larger data file

# terminal command to run page locally
# streamlit run dashboard.py

# helper function to format list-of-dicts into table format
def format_for_table(data):
    if not data:
        return []
    headers = list(data[0].keys())
    rows = [[row[h] for h in headers] for row in data]
    return [headers] + rows

# cache the dataset so it doesn’t reload each time you press a button
# helps with scaling and performance
@st.cache_data
def load_data(format=None):
    if format == "table":
        return read_csv(path, table_format=True)
    else:
        return read_csv(path)

table_data = load_data("table")
data = load_data()


# VIEW ENTIRE DATASET
# Streamlit expander toggles table visibility
# can also add different datasets here in the future when we work with join
st.write("## View Dataset")

with st.expander("View Entire Data Table"):
    if table_data:
        paginate_table(table_data, key_prefix="main_table") # data loads as a full table
    else:
        st.error("Failed to load data.")


cols = list(data[0].keys())  # list of cols in data


# FILTER DATASET
# FILTER DATASET
st.write("## Filter Dataset by Column")

filter_col = st.selectbox("Select Column to Filter", cols, key="filter_col")
operator = st.selectbox("Select operator", ["==", "!=", ">", "<", ">=", "<="], key="filter_op")
value = st.text_input("Enter value", key="filter_value")

if st.button("Filter"):
    filtered_data = filter_data(data, filter_col, operator, value)
    if filtered_data:
        st.session_state.filtered_table_data = format_for_table(filtered_data)
    else:
        st.session_state.filtered_table_data = None

# display after filtering
if "filtered_table_data" in st.session_state and st.session_state.filtered_table_data:
    paginate_table(st.session_state.filtered_table_data, key_prefix="filtered_table")


# SORT DATA SET - sort by col (asc or desc)
st.write("## Sort Dataset by Column")

sort_col = st.selectbox("Select Column to Sort", cols, key="sort_col")
order_by = st.selectbox("Select Order", ["asc", "desc"], key="sort_order")

if st.button("Sort"):
    sorted_data = sort_data(data, sort_col, order_by)
    if sorted_data:
        st.session_state.sorted_table_data = format_for_table(sorted_data)
    else:
        st.session_state.sorted_table_data = None

# display after sorting
if "sorted_table_data" in st.session_state and st.session_state.sorted_table_data:
    paginate_table(st.session_state.sorted_table_data, key_prefix="sorted_table")

# GROUP BY SECTION
# GROUP BY SECTION
st.write("## Group By and Aggregate")

group_col = st.selectbox("Select column to group by", cols, key="group_col")
agg_col = st.selectbox("Select column to aggregate", cols, key="agg_col")
agg_func_name = st.selectbox("Select aggregation function", ["count", "sum", "avg", "min", "max"], key="agg_func")

# define aggregation logic
if agg_func_name == "count":
    agg_func = lambda vals: len(vals)
elif agg_func_name == "sum":
    agg_func = lambda vals: sum(vals)
elif agg_func_name == "avg":
    agg_func = lambda vals: sum(vals) / len(vals) if vals else 0
elif agg_func_name == "min":
    agg_func = lambda vals: min(vals)
elif agg_func_name == "max":
    agg_func = lambda vals: max(vals)

if st.button("Run Group By"):
    grouped = group_by_aggregate(data, group_col, agg_col, agg_func)
    table_ready = [[group_col, f"{agg_func_name}({agg_col})"]] + [
        [key, val] for key, val in grouped.items()
    ]
    st.session_state.grouped_table_data = table_ready

# display after grouping
if "grouped_table_data" in st.session_state and st.session_state.grouped_table_data:
    paginate_table(st.session_state.grouped_table_data, key_prefix="grouped_table")
