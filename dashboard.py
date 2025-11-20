import streamlit as st  # to run: streamlit run dashboard.py
from read_csv import read_csv
from filter_data import filter_data
from sort_data import sort_data
from aggregate import group_by_aggregate
from join import inner_join, left_join
from paginate_table import paginate_table
from chunked_csv_read import chunked_csv_reader
from projection import project


# ==========================
# DATA PATHS
# ==========================
countries_path = "data/countries.csv"
food_imports_path = "data/FoodImports.csv"

# ==========================
# HELPER FUNCTIONS
# ==========================
def get_column_types(data):
    col_types = {}
    for col in data[0].keys():
        col_type = None
        for row in data:
            val = row[col]
            if val is None or val == '':
                continue  # skip missing/null values in type detection
            try:
                float(val)
                col_type = 'numeric'
            except ValueError:
                col_type = 'string'
                break  # if any value for col is non-numeric, treat as string
        if col_type is None:
            col_type = 'string'  # default if all values are null
        col_types[col] = col_type
    return col_types


def format_for_table(data):
    if not data:
        return []
    headers = list(data[0].keys())
    rows = [[row.get(h) for h in headers] for row in data]
    return [headers] + rows

@st.cache_data
def load_data(path, format=None):
    data = read_csv(path)
    if format == "table":
        return format_for_table(data)
    return data

# ==========================
# AVAILABLE DATASETS
# ==========================
datasets = {
    "Food Imports": (load_data(food_imports_path), load_data(food_imports_path, "table")),
    "Countries": (load_data(countries_path), load_data(countries_path, "table")),
}

# tables for JOIN
table1 = read_csv(countries_path)
table1_col_types = get_column_types(table1)

table2 = read_csv(food_imports_path)
table2_col_types = get_column_types(table2)

# ==========================================================
#                   DASHBOARD START
# ==========================================================

st.title("Interactive Data Processing Dashboard")
# dashboard instructions for users
st.write("This dashboard lets you interactively explore and analyze two datasets using several optional tools. " \
         "Start by selecting a dataset from the sidebar. You can filter the data by " \
         "choosing a column and entering a value, sort the results by any column, or " \
         "group and aggregate the data to compute summary statistics. If you want to combine " \
         "datasets, you can also perform inner or left joins using matching keys from each table. " \
         "All features are optional, so you can use as many or as few as you need. After applying your " \
         "selections, the processed results will appear below along with an automatically " \
         "paginated table you can scroll through. This makes it easy to examine raw data, " \
         "transformed data, and joined tables in a clean, organized view."
        )

st.subheader("Preview Table 1 (Countries)")
st.dataframe(table1[:10])

st.subheader("Preview Table 2 (Food Imports)")
st.dataframe(table2[:10])

# ==========================
# DATASET SELECTION
# ==========================
dataset_name = st.selectbox("Select a dataset:", list(datasets.keys()))

# original dataset + table version
original_data, original_table = datasets[dataset_name]

# Determine starting dataset for pipeline:
# If we JUST ran a join → use joined data
# Otherwise → use original
if "joined_data" in st.session_state:
    current_data = st.session_state.joined_data
else:
    current_data = original_data

