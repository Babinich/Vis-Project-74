from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids

def render(app: Dash) -> html.Div:
    # List of numerical statistics for shading
    statistics = [
        "goals_per90", "assists_per90", "goals_pens_per90", "goals_assists_per90",
        "goals_assists_pens_per90", "shots_per90", "shots_on_target_per90", "xg_per90",
        "xg_assist_per90", "npxg_per90", "xg_xg_assist_per90", "npxg_xg_assist_per90",
        "gk_shots_on_target_against", "gk_save_pct", "games_complete", "gk_clean_sheets_pct",
        "possession", "passes_pct", "average_shot_distance", "dribbles_completed_pct",
        "tackles_won", "fouled", "avg_age", "cards_yellow", "cards_red", "cards_yellow_red"
    ]

    return html.Div(
        children=[
            html.Label("Layers"),
            dcc.Dropdown(
                id=ids.LAYERS,
                options=[{"label": stat, "value": stat} for stat in statistics],
                value=statistics[0],  # Default value
                multi=False,
                clearable=False
            ),
            # Add a color legend or bar here if needed
        ]
    )
