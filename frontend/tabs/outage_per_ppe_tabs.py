from dash import html, dcc

def regression_tab(visualizer):
    return dcc.Tab(label='Outage Frequency vs PP&E', value='tab-1', children=[
        html.Div([__datepicker(visualizer=visualizer, number=1)]),
        html.Div([
            __singular_checkbox(id='ci-checklist', label='Enable Interval', value='CI'),
            __toggle_switch(id='view-toggle', label1='Aggregated', label2='Granular', default='Aggregated')
        ]),
        html.Div([__dropdown(visualizer=visualizer, number=1)]),
        dcc.Graph(id='graph-tab1')
    ])


def line_chart_tab(visualizer):
    return dcc.Tab(label='Outage over Time', value='tab-2', children=[
                html.Div([__datepicker(visualizer=visualizer, number=2)]),
                html.Div([__dropdown(visualizer=visualizer, number=2)]),
                dcc.Graph(id='graph-tab2')
            ])

def boxplot_tab(visualizer):
    return dcc.Tab(label='Outage Box Plot', value='tab-3', children=[
                html.Div([__datepicker(visualizer=visualizer, number=3)]),
                html.Div([__dropdown(visualizer=visualizer, number=3)]),
                html.Div([__singular_checkbox(id='grand-total-checklist',label='Grand Total', value='GT',default_options=['GT'])]),
                dcc.Graph(id='graph-tab3')
            ])

def __datepicker(visualizer, number):
    return dcc.DatePickerRange(
                id=f'date-picker-range{number}',
                start_date=visualizer.df['Date'].min(),
                end_date=visualizer.df['Date'].max(),
                display_format='YYYY-MM-DD'
            )

def __dropdown(visualizer, number):
     return dcc.Dropdown(
                id=f'company-dropdown-tab{number}',
                options=[{'label': company, 'value': company} for company in visualizer.df['Company'].dropna().unique()],
                value=list(visualizer.df['Company'].unique()),
                multi=True
            )

def __singular_checkbox(id, label, value, default_options=[]):
    return dcc.Checklist(
                id=id,
                options=[{'label': f'{label}', 'value': f'{value}'}],
                value=default_options
            )

def __toggle_switch(id, label1, label2, default):
    return html.Div([
        dcc.RadioItems(
            id=id,
            options=[
                {'label': label1, 'value': 'Aggregated'},
                {'label': label2, 'value': 'Granular'}
            ],
            value=default,
            labelStyle={'display': 'inline-block', 'margin-right': '10px'},
            style={'marginTop': 10, 'marginBottom': 10}
        )
    ])


# Unused

"""def upload_tab():
    return dcc.Tab(label='Data Upload', value='tab-4', children=[
        html.Div([
            dcc.Upload(
                id='upload-outage-data',
                children=html.Button('Upload Outage Data'),
                multiple=False
            ),
            html.Br(),
            dcc.Upload(
                id='upload-ppe-data',
                children=html.Button('Upload PPE Data'),
                multiple=False
            ),
            html.Br(),
            html.Button('Process New Data', id='process-data-btn', n_clicks=0),
            html.Div([
                html.Div(id='upload-progress-bar', style={'width': '0%', 'height': '30px', 'background-color': '#007BFF'}),
            ], style={'width': '100%', 'background-color': '#ddd', 'height': '30px'}),
            html.Div(id='upload-status')
        ])
    ])"""