from dash import dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc
from app import app
from map import Map
from subprocess import check_output
import socket
from flask import request
from source.util.database import Database
from source.network.mesh import Mesh
from source.util.settings import Settings
from source.util.image import Image
from source.website.graph import Graph
from source.util.timekeeper import Timestamps
from source.website.gauges import Gauges
from source.website.pages import home, map_example, node_table, updater, example_maps, image_example, node_details, \
    node_list, dashboard, mesh_manager

config = Settings('general.config')
nodes_config = Settings('nodes.config')
nodes_db = Database(config.get_setting('databases', 'nodes_db_path'))
sensors_db = Database(config.get_setting('databases', 'sensor_data_db_path'))
mesh = Mesh()


# navbar = dbc.NavbarSimple(
#     children=[
#         dbc.NavItem(dbc.NavLink("Home Page", href="/home")),
#         dbc.NavItem(dbc.NavLink("Node List", href="/node-list")),
#         dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard")),
#         dbc.NavItem(dbc.NavLink("Network", href="/mesh-manager")),
#         dbc.DropdownMenu(
#             children=[
#                 dbc.DropdownMenuItem("Dev Tools", header=True),
#                 dbc.DropdownMenuItem("Map Test", href="/map-example"),
#                 dbc.DropdownMenuItem("Nodes List Table", href="/nodes-table"),
#                 dbc.DropdownMenuItem("Example Maps", href="/example-maps"),
#                 dbc.DropdownMenuItem("Example Image", href="/example-image"),
#                 dbc.DropdownMenuItem("Example Node Detail", href="/node_details-4144723677"),
#             ],
#             nav=True,
#             in_navbar=True,
#             label="Developer",
#         ),
#         dbc.NavItem(dbc.NavLink("Login", href="/login")),
#     ],
#     brand="Remote Area Monitoring",
#     brand_href="/home",
#     color="primary",
#     dark=True,
# )

nav_items = dbc.Row([
    dbc.Col([dbc.NavItem(dbc.NavLink("Dashboard", href="/dashboard"))], width='auto'),
    dbc.Col([dbc.NavItem(dbc.NavLink("Node List", href="/node-list"))], width='auto'),
    dbc.Col([dbc.NavItem(dbc.NavLink("Network", href="/mesh-manager"))], width='auto'),
    dbc.Col([
        dbc.DropdownMenu(
                children=[
                    dbc.DropdownMenuItem("Dev Tools", header=True),
                    dbc.DropdownMenuItem("Map Test", href="/map-example"),
                    dbc.DropdownMenuItem("Nodes List Table", href="/nodes-table"),
                    dbc.DropdownMenuItem("Example Maps", href="/example-maps"),
                    dbc.DropdownMenuItem("Example Image", href="/example-image"),
                    dbc.DropdownMenuItem("Example Node Detail", href="/node_details-4144723677"),
                ],
                nav=True,
                in_navbar=True,
                label="Developer",
            )
        ], width='auto')
    ],
    className="g-0 ms-auto flex-nowrap mt-3 mt-md-0",
    align="center",
)

