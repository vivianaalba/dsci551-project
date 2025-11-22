import streamlit as st  # to run: streamlit run dashboard.py
from read_csv import read_csv
from filter_data import filter_data
from sort_data import sort_data
from aggregate import group_by_aggregate, group_by
from join import inner_join, left_join
from paginate_table import paginate_table
from chunked_csv_read import chunked_csv_reader
from projection import project
from limit_data import limit_data

# ==========================
# PAGE CONFIG
# ==========================
st.set_page_config(
    page_title="Data2App Dashboard",
    layout="wide",
)

# ==========================
# HELPER FUNCTIONS
# ==========================

# get col types for filtering, sorting, and projection options
# chose to implement this so that user does not have to manually type
# each function handles types internally
def get_column_types(data):
    """Infer column types (numeric vs string) based on current dataset."""
    if not data:
        return {}
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
                break  # if any val for col is non-numeric, treat as string
        if col_type is None:
            col_type = 'string'  # default if all values are null
        col_types[col] = col_type
    return col_types

# format output data from list of dicts to rows table format
# suitable for the st.table display
def format_for_table(data):
    if not data:
        return []
    headers = list(data[0].keys())
    rows = [[row.get(h) for h in headers] for row in data]
    return [headers] + rows


# chached data loading for performance
# used for scalability purposes -- data does not have to reaload after processing
@st.cache_data
def load_data(path, format=None):
    """Load CSV using custom reader, optionally as table format."""
    data = read_csv(path)
    if format == "table":
        return format_for_table(data)
    return data


# ==========================
# AVAILABLE DATASETS
# ==========================

# application can be used with more datasets 
# add paths and load datasets here 
# can replace current datasets as table1 and table2
countries_path = "data/countries.csv"
food_imports_path = "data/FoodImports.csv"


datasets = {
    "Food Imports": (load_data(food_imports_path), load_data(food_imports_path, "table")),
    "Countries": (load_data(countries_path), load_data(countries_path, "table")),
}

dataset_paths = {
    "Food Imports": food_imports_path,
    "Countries": countries_path,
}

# pre-load full tables for joins
table1 = read_csv(countries_path)       # Countries data
table2 = read_csv(food_imports_path)    # Food Imports data

# ==========================================================
#                   SIDEBAR CONTROLS
# ==========================================================
st.sidebar.title("Controls")

# select dataset to process (filter, projection, sort, group, aggregate)
dataset_name = st.sidebar.selectbox("Select dataset", list(datasets.keys()))
original_data, original_table = datasets[dataset_name]
file_path = dataset_paths[dataset_name]

# determine starting dataset: joined result if exists, else original
# pipeline is similar to sql -- we start with joined data in processing
if "joined_data" in st.session_state:
    current_data = st.session_state.joined_data
else:
    current_data = st.session_state.get("current_data", original_data)

# get cols for current active data
cols = list(current_data[0].keys()) if current_data else []

