import json

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
import dash_renderjson


class Manager:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('general.config')
        self.default_config = Settings('default_general.config')
        self.nodes_config = Settings('nodes.config')
        self.nodes_db = Database(self.config.get_setting('databases', 'nodes_db_path'))
        self.sensors_db = Database(self.config.get_setting('databases', 'sensor_data_db_path'))
        self.map = Map()

    def __get_mesh_settings_modal(self):
        modal = html.Div([
            dbc.Modal(
                [
                    dbc.ModalHeader(dbc.ModalTitle('Mesh Network Settings'), close_button=True),
                    dbc.ModalBody([
                        html.H5('General'),
                        html.Hr(className="my-2"),
                        dbc.Label('Sensor Polling Interval'),
                        dbc.InputGroup([
                            dbc.InputGroupText('Default: ' +
                                               self.default_config.get_setting('mesh_network',
                                                                               'sensor_polling_interval')),
                            dbc.Input(placeholder=self.config.get_int_setting('mesh_network',
                                                                              'sensor_polling_interval'),
                                      type='number', id='mesh-settings-sensor_polling_interval'),
                            dbc.InputGroupText('seconds'),
                        ], className="mb-3"),
                        html.Br(),

                        dbc.Label('Image Polling Interval'),
                        dbc.InputGroup([
                            dbc.InputGroupText('Default: ' +
                                               self.default_config.get_setting('mesh_network',
                                                                               'image_polling_interval')),
                            dbc.Input(placeholder=self.config.get_int_setting('mesh_network',
                                                                              'image_polling_interval'),
                                      type='number', id='mesh-settings-image_polling_interval'),
                            dbc.InputGroupText('seconds'),
                        ], className="mb-3"),
                        html.Br(),

                        dbc.Label('Image Retry Attempts'),
                        dbc.InputGroup([
                            dbc.InputGroupText('Default: ' +
                                               self.default_config.get_setting('mesh_network', 'image_retry')),
                            dbc.Input(placeholder=self.config.get_int_setting('mesh_network', 'image_retry'),
                                      type='number', id='mesh-settings-image_retry'),
                            dbc.InputGroupText('Attempts'),
                        ], className="mb-3"),
                        html.Br(),

                        dbc.Label('Image Retry Delay'),
                        dbc.InputGroup([
                            dbc.InputGroupText('Default: ' +
                                               self.default_config.get_setting('mesh_network', 'image_retry_delay')),
                            dbc.Input(placeholder=self.config.get_int_setting('mesh_network', 'image_retry_delay'),
                                      type='number', id='mesh-settings-image_retry_delay'),
                            dbc.InputGroupText('seconds'),
                        ], className="mb-3"),
                        html.Br(),

                        html.H5('Serial Com Port'),
                        html.Hr(className="my-2"),
                        dbc.Label('COM Port Address'),
                        dbc.InputGroup([
                            dbc.InputGroupText('Default: ' +
                                               self.default_config.get_setting('mesh_network', 'port')),
                            dbc.Input(placeholder=self.config.get_setting('mesh_network', 'port'),
                                      type='text', id='mesh-settings-port'),
                            dbc.InputGroupText('seconds'),
                        ], className="mb-3"),
                        html.Br(),

                        dbc.Label('Baud Rate'),
                        dbc.InputGroup([
                            dbc.InputGroupText('Default: ' +
                                               self.default_config.get_setting('mesh_network', 'baud_rate')),
                            dbc.Input(placeholder=self.config.get_int_setting('mesh_network', 'baud_rate'),
                                      type='number', id='mesh-settings-baud_rate'),
                            dbc.InputGroupText('seconds'),
                        ], className="mb-3"),
                        html.Br(),

                        html.H5('Communication Timeouts'),
                        html.Hr(className="my-2"),

                        dbc.Label('Connection Timeout'),
                        dbc.InputGroup([
                            dbc.InputGroupText('Default: ' +
                                               self.default_config.get_setting('mesh_network', 'connection_timeout')),
                            dbc.Input(placeholder=self.config.get_int_setting('mesh_network', 'connection_timeout'),
                                      type='number', id='mesh-settings-connection_timeout'),
                            dbc.InputGroupText('seconds'),
                        ], className="mb-3"),
                        html.Br(),

                        dbc.Label('Serial Timeout'),
                        dbc.InputGroup([
                            dbc.InputGroupText('Default: ' +
                                               self.default_config.get_setting('mesh_network', 'serial_timeout')),
                            dbc.Input(placeholder=self.config.get_int_setting('mesh_network', 'serial_timeout'),
                                      type='number', id='mesh-settings-serial_timeout'),
                            dbc.InputGroupText('seconds'),
                        ], className="mb-3"),
                        html.Br(),

                        dbc.Label('Receive Timeout'),
                        dbc.InputGroup([
                            dbc.InputGroupText('Default: ' +
                                               self.default_config.get_setting('mesh_network', 'receive_timeout')),
                            dbc.Input(placeholder=self.config.get_int_setting('mesh_network', 'receive_timeout'),
                                      type='number', id='mesh-settings-receive_timeout'),
                            dbc.InputGroupText('seconds'),
                        ], className="mb-3"),
                        html.Br(),

                        dbc.Label('Image Timeout'),
                        dbc.InputGroup([
                            dbc.InputGroupText('Default: ' +
                                               self.default_config.get_setting('mesh_network', 'image_timeout')),
                            dbc.Input(placeholder=self.config.get_int_setting('mesh_network', 'image_timeout'),
                                      type='number', id='mesh-settings-image_timeout'),
                            dbc.InputGroupText('seconds'),
                        ], className="mb-3"),
                        html.Br(),

                        html.H5('Aggregator Node Settings'),
                        html.Hr(className="my-2"),

                    ]),
                    dbc.ModalFooter([
                        dbc.Button('Save & Close', id='mesh-settings-save-close', className='ms-auto', n_clicks=0,
                                   color='success'),
                        dbc.Button('Close Without Saving', id='mesh-settings-close', className='ms-auto', n_clicks=0,
                                   color='danger'),
                    ])
                ],
                id='mesh-settings-modal',
                is_open=False,
                backdrop='static',
                size='lg',
                scrollable=True
            )

        ])
        return modal

    def __get_rows(self):
        rows = list()
        break_row = dbc.Row([dbc.Col([html.Br()], width='auto')], justify='center')
        rows.append(break_row)
        line_row = dbc.Row([dbc.Col([html.Hr(className="my-2")], width='auto')], justify='center')

        connected_nodes = self.nodes_config.get_list_setting('connected_nodes', 'node_ids')
        nodes = self.nodes_db.get_all()
        # TODO: Fix error when connected nodes is none
        # TODO: fix error in nodes list for same probelm
        if connected_nodes is not None and len(connected_nodes) > 0:
            num_nodes = len(connected_nodes)
            if num_nodes == 1:
                node_str = str(num_nodes) + ' Node Connected'
            else:
                node_str = str(num_nodes) + ' Nodes Connected'
            network_status = 'Online: ' + node_str
            status_color = '#00ff55'
        else:
            network_status = 'Offline'
            status_color = '#d40000'
        num_disconnected = 0
        for node in nodes:
            if node['node_id'] in connected_nodes:
                continue
            elif node['status'] == 'active':
                num_disconnected += 1
                network_status = 'Degraded'
                status_color = '#f59042'
        if 'Degraded' in network_status:
            if num_disconnected == 1:
                network_status += ': ' + str(num_disconnected) + ' Node Disconnected'
            elif num_disconnected > 1:
                network_status += ': ' + str(num_disconnected) + ' Nodes Disconnected'
        # network_polling = self.config.get_bool_setting('mesh_network', 'polling')
        # if network_polling is None:
        #     network_polling = False
        sensor_polling = self.config.get_bool_setting('mesh_network', 'sensor_polling')
        if sensor_polling is None:
            sensor_polling = False
        image_polling = self.config.get_bool_setting('mesh_network', 'image_polling')
        if image_polling is None:
            image_polling = False
        last_updated = self.ts.get_time_date_string(self.nodes_config.get_float_setting('connected_nodes',
                                                                                        'last_updated'))
        network_quick_controls = dbc.Row([
            dbc.Col([
                html.Div([
                    html.H5("Mesh Overview", className="display-3"),
                    html.Hr(className="my-2"),
                    html.P('Network Status'),
                    dbc.Row([
                        dbc.Col([
                            daq.Indicator(
                                label=network_status,
                                color=status_color,
                                size=30,
                            )
                        ], width='auto'),
                    ], justify='center'),
                    break_row,
                    dbc.Row([dbc.Col([html.P('Last Updated: ' + last_updated, style={'font-size': '14px'})],
                                     width='auto')], justify='center'),
                    html.Hr(className="my-2"),
                    html.P('Quick Controls'),
                    dbc.Row([
                        dbc.Col([
                            dbc.Switch(
                                id='network-sensor-polling-switch',
                                label='Sensor Polling',
                                value=sensor_polling,
                            )
                        ], width='auto'),
                        dbc.Col([
                            dbc.Switch(
                                id='network-image-polling-switch',
                                label='Image Polling',
                                value=image_polling,
                            )
                        ], width='auto')
                    ], justify='center'),
                    html.Hr(className="my-2"),
                    # html.P('Mesh Settings'),
                    dbc.Row([
                        dbc.Button('Edit Mesh Settings', id='mesh-open-settings-button', n_clicks=0),
                        self.__get_mesh_settings_modal()
                    ], justify='center')
                ], className="h-100 p-5 bg-light border rounded-3")
            ], width='auto')
        ], justify='center')
        rows.append(network_quick_controls)

        rows.append(break_row)
        rows.append(line_row)

        map_title = dbc.Row([dbc.Col([html.H2('Mesh Nodes Map')], width='auto')],
                        justify='center')
        rows.append(map_title)

        rows.append(break_row)

        network_map = dbc.Row([
            dbc.Col([
                Map().get_node_status_map()
            ], width='8', xl='6')
        ], justify='center')
        rows.append(network_map)

        rows.append(break_row)

        topology_title = dbc.Row([dbc.Col([html.H4('Network Topology')], width='auto')], justify='center')
        rows.append(topology_title)
        last_updated = self.ts.get_time_date_string(self.nodes_config.get_float_setting('connected_nodes',
                                                                                        'last_updated'))
        last_updated_row = dbc.Row([dbc.Col([html.P('Last Updated: ' + last_updated)], width='auto')], justify='center')
        rows.append(last_updated_row)

        topology = self.nodes_config.get_setting('connected_nodes', 'topology')
        if topology is None:
            topology_row = dbc.Row([dbc.Col([html.P('No Topology Data Available')], width='auto')], justify='center')
        else:
            topology = json.loads(topology)
            topology_row = dbc.Row([
                dbc.Col([
                    dash_renderjson.DashRenderjson(id='no-id-topology', data=topology, max_depth=-1, invert_theme=True)
                ], width='auto')
            ], justify='center')
        rows.append(topology_row)

        hidden_divs = dbc.Row([
            html.Div([], id='network-hidden-div-polling-switch'),
        ])
        rows.append(hidden_divs)
        return rows

    def get_layout(self):
        return html.Div(self.__get_rows())
