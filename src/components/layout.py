from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from . import x_axis_dropdown
from . import y_axis_dropdown
from . import filter
from . import search_bar
from . import scatter_plot
from . import layers





category_list = ["goals_per90", "assists_per90",  "goals_pens_per90", "goals_assists_per90", "goals_assists_pens_per90",
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
                dbc.Col([
                    html.Div(
                        className="x-dropdown",
                        children=[x_axis_dropdown.render(app)],
                        style={'width': '70%'},
                    ),
                    html.Div(
                        className="y-dropdown",
                        children=[y_axis_dropdown.render(app)],
                        style={'width': '70%'},
                    ),
                    html.Div(
                        className="filter",
                        children=[filter.render(app)],
                        style={'width': '70%'},
                    ),
                    html.Div(
                        className="search-bar",
                        children=[search_bar.render(app)],
                        style={'width': '70%'},
                    ),
                    html.Div(  # Adding the layers dropdown
                        className="layers",
                        children=[layers.render(app)],
                        style={'width': '70%'},
                    ),
                    html.Div(id='color-bar', style={'height': '50px', 'marginTop': '20px'}),  # Color bar
                ], width=2, style={'marginTop': '3%'}),

                dbc.Col([
                    html.Div(
                        className="scatter-plot",
                        children=[scatter_plot.render(app)],
                        style={'width': '100%', 'display': 'inline-block', 'vertical-align': 'top'}
                    )
                ], width=8),

                dbc.Col([
                    html.Div([dcc.Graph(id="point-comparison")])  # Point comparison component
                ], width=2)
            ]),
            dbc.Row([
                dbc.Col([
                    html.Div(
                        dcc.Dropdown(
                            id='cat-1',
                            options=category_list,
                            value=category_list[0],
                            multi=False,
                            placeholder="Select category 1",
                            style={'marginTop': '3.5rem'},
                        ),
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id='cat-2',
                            options=category_list,
                            value=category_list[1],
                            multi=False,
                            placeholder="Select category 2",
                            style={'marginTop': '1rem'},
                        ),
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id='cat-3',
                            options=category_list,
                            multi=False,
                            placeholder="Select category 3",
                            style={'marginTop': '1rem'},
                        ),
                    ),
                    html.Div(
                        dcc.Dropdown(
                            id='cat-4',
                            options=category_list,
                            multi=False,
                            placeholder="Select category 4",
                            style={'marginTop': '1rem'},
                        ),
                    ),
                ], width=2, style={'marginTop': '3%'}),
                dbc.Col([
                    html.Div([
                        dcc.Graph(id="second-view")
                    ])
                ], width=10)
            ])
        ]
    )


# html.Div(
#             className="scatter-plot",
#             children=[scatter_plot.render(app)],
#             style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '20px'}


#     className="app-div",
#     children=[
#         html.H1(app.title),
#         html.Hr(),
#         html.Div(
#             className="left-bar-dropdowns",
#             children=[
#                 html.Div(
#                     className="x-dropdown",
#                     children=[x_axis_dropdown.render(app)],
#                     style={'display': 'inline-block', 'width': '10%'},
#                 ),
#                 html.Div(
#                     className="y-dropdown",
#                     children=[y_axis_dropdown.render(app)],
#                     style={'display': 'inline-block', 'width': '10%', 'margin-left': '10px'}
#                 ),
#                 html.Div(
#                     className="filter",
#                     children=[filter.render(app)],
#                     style={'width': '10%'}
#                 ),
#                 html.Div(
#                     className="search-bar",
#                     children=[search_bar.render(app)],
#                     style={'width': '10%'}
#                 ),

#             ]
#         ),
#         html.Div(
#             className="scatter-plot",
#             children=[scatter_plot.render(app)],
#             style={'width': '30%', 'display': 'inline-block', 'vertical-align': 'top', 'margin-left': '20px'}
#         )
#     ]
# )