navbar = dbc.Navbar(
    dbc.Container(
        [
            html.A(
                # Use row and col to control vertical alignment of logo / brand
                dbc.Row(
                    [
                        dbc.Col(html.Img(src='/assets/logo_no_background.png', height="50px")),
                        dbc.Col(dbc.NavbarBrand("Remote Area Monitoring", className="ms-2")),
                    ],
                    align="center",
                    className="ml-auto",
                ),
                href="/dashboard",
                style={"textDecoration": "none"},
            ),
            dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
            dbc.Collapse(
                nav_items,
                id="navbar-collapse",
                is_open=False,
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    className="ml-auto",
    sticky='top'
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


@app.callback(
    Output("navbar-collapse", "is_open"),
    [Input("navbar-toggler", "n_clicks")],
    [State("navbar-collapse", "is_open")],
)
def toggle_navbar_collapse(n, is_open):
    if n:
        return not is_open
    return is_open


@app.callback(Output('map-example-view', 'children'),
              Input('map-example-button', 'n_clicks'),
              State('map-example-lat', 'value'),
              State('map-example-lon', 'value'),
              State('map-example-size', 'value'),
              State('map-example-zoom', 'value'))
def update_example_map(n_clicks, lat, lon, size, zoom):
    try:
        lat = float(lat)
        lon = float(lon)
        size = float(size)
        zoom = int(zoom)
    except TypeError:
        print('map example type exception')
        lat = 28.602374
        lon = -81.200164
        size = 8.0
        zoom = 8
    return Map().get_single_point_map_div(lat, lon, size=size, zoom=zoom)


@app.callback(Output('node-detail-image-view', 'children'),
              Input('node-detail-image-drop', 'value'))
def update_node_detail_image(value):
    print(value)
    return Image().get_image_div_with_timestring(value)


@app.callback(Output('node-detail-graph-view', 'children'),
              Input('node-detail-graph-drop', 'value'))
def update_node_detail_image(value):
    print(value)
    return Graph().get_single_select_graph(value)


@app.callback([Output('dash-row-one-gauges', 'children'),
               Output('dash-row-two-gauges', 'children')],
              [Input('dash-gauge-timeframe', 'value'),
               Input('dash-gauge-timestamp', 'value')])
def update_dashboard_gauges(timeframe, timestamp):
    return Gauges().get_dashboard_gauges(timeframe, timestamp)


@app.callback(Output('dash-graph-view', 'children'),
              Input('dash-graph-drop', 'value'))
def update_dashboard_graph(value):
    return Graph().get_all_select_graph(value)


@app.callback(Output('dash-map-view', 'children'),
              Input('dash-map-drop', 'value'))
def update_dashboard_graph(value):
    return Map().get_animated_heatmap(value)


@app.callback(Output('network-hidden-div-polling-switch', 'children'),
              [Input('network-sensor-polling-switch', 'value'),
               Input('network-image-polling-switch', 'value')])
def update_network_polling(sensor_polling, image_polling):
    config.set_setting('mesh_network', 'sensor_polling', str(sensor_polling))
    config.set_setting('mesh_network', 'image_polling', str(image_polling))


@app.callback(Output('mesh-settings-modal', 'is_open'),
              [
                Input('mesh-open-settings-button', 'n_clicks'),
                Input('mesh-settings-close', 'n_clicks'),
                Input('mesh-settings-save-close', 'n_clicks')
              ],
              State('mesh-settings-modal', 'is_open'))
def update_mesh_settings_modal_state(open_clicks, close_clicks, close_save_clicks, modal_state):
    changed_id = [p['prop_id'] for p in callback_context.triggered][0]
    if 'mesh-settings-save-close' in changed_id:
        print('Save and Close Clicked')
        return not modal_state
    elif 'mesh-open-settings-button' in changed_id:
        print('Open Button Clicked')
        return not modal_state
    elif 'mesh-settings-close' in changed_id:
        print('Close Button Clicked')
        return not modal_state
    return modal_state


# Navigate pages
@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/map-example':
        return map_example.MapExample().get_layout()
    elif pathname == '/nodes-table':
        return node_table.NodeTable(mesh).get_layout()
    elif 'update' in pathname:
        return updater.Updater(mesh).get_layout()
    elif pathname == '/example-maps':
        return example_maps.ExampleMaps().get_layout()
    elif pathname == '/example-image':
        return image_example.ImageExample().get_layout()
    elif 'node_details' in pathname:
        return node_details.NodeDetails(pathname).get_layout()
    elif pathname == '/node-list':
        return node_list.NodeList().get_layout()
    elif pathname == '/dashboard':
        return dashboard.Dashboard().get_layout()
    elif pathname == '/mesh-manager':
        return mesh_manager.Manager().get_layout()
    else:
        return dashboard.Dashboard().get_layout()


if __name__ == '__main__':
    try:
        ip_address = socket.gethostbyname(socket.gethostname())
    except:
        ip_address = check_output(["hostname", "-I"]).decode("utf-8").split(" ")[0]
    print("IP Address: ", ip_address)
    port = 8050
    print("Port: ", port)
    config.set_setting('website', 'ip_address', str(ip_address))
    config.set_setting('website', 'port', str(port))
    app.run_server(debug=False, host=ip_address, port=port)
