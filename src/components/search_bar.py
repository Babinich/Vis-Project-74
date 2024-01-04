from dash import Dash, html, dcc
from dash.dependencies import Input, Output

from . import ids

def render(app: Dash) -> html.Div:

    teams = ['Argentina', 'Australia', 'Belgium', 'Brazil', 'Cameroon', 'Canada', 'Costa Rica', 'Croatia', 
             'Denmark', 'Ecuador', 'England', 'France', 'Germany', 'Ghana', 'Iran', 'Japan', 'Korea Republic', 
             'Mexico', 'Morocco', 'Netherlands', 'Poland', 'Portugal', 'Qatar', 'Saudi Arabia', 'Senegal', 'Serbia',
             'Spain', 'Switzerland', 'Tunisia', 'United States', 'Uruguay', 'Wales']
 
    return html.Div(
        children=[
            html.Label("Search bar"),
            dcc.Dropdown(
                id=ids.SEARCH_BAR,
                options=[{"label": attribute, "value": attribute} for attribute in teams],
                multi=True, 
            ),
        ]
    )