import pandas as pd
import numpy as np
from scipy.stats import linregress, t
from config import company_aliases_2, quarters_mapping
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf


class VisHelper:
    def __init__(self, df):
        self.df = df
        self.__check_columns_exist()
        self.preprocess_data()

    def filter_dataframe(self, selected_companies=None, start_date=None, end_date=None):
        df_filtered = self.df
        if selected_companies is not None:
            df_filtered = df_filtered[df_filtered['Company'].isin(selected_companies)]
        if start_date is not None:
            df_filtered = df_filtered[df_filtered['Date'] >= pd.to_datetime(start_date)]
        if end_date is not None:
            df_filtered = df_filtered[df_filtered['Date'] <= pd.to_datetime(end_date)]
        return df_filtered

    def group_and_aggregate(self, df):
        return df.groupby('Company').agg({'Count': 'mean', 'PP&E': 'mean', 'Outage per PP&E': 'mean'}).reset_index()

    def perform_regression(self, grouped_df):
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
    
    def calculate_prediction_interval(self, df, pi, residual_std, line_x, line_y):
        z_score = stats.norm.ppf((1 + pi / 100) / 2)
        prediction_std_error = residual_std * np.sqrt(1 + 1/len(df) + (line_x - np.mean(df['PP&E']))**2 / np.sum((df['PP&E'] - np.mean(df['PP&E']))**2))
        pi_upper = line_y + z_score * prediction_std_error
        pi_lower = line_y - z_score * prediction_std_error
        return pi_upper, pi_lower

    def perform_quantile_regression(self, df, quantile, x):
        formula = 'Count ~ Q("PP&E")'  # Using Q() to safely quote the variable name
        try:
            # Fitting the quantile regression model
            model = smf.quantreg(formula, df)
            results = model.fit(q=quantile)
            
            # Making predictions
            y_pred = results.predict(x[['PP&E']])  # Ensure x has a column 'PP&E'

            # Extracting coefficients
            intercept = results.params['Intercept']
            slope = results.params.get('Q("PP&E")', None)  # Using get to avoid KeyError if the model fails

            return y_pred, slope, intercept
        except Exception as e:
            print("Error in performing quantile regression:", e)
            return None, None, None



    def calculate_confidence_interval(self, grouped_df, ci, residual_std, line_x, line_y):
        x_bar = np.mean(grouped_df['PP&E'])
        n = len(grouped_df['PP&E'])
        t_crit = stats.t.ppf((1 + ci/100) / 2, df=n-2)
        se_forecast = residual_std * np.sqrt(1 / n + (line_x - x_bar) ** 2 / np.sum((grouped_df['PP&E'] - x_bar) ** 2))
        ci_upper = line_y + t_crit * se_forecast
        ci_lower = line_y - t_crit * se_forecast
        return ci_upper, ci_lower

        

    def grand_total(self, include_grand_total, df_filtered):
        if include_grand_total:
            grand_total = df_filtered.copy()
            grand_total['Company'] = 'All Companies'
            return pd.concat([df_filtered, grand_total], ignore_index=True)
        return df_filtered
    
    def preprocess_data(self):
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



