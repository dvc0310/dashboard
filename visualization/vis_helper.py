import pandas as pd
import numpy as np
from config.config import company_aliases_2, quarters_mapping
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf

class VisHelper:
    def __init__(self, df):
        """
        Initializes the VisHelper class with a DataFrame and preprocesses the data.

        Parameters:
            df (DataFrame): The initial dataset to be processed and analyzed.

        Performs initial preprocessing of the data which includes mapping company aliases,
        converting quarters and years to datetime, and calculating outage per PP&E.
        """
        self.df = df
        self.__check_columns_exist()
        self.preprocess_data()

    def filter_dataframe(self, selected_companies=None, start_date=None, end_date=None):
        """
        Filters the DataFrame based on selected companies and a date range.

        Parameters:
            selected_companies (list, optional): List of companies to include in the filter.
            start_date (str, optional): The start date of the data to include (inclusive).
            end_date (str, optional): The end date of the data to include (inclusive).

        Returns:
            DataFrame: The filtered DataFrame.
        """
        df_filtered = self.df
        if selected_companies is not None:
            df_filtered = df_filtered[df_filtered['Company'].isin(selected_companies)]
        if start_date is not None:
            df_filtered = df_filtered[df_filtered['Date'] >= pd.to_datetime(start_date)]
        if end_date is not None:
            df_filtered = df_filtered[df_filtered['Date'] <= pd.to_datetime(end_date)]
        return df_filtered

    def group_and_aggregate(self, df):
        """
        Aggregates the data by company, calculating average count, PP&E, and outage per PP&E.

        Parameters:
            df (DataFrame): The DataFrame to be aggregated.

        Returns:
            DataFrame: The aggregated DataFrame with averages of Count, PP&E, and outage per PP&E.
        """
        return df.groupby('Company').agg({'Count': 'mean', 'PP&E': 'mean', 'Outage per PP&E': 'mean'}).reset_index()

    def perform_regression(self, grouped_df):
        """
        Performs linear regression on the aggregated data.

        Parameters:
            grouped_df (DataFrame): The DataFrame containing grouped data for regression analysis.

        Returns:
            tuple: Regression parameters including slope, intercept, r_value, p_value, residual_std, line_x, and line_y.
        """
        X = sm.add_constant(grouped_df['PP&E'])
        y = grouped_df['Count']
        model = sm.OLS(y, X).fit()

        intercept, slope = model.params
        residuals = model.resid
        residual_std = np.std(residuals, ddof=1)  # Calculate the standard deviation of residuals

        r_value = model.rsquared**0.5
        p_value = model.pvalues['PP&E']

        line_x = np.linspace(grouped_df['PP&E'].min(), grouped_df['PP&E'].max(), 100)
        line_y = slope * line_x + intercept

        return slope, intercept, r_value, p_value, residual_std, line_x, line_y
    
    def perform_quantile_regression(self, df, quantile, x):
        """
            Performs quantile regression based on the specified quantile and predicts values using the provided DataFrame.

            Parameters:
                df (DataFrame): The DataFrame containing the data for the regression, with 'Count' as the dependent variable
                                and 'PP&E' as the independent variable.
                quantile (float): The quantile for which the regression is performed (e.g., 0.5 for median).
                x (DataFrame): The DataFrame with 'PP&E' values on which predictions are to be made.

            Returns:
                tuple: A tuple containing the predicted values (y_pred), the slope of the regression, and the intercept.
                    Returns (None, None, None) if an error occurs.

            This method uses the Statsmodels Quantile Regression function to fit a model to the specified quantile.
        """
        formula = 'Count ~ Q("PP&E")' 
        try:
            # Fitting the quantile regression model
            model = smf.quantreg(formula, df)
            results = model.fit(q=quantile)
            
            # Making predictions
            y_pred = results.predict(x[['PP&E']]) 

            # Extracting coefficients
            intercept = results.params['Intercept']
            slope = results.params.get('Q("PP&E")', None)  #

            return y_pred, slope, intercept
        except Exception as e:
            print("Error in performing quantile regression:", e)
            return None, None, None


    def calculate_confidence_interval(self, grouped_df, ci, residual_std, line_x, line_y):
        """
        Calculates the confidence intervals for the regression line at a specified confidence level.

        Parameters:
            grouped_df (DataFrame): The DataFrame with aggregated data used for the regression.
            ci (float): The desired confidence level (e.g., 95 for 95% confidence).
            residual_std (float): The standard deviation of the residuals from the regression.
            line_x (array): The x-values (independent variable) of the regression line.
            line_y (array): The y-values (predicted dependent variable) of the regression line.

        Returns:
            tuple: Upper and lower bounds of the confidence interval for the regression line.

        """
        x_bar = np.mean(grouped_df['PP&E'])
        n = len(grouped_df['PP&E'])
        t_crit = stats.t.ppf((1 + ci/100) / 2, df=n-2)
        se_forecast = residual_std * np.sqrt(1 / n + (line_x - x_bar) ** 2 / np.sum((grouped_df['PP&E'] - x_bar) ** 2))
        ci_upper = line_y + t_crit * se_forecast
        ci_lower = line_y - t_crit * se_forecast
        return ci_upper, ci_lower


    def grand_total(self, include_grand_total, df_filtered):
        """
        Optionally appends a row with grand total calculations to the filtered DataFrame.

        Parameters:
            include_grand_total (bool): Determines whether to include a grand total row.
            df_filtered (DataFrame): The DataFrame to which the grand total row might be added.

        Returns:
            DataFrame: The DataFrame with or without a grand total row based on the parameter.

        If 'include_grand_total' is True, a new row labeled 'All Companies' is added to the DataFrame,
        which contains the aggregation of all data in the DataFrame. This row is useful for comparative
        analysis and visualization where a summary row is needed.
        """
        if include_grand_total:
            grand_total = df_filtered.copy()
            grand_total['Company'] = 'All Companies'
            return pd.concat([df_filtered, grand_total], ignore_index=True)
        return df_filtered
    
    def preprocess_data(self):
        """
        Preprocesses the initial DataFrame by mapping company aliases, converting date fields, and calculating derived metrics.
        """
        self.df['Company'] = self.df['Company'].map(company_aliases_2)
        self.df['Date'] = pd.to_datetime(self.df['Year'].astype(str) + '-' + self.df['Quarter'].map(quarters_mapping).astype(str))
        self.df['Outage per PP&E'] = self.df['Count'] / self.df['PP&E']
        self.df['PP&E'] = pd.to_numeric(self.df['PP&E'], errors='coerce')
        self.df = self.df.dropna(subset=['PP&E'])

    def __check_columns_exist(self):
        required_columns = ['Company', 'Year', 'Quarter', 'Count', 'PP&E']
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # Unused
    def calculate_prediction_interval(self, df, pi, residual_std, line_x, line_y):
        z_score = stats.norm.ppf((1 + pi / 100) / 2)
        prediction_std_error = residual_std * np.sqrt(1 + 1/len(df) + (line_x - np.mean(df['PP&E']))**2 / np.sum((df['PP&E'] - np.mean(df['PP&E']))**2))
        pi_upper = line_y + z_score * prediction_std_error
        pi_lower = line_y - z_score * prediction_std_error
        return pi_upper, pi_lower



