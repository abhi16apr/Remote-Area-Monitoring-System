import dash_bootstrap_components as dbc
from dash import html, dcc
from source.util.settings import Settings
from source.util.database import Database
from source.util.timekeeper import Timestamps


class NodeList:
    def __init__(self):
        self.ts = Timestamps()
        self.config = Settings('general.config')
        self.connected_nodes_config = Settings('nodes.config')
        self.nodes_db = Database(self.config.get_setting('databases', 'nodes_db_path'))
        self.nodes_data = self.nodes_db.get_all()
        self.connected_nodes = self.connected_nodes_config.get_list_setting('connected_nodes', 'node_ids')
        self.connections_last_update = self.connected_nodes_config.get_float_setting('connected_nodes', 'last_updated')

    def __get_card_columns(self):
        columns = list()
        completed_nodes = list()
        # print(self.connected_nodes)
        for node in self.connected_nodes:
            node_info = next((record for record in self.nodes_data if record['node_id'] == node), None)
            # print(node)
            # print(node_info)
            if node_info is not None and node not in completed_nodes:
                card_content = [
                    dbc.CardHeader('Connected', style={'color': 'green'}),
                    dbc.CardBody(
                        [
                            html.H5(str(node), className='card-title'),
                            html.P('Updated: ' +
                                   self.ts.get_long_timestring(self.connections_last_update)),
                            dbc.CardLink('Node Details', href='/node_details-' + str(node))
                        ]
                    )
                ]
                columns.append(dbc.Col(dbc.Card(card_content, color='success', outline=True), width='auto'))
                completed_nodes.append(node)
        for node in self.connected_nodes:
            if node not in completed_nodes:
                card_content = [
                    dbc.CardHeader('Connected -> Not Configured'),
                    dbc.CardBody(
                        [
                            html.H5(str(node), className='card-title'),
                            html.P('Updated: ' +
                                   self.ts.get_long_timestring(self.connections_last_update)),
                            dbc.CardLink('Node Setup', href='/node_list')
                        ]
                    )
                ]
                columns.append(dbc.Col(dbc.Card(card_content, color='secondary', outline=True), width='auto'))
                completed_nodes.append(node)
        for record in self.nodes_data:
            if record['node_id'] not in completed_nodes:
                card_content = [
                    dbc.CardHeader('Disconnected', style={'color': 'red'}),
                    dbc.CardBody(
                        [
                            html.H5(str(record['node_id']), className='card-title'),
                            html.P('Updated: ' +
                                   self.ts.get_long_timestring(self.connections_last_update)),
                            dbc.CardLink('Node Details', href='/node_details-' + str(record['node_id']))
                        ]
                    )
                ]
                columns.append(dbc.Col(dbc.Card(card_content, color='danger', outline=True), width='auto'))
                completed_nodes.append(record['node_id'])
        return columns

    def __get_rows(self):
        rows = list()
        rows.append(html.Br())
        single_row = list()
        columns = self.__get_card_columns()
        # return dbc.Row(columns, justify='center', className="mb-4")
        # print(columns)
        chunks = [columns[x:x + 3] for x in range(0, len(columns), 3)]
        for chunk in chunks:
            rows.append(dbc.Row(children=chunk, justify='center', className="mb-4"))
        return rows

    def get_layout(self):
        default_layout = html.Div([
            html.Br(),
            html.H1('Node Data Unavailable')
        ])
        if self.connected_nodes is None and len(self.nodes_data) < 1:
            return default_layout
        layout = html.Div(self.__get_rows())
        return layout
