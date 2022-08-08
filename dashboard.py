from source.util.analysis import Analysis
from source.util.database import Database
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from source.util.settings import Settings
from source.util.conversions import Convert
from source.website.map import Map
from source.util.image import Image
from source.util.timekeeper import Timestamps


class Dashboard:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('general.config')
        self.nodes_config = Settings('nodes.config')
        self.nodes_db = Database(self.config.get_setting('databases', 'nodes_db_path'))
        self.sensors_db = Database(self.config.get_setting('databases', 'sensor_data_db_path'))
        self.map = Map()
        self.image = Image()
        self.convert = Convert()

    def __get_rows(self):
        rows = list()
        break_row = dbc.Row([dbc.Col([html.Br()], width='auto')], justify='center')
        rows.append(break_row)

        environment_title = dbc.Row([dbc.Col([html.H1('Environmental Data')], width='auto')], justify='center')
        rows.append(environment_title)

        data = self.sensors_db.get_records(self.ts.get_24h_timestamp())
        if data is None or len(data) < 1:
            data = self.sensors_db.get_all()
        analysis = Analysis(data)
        last_updated_row = dbc.Row([dbc.Col([html.P('Date Last Updated: ' + analysis.get_last_update_string())],
                                 width='auto')],
                        justify='center')
        rows.append(last_updated_row)

        rows.append(break_row)

        overview_title = dbc.Row([dbc.Col([html.H3('Environment Overview')], width='auto')], justify='center')
        rows.append(overview_title)
        rows.append(break_row)

        timeframe_select_row = dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.RadioItems(
                        id="dash-gauge-timeframe",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Average", "value": 'Current'},
                            {"label": "Minimums", "value": 'Minimums'},
                            {"label": "Maximums", "value": 'Maximums'},
                        ],
                        value='Current',
                    )
                ], className="radio-group"),
            ], width='auto')
        ], justify='center')
        rows.append(timeframe_select_row)

        rows.append(break_row)

        timestamp_select_row = dbc.Row([
            dbc.Col([
                html.Div([
                    dbc.RadioItems(
                        id="dash-gauge-timestamp",
                        className="btn-group",
                        inputClassName="btn-check",
                        labelClassName="btn btn-outline-primary",
                        labelCheckedClassName="active",
                        options=[
                            {"label": "Hour", "value": self.ts.get_1h_timestamp()},
                            {"label": "Day", "value": self.ts.get_24h_timestamp()},
                            {"label": "Week", "value": self.ts.get_1week_timestamp()},
                        ],
                        value=self.ts.get_1h_timestamp(),
                    )
                ], className="radio-group"),
            ], width='auto')
        ], justify='center')
        rows.append(timestamp_select_row)

        row_one_gauges = dbc.Row(id='dash-row-one-gauges', justify='center')
        rows.append(row_one_gauges)
        row_two_gauges = dbc.Row(id='dash-row-two-gauges', justify='center')
        rows.append(row_two_gauges)

        rows.append(break_row)

        environment_graph_title = dbc.Row([dbc.Col([html.H2('Environmental Graphs')], width='auto')], justify='center')
        rows.append(environment_graph_title)

        graph_options = ['Temperature', 'Humidity', 'Pressure', 'CO2', 'TVOC', 'Soil Moisture', 'Wind Speed',
                         'Wind Direction']
        graph_drop = dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    graph_options,
                    value=graph_options[0],
                    searchable=False,
                    clearable=False,
                    id='dash-graph-drop'
                )
            ], width='4')
        ], justify='center')
        rows.append(graph_drop)

        graph_div_row = dbc.Row([
            dbc.Col([
                html.Div(id='dash-graph-view')
            ], width='10', xl='10')
        ], justify='center')
        rows.append(graph_div_row)

        rows.append(break_row)

        environment_map_title = dbc.Row([dbc.Col([html.H2('Environment Map')], width='auto')], justify='center')
        rows.append(environment_map_title)

        map_options = ['Temperature', 'Humidity', 'Pressure', 'CO2', 'TVOC', 'Soil Moisture', 'Wind Speed'  ]
        map_drop = dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    map_options,
                    value=map_options[0],
                    searchable=False,
                    clearable=False,
                    id='dash-map-drop'
                )
            ], width='4')
        ], justify='center')
        rows.append(map_drop)

        map_div_row = dbc.Row([
            dbc.Col([
                html.Div(id='dash-map-view')
            ], width='10', xl='10')
        ], justify='center')
        rows.append(map_div_row)

        rows.append(break_row)
        return rows

    def get_layout(self):
        return html.Div(self.__get_rows())
