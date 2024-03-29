from dash import Dash, html, dcc

from . import ids


def render(app: Dash) -> html.Div:

    category_list = ["goals_per90", "assists_per90",  "goals_pens_per90", "goals_assists_per90", "goals_assists_pens_per90",
                     "shots_per90", "gk_shots_on_target_against", "games_complete",   "possession", "passes_pct",
                     "dribbles_completed_pct", "tackles_won", "fouled", "avg_age", "cards_yellow" ]
    
    return html.Div(
        children=[
            html.Label("PCP 4th category"),
            dcc.Dropdown(
                id=ids.CATEGORY_DROPDOWN_4,
                options=category_list,
                value=category_list[3],
                multi=False,
                placeholder="Select category 4",    
            ),
        ]
    )