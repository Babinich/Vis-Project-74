from dash import Dash, html, dcc, Patch
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from plotly.graph_objs import Figure

from . import ids

TEAM_DATA = pd.read_csv('Data/team_data.csv', delimiter=',')
df = TEAM_DATA


def render(app: Dash):
    @app.callback(
        Output(ids.SCATTER_PLOT, "figure"),
        Input(ids.X_AXIS_DROPDOWN, "value"),
        Input(ids.Y_AXIS_DROPDOWN, "value"),
        Input(ids.FILTER, "value")
    )
    def update_scatter_plot(x_axis: str, y_axis: str, filter: int) -> Figure:

        df["group"] = pd.Categorical(df["group"])

        filters = ["team", "group", ("pld_round_of_16", "won_round_of_16", "Round of 16"),
                   ("pld_quarter_finals", "won_quarter_finals", "Quarter Finals"),
                   ("pld_semi_finals", "won_semi_finals", "Semi Finals"),
                   ("pld_third_place", "won_third_place", "Third Place"), ("pld_finals", "won_finals", "Finals")]

        order_of_categories = [
            {"group": ["group 1", "group 2", " group 3", "group 4", "group 5", "group 6", "group 7", "group 8"]}]

        # print((x_axis, y_axis, filter))
        if filter == 1:
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], color=filters[filter],  hover_data=['team'], 
                             labels={filters[filter]: "Groups"}, category_orders = order_of_categories[0])

        elif (filter > 1) and (filter <= 6):
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], color=filters[filter][0], symbol=filters[filter][1], 
                             hover_data=['team'], labels={filters[filter][0]: filters[filter][2], filters[filter][1]: "Result" } )
        
        else:
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], hover_data=['team'])

        return fig

    @app.callback(
        Output(ids.SCATTER_PLOT, "figure", allow_duplicate=True),
        Input(ids.SEARCH_BAR, "value"),
        prevent_initial_call=True
    )
    def update_markers(teams):
        teams_count = list(df[df.team.isin(teams)].index)
        patched_figure = Patch()
        updated_markers = [
            "black" if i in teams_count else "blue" for i in range(len(df) + 1)
        ]
        patched_figure['data'][0]['marker']['color'] = updated_markers
        return patched_figure

    return dcc.Graph(id=ids.SCATTER_PLOT)
