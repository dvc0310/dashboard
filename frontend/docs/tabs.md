
# Tabs Module Documentation

## Overview

The `tabs` module in the `frontend` package of the Dash web application provides distinct views for different types of data visualizations. Each tab is designed to display specific aspects of the data related to outage frequency versus PP&E, outage over time, and outage box plots.

## Table of Contents

1. [Overview](#overview)
2. [Regression Tab](#regression-tab)
3. [Line Chart Tab](#line-chart-tab)
4. [Boxplot Tab](#boxplot-tab)
5. [Components Used](#components-used)
6. [Usage](#usage)

## Regression Tab

### File: `regression_tab`

- **Function**: `regression_tab(visualizer)`
- **Purpose**: Displays a regression analysis of outage frequency vs. PP&E.
- **Components**:
  - `DatePickerRange`: Allows the user to select a date range to visualize the data.
  - `Dropdown`: Enables selection of companies to include in the analysis.
  - `Checklist`: Option to enable interval calculations.
  - `RadioItems`: Toggle between 'Aggregated' and 'Granular' views.
  - `Graph`: Displays the regression graph.

## Line Chart Tab

### File: `line_chart_tab`

- **Function**: `line_chart_tab(visualizer)`
- **Purpose**: Shows how the outage varies over time.
- **Components**:
  - `DatePickerRange`: Users can specify the time range for the data shown in the graph.
  - `Dropdown`: Select which companies' data to display.
  - `Graph`: The line chart visualization of the outage data over time.

## Boxplot Tab

### File: `boxplot_tab`

- **Function**: `boxplot_tab(visualizer)`
- **Purpose**: Provides a boxplot view for outage data, which is useful for statistical analysis.
- **Components**:
  - `DatePickerRange`: Selects the date range for the boxplot visualization.
  - `Dropdown`: Allows the selection of companies.
  - `Checklist`: Option to include grand total data in the visualization.
  - `Graph`: Displays the boxplot.

## Components Used

- **`DatePickerRange`**: Allows users to pick a start and end date to filter the data.
- **`Dropdown`**: Enables selection of multiple companies to be displayed in the graphs.
- **`Checklist`**: Provides options like enabling intervals or including grand totals in graphs.
- **`RadioItems`**: Used for toggling between different view modes in the visualizations.
- **`Graph`**: The component where the actual plots are rendered based on user input.

## Usage

These tabs are integrated into the main layout of the Dash application and are interacted with through the user interface. Each tab responds to input changes and updates its display accordingly.
