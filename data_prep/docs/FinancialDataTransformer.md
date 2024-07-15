
# FinancialDataTransformer Detailed Documentation

## Overview

The `FinancialDataTransformer` class is specifically designed for loading, cleaning, and preparing financial data related to property, plant, and equipment (PP&E). This documentation outlines the functions and processes involved in transforming financial data to ensure it is ready for analysis and integration with other data sources.

## Methods Detail

### Constructor: `__init__(financial_data_file_name, folder='datasets')`
- **Purpose**: Initializes a new instance of the FinancialDataTransformer with specified parameters.
- **Parameters**:
  - `financial_data_file_name` (str): Filename of the financial data CSV file.
  - `folder` (str): Directory containing the data files, defaults to 'datasets'.
- **Action**: Sets up the file path for the financial data and initializes placeholders for data handling.

### `get_financial_data()`
- **Purpose**: Retrieves the transformed financial data. If the data has not been prepared, it triggers the data loading and preparation sequence.
- **Returns**: A DataFrame containing the prepared financial data.
- **Process**:
  1. Checks if data is already prepared; if not, calls `__load_financial_data()`.
  2. Removes unnecessary columns with `__remove_column()`.
  3. Transforms wide-format data into a long format using `__unpivot_data()`.

### `set_financial_data(financial_data_file_name, folder='datasets')`
- **Purpose**: Resets the financial data source and reloads the data based on the new source file.
- **Action**: Updates the file path and reloads the data to refresh the internal state and data representations.

### Private Methods

#### `__load_financial_data()`
- **Action**: Loads financial data from the CSV file. Ensures all necessary preprocessing steps are applied, including validation of column names and conversion of data types.
- **Detailed Steps**:
  1. Calls `read_file` to load data using the detected encoding.
  2. Validates the presence and format of critical columns.
  3. Converts string representations of numbers to numeric types.

#### `__remove_column(column_name)`
- **Purpose**: Removes a specified column from the DataFrame to streamline the dataset.
- **Parameters**:
  - `column_name` (str): Name of the column to be removed.

#### `__unpivot_data(id_vars, var_name='Quarter', value_name='PP&E')`
- **Purpose**: Transforms the dataset from a wide format (multiple PP&E columns per year) to a long format (single PP&E column with multiple rows).
- **Action**: Uses Pandas `melt` function to reshape the DataFrame. This is particularly useful for merging with other datasets that require a uniform structure.

#### `__validate_column_names()`
- **Purpose**: Ensures that all column names in the financial data match expected patterns, crucial for subsequent data processing stages.
- **Validation**:
  - Checks if columns match the 'CQ{quarter_number}{year}' format and filters out irrelevant columns.

#### `__convert_string_to_numeric()`
- **Purpose**: Converts columns that should represent numeric values from strings to appropriate numeric types, handling non-convertible values gracefully.

### Example of Usage
Here is how you might typically instantiate and use the `FinancialDataTransformer` within a data processing workflow:

```python
# Initialize the transformer
financial_transformer = FinancialDataTransformer('financial_data_2023.csv')

# Retrieve and display the processed financial data
processed_data = financial_transformer.get_financial_data()
print(processed_data.head())
```

