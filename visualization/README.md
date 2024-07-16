
# Visualization Package Documentation

## Overview

The `visualization` package provides tools for preprocessing, analyzing, and visualizing outage data in relation to property, plant, and equipment (PP&E) values. It includes classes for data manipulation and generating interactive plots to help users understand and explore their data effectively.

## Table of Contents

1. [Overview](#overview)
2. [Components](#components)
3. [Usage](#usage)
4. [Detailed Documentation](#detailed-documentation)

## Components

### 1. VisHelper
The `VisHelper` class is designed to facilitate the preprocessing and analysis of outage data. It provides methods to filter, aggregate, and perform statistical analyses on the data.

- **Features**:
  - Data filtering by company and date range.
  - Aggregation of data by company.
  - Regression and quantile regression analysis.
  - Calculation of confidence and prediction intervals.
  - Data preprocessing, including date conversion and calculation of outage per PP&E.

For more detailed information, refer to the [VisHelper Documentation](docs/VisHelper.md).

### 2. PlotlyVisualizer
The `PlotlyVisualizer` class is responsible for generating interactive data visualizations using Plotly. It provides methods to create various types of plots, including scatter plots, line charts, and box plots, to help analyze and understand outage data in relation to PP&E.

- **Features**:
  - Scatter plots showing outage frequency vs. PP&E.
  - Line charts showing outage per PP&E over time.
  - Box plots for outage data analysis.
  - Support for confidence and prediction intervals.
  - Interactive plots with detailed hover information.

For more detailed information, refer to the [PlotlyVisualizer Documentation](docs/PlotlyVisualizer.md).

## Usage

Here is an example of how to use the `visualization` package to preprocess data and create a visualization:

```python
from visualization import VisHelper, PlotlyVisualizer

# Load the data
df = pd.read_csv('prepared_data.csv')

# Initialize the VisHelper
vis_helper = VisHelper(df)

# Filter the data
filtered_df = vis_helper.filter_dataframe(selected_companies=['CompanyA', 'CompanyB'], start_date='2021-01-01', end_date='2023-01-01')

# Initialize the PlotlyVisualizer
visualizer = PlotlyVisualizer()

# Plot average outage frequency vs. PP&E
visualizer.plot_average_outage_vs_ppe(selected_companies=['CompanyA', 'CompanyB'], start_date='2021-01-01', end_date='2023-01-01')
```


## Detailed Documentation

For more detailed information on each class and its methods, please refer to the following documents:

- [VisHelper Documentation](docs/VisHelper.md)
- [PlotlyVisualizer Documentation](docs/PlotlyVisualizer.md)

