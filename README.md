# dsci551-project
A data-driven web application that parses, filters, groups, aggregates, and joins CSV datasets using custom Python functions.

## Overview
This project implements an Interactive Data Processing Dashboard using Python and Streamlit. The dashboard allows users to explore and analyze datasets using common data operations such as filtering, sorting, grouping, aggregating, and joining tables. All features are optional, giving users flexibility in how they manipulate and view data. <br>

The project is designed to mimic basic SQL operations without using libraries like pandas or json for the main data operations, fulfilling educational goals of understanding data processing under the hood. <br>

## Features

1. **Dataset Selection**  
   Users can choose from multiple datasets to explore. Currently available datasets:  
   - Countries (`countries.csv`) 
   - Food Imports (`FoodImports.csv`: U. S. Department of Agriculture, Economic Research Service. U.S. Food Imports Data. https://www.ers.usda.gov/data-products/us-food-imports)

2. **Filter Data**  
   - Users can filter datasets by column, operator, and value.  
   - Only appropriate operators are available depending on column type:  
     - **String columns:** `equal to`, `not equal to`  
     - **Numeric columns:** `equal to`, `not equal to`, `greater than`, `less than`, `greater or equal`, `less or equal`  
   - Filtering is **case-insensitive** and strips whitespace for string comparisons.  

3. **Sort Data**  
   - Sort any column in ascending or descending order.  
   - Works on numeric and string columns.  

4. **Group and Aggregate**  
   - Group by a selected column and aggregate another column using:  
     - `count`, `sum`, `avg`, `min`, `max`  
   - Output is displayed in a table format ready for further inspection.  

5. **Join Tables**  
   - Perform **inner** or **left joins** between two datasets (Countries & Food Imports).  
   - Users select the join columns and type interactively.  
   - Join results can be viewed in a paginated table and downloaded as a CSV file.  

6. **Run All Steps**  
   - Apply **filter → sort → group & aggregate** in sequence automatically.  
   - All features are optional; users can skip any step.  

7. **Reset All**  
   - Clears all applied filters, sorts, aggregations, joins, and cached data.  
   - Resets the dashboard to its original state.  

8. **Paginated Table View**  
   - Uses a custom pagination function to display tables in manageable pages.  
   - Improves readability and reduces scrolling fatigue.  


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
├─ dashboard.py           # Main Streamlit app
├─ read_csv.py            # Custom CSV reader
├─ parser.py              # Parses file data
├─ aggregate.py           # Validates file path
├─ filter_data.py         # Function for filtering datasets
├─ sort_data.py           # Function for sorting datasets
├─ aggregate.py           # Group & aggregate function
├─ join.py                # Inner and left join functions
├─ projection.py          # Projection of data
├─ paginate_table.py      # Table pagination helper
├─ chunked_csv_read.py    # Handles scaling for large data
├─ data/
│   ├─ countries.csv
│   └─ FoodImports.csv
├─ requirements.txt
└─ README.md
