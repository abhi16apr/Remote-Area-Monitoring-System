from dash import Dash, dcc, html, Input, Output, State
import dash_bootstrap_components as dbc
from source.util.image import Image
from source.util.settings import Settings
from source.util.database import Database


class ImageExample:
    def __init__(self):
        self.nodes_db = Database(Settings('general.config').get_setting('databases', 'nodes_db_path'))
        self.img = Image()

    def get_layout(self):
        nodes = self.nodes_db.get_all()
        divs = [html.Br()]
        for node in nodes:
            div = self.img.get_test_image_div(node['node_id'])
            if div is None:
                continue
            divs.extend(div)
            divs.append(html.Br())
        divs.append(html.Br())
        layout = html.Div(divs)
        return layout
