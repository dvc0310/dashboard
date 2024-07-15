

# Frontend Package Documentation

## Overview

The `frontend` package is responsible for defining the user interface and interactivity of the Dash web application. It manages the layout, the callbacks that handle user interactions, and the tabs that segment the data visualization into different views.

## Table of Contents

1. [Layout Configuration](#layout-configuration)
2. [Callback Functions](docs/callbacks.md)
3. [Tabs](docs/tabs.md)
4. [Usage](#usage)
5. [Dash Guides](#dash-guides)


## Layout Configuration

### File: `layout.py`

This module sets up the main layout of the Dash application. It integrates multiple tabs for displaying various data visualizations and controls like date pickers, dropdowns, and checkboxes for user interaction.

- **Key Components**:
  - `dcc.Tabs`: Manages different visualization tabs.
  - `dcc.Store`: Stores the filenames for quick access across callbacks.
  - `dcc.Download`: Facilitates downloading of data directly from the dashboard.

#### Note: Currently, the dcc.Store and dcc.Download compenents does not do anything. 

### Usage

The layout is automatically applied when you run the Dash application and does not require manual activation.

## Callback Functions

For detailed explanations of the callback functions defined in the `callbacks.py` file, refer to the [Detailed Callback Documentation](docs/callbacks.md).

## Tabs

For a detailed breakdown of each tab module within the application, refer to the [Tabs Documentation](docs/tabs.md).

## Usage

Tabs are imported and utilized in the main layout to provide structured navigation and visualization options to the user. Callbacks are registered when the Dash app is initialized and run, listening for changes to input components to update the UI dynamically.

## Dash Guides

For more information on Dash layouts and callbacks, refer to the official Dash documentation:

- [Dash Layouts](https://dash.plotly.com/layout)
- [Dash Callbacks](https://dash.plotly.com/basic-callbacks)

