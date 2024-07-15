
# PlotlyVisualizer Documentation

## Overview

The `PlotlyVisualizer` class in the `visualization` package is responsible for generating interactive data visualizations using Plotly. It provides methods to create various types of plots, including scatter plots, line charts, and box plots, to help analyze and understand outage data in relation to property, plant, and equipment (PP&E).

## Table of Contents

1. [Overview](#overview)
2. [Initialization](#initialization)
3. [Methods](#methods)
    - [load_data](#load_data)
    - [update_data](#update_data)
    - [plot_average_outage_vs_ppe](#plot_average_outage_vs_ppe)
    - [plot_granular_outage_vs_ppe](#plot_granular_outage_vs_ppe)
    - [plot_outage_per_ppe_over_time](#plot_outage_per_ppe_over_time)
    - [plot_outage_per_ppe_boxplot](#plot_outage_per_ppe_boxplot)
4. [Private Methods](#private-methods)
    - [__add_prediction_intervals](#__add_prediction_intervals)
    - [__create_figure](#__create_figure)
    - [__add_confidence_intervals](#__add_confidence_intervals)
    - [__create_outage_time_plot](#__create_outage_time_plot)
    - [__plot_percentiles](#__plot_percentiles)
5. [Usage](#usage)
6. [Conclusion](#conclusion)

## Initialization

### Constructor: `__init__(filename='prepared_data.csv', directory='visualization')`
- **Purpose**: Initializes a new instance of the `PlotlyVisualizer` with specified parameters.
- **Parameters**:
  - `filename` (str, optional): The name of the CSV file containing the prepared data. Default is 'prepared_data.csv'.
  - `directory` (str, optional): The directory where the data files are stored. Default is 'visualization'.

### Example Usage

```python
visualizer = PlotlyVisualizer(filename='prepared_data.csv', directory='visualization')
```

## Methods

### `load_data()`
- **Purpose**: Loads the data from the specified CSV file and initializes the `VisHelper` object for further data manipulation.
- **Action**: Reads the CSV file, detects encoding, and loads the data into a DataFrame.

### `update_data()`
- **Purpose**: Reloads the data from the CSV file. This is useful if the data file has been updated.
- **Action**: Calls `load_data()` to refresh the internal DataFrame.

### `plot_average_outage_vs_ppe(ci=95, enable_ci=False, dashboard=False, selected_companies=None, start_date=None, end_date=None)`
- **Purpose**: Creates a scatter plot showing the average outage frequency versus average PP&E for selected companies and date ranges.
- **Parameters**:
  - `ci` (int, optional): Confidence interval percentage. Default is 95.
  - `enable_ci` (bool, optional): Whether to enable confidence intervals. Default is False.
  - `dashboard` (bool, optional): If True, returns the figure object instead of displaying it. Default is False.
  - `selected_companies` (list, optional): List of selected companies to include in the plot.
  - `start_date` (str, optional): Start date for filtering data.
  - `end_date` (str, optional): End date for filtering data.
- **Returns**: A Plotly figure object if `dashboard` is True, otherwise displays the plot.

### `plot_granular_outage_vs_ppe(pi=95, enable_pi=False, dashboard=False, selected_companies=None, start_date=None, end_date=None)`
- **Purpose**: Creates a granular scatter plot showing outage frequency versus PP&E with optional prediction intervals.
- **Parameters**:
  - `pi` (int, optional): Prediction interval percentage. Default is 95.
  - `enable_pi` (bool, optional): Whether to enable prediction intervals. Default is False.
  - `dashboard` (bool, optional): If True, returns the figure object instead of displaying it. Default is False.
  - `selected_companies` (list, optional): List of selected companies to include in the plot.
  - `start_date` (str, optional): Start date for filtering data.
  - `end_date` (str, optional): End date for filtering data.
- **Returns**: A Plotly figure object if `dashboard` is True, otherwise displays the plot.

### `plot_outage_per_ppe_over_time(show_percentiles=True, dashboard=False, selected_companies=None, start_date=None, end_date=None)`
- **Purpose**: Creates a line chart showing outage per PP&E over time for selected companies and date ranges.
- **Parameters**:
  - `show_percentiles` (bool, optional): Whether to show percentile lines. Default is True.
  - `dashboard` (bool, optional): If True, returns the figure object instead of displaying it. Default is False.
  - `selected_companies` (list, optional): List of selected companies to include in the plot.
  - `start_date` (str, optional): Start date for filtering data.
  - `end_date` (str, optional): End date for filtering data.
- **Returns**: A Plotly figure object if `dashboard` is True, otherwise displays the plot.

### `plot_outage_per_ppe_boxplot(include_grand_total=False, dashboard=False, selected_companies=None, start_date=None, end_date=None)`
- **Purpose**: Creates a boxplot showing outage per PP&E for selected companies and date ranges.
- **Parameters**:
  - `include_grand_total` (bool, optional): Whether to include a grand total in the plot. Default is False.
  - `dashboard` (bool, optional): If True, returns the figure object instead of displaying it. Default is False.
  - `selected_companies` (list, optional): List of selected companies to include in the plot.
  - `start_date` (str, optional): Start date for filtering data.
  - `end_date` (str, optional): End date for filtering data.
- **Returns**: A Plotly figure object if `dashboard` is True, otherwise displays the plot.

## Private Methods

### `__add_prediction_intervals(fig, line_x, pi_upper, pi_lower, slope95, intercept95, slope5, intercept5)`
- **Purpose**: Adds prediction interval lines to the figure.
- **Parameters**:
  - `fig`: The Plotly figure object.
  - `line_x`: X-values for the prediction intervals.
  - `pi_upper`: Upper prediction interval line values.
  - `pi_lower`: Lower prediction interval line values.
  - `slope95`: Slope of the 95th quantile regression line.
  - `intercept95`: Intercept of the 95th quantile regression line.
  - `slope5`: Slope of the 5th quantile regression line.
  - `intercept5`: Intercept of the 5th quantile regression line.

### `__create_figure(grouped_df, line_x, line_y, slope, intercept, r_value=None, pi=False)`
- **Purpose**: Creates a scatter plot with a regression line.
- **Parameters**:
  - `grouped_df`: DataFrame with grouped data.
  - `line_x`: X-values for the regression line.
  - `line_y`: Y-values for the regression line.
  - `slope`: Slope of the regression line.
  - `intercept`: Intercept of the regression line.
  - `r_value` (optional): Correlation coefficient.
  - `pi` (bool, optional): Whether the plot is for prediction intervals. Default is False.
- **Returns**: A Plotly figure object and initial sizes for scatter plot markers.

### `__add_confidence_intervals(fig, line_x, ci_upper, ci_lower)`
- **Purpose**: Adds confidence interval lines to the figure.
- **Parameters**:
  - `fig`: The Plotly figure object.
  - `line_x`: X-values for the confidence intervals.
  - `ci_upper`: Upper confidence interval line values.
  - `ci_lower`: Lower confidence interval line values.

### `__create_outage_time_plot(df_filtered)`
- **Purpose**: Creates a line chart showing outage per PP&E over time.
- **Parameters**:
  - `df_filtered`: Filtered DataFrame.
- **Returns**: A Plotly figure object.

### `__plot_percentiles(df_filtered, fig)`
- **Purpose**: Plots percentile lines on the line chart.
- **Parameters**:
  - `df_filtered`: Filtered DataFrame.
  - `fig`: The Plotly figure object.

## Usage

The `PlotlyVisualizer` class can be used to create various interactive plots for analyzing outage data. Here's an example of how to create a scatter plot showing average outage frequency vs. PP&E:

```python
from visualization import PlotlyVisualizer

# Initialize the visualizer
visualizer = PlotlyVisualizer(filename='prepared_data.csv', directory='visualization')

# Plot average outage frequency vs. PP&E
visualizer.plot_average_outage_vs_ppe(selected_companies=['CompanyA', 'CompanyB'], start_date='2021-01-01', end_date='2023-01-01')
```

