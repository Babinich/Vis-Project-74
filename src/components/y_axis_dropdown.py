from dash import Dash, html, dcc
from dash.dependencies import Input, Output

from . import ids

def render(app: Dash) -> html.Div:

    y_axis_col = ["assists_per90","shots_on_target_per90","xg_per90", "xg_assist_per90", "npxg_per90", "xg_xg_assist_per90", 
                  "npxg_xg_assist_per90", "gk_save_pct", "gk_clean_sheets_pct"] 

    return html.Div(
        children=[
            html.Label("Y axis"),
            dcc.Dropdown(
                id=ids.Y_AXIS_DROPDOWN,
                options=[{"label": attribute, "value": attribute} for attribute in y_axis_col],
                value="assists_per90",
                multi=False, 
                clearable=False,
            ),
        ]
    )