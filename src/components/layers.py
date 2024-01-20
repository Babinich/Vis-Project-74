from dash import Dash, html, dcc
from dash.dependencies import Input, Output
from . import ids

def render(app: Dash) -> html.Div:
    # Specific columns for shading
    statistics = [
        "possession", "passes_pct", "dribbles_completed_pct", 
        "tackles_won", "fouled", "avg_age", "cards_yellow"
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
            
        ]
    )
