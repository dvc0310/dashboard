
# OutageDataProcessor Detailed Documentation

## Overview

The `OutageDataProcessor` class is responsible for loading, processing, and aggregating outage data. It filters the data based on specified years and company names, converts date columns to datetime objects, and aggregates data to provide insights into outage frequency over time.


## Methods Detail

### Constructor: `__init__(outage_file_name, start_year, end_year, folder='datasets')`
- **Purpose**: Initializes a new instance of the `OutageDataProcessor` with specified parameters.
- **Parameters**:
  - `outage_file_name` (str): Name of the outage data CSV file.
  - `start_year` (int): The start year for filtering data.
  - `end_year` (int): The end year for filtering data.
  - `folder` (str, optional): Directory where the data files are located, defaults to 'datasets'.
- **Action**: Sets up the file path for the outage data, initializes the year range for filtering, and loads the data.

### Example Usage

```python
processor = OutageDataProcessor('outage_data.csv', 2021, 2023)
```

### `load_data()`
- **Purpose**: Loads data from the specified CSV file, applying filters to include only relevant years, companies, and final report statuses.
- **Process**:
  1. **Column Selection**: Specifies columns to be used from the CSV file.
  2. **Chunk Reading**: Reads the CSV file in chunks to handle large datasets efficiently.
  3. **Filtering**: Applies filters on each chunk to retain only the required data.
  4. **Combining Chunks**: Combines the filtered chunks into a single DataFrame for further processing.

### `get_outage_frequency()`
- **Purpose**: Aggregates the processed data by 'Company', 'Year', and 'Quarter', and counts the occurrences of outages.
- **Returns**: A DataFrame with aggregated outage data.
- **Process**:
  1. **Aggregation**: Groups the data by 'Company', 'Year', and 'Quarter'.
  2. **Counting**: Counts the number of outages for each group.
  3. **Validation**: Checks if the data is loaded and not empty before proceeding with aggregation.

### Private Methods

#### `_combine_chunks(filtered_chunks)`
- **Purpose**: Combines filtered chunks of data into a single DataFrame and processes date and company information.
- **Process**:
  1. **Concatenation**: Combines all filtered chunks into a single DataFrame.
  2. **Renaming Columns**: Renames the relevant columns for consistency.
  3. **Extracting Year and Quarter**: Derives 'Year' and 'Quarter' from the incident date.
  4. **Logging**: Logs the successful loading and processing of data.

#### `_datetime_conversion(column)`
- **Purpose**: Converts string representations of dates into `datetime` objects using multiple specified formats to ensure accuracy.
- **Process**:
  1. **Conversion Attempt**: Tries to convert the date using a list of specified formats.
  2. **Fallback Conversion**: Uses a fallback conversion with error handling if the specified formats fail.

#### `_filter_by_company_status_year(chunk)`
- **Purpose**: Filters each chunk of data by company status, incident year, and report status.
- **Process**:
  1. **Date Conversion**: Converts the incident date to `datetime`.
  2. **Company Mapping**: Maps company names using predefined aliases.
  3. **Filtering Conditions**: Applies conditions to retain only relevant data based on year range, final report status, and valid company names.

#### `_read_csv_by_chunks(chunk_size, use_columns, filtered)`
- **Purpose**: Reads large CSV files in manageable chunks, applying filters during the process to minimize memory usage.
- **Parameters**:
  - `chunk_size` (int): Number of rows to read per chunk.
  - `use_columns` (list): List of columns to read from the CSV.
  - `filtered` (list): List to store filtered chunks.

### Example of Usage

```python
from data_prep import OutageDataProcessor

# Initialize the processor
processor = OutageDataProcessor('outage_data.csv', 2021, 2023)

# Load and process the data
processor.load_data()

# Get aggregated outage frequency data
outage_data = processor.get_outage_frequency()
print(outage_data.head())
```