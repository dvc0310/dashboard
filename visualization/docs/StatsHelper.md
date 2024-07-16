# StatsHelper Documentation

## Overview

The `StatsHelper` class is a helper class designed to perform statistical analyses on outage data in relation to property, plant, and equipment (PP&E) values. This class provides methods to perform linear regression, quantile regression, and calculate prediction and confidence intervals.

## Table of Contents

1. [Overview](#overview)
2. [Initialization](#initialization)
3. [Methods](#methods)
    - [perform_regression](#perform_regression)
    - [calculate_prediction_interval](#calculate_prediction_interval)
    - [perform_quantile_regression](#perform_quantile_regression)
    - [calculate_confidence_interval](#calculate_confidence_interval)
4. [Usage](#usage)
5. [Conclusion](#conclusion)

## Initialization

### Constructor: `__init__(df)`
- **Purpose**: Initializes a new instance of the `StatsHelper` class with a DataFrame.
- **Parameters**:
  - `df` (DataFrame): The input data to be analyzed.

### Example Usage

```python
df = pd.read_csv('prepared_data.csv')
stats_helper = StatsHelper(df)
```

## Methods

### `perform_regression`
- **Purpose**: Performs a linear regression analysis on the grouped data.
- **Parameters**:
  - `grouped_df` (DataFrame): The grouped data on which to perform the regression.
- **Returns**: Regression parameters including slope, intercept, r_value, p_value, residual_std, line_x, and line_y.

### `calculate_prediction_interval`
- **Purpose**: Calculates the prediction interval for the regression line.
- **Parameters**:
  - `df` (DataFrame): The original DataFrame.
  - `pi` (float): Prediction interval percentage.
  - `residual_std` (float): Standard deviation of residuals.
  - `line_x` (array): X-values for the regression line.
  - `line_y` (array): Y-values for the regression line.
- **Returns**: Upper and lower prediction intervals.

### `perform_quantile_regression`
- **Purpose**: Performs a quantile regression analysis on the data.
- **Parameters**:
  - `df` (DataFrame): The DataFrame on which to perform the regression.
  - `quantile` (float): The quantile to be estimated.
  - `x` (DataFrame): The predictor values.
- **Returns**: Predicted values, slope, and intercept.

### `calculate_confidence_interval`
- **Purpose**: Calculates the confidence interval for the regression line.
- **Parameters**:
  - `grouped_df` (DataFrame): The grouped data.
  - `ci` (float): Confidence interval percentage.
  - `residual_std` (float): Standard deviation of residuals.
  - `line_x` (array): X-values for the regression line.
  - `line_y` (array): Y-values for the regression line.
- **Returns**: Upper and lower confidence intervals.

## Usage

The `StatsHelper` class can be used to perform statistical analyses on preprocessed data. Here's an example of how to use the class:

```python
from statistics import StatsHelper

# Initialize the helper with the DataFrame
df = pd.read_csv('prepared_data.csv')
stats_helper = StatsHelper(df)

# Perform regression analysis
grouped_df = vis_preprocessor.group_and_aggregate(df)
slope, intercept, r_value, p_value, residual_std, line_x, line_y = stats_helper.perform_regression(grouped_df)

# Calculate confidence intervals
ci_upper, ci_lower = stats_helper.calculate_confidence_interval(grouped_df, ci=95, residual_std=residual_std, line_x=line_x, line_y=line_y)
```
