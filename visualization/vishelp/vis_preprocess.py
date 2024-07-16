import pandas as pd
import numpy as np
from config.config import company_aliases_2, quarters_mapping

class VisualizationPreprocessor:
    def __init__(self, df):
        self.df = df
        self.__check_columns_exist()

    def preprocess_data(self, df):
        df['Company'] = df['Company'].map(company_aliases_2)
        df['Date'] = pd.to_datetime(df['Year'].astype(str) + '-' + df['Quarter'].map(quarters_mapping).astype(str))
        df['Outage per PP&E'] = df['Count'] / self.df['PP&E']
        df['PP&E'] = pd.to_numeric(df['PP&E'], errors='coerce')
        df = df.dropna(subset=['PP&E'])
        return df

    def filter_dataframe(self, df, selected_companies=None, start_date=None, end_date=None):
        df_filtered = df
        if selected_companies is not None:
            df_filtered = df_filtered[df_filtered['Company'].isin(selected_companies)]
        if start_date is not None:
            df_filtered = df_filtered[df_filtered['Date'] >= pd.to_datetime(start_date)]
        if end_date is not None:
            df_filtered = df_filtered[df_filtered['Date'] <= pd.to_datetime(end_date)]
        return df_filtered

    def group_and_aggregate(self, df):
        return df.groupby('Company').agg({'Count': 'mean', 'PP&E': 'mean', 'Outage per PP&E': 'mean'}).reset_index()

    def grand_total(self, include_grand_total, df):
        if include_grand_total:
            grand_total = df.copy()
            grand_total['Company'] = 'All Companies'
            return pd.concat([df, grand_total], ignore_index=True)
        return df

    def __check_columns_exist(self):
        required_columns = ['Company', 'Year', 'Quarter', 'Count', 'PP&E']
        missing_columns = [col for col in required_columns if col not in self.df.columns]
        if missing_columns:
            raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")