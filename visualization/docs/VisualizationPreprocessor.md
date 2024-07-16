
# VisualizationPreprocessor Documentation

## Overview

The `VisualizationPreprocessor` class is a helper class designed to facilitate the preprocessing and analysis of outage data in relation to property, plant, and equipment (PP&E) values. This class provides methods to filter, aggregate, and prepare data for visualization.

## Table of Contents

1. [Overview](#overview)
2. [Initialization](#initialization)
3. [Methods](#methods)
    - [filter_dataframe](#filter_dataframe)
    - [group_and_aggregate](#group_and_aggregate)
    - [grand_total](#grand_total)
    - [preprocess_data](#preprocess_data)
4. [Private Methods](#private-methods)
    - [__check_columns_exist](#__check_columns_exist)
5. [Usage](#usage)

## Initialization

### Constructor: `__init__(df)`
- **Purpose**: Initializes a new instance of the `VisualizationPreprocessor` class with a DataFrame.
- **Parameters**:
  - `df` (DataFrame): The input data to be processed and analyzed.
- **Action**: Checks for the presence of required columns and preprocesses the data.

### Example Usage

```python
df = pd.read_csv('prepared_data.csv')
vis_preprocessor = VisualizationPreprocessor(df)
```

## Methods

### `filter_dataframe`
- **Purpose**: Filters the DataFrame based on selected companies and date range.
- **Parameters**:
  - `selected_companies` (list, optional): List of companies to include.
  - `start_date` (str, optional): Start date for filtering data.
  - `end_date` (str, optional): End date for filtering data.
- **Returns**: A filtered DataFrame.

### `group_and_aggregate`
- **Purpose**: Groups and aggregates the data by company, calculating the mean of 'Count', 'PP&E', and 'Outage per PP&E'.
- **Parameters**:
  - `df` (DataFrame): The DataFrame to be grouped and aggregated.
- **Returns**: A grouped and aggregated DataFrame.

### `grand_total`
- **Purpose**: Adds a grand total row to the DataFrame if specified.
- **Parameters**:
  - `include_grand_total` (bool): Whether to include the grand total.
  - `df` (DataFrame): The filtered DataFrame.
- **Returns**: A DataFrame with the grand total row included if specified.

### `preprocess_data`
- **Purpose**: Preprocesses the data by mapping company names, converting date columns, and calculating 'Outage per PP&E'.
- **Action**: Applies necessary transformations and drops rows with missing values in the 'PP&E' column.

## Private Methods

### `__check_columns_exist`
- **Purpose**: Ensures the required columns are present in the DataFrame.
- **Action**: Raises a `ValueError` if any required columns are missing.

## Usage

The `VisualizationPreprocessor` class can be used to preprocess and analyze data before visualization. Here's an example of how to use the class:

```python
from visualization import VisualizationPreprocessor

# Initialize the helper with the DataFrame
df = pd.read_csv('prepared_data.csv')
vis_preprocessor = VisualizationPreprocessor(df)

# Filter the data
filtered_df = vis_preprocessor.filter_dataframe(selected_companies=['CompanyA', 'CompanyB'], start_date='2021-01-01', end_date='2023-01-01')

# Group and aggregate the data
grouped_df = vis_preprocessor.group_and_aggregate(filtered_df)
```


