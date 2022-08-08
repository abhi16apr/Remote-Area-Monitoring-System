from dash import html


class Home:
    def get_layout(self):
        home_page_layout = html.Div([
            html.H1('Home Page')
        ],
            style={'display': 'flex', 'justifyContent': 'center'}
        )
        return home_page_layout