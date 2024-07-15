import os
import pandas as pd
import numpy as np

def find_project_root(current_dir):
    marker = 'marker'  
    while current_dir != os.path.dirname(current_dir):  # Stop when the root directory is reached
        if marker in os.listdir(current_dir):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    raise Exception("Project root with marker not found.")

def change_to_root():
    cwd = os.getcwd()
    print("Current working directory:", cwd)
    project_root = find_project_root(cwd)
    os.chdir(project_root)
    print("Changed to project root directory:", os.getcwd())

def transform_ppe_data(ppe_data, save_to_excel=False, folder='.', excel_filename="transformed_ppe_data.xlsx", save_to_csv=False, csv_filename="transformed_ppe_data.csv"):
    ppe = ppe_data.copy()
    ppe.rename(columns={'Company': 'SP_ENTITY_NAME'}, inplace=True)
    empty_df = pd.DataFrame(np.nan, index=range(6), columns=ppe.columns)
    new_df = pd.concat([empty_df, ppe], ignore_index=True)
    new_df.iloc[3] = new_df.columns

    # Insert a new column with NaNs at the specified index
    new_df.insert(1, 'NewEmptyColumn', np.nan)
    new_df.at[3, 'NewEmptyColumn'] = "SP_ENTITY_ID"
    columns_to_update = [col for col in new_df.columns if col not in ['SP_ENTITY_NAME', 'NewEmptyColumn']]
    
    # Set the value of the cells in the 4th row (index 2) to 'PP&E' for the specified columns
    new_df.loc[2, columns_to_update] = 'PP&E'

    # List all columns except 'SP_ENTITY_NAME' and 'NewEmptyColumn'
    columns_to_shift = [col for col in new_df.columns if col not in ['SP_ENTITY_NAME', 'NewEmptyColumn']]
    last_sp_entity= new_df.iloc[-1]
    new_df[columns_to_shift] = new_df[columns_to_shift].shift(1)

    # Correctly shift the 'SP_ENTITY_NAME' column
    new_df['SP_ENTITY_NAME'].iloc[5:] = new_df['SP_ENTITY_NAME'].iloc[5:].shift(1)
    new_df = pd.concat([new_df, pd.DataFrame(last_sp_entity).T], axis=0, ignore_index=True)

    # Replace column names with np.NaN
    new_df.columns = [np.nan] * new_df.shape[1]

    if save_to_excel:
        new_df.to_excel(f'{folder}/{excel_filename}', index=False)
    
    if save_to_csv:
        new_df.to_csv(f'{folder}/{csv_filename}', index=False)

    return new_df
