import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np

class StatsHelper:
    def __init__(self, df):
        self.df = df
        self.__check_columns_exist()

    def perform_regression(self, df):
        X = sm.add_constant(df['PP&E'])
        y = df['Count']
        model = sm.OLS(y, X).fit()

        intercept, slope = model.params
        residuals = model.resid
        residual_std = np.std(residuals, ddof=1)

        r_value = model.rsquared**0.5
        p_value = model.pvalues['PP&E']

        line_x = np.linspace(df['PP&E'].min(), df['PP&E'].max(), 100)
        line_y = slope * line_x + intercept

        return slope, intercept, r_value, p_value, residual_std, line_x, line_y

    def perform_quantile_regression(self, df, quantile, x):
        formula = 'Count ~ Q("PP&E")'
        try:
            model = smf.quantreg(formula, df)
            results = model.fit(q=quantile)
            y_pred = results.predict(x[['PP&E']])
            intercept = results.params['Intercept']
            slope = results.params.get('Q("PP&E")', None)
            return y_pred, slope, intercept
        except Exception as e:
            print("Error in performing quantile regression:", e)
            return None, None, None

    def calculate_confidence_interval(self, df, ci, residual_std, line_x, line_y):
        x_bar = np.mean(df['PP&E'])
        n = len(df['PP&E'])
        t_crit = stats.t.ppf((1 + ci/100) / 2, df=n-2)
        se_forecast = residual_std * np.sqrt(1 / n + (line_x - x_bar) ** 2 / np.sum((df['PP&E'] - x_bar) ** 2))
        ci_upper = line_y + t_crit * se_forecast
        ci_lower = line_y - t_crit * se_forecast
        return ci_upper, ci_lower
    
    def __check_columns_exist(self):
        required_columns = ['Company', 'Year', 'Quarter', 'Count', 'PP&E']
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
