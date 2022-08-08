import source.network.node_manager
import source.util.database
import plotly.graph_objects as go
import pandas as pd
from dash import html, dcc
from source.util.settings import Settings
from source.util.database import Database


class NodeTable:
    def __init__(self, mesh: source.network.mesh.Mesh):
        self.config = Settings('general.config')
        self.db = Database(self.config.get_setting('databases', 'nodes_db_path'))
        self.mesh = mesh

    def get_layout(self):
        layout = html.Div([
            html.Br(),
            self.__get_table()
        ])
        return layout

    def __get_node_data(self):
        connected_nodes = self.mesh.list_connected_nodes()
        nodes = self.db.get_all()
        print(nodes)
        print(connected_nodes)
        for node in nodes:
            if node['node_id'] in connected_nodes:
                node['connection_status'] = 'Connected'
                connected_nodes.remove(node['node_id'])
            else:
                node['connection_status'] = 'Disconnected'
        if nodes is not None and len(nodes) > 0:
            keys = nodes[0].keys()
        else:
            keys = ['node_id', 'status', 'connection_status']
        for node in connected_nodes:
            node_data = dict()
            for key in keys:
                node_data[key] = '-'
            node_data['node_id'] = node
            node_data['status'] = 'Not Configured'
            node_data['connection_status'] = 'Connected'
            nodes.append(node_data)
        return nodes

    def __get_table(self):
        table_data = self.__get_node_data()
        table_data = pd.DataFrame(table_data)
        print(table_data)
        fig = go.Figure(data=[go.Table(
            header=dict(values=list(table_data.columns),
                        align='left'),
            cells=dict(values=[table_data[col] for col in table_data.columns],
                       align='left')
        )])
        div = html.Div([
            dcc.Graph(figure=fig)
        ])
        return div

