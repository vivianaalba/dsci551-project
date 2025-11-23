# dsci551-project
A data-driven web application that parses, filters, projects, groups, aggregates, and joins CSV datasets using custom Python functions.
Project by: Viviana Alba, Kayla Hoffman -- M/W Section

## Overview
This project implements an Interactive Data Processing Dashboard using Python and Streamlit. The dashboard allows users to explore and analyze datasets using common data operations such as filtering, projection, sorting, grouping, aggregating, and joining tables. All features are optional, giving users flexibility in how they manipulate and view data. <br>

This project is designed to mimic basic SQL operations without using libraries like pandas or json for the main data operations while working with a user friendly UI. <br>

## Features

1. **Dataset Selection**  
   Users can choose from multiple datasets to explore. Currently available datasets:  
   - Countries (`countries.csv`: Global Country Information Dataset 2023
 , Kaggle, https://www.kaggle.com/datasets/nelgiriyewithana/countries-of-the-world-2023)
   - Food Imports (`FoodImports.csv`: U.S. Department of Agriculture, Economic Research Service. U.S. Food Imports Data. https://www.ers.usda.gov/data-products/us-food-imports)

2. **Filter Data**  
   - Users can filter datasets by column, operator, and value.  
   - Only appropriate operators are available depending on column type:  
     - **String columns:** `equal to`, `not equal to`  
     - **Numeric columns:** `equal to`, `not equal to`, `greater than`, `less than`, `greater or equal`, `less or equal`  
   - Filtering is **case-insensitive**, strips whitespace, and supports cleaned numeric formats (e.g., `"1,000"` → `1000`).  

3. **Project (Select Columns)**  
   - Users can choose specific columns to *keep* in the dataset.  
   - Supports flexible column subsets for focused analysis.  
   - Projection integrates seamlessly with all other operations and the Run All pipeline.

4. **Sort Data**  
   - Sort by any column in ascending or descending order.  
   - Works for numeric and string data types.  
   - Can also sort the **results of aggregations**, enabling ranked summaries.

5. **Group and Aggregate**  
   - Group rows by a selected column and compute an aggregation on another column using:  
     - `count`, `sum`, `avg`, `min`, `max`  
   - Automatically handles numeric cleaning and conversion.  
   - Aggregated output is sortable and displayed in a clean table format.

6. **Join Tables**  
   - Perform **inner** or **left** joins between the Countries and Food Imports datasets.  
   - Users select the join columns interactively.  
   - Joined data becomes the active dataset for further filtering, projecting, sorting, and aggregating.

7. **Run All Steps**  
   - Executes the full pipeline automatically:  
     **JOIN → PROJECT → FILTER → SORT → GROUP & AGGREGATE**  
   - Allows users to build complex data transformations with a single click.  
   - All steps are optional; skipped steps leave the data unchanged.
   - Current Pipeline:
      - Join applied (Countries.Code = FoodImports.Country)
      - Projection: [country, region, gdp]
      - Filter: gdp > 5000
      - Sort: gdp desc
      - Aggregate: group by region, avg(gdp)

8. **Limit**  
   - Users can restrict the number of rows displayed in the final output table.  
   - Useful for large results or testing workflows on smaller samples.

9. **Reset All**  
   - Clears all filters, projections, sorts, joins, aggregated results, and cached data.  
   - Returns the dashboard to its original state for fresh analysis.

10. **Scaling Features**
   - **Chunked Reading for Scalability**  
      - Implements custom `chunked_csv_reader` to load large CSV files in batches.  
      - Prevents memory overload by processing data incrementally.  
      - Supports scalable previewing and step-by-step processing of large datasets.
   - **Paginated Table View**  
      - Uses a custom pagination system to display large tables in manageable pages.  
      - Supports horizontal scrolling for wide tables, improving readability.  
      - Ideal for datasets with many columns.
   - **Caching Data in Dashboard**
      - Allows for faster processing when using large datasets by preventing contstant reload of data.


## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-folder>

2. **Install Dependencies**
   ```bash
    pip install -r requirements.txt

4. **Run Dashboard**
   ```bash
    streamlit run dashboard.py


## Using the Dashboard
1. Select a dataset from the dropdown menu.
2. Optionally filter, sort, group & aggregate the data.
3. Optionally join two tables using matching columns.
4. Use “Run All Steps” to apply selected operations sequentially.
5. View processed data in the paginated table and download CSV for joined data.
6. Click “Reset All” to restart the analysis with the original dataset.

## Implementation Notes
- No external libraries for data processing are used; all filtering, sorting, grouping, and joins are implemented manually.
- Column type detection is performed dynamically for each dataset to ensure proper operator selection.
- Optional feature usage: Users can apply any combination of steps; skipping a step leaves the dataset unchanged.
- Scalability: Tables are paginated to handle larger datasets. Caching is implemented via st.cache_data for faster reloads.

## File Structure
```bash
project-root/
│
├─ dashboard.py           # Streamlit UI, implementation
├─ read_csv.py            # Custom CSV reader
├─ parser.py              # Parses data and cleans fields
├─ validate_path.py       # Validates file path
├─ aggregate.py           # Aggregate / group by column
├─ filter_data.py         # Function for filtering datasets
├─ sort_data.py           # Function for sorting datasets
├─ join.py                # Inner and left join functions
├─ projection.py          # Projection of data
├─ paginate_table.py      # Table pagination helper function
├─ chunked_csv_read.py    # Handles scaling for large data
├─ limit_data.py          # Limit feature for final table
├─ data/
│   ├─ countries.csv
│   └─ FoodImports.csv
├─ requirements.txt       # project only uses Streamlit UI
└─ README.md
