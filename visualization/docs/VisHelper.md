# VisHelper Documentation

## Overview

The `VisHelper` class is a helper class designed to facilitate the preprocessing and analysis of outage data in relation to property, plant, and equipment (PP&E) values. This class provides methods to filter, aggregate, and perform statistical analyses on the data, preparing it for visualization.

## Table of Contents

1. [Overview](#overview)
2. [Initialization](#initialization)
3. [Methods](#methods)
    - [filter_dataframe](#filter_dataframe)
    - [group_and_aggregate](#group_and_aggregate)
    - [perform_regression](#perform_regression)
    - [calculate_prediction_interval](#calculate_prediction_interval)
    - [perform_quantile_regression](#perform_quantile_regression)
    - [calculate_confidence_interval](#calculate_confidence_interval)
    - [grand_total](#grand_total)
    - [preprocess_data](#preprocess_data)
4. [Private Methods](#private-methods)
    - [__check_columns_exist](#__check_columns_exist)
5. [Usage](#usage)
6. [Conclusion](#conclusion)

## Initialization

### Constructor: `__init__(df)`
- **Purpose**: Initializes a new instance of the `VisHelper` class with a DataFrame.
- **Parameters**:
  - `df` (DataFrame): The input data to be processed and analyzed.
- **Action**: Checks for the presence of required columns and preprocesses the data.

### Example Usage

```python
df = pd.read_csv('prepared_data.csv')
vis_helper = VisHelper(df)
```

## Methods

### `filter_dataframe(selected_companies=None, start_date=None, end_date=None)`
- **Purpose**: Filters the DataFrame based on selected companies and date range.
- **Parameters**:
  - `selected_companies` (list, optional): List of companies to include.
  - `start_date` (str, optional): Start date for filtering data.
  - `end_date` (str, optional): End date for filtering data.
- **Returns**: A filtered DataFrame.

### `group_and_aggregate(df)`
- **Purpose**: Groups and aggregates the data by company, calculating the mean of 'Count', 'PP&E', and 'Outage per PP&E'.
- **Parameters**:
  - `df` (DataFrame): The DataFrame to be grouped and aggregated.
- **Returns**: A grouped and aggregated DataFrame.

### `perform_regression(grouped_df)`
- **Purpose**: Performs a linear regression analysis on the grouped data.
- **Parameters**:
  - `grouped_df` (DataFrame): The grouped data on which to perform the regression.
- **Returns**: Regression parameters including slope, intercept, r_value, p_value, residual_std, line_x, and line_y.

### `calculate_prediction_interval(df, pi, residual_std, line_x, line_y)`
- **Purpose**: Calculates the prediction interval for the regression line.
- **Parameters**:
  - `df` (DataFrame): The original DataFrame.
  - `pi` (float): Prediction interval percentage.
  - `residual_std` (float): Standard deviation of residuals.
  - `line_x` (array): X-values for the regression line.
  - `line_y` (array): Y-values for the regression line.
- **Returns**: Upper and lower prediction intervals.

### `perform_quantile_regression(df, quantile, x)`
- **Purpose**: Performs a quantile regression analysis on the data.
- **Parameters**:
  - `df` (DataFrame): The DataFrame on which to perform the regression.
  - `quantile` (float): The quantile to be estimated.
  - `x` (DataFrame): The predictor values.
- **Returns**: Predicted values, slope, and intercept.

### `calculate_confidence_interval(grouped_df, ci, residual_std, line_x, line_y)`
- **Purpose**: Calculates the confidence interval for the regression line.
- **Parameters**:
  - `grouped_df` (DataFrame): The grouped data.
  - `ci` (float): Confidence interval percentage.
  - `residual_std` (float): Standard deviation of residuals.
  - `line_x` (array): X-values for the regression line.
  - `line_y` (array): Y-values for the regression line.
- **Returns**: Upper and lower confidence intervals.

### `grand_total(include_grand_total, df_filtered)`
- **Purpose**: Adds a grand total row to the DataFrame if specified.
- **Parameters**:
  - `include_grand_total` (bool): Whether to include the grand total.
  - `df_filtered` (DataFrame): The filtered DataFrame.
- **Returns**: A DataFrame with the grand total row included if specified.

### `preprocess_data()`
- **Purpose**: Preprocesses the data by mapping company names, converting date columns, and calculating 'Outage per PP&E'.
- **Action**: Applies necessary transformations and drops rows with missing values in the 'PP&E' column.

## Private Methods

### `__check_columns_exist()`
- **Purpose**: Checks if the required columns are present in the DataFrame.
- **Action**: Raises a ValueError if any required columns are missing.

## Usage

The `VisHelper` class can be used to preprocess and analyze data before visualization. Here's an example of how to use the class:

```python
from visualization import VisHelper

# Initialize the helper with the DataFrame
df = pd.read_csv('prepared_data.csv')
vis_helper = VisHelper(df)

# Filter the data
filtered_df = vis_helper.filter_dataframe(selected_companies=['CompanyA', 'CompanyB'], start_date='2021-01-01', end_date='2023-01-01')

# Group and aggregate the data
grouped_df = vis_helper.group_and_aggregate(filtered_df)

# Perform regression analysis
slope, intercept, r_value, p_value, residual_std, line_x, line_y = vis_helper.perform_regression(grouped_df)

# Calculate confidence intervals
ci_upper, ci_lower = vis_helper.calculate_confidence_interval(grouped_df, ci=95, residual_std=residual_std, line_x=line_x, line_y=line_y)
```

