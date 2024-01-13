from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
from . import x_axis_dropdown
from . import y_axis_dropdown
from . import filter
from . import search_bar
from . import scatter_plot
from . import layers

def create_layout(app: Dash) -> dbc.Container:
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
