from dash.dependencies import Input, Output, State
import base64
import io
import pandas as pd
from dash import html
import dash
from dash.exceptions import PreventUpdate
import os
from data_prep import DataPreparer

def register_callbacks(app, visualizer):
    @app.callback(
        Output('graph-tab1', 'figure'),
        [Input('company-dropdown-tab1', 'value'),
        Input('ci-checklist', 'value'),
        Input('view-toggle', 'value'),
        Input('date-picker-range1', 'start_date'),
        Input('date-picker-range1', 'end_date')])
    def update_graph_tab1(selected_companies, ci_values, view_mode, start_date, end_date):
        enable_ci = 'CI' in ci_values
        #enable_pi = 'PI' in pi_values

        if view_mode == 'Granular':
            return visualizer.plot_granular_outage_vs_ppe(selected_companies=selected_companies, enable_pi=enable_ci, start_date=start_date, end_date=end_date, dashboard=True)
        else:
            return visualizer.plot_average_outage_vs_ppe(selected_companies=selected_companies, enable_ci=enable_ci, start_date=start_date, end_date=end_date, dashboard=True)

    @app.callback(
        Output('graph-tab2', 'figure'),
        [Input('company-dropdown-tab2', 'value'),
         Input('date-picker-range2', 'start_date'),
         Input('date-picker-range2', 'end_date')])
    def update_graph_tab2(selected_companies, start_date, end_date):
        return visualizer.plot_outage_per_ppe_over_time(selected_companies=selected_companies, start_date=start_date, end_date=end_date, dashboard=True)

    @app.callback(
        Output('graph-tab3', 'figure'),
        [Input('company-dropdown-tab3', 'value'),
         Input('grand-total-checklist', 'value'),     
         Input('date-picker-range3', 'start_date'),
         Input('date-picker-range3', 'end_date')])
    def update_graph_tab3(selected_companies, gt_values, start_date, end_date):
        include_grand_total = 'GT' in gt_values
        return visualizer.plot_outage_per_ppe_boxplot(selected_companies=selected_companies, include_grand_total=include_grand_total, start_date=start_date, end_date=end_date, dashboard=True)
    
    @app.callback(
        Output('pi-options', 'children'),
        [Input('view-toggle', 'value')])
    def display_pi_options(view_mode):
        if view_mode == 'Granular':
            return html.Div([
                __singular_checkbox(id='pi-checklist', label='Enable Prediction Intervals', value='PI', default_options=[])
            ])
        return None  # Don't display anything if not in Granular mode


from dash import dcc

def __singular_checkbox(id, label, value, default_options):
    return dcc.Checklist(
        id=id,
        options=[{'label': label, 'value': value}],
        value=default_options,
        style={'padding': '10px'}  # Add some padding for better UI
    )

    # Unused
    """@app.callback(
        [Output('upload-status', 'children'),
        Output('stored-filenames', 'data')],  # Update output to include the store
        [Input('upload-outage-data', 'contents'),
        Input('upload-ppe-data', 'contents'),
        Input('process-data-btn', 'n_clicks')],
        [State('upload-outage-data', 'filename'),
        State('upload-ppe-data', 'filename'),
        State('stored-filenames', 'data')]  # Add stored filenames as a State
    )
    def handle_file_upload(outage_contents, ppe_contents, n_clicks, outage_filename, ppe_filename, stored_filenames):
        print("Callback triggered1!")  # Shows callback is being triggered

        ctx = dash.callback_context
        print("Callback triggered!")  # Shows callback is being triggered
        if not ctx.triggered:
            print("No trigger found. Waiting for inputs...")  # Indicates waiting state
            return 'Awaiting uploads and processing...', stored_filenames

        triggered_id = ctx.triggered[0]['prop_id'].split('.')[0]
        print(f"Triggered by: {triggered_id}")  # Identifies the input that triggered the callback

        if triggered_id in ['upload-outage-data', 'upload-ppe-data']:
            if triggered_id == 'upload-outage-data' and outage_contents:
                print(f"Uploading outage data: {outage_filename}")  # Before saving the file
                save_file('datasets', outage_filename, outage_contents)
                stored_filenames['outage'] = outage_filename
                print(f"Outage data saved: {stored_filenames['outage']}")  # After saving the file
            elif triggered_id == 'upload-ppe-data' and ppe_contents:
                print(f"Uploading PPE data: {ppe_filename}")  # Before saving the file
                save_file('datasets', ppe_filename, ppe_contents)
                stored_filenames['ppe'] = ppe_filename
                print(f"PPE data saved: {stored_filenames['ppe']}")  # After saving the file
            return 'Files uploaded. Click "Process New Data" to update visuals.', stored_filenames

        if triggered_id == 'process-data-btn' and n_clicks > 0:
            print("Processing data button clicked.")  # Indicates processing attempt
            # Check if filenames are stored
            if stored_filenames['outage'] and stored_filenames['ppe']:
                print(f"Using stored filenames: Outage - {stored_filenames['outage']}, PPE - {stored_filenames['ppe']}")  # File names being used
                dataprep = DataPreparer(
                    start_year=2016, end_year=2023,
                    folder='datasets',
                    outage_file_name=stored_filenames['outage'],
                    financial_file_name=stored_filenames['ppe']
                )
                dataprep.save_to_csv(folder='datasets')
                visualizer.update_data()  # Assume this updates some visual component
                
                print("Data preparation and visual update completed.")  # Confirmation of completion
                return 'Data processed and visuals updated.', stored_filenames

        print("No valid actions performed.")  # If none of the conditions were met
        return 'No new files uploaded or processed.', stored_filenames



    @app.callback(
        Output('upload-progress-bar', 'style'),
        [Input('upload-outage-data', 'filename'),  # Trigger updates based on file upload
        Input('upload-ppe-data', 'filename')]
    )
    def update_progress_bar(*filenames):
        # Simple example to set progress based on file upload
        if any(filenames):
            return {'width': '100%', 'height': '30px', 'background-color': '#007BFF'}
        return {'width': '0%', 'height': '30px', 'background-color': '#007BFF'}


def save_file(directory, filename, content):
    print(f"Starting to save file: {filename}")  # Debugging statement
    content_type, content_string = content.split(',')
    decoded = base64.b64decode(content_string)
    path = os.path.join(directory, filename)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(path, 'wb') as f:
        f.write(decoded)
    print(f"File {filename} saved in {directory}")
"""