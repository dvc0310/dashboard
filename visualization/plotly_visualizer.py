import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import linregress, t
import numpy as np
from data_prep import find_encoding
from config import company_aliases_2, quarters_mapping
from .vis_helper import VisHelper


class PlotlyVisualizer:
    def __init__(self, filename='prepared_data.csv', directory='visualization'):
        self.directory = directory
        self.filename = filename
        self.load_data()

    def load_data(self):
        csv_path = f'{self.directory}/{self.filename}'
        self.df = pd.read_csv(csv_path, encoding=find_encoding(csv_path))
        self.vh = VisHelper(self.df)

    def update_data(self):
        self.load_data() 

    def plot_average_outage_vs_ppe(self, ci=95, enable_ci=False, dashboard=False, selected_companies=None, start_date=None, end_date=None):
        df_filtered = self.vh.filter_dataframe(selected_companies, start_date, end_date)
        grouped_df = self.vh.group_and_aggregate(df_filtered)
        slope, intercept, r_value, p_value, std_err, line_x, line_y = self.vh.perform_regression(grouped_df)
        if enable_ci:
            ci_upper, ci_lower = self.vh.calculate_confidence_interval(grouped_df, ci, std_err, line_x, line_y)
        else:
            ci_upper, ci_lower = None, None

        fig, _ = self.__create_figure(grouped_df, line_x, line_y, slope, intercept, r_value)
        if enable_ci:
            self.__add_confidence_intervals(fig, line_x, ci_upper, ci_lower)
        if dashboard:
            return fig
        fig.show()


    def plot_granular_outage_vs_ppe(self, pi=95, enable_pi=False, dashboard=False, selected_companies=None, start_date=None, end_date=None):
        df_filtered = self.vh.filter_dataframe(selected_companies, start_date, end_date)
        line_x = np.linspace(df_filtered['PP&E'].min(), df_filtered['PP&E'].max(), 100)
        x = pd.DataFrame(line_x, columns=["PP&E"])
        # Using quantile regression for the median and the prediction intervals
        line_y_50, slope, intercept = self.vh.perform_quantile_regression(df_filtered, 0.50, x)
        line_y_95,slope95, intercept95  = self.vh.perform_quantile_regression(df_filtered, 0.95, x)
        line_y_05, slope5, intercept5= self.vh.perform_quantile_regression(df_filtered, 0.05, x)
        
        
        fig, sizes = self.__create_figure(df_filtered, line_x, line_y_50, pi=enable_pi, slope=slope, intercept=intercept)
        
        if enable_pi:
            self.__add_prediction_intervals(fig, line_x, line_y_95, line_y_05, slope95, intercept95, slope5, intercept5)
            # Identify points above the upper prediction interval line
            points_above_upper = df_filtered[df_filtered['Count'] > np.interp(df_filtered['PP&E'], line_x, line_y_95)]
            hover_text_outliers = [
                f"Company: {comp}<br>PP&E: {pp:.2f}<br>Count: {cnt:.2f}<br>Outage per PP&E: {opp:.2f}<br><b>Outlier</b>"
                for comp, pp, cnt, opp in zip(points_above_upper['Company'],points_above_upper['PP&E'], points_above_upper['Count'], points_above_upper['Outage per PP&E'])
            ]
            # Add these points as a separate trace
            fig.add_trace(go.Scatter(
                x=points_above_upper['PP&E'],
                y=points_above_upper['Count'],
                mode='markers',
                name='Points Above 95th Quantile',
                marker=dict(color='black', size=8),
                text=hover_text_outliers,
                hoverinfo='text',
                showlegend=True
            ))
        
        if dashboard:
            return fig
        fig.show()



    def plot_outage_per_ppe_over_time(self, show_percentiles=True, dashboard=False, selected_companies=None, start_date=None, end_date=None):
        df_filtered = self.vh.filter_dataframe(selected_companies, start_date, end_date)
        fig = self.__create_outage_time_plot(df_filtered)

        if show_percentiles:
            self.__plot_percentiles(df_filtered, fig)

        if dashboard:
            return fig
        fig.show()


    def plot_outage_per_ppe_boxplot(self, include_grand_total=False, dashboard=False, selected_companies = None,start_date=None,end_date=None):
        df_filtered = self.vh.filter_dataframe(selected_companies, start_date, end_date)
        data = self.vh.grand_total(include_grand_total=include_grand_total, df_filtered=df_filtered)

        data['Outage per PP&E Rounded'] = data['Outage per PP&E'].round(1)

        fig = px.box(data, x='Company', y='Outage per PP&E', color='Company', points="all",
                    title='Outage per PP&E by Company',
                    hover_data={'Outage per PP&E': ':.2f',  
                                'Outage per PP&E Rounded': True})  
 
        fig.update_layout(
            colorway=['#636EFA', '#EF553B', '#00CC96', '#AB63FA', '#FFA15A', '#19D3F3', '#FF6692', '#B6E880', '#FF97FF', '#FECB52']
        )
        if dashboard:
            return fig
        fig.show()

    def __add_prediction_intervals(self, fig, line_x, pi_upper, pi_lower, slope95, intercept95, slope5, intercept5):
        # Add upper and lower prediction interval lines
        equation_text95 = f'Equation:<br>{slope95:.2f} * PP&E + {intercept95:.2f}'
        hover_text95 = [f"{equation_text95}<br>Predicted Outage Freq (Upper Bound):<br>{y:.1f}" for y in pi_upper]
        equation_text5 = f'Equation:<br>{slope5:.2f} * PP&E + {intercept5:.2f}'
        hover_text5 = [f"{equation_text5}<br>Predicted Outage Freq (Lower Bound):<br>{y:.1f}" for y in pi_lower]
        fig.add_trace(go.Scatter(
            x=line_x,
            y=pi_upper,
            mode='lines',
            name='95th Quantile',
            line=dict(color='red', dash='dash'),
            #hovertemplate='Upper Quantile Regression Line<br>PP&E: %{x:.2f}<br>Outage Count: %{y:.2f}<extra></extra>', 
            text=hover_text95,
            hoverinfo='text',
            showlegend=True
        ))
        fig.add_trace(go.Scatter(
            x=line_x,
            y=pi_lower,
            mode='lines',
            name='5th Quantile',
            line=dict(color='blue', dash='dash'),
            fill='tonexty',  # Fill between the upper and lower bounds
            #hovertemplate='Lower Quantile Regression Line<br>PP&E: %{x:.2f}<br>Outage Count: %{y:.2f}<extra></extra>',  
            fillcolor='rgba(0, 255, 0, 0.2)',
            text=hover_text5,
            hoverinfo='text',
            showlegend=True
        ))


    def __create_figure(self, grouped_df, line_x, line_y, slope, intercept, r_value=None, pi=False):
        if pi:
            title = 'Outage Frequency vs. PP&E by Company'
        else:
            title = 'Average Outage Frequency vs. Average PP&E by Company'
        
        fig = px.scatter(
            grouped_df, 
            x='PP&E', 
            y='Count', 
            color='Company', 
            size='Outage per PP&E', 
            title=title,
            hover_data={
                'PP&E': ':.2f',
                'Count': ':.2f',
                'Outage per PP&E': ':.2f',
            }
        )

        equation_text = f'Predicted Outage Freq. = {slope:.2f} * PP&E + {intercept:.2f}'

        if r_value is not None:
            r_value_text = f'Correlation coefficient: {r_value:.2f}'
            hover_text = [f"{equation_text}<br>{r_value_text}<br>Outage Count: {y:.1f}" for y in line_y]
        else:
            hover_text = [f"{equation_text}<br>Outage Count: {y:.1f}" for y in line_y]

        fig.add_trace(go.Scatter(
            x=line_x, 
            y=line_y, 
            mode='lines', 
            name='Regression Line',
            text=hover_text, 
            hoverinfo='text'
        ))

        initial_sizes = px.scatter(
            grouped_df, 
            x='PP&E', 
            y='Count', 
            size='Outage per PP&E'
        ).data[0].marker.size

        return fig, initial_sizes

    def __add_confidence_intervals(self, fig, line_x, ci_upper, ci_lower):
        # Add upper confidence interval line
        fig.add_trace(go.Scatter(
            x=line_x,
            y=ci_upper,
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
            y=ci_lower,
            mode='lines',
            name='Lower Confidence Interval',
            hoverlabel=dict(namelength=-1),  # Do not truncate hover label text
            line=dict(color='rgba(0, 0, 255, 0.5)', dash='dash'),  # Blue dashed line
            fill='tonexty',  # Fill the area between the upper and lower confidence interval lines
            fillcolor='rgba(0, 255, 0, 0.1)',  # Light red fill
            hovertemplate='Lower Confidence Interval<br>PP&E: %{x:.2f}<br>Outage Count: %{y:.2f}<extra></extra>',  # Custom hover template

            showlegend=True
        ))


    def __create_outage_time_plot(self, df_filtered):
        return px.line(df_filtered, x='Date', y='Outage per PP&E', color='Company', markers=True, title='Outage per PP&E by Company Over Time')

    def __plot_percentiles(self, df_filtered, fig):
        percentiles = df_filtered['Outage per PP&E'].quantile([0.05, 0.25, 0.5, 0.75, 0.95])
        values = [percentiles[q] for q in [0.05, 0.25, 0.5, 0.75, 0.95]]
        full_dates = pd.date_range(start=df_filtered['Date'].min(), end=df_filtered['Date'].max(), freq='D')
        colors = ['blue', 'green', 'red', 'green', 'blue']
        percents = ['5th', '25th', 'Median', '75th', '95th']

        for y, color, name in zip(values, colors, percents):
            y_values = [y] * len(full_dates)
            hover_text = [f"{name} percentile: {y:.1f}"] * len(full_dates)

            fig.add_trace(go.Scatter(
                x=full_dates, y=y_values,
                mode='lines',
                line=dict(color=color, dash='dash' if name != 'Median' else 'solid', width=1),
                opacity=0.5, 
                name=name,
                showlegend=False,
                hoverinfo='text',
                text=hover_text
            ))
