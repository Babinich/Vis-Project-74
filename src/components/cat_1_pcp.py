from dash import Dash, html, dcc

from . import ids


def render(app: Dash) -> html.Div:

    category_list = ["goals_per90", "assists_per90",  "goals_pens_per90", "goals_assists_per90", "goals_assists_pens_per90",
                     "shots_per90", "gk_shots_on_target_against", "games_complete",   "possession", "passes_pct",
                     "dribbles_completed_pct", "tackles_won", "fouled", "avg_age", "cards_yellow" ]

    return html.Div(
        children=[
            html.Label("PCP 1st category"),
            dcc.Dropdown(
                id=ids.CATEGORY_DROPDOWN_1,
                options=category_list,
                value=category_list[0],
                multi=False,
                placeholder="Select category 1",     
            ),
        ]
    )