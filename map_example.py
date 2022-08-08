from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc


class MapExample:
    def get_layout(self):
        layout = html.Div([
            html.Br(),
            self.__get_map_view(),
            html.Br(),
            self.__get_input_with_label('Latitude', 'map-example-lat', '28.602374', type='number', value='28.602374',
                                        debounce=True),
            html.Br(),
            self.__get_input_with_label('Longitude', 'map-example-lon', '-81.200164', type='number', value='-81.200164',
                                        debounce=True),
            html.Br(),
            self.__get_input_with_label('Point Size', 'map-example-size', '10', type='number', value='10',
                                        debounce=True),
            html.Br(),
            self.__get_input_with_label('Zoom', 'map-example-zoom', '8', type='number', value='8',
                                        debounce=True),
            html.Br(),
            self.__get_button(),
            html.Br(),

            ],
        )
        return layout

    def __get_map_view(self):
        map_view = html.Div([
            html.Div(id='map-example-view')
            ],
            style={'display': 'flex', 'justifyContent': 'center'}
        )
        return map_view

    def __get_input_with_label(self, label: str, input_id: str, placeholder: str, value: str = '', type: str = 'text',
                               debounce=False, width: str = '400px'):
        labeled_input = html.Div([dbc.FormFloating(
                [
                    dbc.Input(id=input_id, type=type, placeholder=placeholder, debounce=debounce, value=value,
                              style={'width': width}),
                    dbc.Label(label),
                ]
            )],
            style={'display': 'flex', 'justifyContent': 'center'}
        )
        return labeled_input

    def __get_button(self):
        submit_button = html.Div([
            html.Button('Map It!', type='submit', id='map-example-button')
            ],
            style={'display': 'flex', 'justifyContent': 'center'}
        )
        return submit_button
