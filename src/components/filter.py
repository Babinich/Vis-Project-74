from dash import Dash, html, dcc
from dash.dependencies import Input, Output

from . import ids

def render(app: Dash) -> html.Div:

    filters = ["teams", "group_stage", "round_of_16", "quarter_finals", "semi_finals", "third_place", "finals"] 

    return html.Div(
        children=[
            html.Label("Filters"),
            dcc.Dropdown(
                id=ids.FILTER,
                options=[{"label": "teams", "value": 0},
                         {"label": "group_stage", "value": 1},
                         {"label": "round_of_16ms", "value": 2},
                         {"label": "quarter_finals", "value": 3},
                         {"label": "semi_finals", "value": 4},
                         {"label": "third_place", "value": 5},
                         {"label": "finals", "value": 6},
                         ],
                value=0,
                multi=False, 
                clearable=False

            ),
        ]
    )
