from dash import Dash, html, dcc

from . import ids


def render(app: Dash) -> html.Div:
    x_axis_col = ['goals_per90', 'assists_per90', 'goals_pens_per90',
                  'goals_assists_per90', 'goals_assists_pens_per90', 'shots_per90',
                  'shots_on_target_per90', 'xg_per90', 'xg_assist_per90', 'npxg_per90',
                  'xg_xg_assist_per90', 'npxg_xg_assist_per90',
                  'gk_shots_on_target_against', 'gk_save_pct', 'games_complete',
                  'gk_clean_sheets_pct']

    return html.Div(
        children=[
            html.Label("X axis"),
            dcc.Dropdown(
                id=ids.X_AXIS_DROPDOWN,
                options=[{"label": attribute, "value": attribute} for attribute in x_axis_col],
                value="goals_per90",
                multi=False,
                clearable=False

            ),
        ]
    )
