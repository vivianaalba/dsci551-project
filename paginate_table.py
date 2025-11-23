import streamlit as st

# helper function to paginate tables 
# prevents scrolling fatigue 
# helps with scaling, prevents long load times
def paginate_table(table_data, key_prefix=""):

    if not table_data or len(table_data) < 2:
        st.warning("No data to display.")
        return

    headers = table_data[0]
    rows = table_data[1:]

    # lets user choose how many rows to see per page
    rows_per_page = st.selectbox(
        "Rows per page",
        [10, 25, 50, 100],
        index=1,
        key=f"{key_prefix}_rows_per_page"
    )

    total_pages = (len(rows) + rows_per_page - 1) // rows_per_page

    # track current page in session state using prefix key
    current_page_key = f"{key_prefix}_current_page"
    if current_page_key not in st.session_state:
        st.session_state[current_page_key] = 1

    # navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    with col1:
        if st.button("Previous", key=f"{key_prefix}_prev",
                     disabled=st.session_state[current_page_key] == 1):
            st.session_state[current_page_key] -= 1
    with col3:
        if st.button("Next", key=f"{key_prefix}_next",
                     disabled=st.session_state[current_page_key] == total_pages):
            st.session_state[current_page_key] += 1
    with col2:
        st.markdown(
            f"<p style='text-align:center;'>Page {st.session_state[current_page_key]} of {total_pages}</p>",
            unsafe_allow_html=True,
        )

    # determines which rows to show
    start_idx = (st.session_state[current_page_key] - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    page_rows = rows[start_idx:end_idx]

    # display paginated table
    st.table([headers] + page_rows)
