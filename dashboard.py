import streamlit as st
from read_csv import read_csv
from filter_data import filter_data
from sort_data import sort_data
from aggregate import group_by_aggregate
from join import inner_join, left_join
from paginate_table import paginate_table

# ==========================
# DATA PATHS
# ==========================
# toy_cereal = "data/toy_data_cereals.csv"
countries_path = "data/countries_of_the_world.csv"
food_imports_path = "data/FoodImports.csv"

# Define table 1 and table 2 for the join function
table1 = read_csv(countries_path)
table2 = read_csv(food_imports_path)

# ==========================
# HELPER FUNCTIONS
# ==========================
def format_for_table(data):
    # Convert list of dicts into table format for paginate_table
    if not data: 
        return []
    headers = list(data[0].keys())
    rows = [[row[h] for h in headers] for row in data]
    return [headers] + rows

@st.cache_data
def load_data(path, format=None):
    data = read_csv(path)
    if format == "table":
        return format_for_table(data)
    return data

# ==========================
# LOAD DATASETS
# ==========================
datasets = {
    "Food Imports": (load_data(food_imports_path), load_data(food_imports_path, "table")),
    # "Toy Cereals": (load_data(toy_data_path), load_data(toy_data_path, "table")),
    "Countries": (load_data(countries_path), load_data(countries_path, "table")),
}

# ==========================
# DASHBOARD UI SETUP
# ==========================
st.title("Interactive Data Processing Dashboard")
st.write("Use the controls below to filter, sort, group, and aggregate datasets interactively.")

# allows users to select dataset for exploration
dataset_name = st.selectbox("Select a dataset:", list(datasets.keys()))
data, table_data = datasets[dataset_name]
cols = list(data[0].keys())

# resets session state
if st.button("Reset All"):
    st.session_state.processed_data = None
    st.session_state.processed_table = None
    st.session_state.filters_applied = None
    st.session_state.sort_applied = None
    st.session_state.group_applied = None
    st.cache_data.clear()
    st.experimental_rerun()

# ==========================
# FILTER
# ==========================
st.header("Step 1: Filter Dataset")

operator_map = {
    "==": "equal to",
    "!=": "not equal to",
    ">": "greater than",
    "<": "less than",
    ">=": "greater than or equal to",
    "<=": "less than or equal to"
}

filter_col = st.selectbox("Select column to filter by", cols, key="filter_col")
selected_written_op = st.selectbox("Select operator", list(operator_map.values()), key="filter_op")
selected_op = [op for op, written in operator_map.items() if written == selected_written_op][0]
filter_value = st.text_input("Enter value", key="filter_value")

# ==========================
# SORT
# ==========================
st.header("Step 2: Sort Dataset")
sort_col = st.selectbox("Select column to sort by", cols, key="sort_col")
order_by = st.selectbox("Select sort order", ["asc", "desc"], key="sort_order")

# ==========================
# GROUP & AGGREGATE
# ==========================
st.header("Step 3: Group and Aggregate")
group_col = st.selectbox("Select column to group by", cols, key="group_col")
agg_col = st.selectbox("Select column to aggregate", cols, key="agg_col")
agg_func_name = st.selectbox("Aggregation Function", ["count", "sum", "avg", "min", "max"], key="agg_func")

# define aggregation function
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

# ==========================
# JOIN SECTION 
# ==========================
st.header("Step 4: Join Two Datasets")

# Preview first 10 rows of each table, as in other steps
st.subheader("Preview of Table 1")
st.dataframe(table1[:10])
st.subheader("Preview of Table 2")
st.dataframe(table2[:10])

columns1 = list(table1[0].keys()) if table1 else []
columns2 = list(table2[0].keys()) if table2 else []

# User selects which column from each table to join on
join_col1 = st.selectbox("Select join column from Table 1", columns1, key="join_col1")
join_col2 = st.selectbox("Select join column from Table 2", columns2, key="join_col2")

join_type = st.selectbox("Join type", ["inner", "left"], key="join_type")

if st.button("Run Join"):
    if join_type == "inner":
        joined = inner_join(table1, table2, join_col1, join_col2)
    else:
        joined = left_join(table1, table2, join_col1, join_col2)
    st.session_state["joined_data"] = joined
    st.session_state["joined_applied"] = (join_col1, join_col2, join_type)

# Show joined table just like groupby or filtered output
if "joined_data" in st.session_state:
    st.subheader("Joined Result (first 20 rows)")
    st.dataframe(st.session_state["joined_data"][:20])
    import pandas as pd
    df = pd.DataFrame(st.session_state["joined_data"])
    st.download_button(
        "Download Joined CSV",
        data=df.to_csv(index=False),
        file_name="joined.csv",
        mime="text/csv"
    )

# ==========================
# RUN ALL STEPS
# ==========================
if st.button("Run All Steps"):
    current_data = data

    # applies filter
    if filter_col and filter_value:
        current_data = filter_data(current_data, filter_col, selected_op, filter_value)
        st.session_state.filters_applied = (filter_col, selected_op, filter_value)

    # applies sort
    if sort_col:
        current_data = sort_data(current_data, sort_col, order_by)
        st.session_state.sort_applied = (sort_col, order_by)

    # applies group & aggregate
    if group_col and agg_col and agg_func_name:
        grouped = group_by_aggregate(current_data, group_col, agg_col, agg_func)
        current_data = [dict(zip([group_col, f"{agg_func_name}({agg_col})"], [k, v])) for k, v in grouped.items()]
        st.session_state.group_applied = (group_col, agg_col, agg_func_name)
        st.session_state.processed_table = format_for_table(current_data)

    # savese final processed data
    st.session_state.processed_data = current_data

# ==========================
# DISPLAY FINAL TABLE
# ==========================
st.header("Step 4: View Final Table")

if "processed_table" in st.session_state:
    table_ready = st.session_state.processed_table
elif "processed_data" in st.session_state: # formats table if needed
    table_ready = format_for_table(st.session_state.processed_data)
else: # no processing done, shows original table
    table_ready = table_data

with st.expander(f"View {dataset_name} Data Table"):
    paginate_table(table_ready, key_prefix=dataset_name.replace(" ", "_"))


