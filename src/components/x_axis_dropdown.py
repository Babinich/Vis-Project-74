from dash import Dash, html, dcc
from dash.dependencies import Input, Output

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






    # all_nations = ["South Korea", "China", "Canada"]

    # @app.callback(
    #     Output(ids.NATION_DROPDOWN, "value" ),
    #     Input(ids.SELECT_ALL_NATIONS_BUTTON, "n_clicks")
    # )

    # def select_all_nations(_: int) -> list[str]:
    #     return all_nations


    # return html.Div(
    #     children=[
    #         html.H6("Nation"),
    #         dcc.Dropdown(
    #             id=ids.NATION_DROPDOWN,
    #             options=[{"label": nation, "value": nation} for nation in all_nations],
    #             value=all_nations,
    #             multi=True, 
    #         ),
    #         html.Button(
    #             className="dropdown-button",
    #             children=["Select All"],
    #             id=ids.SELECT_ALL_NATIONS_BUTTON,
    #         ),
    #     ]
    # )