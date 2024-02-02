from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from . import x_axis_dropdown
from . import y_axis_dropdown
from . import filter
from . import search_bar
from . import scatter_plot
from . import point_comparison
from . import cat_1_pcp
from . import cat_2_pcp
from . import cat_3_pcp
from . import cat_4_pcp

category_list = ["goals_per90", "assists_per90", "goals_pens_per90", "goals_assists_per90", "goals_assists_pens_per90",
                 "shots_per90", "gk_shots_on_target_against", "games_complete"]


def create_layout(app: Dash) -> dbc.Container:  # we get the information from the app what the title is etc.

    return dbc.Container(
        className="app-div",
        children=[
            dbc.Row([
                dbc.Col([
                    html.H1(app.title, style={'textAlign': 'center'}),
                    html.Hr(),
                ], width=12)
            ]),
            dbc.Row([
                dbc.Col(
                    [
                        html.Div(
                            html.H5("Point comparison control"),
                            style={'position': 'relative', 'top': '180px'}
                        ),                         
                        html.Div(
                            dbc.Checkbox(id="lock-teams", label="Lock teams"),
                            style={'marginTop': '100%'}
                        ),
                        html.Div(
                            dbc.Button("Clear teams", id="clear-teams", color="primary"),
                        ),
                    ],
                    width=2
                ),
                dbc.Col([
                    html.Div(
                        className="point-comparison",
                        children=[point_comparison.render(app)],
                        style={"vertical-align": 'top'}
                    ) # Point comparison component
                ], width=10)
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(
                        html.H5("Scatter plot features selection"),
                    ),    
                    html.Div(
                        className="x-dropdown",
                        children=[x_axis_dropdown.render(app)],
                    ),
                    html.Div(
                        className="y-dropdown",
                        children=[y_axis_dropdown.render(app)],
                    ),
                    html.Div(
                        className="filter",
                        children=[filter.render(app)],
                    ),
                    html.Div(
                        className="search-bar",
                        children=[search_bar.render(app)],
                    ),
                    html.Div(
                        html.H5("Relation selection"),
                        style={'marginTop': '15%'}
                    ),
                    html.Div(
                        dbc.Checkbox(id="clear-scatter", label="show PCP -> Scatter"),

                    ),
                    html.Div(
                        dbc.Checkbox(id="clear-pcp", label="show Scatter -> PCP"),
                        
                    ),], width=2, style={'marginTop': '3%'}),

                dbc.Col([
                    html.Div(
                        className="scatter-plot",
                        children=[scatter_plot.render(app)],
                        style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'}
                    )
                ], width=10, style={'position': 'relative', 'top': '5px'}),
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(
                        html.H5("PCP attributes selection"),
                        style={'position': 'relative', 'top': '30px'},
                    ),                    
                    html.Div(
                        className="cat-1-pcp",
                        children=[cat_1_pcp.render(app)],
                        style={'marginTop': '3.5rem'},
                    ),
                    html.Div(
                        className="cat-2-pcp",
                        children=[cat_2_pcp.render(app)],
                        style={'marginTop': '1rem'},                       
                    ),
                    html.Div(
                        className="cat-3-pcp",
                        children=[cat_3_pcp.render(app)],
                        style={'marginTop': '1rem'},
                    ),
                    html.Div(
                        className="cat-4-pcp",
                        children=[cat_4_pcp.render(app)],
                        style={'marginTop': '1rem'},
                    ),
                ], width=2),
                dbc.Col([
                    html.Div([
                        dcc.Graph(id="pcp")
                    ])
                ], width=10)
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(id='dummy-output'),
                ])
            ])
        ]
    )
