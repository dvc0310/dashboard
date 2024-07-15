
# FinancialDataTransformer Detailed Documentation

## Overview

The `FinancialDataTransformer` class is specifically designed for loading, cleaning, and preparing financial data related to property, plant, and equipment (PP&E). This documentation outlines the functions and processes involved in transforming financial data to ensure it is ready for analysis and integration with other data sources.

## Methods Detail

### Constructor: `__init__(financial_data_file_name, folder='datasets')`
- **Purpose**: Initializes a new instance of the FinancialDataTransformer with specified parameters.
- **Parameters**:
  - `financial_data_file_name` (str): Filename of the financial data CSV file.
  - `folder` (str): Directory containing the data files, defaults to 'datasets'.
  - `normalize` (bool): Divides the financial data by 1 billion if set to True
- **Action**: Sets up the file path for the financial data and initializes placeholders for data handling.

### `get_financial_data`
- **Purpose**: Retrieves the prepared financial data, ensuring it's loaded and prepared only once unless explicitly reset.
- **Returns**: A pandas DataFrame containing the prepared financial data.

### `set_financial_data(financial_data_file_name, folder='datasets', normalize=False)`
- **Purpose**: Sets the financial data file path and loads the data by initiating the preparation process. Allows for reinitialization with new data parameters.
- **Parameters**:
  - `financial_data_file_name` (str): The name of the file containing the financial data.
  - `folder` (str, optional): The directory where financial data files are stored. Defaults to 'datasets'.
  - `normalize` (bool, optional): Whether to normalize the data during the preparation. Defaults to `False`.
- **Action**: Resets the data preparation status and triggers reloading and re-preparing the data based on the new file path.

### `prepare_financial_data`
- **Purpose**: Conducts a series of data preparation steps to ready the financial data for analysis.
- **Steps**: Includes reading the data, aligning and formatting columns, filtering and converting data types, and more, as detailed in the method-specific documentation.

### Example of Usage
Here is how you might typically instantiate and use the `FinancialDataTransformer`:

```python
# Initialize the transformer
financial_transformer = FinancialDataTransformer('financial_data_2023.csv', 'data')

# Retrieve and display the processed financial data
processed_data = financial_transformer.get_financial_data()
print(processed_data.head())

```

```python
# Initialize the transformer
financial_transformer = FinancialDataTransformer('financial_data_2023.csv', 'data')

# Set and display new financial data
processed_data = financial_transformer.set_financial_data(('financial_data_2024.csv', 'datasets', False)
processed_data = financial_transformer.get_financial_data()
print(processed_data.head())

```
