
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

### `load_and_process_outage_data()`
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