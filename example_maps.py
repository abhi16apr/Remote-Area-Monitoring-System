from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from source.website.map import Map


class ExampleMaps:
    def __init__(self):
        self.map = Map()

    def get_layout(self):
        layout = html.Div([
            html.Br(),
            self.map.get_all_nodes_map_div(),
            html.Br(),
        ])
        return layout
