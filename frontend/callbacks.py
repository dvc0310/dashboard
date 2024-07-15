from dash.dependencies import Input, Output
from dash import html
from dash import dcc

def register_callbacks(app, visualizer):
    @app.callback(
        Output('graph-tab1', 'figure'),
        [Input('company-dropdown-tab1', 'value'),
        Input('checklist', 'value'),
        Input('view-toggle', 'value'),
        Input('date-picker-range1', 'start_date'),
        Input('date-picker-range1', 'end_date')])
    def update_graph_tab1(selected_companies, interval_values, view_mode, start_date, end_date):
        enable_interval = 'Interval' in interval_values

        if view_mode == 'Granular':
            return visualizer.plot_granular_outage_vs_ppe(selected_companies=selected_companies, enable_interval=enable_interval, start_date=start_date, end_date=end_date, dashboard=True)
        else:
            return visualizer.plot_average_outage_vs_ppe(selected_companies=selected_companies, enable_interval=enable_interval, start_date=start_date, end_date=end_date, dashboard=True)

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
    
