
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

### `plot_average_outage_vs_ppe(ci=95, enable_interval=False, dashboard=False, selected_companies=None, start_date=None, end_date=None)`
- **Purpose**: Creates a scatter plot showing the average outage frequency versus average PP&E for selected companies and date ranges.
- **Parameters**:
  - `enable_interval` (bool, optional): Whether to enable confidence intervals. Default is False.
  - `dashboard` (bool, optional): If True, returns the figure object instead of displaying it. Default is False.
  - `selected_companies` (list, optional): List of selected companies to include in the plot.
  - `start_date` (str, optional): Start date for filtering data.
  - `end_date` (str, optional): End date for filtering data.
- **Returns**: A Plotly figure object if `dashboard` is True, otherwise displays the plot.

### `plot_granular_outage_vs_ppe(pi=95, enable_interval=False, dashboard=False, selected_companies=None, start_date=None, end_date=None)`
- **Purpose**: Creates a granular scatter plot showing outage frequency versus PP&E with optional prediction intervals.
- **Parameters**:
  - `enable_interval` (bool, optional): Whether to enable prediction intervals. Default is False.
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


## Usage

The `PlotlyVisualizer` class can be used to create various interactive plots for analyzing outage data. Here's an example of how to create a scatter plot showing average outage frequency vs. PP&E:

```python
from visualization import PlotlyVisualizer

# Initialize the visualizer
visualizer = PlotlyVisualizer(filename='prepared_data.csv', directory='visualization')

# Plot average outage frequency vs. PP&E
visualizer.plot_average_outage_vs_ppe(selected_companies=['CompanyA', 'CompanyB'], start_date='2021-01-01', end_date='2023-01-01')
```

