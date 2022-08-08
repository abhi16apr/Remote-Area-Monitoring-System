import json

from source.util.analysis import Analysis
from source.network.mesh import Mesh
from source.util.database import Database
from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq
from source.util.settings import Settings
from source.util.conversions import Convert
from source.website.map import Map
from source.util.image import Image
from source.util.timekeeper import Timestamps


class NodeDetails:
    def __init__(self, pathname: str):
        self.config = Settings('general.config')
        self.connected_nodes_config = Settings('nodes.config')
        self.ts = Timestamps()
        self.nodes_db = Database(self.config.get_setting('databases', 'nodes_db_path'))
        self.sensors_db = Database(self.config.get_setting('databases', 'sensor_data_db_path'))
        self.map = Map()
        self.image = Image()
        self.convert = Convert()
        self.node_id = self.__get_node_id(pathname)
        self.node_config = self.__get_node_config()
        self.sensor_data = self.__get_node_sensor_data()
        self.analysis = Analysis(self.sensor_data)
        self.analyzed_data = self.analysis.get_gauge_data()

    def __get_node_id(self, pathname: str):
        try:
            # example pathname: /node_details-123456789
            node_id = int(pathname.split('-')[1])
            return node_id
        except Exception as e:
            print(e)
            return None

    def __get_node_config(self):
        if self.node_id is None:
            return None
        data = self.nodes_db.get_data_single_field('node_id', self.node_id)
        if len(data) > 0:
            data = data[0]
        return data

    def __get_node_sensor_data(self, end_timestamp=None):
        if self.node_id is None:
            return None
        data = self.sensors_db.get_data_single_field('node_id', self.node_id, timestamp=end_timestamp)
        return data

    def __get_rows(self):
        rows = list()
        break_row = dbc.Row([dbc.Col([html.Br()], width='auto')], justify='center')
        rows.append(break_row)

        row_1 = dbc.Row([dbc.Col([html.H2('Environmental Data for ' + str(self.node_id))], width='auto')],
                        justify='center')
        rows.append(row_1)
        row_2 = dbc.Row([dbc.Col([html.P('Date Last Updated: ' + self.analysis.get_last_update_string())],
                                 width='auto')],
                        justify='center')
        rows.append(row_2)

        rows.append(break_row)

        current_data_title = dbc.Row([
            dbc.Col([
                html.H4('Current Environmental Data')
            ], width='auto')
        ], justify='center')
        rows.append(current_data_title)

        temperature_data = next(record for record in self.analyzed_data if record['name'] == 'air_temperature_C')
        temperature_data['current_value'] = self.convert.temperature(temperature_data['current_value'])

        if self.config.get_setting('units', 'unit') == 'imperial':
            maximum_temp = self.config.get_int_setting('units', 'max_temperature_f')
            minimum_temp = self.config.get_int_setting('units', 'min_temperature_f')
            units = '\xb0F'
        else:
            maximum_temp = self.config.get_int_setting('units', 'max_temperature_c')
            minimum_temp = self.config.get_int_setting('units', 'min_temperature_c')
            units = '\xb0C'

        humidity_data = next(record for record in self.analyzed_data if record['name'] == 'humidity')

        pressure_data = next(record for record in self.analyzed_data if record['name'] == 'air_pressure_Pa')
        pressure_mbar = self.convert.pressure_mbar(pressure_data['current_value'])
        max_mbar = self.config.get_int_setting('units', 'max_mbar')
        min_mbar = self.config.get_int_setting('units', 'min_mbar')

        soil_data = next(record for record in self.analyzed_data if record['name'] == 'soil_moisture_adc')
        soil_sat = self.convert.soil_moisture(soil_data['current_value'])

        row_3 = dbc.Row([
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='Temperature',
                        units=units,
                        value=temperature_data['current_value'],
                        max=maximum_temp,
                        min=minimum_temp,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        # scale={'start': 973, 'interval': 10, 'labelInterval': 1},
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='Pressure',
                        units='mbar',
                        value=pressure_mbar,
                        max=max_mbar,
                        min=min_mbar,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='Humidity',
                        units='%',
                        value=self.convert.humidity(humidity_data['current_value']),
                        max=100,
                        min=0,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color={'default': '#0d6dfd', "gradient": True, "ranges": {"red": [0, 20], "yellow": [20, 50],
                                                                                  "green": [50, 100]}},
                        label='Soil Moisture Saturation',
                        units='%',
                        value=soil_sat,
                        max=100,
                        min=0,
                    )
                ])
            ], width='auto')
        ], justify='center')

        rows.append(row_3)

        wind_speed_data = next(record for record in self.analyzed_data if record['name'] == 'wind_speed_mph')
        wind_speed = wind_speed_data['current_value']
        if self.config.get_setting('units', 'unit') == 'imperial':
            max_wind_speed = self.config.get_int_setting('units', 'max_wind_speed_mph')
            min_wind_speed = self.config.get_int_setting('units', 'min_wind_speed_mph')
            wind_speed_units = 'MPH'
        else:
            max_wind_speed = self.config.get_int_setting('units', 'max_wind_speed_ms')
            min_wind_speed = self.config.get_int_setting('units', 'min_wind_speed_ms')
            wind_speed_units = 'm/s'

        wind_direction_data = next(record for record in self.analyzed_data if record['name'] == 'wind_direction')
        wind_direction_string = str(round(wind_direction_data['current_value']))

        co2_data = next(record for record in self.analyzed_data if record['name'] == 'co2_ppm')
        co2 = co2_data['current_value']
        co2_unit = 'PPM'
        min_co2 = self.config.get_int_setting('units', 'min_co2')
        max_co2 = self.config.get_int_setting('units', 'max_co2')
        if co2 > max_co2:
            max_co2 = co2

        tvoc_data = next(record for record in self.analyzed_data if record['name'] == 'tvoc_ppb')
        tvoc = tvoc_data['current_value']
        tvoc_unit = 'PPB'
        min_tvoc = self.config.get_int_setting('units', 'min_tvoc')
        max_tvoc = self.config.get_int_setting('units', 'max_tvoc')
        if tvoc > max_tvoc:
            max_tvoc = tvoc

        row_4 = dbc.Row([
            dbc.Col([
                html.Div([
                    daq.LEDDisplay(
                        color='#0d6dfd',
                        label='Wind Direction Degrees',
                        value=wind_direction_string,
                        # size=64
                    )
                ])
            ], width='auto', align='center'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='Wind Speed',
                        units=wind_speed_units,
                        value=wind_speed,
                        max=max_wind_speed,
                        min=min_wind_speed,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        scale={'start': 0, 'interval': 100, 'labelInterval': 2},
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='CO2',
                        units=co2_unit,
                        value=co2,
                        max=max_co2,
                        min=min_co2,
                    )
                ])
            ], width='auto'),
            dbc.Col([
                html.Div([
                    daq.Gauge(
                        showCurrentValue=True,
                        color='#0d6dfd',
                        label='TVOC',
                        units=tvoc_unit,
                        value=tvoc,
                        max=max_tvoc,
                        min=min_tvoc,
                    )
                ])
            ], width='auto'),
        ], justify='center')

        rows.append(row_4)

        graphs = self.analysis.get_node_graphs_list()
        options = list()
        for graph in graphs:
            option = str(self.node_id) + ' -> ' + graph
            # option = {
            #     'label': graph,
            #     'value': str(self.node_id) + '-' + graph
            #     # 'value': json.dumps({'node_id': self.node_id, 'graph': graph}).encode('utf-8')
            # }
            options.append(option)

        graph_title_row = dbc.Row([
            dbc.Col([
                html.H4('Environmental Graphs')
            ], width='auto')
        ], justify='center')
        rows.append(graph_title_row)

        graph_drop = dbc.Row([
            dbc.Col([
                dcc.Dropdown(
                    options,
                    value=options[0],
                    searchable=True,
                    clearable=False,
                    id='node-detail-graph-drop'
                )
            ], width='4')
        ], justify='center')
        rows.append(graph_drop)

        graph_div_row = dbc.Row([
            dbc.Col([
                html.Div(id='node-detail-graph-view')
            ], width='10', xl='10')
        ], justify='center')
        rows.append(graph_div_row)

        rows.append(break_row)

        location_title_row = dbc.Row([
            dbc.Col([
                html.H3('Node Location')
            ], width='auto')
        ], justify='center')
        rows.append(location_title_row)

        location_info_row = dbc.Row([
            dbc.Col([
                html.P('Latitude: ' + str(self.node_config['lat']))
            ], width='auto'),
            dbc.Col([
                html.P('Longitude: ' + str(self.node_config['lon']))
            ], width='auto'),
        ], justify='center')
        rows.append(location_info_row)

        map_row = dbc.Row([
            dbc.Col([
                self.map.get_single_point_map_div(latitude=self.node_config['lat'], longitude=self.node_config['lon'],
                                                  zoom=15, style='stamen-terrain')
            ], width='8', xl='6'),
        ], justify='center')
        rows.append(map_row)

        spacer_row = dbc.Row([dbc.Col([html.Hr()], width='auto')], justify='center')

        if self.node_config['node_config']['camera']:
            rows.append(spacer_row)
            picture_heading_row = dbc.Row([dbc.Col([html.H3('Node Images')], width='auto')], justify='center')
            rows.append(picture_heading_row)

            options = self.image.get_image_list(self.node_id)
            if options is None or len(options) < 1:
                options = ['No Images Available']
            image_selection_row = dbc.Row([
                dbc.Col([
                    dcc.Dropdown(
                        options,
                        value=options[0],
                        searchable=True,
                        clearable=False,
                        id='node-detail-image-drop'
                    )
                ], width='4')
            ], justify='center')
            rows.append(image_selection_row)

            image_row = dbc.Row([
                dbc.Col([
                    html.Div(id='node-detail-image-view')
                ], width='auto')
            ], justify='center')
            rows.append(image_row)

        row_5 = dbc.Row([dbc.Col([html.Hr()], width='auto')], justify='center')
        rows.append(row_5)

        row_6 = dbc.Row([dbc.Col([html.H2('Node Health')], width='auto')], justify='center')
        rows.append(row_6)
        # rows.append(row_2)

        # TODO: give the user a way to edit node config
        connected_nodes = self.connected_nodes_config.get_list_setting('connected_nodes', 'node_ids')
        connection_last_updated = self.connected_nodes_config.get_float_setting('connected_nodes', 'last_updated')
        sensor_data_last_update = next(record for record in self.analyzed_data if record['name'] == 'timestamp')
        # print(sensor_data_last_update)
        if sensor_data_last_update['max_value'] > connection_last_updated:
            connection_last_updated = sensor_data_last_update['max_value']
        last_updated_string = self.ts.get_long_timestring(connection_last_updated)
        connection_status = 'Disconnected'
        connection_color = 'red'
        if connected_nodes is not None and len(connected_nodes) > 0:
            if self.node_id in connected_nodes:
                connection_status = 'Connected'
                connection_color = 'green'

        last_updated_row = dbc.Row([dbc.Col([html.P('Date Last Updated: ' + last_updated_string)],
                                 width='auto')],
                        justify='center')
        rows.append(last_updated_row)

        connection_status_row = dbc.Row([
            dbc.Col([
                html.H3('Network Status: ' + connection_status, style={'color': connection_color}),
                html.H3('Polling Status: ' + self.node_config['status'])
            ], width='auto')
        ], justify='center')
        rows.append(connection_status_row)

        break_row = dbc.Row([dbc.Col([html.Br()], width='auto')], justify='center')
        rows.append(break_row)

        voltage_data = next(record for record in self.analyzed_data if record['name'] == 'bus_voltage_V')
        voltage = voltage_data['current_value']
        volts_min = self.config.get_float_setting('units', 'volts_min')
        volts_max = self.config.get_float_setting('units', 'volts_max')
        if 2.8 < voltage < 4.3:
            volts_color = '#02b502'
        else:
            volts_color = '#ff4242'
        if voltage > volts_max:
            volts_max = voltage
        if voltage < volts_min:
            volts_min = voltage

        current_data = next(record for record in self.analyzed_data if record['name'] == 'current_mA')
        current = current_data['current_value']
        current_min = self.config.get_float_setting('units', 'current_min')
        current_max = self.config.get_float_setting('units', 'current_max')
        if current > 0:
            current_label = 'Battery Current -> Charging'
            current_color = '#02b502'
        else:
            current_label = 'Battery Current -> Discharging'
            current_color = '#ff4242'
        if current > current_max:
            current_max = current
        if current < current_min:
            current_min = current

        # power_data = next(record for record in self.analyzed_data if record['name'] == 'power_mW')
        power = voltage * abs(current)
        power = round(power / 1000, 3)
        power_color = {"gradient": True, "ranges": {"green": [0, 2.2], "yellow": [2.2, 2.8], "red": [2.8, 3]}}

        power_status_row = dbc.Row([
            dbc.Col([
                daq.Tank(
                    value=voltage,
                    units='Volts',
                    color=volts_color,
                    showCurrentValue=True,
                    max=volts_max,
                    min=volts_min,
                    label='Battery Voltage'
                )
            ], width='auto'),
            dbc.Col([
                daq.Gauge(
                    value=current,
                    units='milliamps',
                    color=current_color,
                    showCurrentValue=True,
                    max=current_max,
                    min=current_min,
                    label=current_label
                )
            ], width='auto'),
            dbc.Col([
                daq.Gauge(
                    value=power,
                    units='watts',
                    color=power_color,
                    showCurrentValue=True,
                    max=3,
                    min=0,
                    label='Power'
                )
            ], width='auto')
        ], justify='center')
        rows.append(power_status_row)

        rows.append(spacer_row)
        return rows

    def get_layout(self):
        default_layout = html.Div([
            html.Br(),
            html.H1('Node Data Unavailable')
        ])
        if self.node_id is None or self.sensor_data is None:
            return default_layout
        return html.Div(self.__get_rows())
