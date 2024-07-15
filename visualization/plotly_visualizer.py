import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from data_prep import find_encoding
from .vis_helper import VisHelper


class PlotlyVisualizer:
    def __init__(self, filename='prepared_data.csv', directory='datasets'):
        """
        Initializes the PlotlyVisualizer with a specific data file and directory.

        Parameters:
            filename (str): The name of the CSV file containing the data. Default is 'prepared_data.csv'.
            directory (str): The directory where the data file is located. Default is 'datasets'.

        Loads the data and sets default colors for plotting.
        """
        self.directory = directory
        self.filename = filename
        self.load_data()
        self.colors = ['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
        
    def load_data(self):
        """
        Loads data from a CSV file located at the specified directory and filename.
        """
        csv_path = f'{self.directory}/{self.filename}'
        self.df = pd.read_csv(csv_path, encoding=find_encoding(csv_path))
        self.vh = VisHelper(self.df)

    def update_data(self):
        """
        Reloads the data from the source file to reflect any updates or changes to the file.
        """
        self.load_data() 

    def plot_average_outage_vs_ppe(self, interval_percent=95, enable_interval=False, dashboard=False, selected_companies=None, start_date=None, end_date=None):
        """
        Plots average outage vs. PP&E with optional confidence intervals.

        Parameters:
            interval_percent (int): The confidence interval percentage, default is 95.
            enable_interval (bool): Flag to enable plotting of confidence intervals.
            dashboard (bool): Flag to determine if the plot should be returned or shown directly.
            selected_companies (list): List of selected companies to filter data.
            start_date (str): Start date for filtering data.
            end_date (str): End date for filtering data.

        Returns:
            plotly.graph_objs.Figure: The figure object with the plotted data, if dashboard is True.
        """
        # Filters the data by company, start date, and end date
        df_filtered = self.vh.filter_dataframe(selected_companies, start_date, end_date)

        # Aggregates the data by Company and gives average PP&E and average outage count
        grouped_df = self.vh.group_and_aggregate(df_filtered)
        slope, intercept, r_value, _, std_err, line_x, line_y = self.vh.perform_regression(grouped_df)

        # Creates a scatter plot and then adds in regression line
        fig = self.__create_scatter_plot(grouped_df, interval=enable_interval)
        self.__create_regression_line(fig=fig, intercept=intercept, line_x=line_x, line_y=line_y, slope=slope, r_value=r_value)

        # Draws confidence intervals if enable_ci is True
        if enable_interval:
            ci_upper, ci_lower = self.vh.calculate_confidence_interval(grouped_df, interval_percent, std_err, line_x, line_y)
            self.__add_confidence_intervals(fig, line_x, ci_upper, ci_lower)

        if dashboard:
            return fig
        fig.show()


    def plot_granular_outage_vs_ppe(self, enable_interval=False, dashboard=False, selected_companies=None, start_date=None, end_date=None):
        """
        Plots granular outage vs. PP&E with options for prediction intervals.

        Parameters:
            enable_interval (bool): If True, includes prediction intervals in the plot.
            dashboard (bool): If True, returns the plot instead of showing it.
            selected_companies (list): Companies to include in the plot.
            start_date (str): Start date for data filtering.
            end_date (str): End date for data filtering.

        Returns:
            plotly.graph_objs.Figure: The plotly figure, if dashboard is True.
        """
        
        # Filters the data by company, start date, and end date
        df_filtered = self.vh.filter_dataframe(selected_companies, start_date, end_date)

        # Generate 100 linearly spaced points between the minimum and maximum values of the 'PP&E' column.
        line_x = np.linspace(df_filtered['PP&E'].min(), df_filtered['PP&E'].max(), 100)
        x = pd.DataFrame(line_x, columns=["PP&E"])

        # Using quantile regression for the median and the quantile intervals
        line_y_50, slope, intercept = self.vh.perform_quantile_regression(df_filtered, 0.50, x)
        line_y_95,slope95, intercept95  = self.vh.perform_quantile_regression(df_filtered, 0.95, x)
        line_y_05, slope5, intercept5= self.vh.perform_quantile_regression(df_filtered, 0.05, x)
        
        # Creates a scatter plot and plots data points
        fig = self.__create_scatter_plot(df_filtered, interval=enable_interval)
        self.__create_regression_line(fig=fig, intercept=intercept, line_x=line_x,line_y=line_y_50,slope=slope, r_value=None)

        # If the interval box is checked, add in the 95th and 5th quantile lines.
        if enable_interval:
            self.__add_quantile_lines(fig, line_x, line_y_95, line_y_05, slope95, intercept95, slope5, intercept5)

            # This marks any point above the 95th as outliers
            self.__mark_outliers(df=df_filtered,fig=fig,line_x=line_x,line_y_95=line_y_95)

        # Updates company colors
        fig.update_layout(colorway=self.colors)

        
        if dashboard:
            return fig
        fig.show()



    def plot_outage_per_ppe_over_time(self, show_percentiles=True, dashboard=False, selected_companies=None, start_date=None, end_date=None):
        """
        Plots outage per PP&E over time, optionally showing percentiles.

        Parameters:
            show_percentiles (bool): Whether to display percentiles on the plot.
            dashboard (bool): Controls whether to return the plot or show it.
            selected_companies (list): Filter data by these companies.
            start_date (str), end_date (str): Date range for filtering data.

        Returns:
            plotly.graph_objs.Figure: The generated figure, if dashboard is True.
        """
       
        # Filters the data by company, start date, and end date
        df_filtered = self.vh.filter_dataframe(selected_companies, start_date, end_date)

        # Creates a line chart of Outages per PP&E over time
        fig = self.__create_outage_time_plot(df_filtered)

        # Adds in median, quartile, 95th percentile, and 5th percentile lines
        if show_percentiles:
            self.__plot_percentiles(df_filtered, fig)

        fig.update_layout(colorway=self.colors)

        if dashboard:
            return fig
        
        fig.show()


    def plot_outage_per_ppe_boxplot(self, include_grand_total=False, dashboard=False, selected_companies = None,start_date=None,end_date=None):
        """
        Creates a box plot for outage per PP&E across selected companies.

        Parameters:
            include_grand_total (bool): Whether to include a grand total box plot.
            dashboard (bool): If True, the plot is returned for display in a dashboard.
            selected_companies (list): Companies to be included in the plot.
            start_date (str), end_date (str): Filtering period for the data.

        Returns:
            plotly.graph_objs.Figure: The plotted figure, if dashboard is True.
        """
        # Filters the data by company, start date, and end date
        df_filtered = self.vh.filter_dataframe(selected_companies, start_date, end_date)

        # Controls whether to include a boxplot that is an aggreagate of all company data
        data = self.vh.grand_total(include_grand_total=include_grand_total, df_filtered=df_filtered)

        # Rounds Outage Per PP&E
        data['Outage per PP&E Rounded'] = data['Outage per PP&E'].round(1)

        # Generate boxplots to visualize 'Outage per PP&E' data, with each boxplot grouped and labeled by company.
        fig = px.box(data, x='Company', y='Outage per PP&E', color='Company', points="all",
                    title='Outage per PP&E by Company',
                    hover_data={'Outage per PP&E': ':.2f',  
                                'Outage per PP&E Rounded': True})  
 
        fig.update_layout(colorway=self.colors)

        if dashboard:
            return fig
        
        fig.show()

    def __add_quantile_lines(self, fig, line_x, upper, lower, slope95, intercept95, slope5, intercept5):
        # Creates Hover Info
        equation_text95 = f'Equation:<br>{slope95:.2f} * PP&E + {intercept95:.2f}'
        hover_text95 = [f"{equation_text95}<br>Predicted Outage Freq (Upper Bound):<br>{y:.1f}" for y in upper]
        equation_text5 = f'Equation:<br>{slope5:.2f} * PP&E + {intercept5:.2f}'
        hover_text5 = [f"{equation_text5}<br>Predicted Outage Freq (Lower Bound):<br>{y:.1f}" for y in lower]

        # Draws the upper and lower quantile regression lines
        fig.add_trace(go.Scatter(
            x=line_x,
            y=upper,
            mode='lines',
            name='95th Quantile',
            line=dict(color='red', dash='dash'),
            text=hover_text95,
            hoverinfo='text',
            showlegend=True
        ))
        fig.add_trace(go.Scatter(
            x=line_x,
            y=lower,
            mode='lines',
            name='5th Quantile',
            line=dict(color='blue', dash='dash'),
            fill='tonexty',
            fillcolor='rgba(0, 255, 0, 0.2)',
            text=hover_text5,
            hoverinfo='text',
            showlegend=True
        ))


    def __create_scatter_plot(self, df, interval=False):
        # Sets title depending on whether or not data is aggregated
        if interval:
            title = 'Outage Frequency vs. PP&E by Company'
        else:
            title = 'Average Outage Frequency vs. Average PP&E by Company'
        
        # Creates a scatterplot and plots the data
        fig = px.scatter(
            df, 
            x='PP&E', 
            y='Count', 
            color='Company', 
            size='Outage per PP&E', 
            title=title,
            opacity=.8,
            hover_data={
                'PP&E': ':.2f',
                'Count': ':.2f',
                'Outage per PP&E': ':.2f',
            }
        )

        return fig

    def __create_regression_line(self, slope, intercept, line_x, line_y, r_value, fig):
            # Equation text for hover info
            equation_text = f'Predicted Outage Freq. = {slope:.2f} * PP&E + {intercept:.2f}'

            # Includes the correlation coefficient if `r_value` is set
            if r_value is not None:
                r_value_text = f'Correlation coefficient: {r_value:.2f}'
                hover_text = [f"{equation_text}<br>{r_value_text}<br>Outage Count: {y:.1f}" for y in line_y]
            else:
                hover_text = [f"{equation_text}<br>Outage Count: {y:.1f}" for y in line_y]

            # Draws the regression line
            fig.add_trace(go.Scatter(
                x=line_x, 
                y=line_y, 
                mode='lines', 
                name='Regression Line',
                text=hover_text, 
                hoverinfo='text'
            ))

    def __add_confidence_intervals(self, fig, line_x, upper, lower):
        # Add upper confidence interval line
        fig.add_trace(go.Scatter(
            x=line_x,
            y=upper,
            mode='lines',
            name='Upper Confidence Interval',
            hoverlabel=dict(namelength=-1),  # Do not truncate hover label text
            line=dict(color='rgba(255, 0, 0, 0.5)', dash='dash'),  # Red dashed line
            hovertemplate='Upper Confidence Interval<br>PP&E: %{x:.2f}<br>Outage Count: %{y:.2f}<extra></extra>',  # Custom hover template
            showlegend=True
        ))

        # Add lower confidence interval line
        fig.add_trace(go.Scatter(
            x=line_x,
            y=lower,
            mode='lines',
            name='Lower Confidence Interval',
            hoverlabel=dict(namelength=-1),  # Do not truncate hover label text
            line=dict(color='rgba(0, 0, 255, 0.5)', dash='dash'),  # Blue dashed line
            fill='tonexty',  # Fill the area between the upper and lower confidence interval lines
            fillcolor='rgba(0, 255, 0, 0.1)',  # Light green fill
            hovertemplate='Lower Confidence Interval<br>PP&E: %{x:.2f}<br>Outage Count: %{y:.2f}<extra></extra>',  # Custom hover template
            showlegend=True
        ))

    def __create_outage_time_plot(self, df):
        return px.line(df, x='Date', y='Outage per PP&E', color='Company', markers=True, title='Outage per PP&E by Company Over Time')

    def __plot_percentiles(self, df, fig):
        # Percentiles
        percentiles = df['Outage per PP&E'].quantile([0.05, 0.25, 0.5, 0.75, 0.95])
        values = [percentiles[q] for q in [0.05, 0.25, 0.5, 0.75, 0.95]]
        percents = ['5th', '25th', '50th', '75th', '95th']

        # Generate a DatetimeIndex of daily dates spanning from the earliest to the latest date in 'df_filtered'.
        full_dates = pd.date_range(start=df['Date'].min(), end=df['Date'].max(), freq='D')

        # Colors
        colors = ['blue', 'green', 'red', 'green', 'blue']

        # Draws dashed lines for the different percentiles
        for y, color, name in zip(values, colors, percents):
            y_values = [y] * len(full_dates)
            hover_text = [f"{name} percentile: {y:.1f}"] * len(full_dates)
            fig.add_trace(go.Scatter(
                x=full_dates, y=y_values,
                mode='lines',
                line=dict(color=color, dash='dash' if name != '50th' else 'solid', width=1),
                opacity=0.5, 
                name=name,
                showlegend=False,
                hoverinfo='text',
                text=hover_text
            ))

    def __mark_outliers(self, fig, df, line_x, line_y_95):
            # Identify points above the upper prediction interval line
            points_above_upper = df[df['Count'] > np.interp(df['PP&E'], line_x, line_y_95)]
            hover_text_outliers = [
                    f"Company: {comp}<br>PP&E: {pp:.2f}<br>Count: {cnt:.2f}<br>Outage per PP&E: {opp:.2f}<br><b>Outlier</b>"
                    for comp, pp, cnt, opp in zip(
                        points_above_upper['Company'],
                        points_above_upper['PP&E'],
                        points_above_upper['Count'],
                        points_above_upper['Outage per PP&E']
                    )
            ]

            # Add these points as a separate trace
            fig.add_trace(go.Scatter(
                x=points_above_upper['PP&E'],
                y=points_above_upper['Count'],
                mode='markers',
                name='Points Above the 95th Quantile',
                marker=dict(color='black', size=8),
                text=hover_text_outliers,
                hoverinfo='text',
                showlegend=True
            ))