# ==========================
# RESET BUTTON
# ==========================
if st.button("Reset All"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.cache_data.clear()
    st.experimental_rerun()

# ==========================
# STEP 1: FILTER
# ==========================
st.header("Step 1: Filter Dataset")

if current_data:
    cols = list(current_data[0].keys())
else:
    cols = []

# Step 1a: choose column
filter_col = st.selectbox("Column to filter by", cols, key="filter_col")

# Step 1b: determine column type
col_types = get_column_types(current_data)
col_type = col_types.get(filter_col, 'string')

# Step 1c: choose operator based on column type
if col_type == 'string':
    available_ops = ["equal to", "not equal to"]
else:
    available_ops = ["equal to", "not equal to", "greater than", "less than", "greater or equal", "less or equal"]

selected_written_op = st.selectbox("Select operator", available_ops)

operator_map = {
    "equal to": "==",
    "not equal to": "!=",
    "greater than": ">",
    "less than": "<",
    "greater or equal": ">=",
    "less or equal": "<="
}
raw_op = operator_map[selected_written_op]

# Step 1d: enter filter value

filter_value = st.text_input("Enter value to filter", key="filter_value")

# Apply Filter button
if st.button("Apply Filter"):
    try:
        current_data = filter_data(current_data, filter_col, raw_op, filter_value)
        st.session_state.current_data = current_data
        st.session_state.processed_table = format_for_table(current_data)
        st.success("Filter applied.")
    except Exception as e:
        st.error(f"Filter error: {e}")

# ==========================
# STEP 2: PROJECT (SELECT COLUMNS)
# ==========================
st.header("Step 2: Select Columns (Projection)")

all_columns = list(current_data[0].keys()) if current_data else []
selected_columns = st.multiselect(
    "Choose columns to KEEP:",
    options=all_columns,
    default=all_columns
)

if st.button("Apply Projection"):
    try:
        current_data = project(current_data, selected_columns)
        st.session_state.current_data = current_data
        st.session_state.processed_table = format_for_table(current_data)
        st.success("Projection applied.")
    except ValueError as e:
        st.error(str(e))

# ==========================
# STEP 3: SORT
# ==========================
st.header("Step 3: Sort Dataset")
sort_col = st.selectbox("Select column to sort by", cols)
order = st.selectbox("Sort order", ["asc", "desc"])

if st.button("Apply Sort"):
    current_data = sort_data(current_data, sort_col, order)
    st.session_state.current_data = current_data
    st.session_state.processed_table = format_for_table(current_data)
    st.success("Sort applied.")

# ==========================
# STEP 4: GROUP + AGGREGATE
# ==========================
st.header("Step 4: Group and Aggregate")

group_col = st.selectbox("Group by column", cols, key="group_col")
agg_col = st.selectbox("Column to aggregate", cols, key="agg_col")
agg_func_name = st.selectbox("Aggregation function", ["count", "sum", "avg", "min", "max"])

# Build aggregation functions
if agg_func_name == "count":
    func = lambda vals: len(vals)
elif agg_func_name == "sum":
    func = lambda vals: sum(vals)
elif agg_func_name == "avg":
    func = lambda vals: sum(vals) / len(vals) if vals else 0
elif agg_func_name == "min":
    func = lambda vals: min(vals)
elif agg_func_name == "max":
    func = lambda vals: max(vals)

if st.button("Apply Group & Aggregate"):
    grouped = group_by_aggregate(current_data, group_col, agg_col, func)
    current_data = [
        {group_col: key, f"{agg_func_name}({agg_col})": value}
        for key, value in grouped.items()
    ]
    st.session_state.current_data = current_data
    st.session_state.processed_table = format_for_table(current_data)
    st.success("Group & Aggregate applied.")

# ==========================
# STEP 5: JOIN DATASETS — now integrated
# ==========================
st.header("Step 5: Join Two Datasets")

cols1 = list(table1[0].keys())
cols2 = list(table2[0].keys())

join_key_1 = st.selectbox("Join column from Countries", cols1)
join_key_2 = st.selectbox("Join column from Food Imports", cols2)

join_type = st.selectbox("Join type", ["inner", "left"])

if st.button("Run Join"):
    if join_type == "inner":
        joined = inner_join(table1, table2, join_key_1, join_key_2)
    else:
        joined = left_join(table1, table2, join_key_1, join_key_2)

    st.session_state.joined_data = joined
    st.session_state.current_data = joined
    st.session_state.processed_table = format_for_table(joined)
    st.success("Join completed! The join result is now your active dataset.")

    st.session_state.processed_table = None
    st.experimental_rerun()

# ==========================
# STEP 6: RUN ALL STEPS AT ONCE
# ==========================
if st.button("Run All Steps"):
    pipeline_data = st.session_state.get("joined_data", original_data)

    # Projection
    if 'selected_columns' in locals():
        try:
            pipeline_data = project(pipeline_data, selected_columns)
        except:
            pass

    # Filter
    pipeline_data = filter_data(pipeline_data, filter_col, raw_op, filter_value)

    # Sort
    pipeline_data = sort_data(pipeline_data, sort_col, order)

    # Group
    grouped = group_by_aggregate(pipeline_data, group_col, agg_col, func)
    pipeline_data = [
        {group_col: k, f"{agg_func_name}({agg_col})": v}
        for k, v in grouped.items()
    ]

    st.session_state.current_data = pipeline_data
    st.session_state.processed_table = format_for_table(pipeline_data)
    st.success("All steps applied successfully.")

# ==========================
# STEP 7: Chunked Data Viewer
# ==========================

st.title("Chunked CSV Data Viewer")

dataset_path = "data/FoodImports.csv"

chunk_size = st.number_input(
    "Number of rows per chunk", 
    min_value=1, 
    value=1000, step=1
)

if st.button("Load Data Chunks"):
    max_chunks_display = 3  # limit number of chunks displayed for performance
    chunk_number = 0
    for chunk in chunked_csv_reader(dataset_path, chunk_size):
        chunk_number += 1
        st.write(f"Chunk {chunk_number} (Rows: {len(chunk)}):")
        headers = list(chunk[0].keys()) if chunk else []
        table = [headers] + [[row[h] for h in headers] for row in chunk]
        st.table(table)
        if chunk_number >= max_chunks_display:
            break
    st.success("Chunks loaded.")

# ==========================
# FINAL OUTPUT TABLE (paginated)
# ==========================
st.header("Final Output Table")

final_data = st.session_state.get("current_data", current_data)
final_table = format_for_table(final_data)

with st.expander("View Processed Table"):
    paginate_table(final_table, key_prefix="final")