# RESET ALL
if st.sidebar.button("Reset All"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.cache_data.clear()
    st.rerun()

st.sidebar.markdown("---")

# ==========================
# SIDEBAR: STEP 1 – FILTER
# ==========================
with st.sidebar.expander("Step 1 · Filter", expanded=False):
    if current_data:
        filter_col = st.selectbox("Column", cols, key="filter_col")

        col_types = get_column_types(current_data)
        col_type = col_types.get(filter_col, 'string')

        # operator choices depend on type
        if col_type == 'string': # cannot sort > or < for strings
            available_ops = ["equal to", "not equal to"]
        else:
            available_ops = [
                "equal to", "not equal to",
                "greater than", "less than",
                "greater or equal", "less or equal"
            ]

        selected_written_op = st.selectbox("Operator", available_ops)

        # maps written operators to actual symbols
        # easier for users to understand
        operator_map = {
            "equal to": "==",
            "not equal to": "!=",
            "greater than": ">",
            "less than": "<",
            "greater or equal": ">=",
            "less or equal": "<="
        }
        raw_op = operator_map[selected_written_op]

        filter_value = st.text_input("Value")

        # chunked filtering option (for scaling)
        # chunks data from CSV file instead of in-memory -- shows scalability
        # can be toggles on and off
        chunked_filter = st.checkbox("Use chunked filtering")
        chunk_size = 1000
        if chunked_filter:
            chunk_size = st.number_input(
                "Chunk size (rows/chunk)",
                min_value=1,
                max_value=100000,
                value=1000,
                step=100,
                key="chunk_size_input"
            )

        if st.button("Apply Filter"):
            try:
                if chunked_filter:
                    # pass CSV file path when chunked filtering
                    filtered = filter_data(
                        file_path,
                        filter_col,
                        raw_op,
                        filter_value,
                        chunked_filter=True,
                        chunk_size=chunk_size
                    )
                else:
                    filtered = filter_data(
                        current_data,
                        filter_col,
                        raw_op,
                        filter_value,
                        chunked_filter=False
                    )
                current_data = filtered
                st.session_state.current_data = current_data
                st.session_state.processed_table = format_for_table(current_data)
                st.success("Filter applied.")
            except Exception as e:
                st.error(f"Filter error: {e}")

        if st.button("Clear Filter"):
            if "filter_value" in st.session_state:
                del st.session_state["filter_value"]
            st.session_state.current_data = original_data
            st.success("Filter cleared.")
            st.rerun()

st.sidebar.markdown("---")

# ==========================
# SIDEBAR: STEP 2 – PROJECTION
# ==========================
with st.sidebar.expander("Step 2 · Projection (Select Columns)", expanded=False):
    all_columns = list(current_data[0].keys()) if current_data else []
    selected_columns = st.multiselect(
        "Columns to KEEP",
        options=all_columns,
        default=all_columns,
        key="selected_columns_multiselect"
    )

    if st.button("Apply Projection"):
        try:
            current_data = project(current_data, selected_columns)
            st.session_state.current_data = current_data
            st.session_state.processed_table = format_for_table(current_data)
            st.success("Projection applied.")
        except ValueError as e:
            st.error(str(e))

    if st.button("Clear Projection"):
        if "selected_columns" in st.session_state:
            del st.session_state["selected_columns"]
        st.session_state.current_data = original_data
        st.success("Projection cleared.")
        st.rerun()

st.sidebar.markdown("---")

# ==========================
# SIDEBAR: STEP 3 – SORT
# ==========================
with st.sidebar.expander("Step 3 · Sort", expanded=False):
    if cols:
        sort_col = st.selectbox("Sort column", cols, key="sort_col")
        order = st.selectbox("Order", ["asc", "desc"], key="sort_order")

        if st.button("Apply Sort"):
            current_data = sort_data(current_data, sort_col, order)
            st.session_state.current_data = current_data
            st.session_state.processed_table = format_for_table(current_data)
            st.success("Sort applied.")

        if st.button("Clear Sort"):
            if "sort_col" in st.session_state:
                del st.session_state["sort_col"]
            st.session_state.current_data = original_data
            st.success("Sort cleared.")
            st.rerun()

st.sidebar.markdown("---")

# ==========================
# SIDEBAR: STEP 4 – GROUP / AGGREGATE
# ==========================

# in this step, users can choose to either group only or group + aggregate
# can also sort the new aggregated results by the aggregated value
# NAN values in count are grouped together
with st.sidebar.expander("Step 4 · Group / Aggregate", expanded=False):
    if cols:
        group_mode = st.radio(
            "Mode",
            ["Group + Aggregate", "Group Only"],
            index=0,
            key="group_mode_radio"
        )

        group_col = st.selectbox("Group by column", cols, key="group_col")

        if group_mode == "Group + Aggregate":
            agg_col = st.selectbox("Column to aggregate", cols, key="agg_col")
            agg_func_name = st.selectbox(
                "Aggregation function",
                ["count", "sum", "avg", "min", "max"],
                key="agg_func_name"
            )

            agg_sort_order = st.selectbox(
                "Sort aggregated results",
                ["asc", "desc"],
                key="agg_sort_order"
            )

            # build aggregation function
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

        if st.button("Apply Grouping"):
            if group_mode == "Group Only":
                grouped = group_by(current_data, group_col)
                current_data = [
                    {group_col: key, "rows": len(rows)}
                    for key, rows in grouped.items()
                ]
                st.success("Simple grouping applied.")
            else:
                grouped = group_by_aggregate(current_data, group_col, agg_col, func)
                result_col_name = f"{agg_func_name}({agg_col})"

                current_data = [
                    {group_col: key, result_col_name: value}
                    for key, value in grouped.items()
                ]

                # sort aggregated results using custom sorter
                # because a new col in created, the sort option does not store this new col
                # group / aggregate step is after sort step in pipeline
                # so we implemented custom aggregation sorter here
                current_data = sort_data(current_data, result_col_name, agg_sort_order)
                st.success("Group & Aggregate applied.")

            st.session_state.current_data = current_data
            st.session_state.processed_table = format_for_table(current_data)

        if st.button("Clear Aggregation"):
            for key in ["group_col", "agg_col", "agg_func_name"]:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.current_data = original_data
            st.success("Aggregation cleared.")
            st.rerun()

st.sidebar.markdown("---")

# ==========================
# SIDEBAR: STEP 5 – JOIN
# ==========================
with st.sidebar.expander("Step 5 · Join Tables", expanded=False):
    cols1 = list(table1[0].keys())
    cols2 = list(table2[0].keys())

    join_key_1 = st.selectbox("Countries join column", cols1, key="join_key_1")
    join_key_2 = st.selectbox("Food Imports join column", cols2, key="join_key_2")
    join_type = st.selectbox("Join type", ["inner", "left"], key="join_type")

    if st.button("Run Join"):
        if join_type == "inner":
            joined = inner_join(table1, table2, join_key_1, join_key_2)
        else:
            joined = left_join(table1, table2, join_key_1, join_key_2)

        st.session_state.joined_data = joined
        st.session_state.current_data = joined
        st.session_state.processed_table = format_for_table(joined)
        st.success("Join completed! Joined table is now active.")

    if st.button("Clear Join"):
        if "joined_data" in st.session_state:
            del st.session_state["joined_data"]
        st.session_state.current_data = original_data
        st.success("Join cleared.")
        st.rerun()

st.sidebar.markdown("---")

# ==========================
# SIDEBAR: STEP 6 – RUN SELECTED STEPS
# ==========================

# pipeline is similar to sql query execution plan
# JOIN → PROJECTION → FILTER → SORT → GROUP/AGGREGATE
with st.sidebar.expander("Step 6 · Run Selected Steps", expanded=False):

    st.write("Select which steps should be included in the pipeline:")
    
    # users can choose whether or not to include each step
    # auto sets to true, but can uncheck to skip step
    # steps are listed in order of pipeline execution
    step_join = st.checkbox("Include Join", value=True)
    step_project = st.checkbox("Include Projection", value=True)
    step_filter = st.checkbox("Include Filter", value=True)
    step_sort = st.checkbox("Include Sort", value=True)
    step_group = st.checkbox("Include Group / Aggregate", value=True)

    st.markdown("---")

    if st.button("Run Pipeline"):
        pipeline_data = st.session_state.get("joined_data", original_data)

        # =====================================
        # 1. JOIN
        # =====================================
        if step_join:
            try:
                if join_type == "inner":
                    pipeline_data = inner_join(table1, table2, join_key_1, join_key_2)
                else:
                    pipeline_data = left_join(table1, table2, join_key_1, join_key_2)
            except Exception as e:
                st.sidebar.error(f"Join skipped: {e}")

        # =====================================
        # 2. PROJECTION
        # =====================================
        if step_project:
            try:
                pipeline_data = project(pipeline_data, selected_columns)
            except Exception as e:
                st.sidebar.error(f"Projection skipped: {e}")

        # =====================================
        # 3. FILTER
        # =====================================
        if step_filter:
            try:
                pipeline_data = filter_data(pipeline_data, filter_col, raw_op, filter_value)
            except Exception as e:
                st.sidebar.error(f"Filter skipped: {e}")

        # =====================================
        # 4. SORT
        # =====================================
        if step_sort:
            try:
                sort_order_val = st.session_state.get("sort_order", "asc")
                pipeline_data = sort_data(pipeline_data, sort_col, sort_order_val)
            except Exception as e:
                st.sidebar.error(f"Sort skipped: {e}")

        # =====================================
        # 5. GROUP + AGGREGATE
        # =====================================
        if step_group:
            try:
                # Build aggregation function again (safe)
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

                grouped = group_by_aggregate(pipeline_data, group_col, agg_col, func)
                pipeline_data = [
                    {group_col: k, f"{agg_func_name}({agg_col})": v}
                    for k, v in grouped.items()
                ]
            except Exception as e:
                st.sidebar.error(f"Grouping skipped: {e}")

        # =====================================
        # FINISH PIPELINE
        # =====================================
        st.session_state.current_data = pipeline_data
        st.session_state.processed_table = format_for_table(pipeline_data)
        st.sidebar.success("Pipeline has been executed!")

# ==========================================================
#                   MAIN PAGE LAYOUT
# ==========================================================

st.title("Interactive Data Processing Dashboard")

st.caption(
    "Explore and analyze CSV datasets using custom-built parsing, filtering, "
    "projection, sorting, grouping, aggregation, joins, and chunked reading. "
    "Use the sidebar to the left to apply various data processing steps. You "
    "can use one or more steps to transform the data as needed and reset "
    "at any time!"
)

# PREVIEW RAW DATASETS
# allows users to see original datasets before processing
with st.expander("Preview Raw Datasets", expanded=False):
    col_a, col_b = st.columns(2)
    with col_a:
        st.markdown("**Countries (first 10 rows)**")
        st.dataframe(table1[:10], use_container_width=True)
    with col_b:
        st.markdown("**Food Imports (first 10 rows)**")
        st.dataframe(table2[:10], use_container_width=True)

st.markdown("---")

# FINAL OUTPUT TABLE
st.header("Processed Output Table")

final_data = st.session_state.get("current_data", current_data)
final_table = format_for_table(final_data)

limit_n = st.number_input(
    "Limit number of rows to display",
    min_value=1,
    step=1,
    value=len(final_data) if final_data else 1,
)

limited_final_data = limit_data(final_data, limit_n)
limited_table = format_for_table(limited_final_data)

with st.expander("View Processed Table"):
    paginate_table(limited_table, key_prefix="final")

st.markdown("---")

# CHUNKED DATA VIEWER
# demonstrates chunked reading for scalability
with st.expander("Chunked CSV Data Viewer (Scalability Demo)", expanded=False):
    st.write(
        "This viewer demonstrates chunked reading of large CSV files using "
        "the custom `chunked_csv_reader` function."
    )

    dataset_path = food_imports_path  # focusing on FoodImports for scaling demo

    chunk_size_view = st.number_input(
        "Rows per chunk",
        min_value=1,
        value=1000,
        step=1,
        key="chunk_view_chunk_size"
    )

    if st.button("Load Data Chunks"):
        max_chunks_display = 3  # limit number of chunks displayed for performance
        chunk_number = 0
        for chunk in chunked_csv_reader(dataset_path, chunk_size_view):
            chunk_number += 1
            st.write(f"Chunk {chunk_number} (Rows: {len(chunk)}):")
            if chunk:
                headers = list(chunk[0].keys())
                table = [headers] + [[row[h] for h in headers] for row in chunk]
                st.table(table)
            else:
                st.write("Empty chunk.")
            if chunk_number >= max_chunks_display:
                break
        st.success("Chunks loaded.")