# Visualization Package Documentation

## Overview

The `visualization` package provides tools for preprocessing, analyzing, and visualizing outage data in relation to property, plant, and equipment (PP&E) values. It includes classes for data manipulation and generating interactive plots to help users understand and explore their data effectively.

## Table of Contents

1. [Overview](#overview)
2. [Components](#components)
3. [Usage](#usage)
4. [Detailed Documentation](#detailed-documentation)

## Components

### 1. VisualizationPreprocessor
The `VisualizationPreprocessor` class is designed to facilitate the preprocessing of outage data. It gives methods to filter, aggregate, and prepare the data for statistical analysis and visualization.

- **Features**:
  - Data filtering by company and date range.
  - Aggregation of data by company.
  - Data preprocessing, including date conversion and calculation of outage per PP&E.
  - Adding grand total rows for overall analysis.

For more detailed information, refer to the [VisualizationPreprocessor Documentation](docs/VisualizationPreprocessor.md).

### 2. StatsHelper
The `StatsHelper` class is responsible for performing statistical analyses on the outage data. It provides methods to perform linear regression, quantile regression, and calculate prediction and confidence intervals.

- **Features**:
  - Linear regression analysis.
  - Quantile regression analysis.
  - Calculation of confidence and prediction intervals.
  - Detailed statistical analysis and regression parameters.

For more detailed information, refer to the [StatsHelper Documentation](docs/StatsHelper.md).

### 3. PlotlyVisualizer
The `PlotlyVisualizer` class is responsible for generating interactive data visualizations using Plotly. It provides methods to create various types of plots, including scatter plots, line charts, and box plots, to help analyze and understand outage data in relation to PP&E.

- **Features**:
  - Scatter plots showing outage frequency vs. PP&E.
  - Line charts showing outage per PP&E over time.
  - Box plots for outage data analysis.
  - Support for confidence and prediction intervals.
  - Interactive plots with detailed hover information.

For more detailed information, refer to the [PlotlyVisualizer Documentation](docs/PlotlyVisualizer.md).

## Usage

Here is an example of how to use the `visualization` package to preprocess data, perform statistical analysis, and create a visualization:

```python
from visualization import VisualizationPreprocessor, StatsHelper, PlotlyVisualizer

# Load the data
df = pd.read_csv('prepared_data.csv')

# Initialize the VisualizationPreprocessor
vis_preprocessor = VisualizationPreprocessor(df)

# Filter the data
filtered_df = vis_preprocessor.filter_dataframe(selected_companies=['CompanyA', 'CompanyB'], start_date='2021-01-01', end_date='2023-01-01')

# Group and aggregate the data
grouped_df = vis_preprocessor.group_and_aggregate(filtered_df)

# Initialize the StatsHelper
stats_helper = StatsHelper(grouped_df)

# Perform regression analysis
slope, intercept, r_value, p_value, residual_std, line_x, line_y = stats_helper.perform_regression(grouped_df)

# Calculate confidence intervals
ci_upper, ci_lower = stats_helper.calculate_confidence_interval(grouped_df, ci=95, residual_std=residual_std, line_x=line_x, line_y=line_y)

# Initialize the PlotlyVisualizer
visualizer = PlotlyVisualizer()

# Plot average outage frequency vs. PP&E
visualizer.plot_average_outage_vs_ppe(grouped_df, line_x, line_y, ci_upper, ci_lower)
```

## Detailed Documentation

For more detailed information on each class and its methods, please refer to the following documents:

- [VisualizationPreprocessor Documentation](docs/VisualizationPreprocessor.md)
- [StatsHelper Documentation](docs/StatsHelper.md)
- [PlotlyVisualizer Documentation](docs/PlotlyVisualizer.md)

