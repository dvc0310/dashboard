import pandas as pd
from .read_util import find_encoding
import logging
from config import company_aliases

class OutageDataProcessor:
    def __init__(self, outage_file_name, start_year, end_year, folder="datasets"):
        """
        Initialize the OutageDataProcessor.

        Parameters:
        - outage_file_name (str): Name of ythe outage data CSV file.
        - start_year (int): The start year for filtering data.
        - end_year (int): The end year for filtering data.
        - mapper_file_name (str): Name of the company name mapper CSV file.
        - folder (str): Folder where the data files are located. Default is 'datasets'.
        """
        self.outage_file_path = f"{folder}/{outage_file_name}"
        self.end_year = end_year
        self.start_year = start_year
        self.data = None

        print(f"Initialized with year range {self.start_year} to {self.end_year}.")
        self.load_data()


    def load_data(self):
        """
        Load data from the CSV file using conditions to filter by specified years and companies.
        """
        use_columns = ['u_company', 'u_incident_date_time', 'u_outage_report_status']
        filtered_chunks = []
        self._read_csv_by_chunks(chunk_size=10000, use_columns=use_columns, filtered=filtered_chunks)
        self._combine_chunks(filtered_chunks)

    def get_outage_frequency(self):
        """
        Aggregate the data by 'Company', 'Year', and 'Quarter', and count occurrences.
        """
        if self.data is not None and not self.data.empty:
            aggregated_data = self.data.groupby(['Company', 'Year', 'Quarter']).size().reset_index(name='Count')
            print("Data aggregated and counted by company, year, and quarter successfully.")
            return aggregated_data
        else:
            print("Data is empty or not loaded properly. Please check the data loading process.")
            return None

    def _combine_chunks(self, filtered_chunks):
        self.data = pd.concat(filtered_chunks, ignore_index=True)
        self.data.rename(columns={'u_company': 'Company'}, inplace=True)
        self.data['Year'] = self.data['u_incident_date_time'].dt.year.astype(int)
        self.data['Quarter'] = 'Q' + self.data['u_incident_date_time'].dt.quarter.astype(str)
        logging.info("Data loaded and processed successfully.")

    def _datetime_conversion(self, column):
        """
        Convert a date column to datetime more reliably by attempting to parse with multiple specified formats.
        This reduces the need for format inference, which can generate warnings when it fails.
        """
        column = column.astype(str)

        date_formats = [
            "%Y-%m-%d %H:%M:%S",  # e.g., 2020-01-31 13:45:01
            "%d-%m-%Y %H:%M",     # e.g., 31-01-2020 13:45
            "%m/%d/%Y",           # e.g., 01/31/2020
            "%Y-%m-%d"
        ]

        for fmt in date_formats:
            try:
                return pd.to_datetime(column, format=fmt)
            except ValueError:
                pass  

        return pd.to_datetime(column, errors='coerce', infer_datetime_format=True)
    
    def _filter_by_company_status_year(self, chunk):
        chunk['u_incident_date_time'] = self._datetime_conversion(chunk['u_incident_date_time'])
        chunk['u_company'] = chunk['u_company'].str.strip()
        chunk['u_company'] = chunk['u_company'].map(company_aliases)

        valid_years = chunk['u_incident_date_time'].dt.year.between(self.start_year, self.end_year)
        final_status = chunk['u_outage_report_status'] == 'Final'
        valid_companies = chunk['u_company'].isin(company_aliases.values())

        chunk = chunk[valid_years & final_status & valid_companies]

    def _read_csv_by_chunks(self, chunk_size, use_columns,filtered):
        for chunk in pd.read_csv(self.outage_file_path, encoding=find_encoding(self.outage_file_path),
                                 usecols=use_columns, chunksize=chunk_size):
            self._filter_by_company_status_year(chunk)
            filtered.append(chunk)