from dash import html, dcc
from .tabs.outage_per_ppe_tabs import boxplot_tab, line_chart_tab, regression_tab
def create_layout(visualizer):
    layout = html.Div([
        dcc.Tabs(id="tabs", value='tab-1', children=[
            regression_tab(visualizer=visualizer),
            line_chart_tab(visualizer=visualizer),
            boxplot_tab(visualizer=visualizer)
        ]),
        html.Div(id='tabs-content'),
        dcc.Store(id='stored-filenames', data={'outage': 'outage_data.csv', 'ppe': 'ppe.csv'}),  # Adding dcc.Store here
        dcc.Download(id="download")
    ], style={'background-color': '#eaeaea'})
    
    return layout

