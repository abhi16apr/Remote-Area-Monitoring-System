from source.network.mesh import Mesh
from dash import html


class Updater:
    def __init__(self, mesh: Mesh):
        self.mesh = mesh
        self.mesh.update_nodes_sensor_data()
        self.mesh.update_nodes_image_data()

    def get_layout(self):
        layout = html.Div([
            html.Br(),
            html.H1('Mesh Network Query...', id='update-complete')
        ])
        return layout
