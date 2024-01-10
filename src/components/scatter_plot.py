from dash import Dash, html, dcc, Patch
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from plotly.graph_objs import Figure

from . import ids

TEAM_DATA = pd.read_csv('Data/team_data.csv', delimiter=',')
df = TEAM_DATA
last_clicked_point = []


# can be used to clear the last_clicked_point list
def reset_points():
    global last_clicked_point
    last_clicked_point.clear()


def render(app: Dash):
    @app.callback(
        Output(ids.SCATTER_PLOT, "figure"),
        [Input(ids.X_AXIS_DROPDOWN, "value"),
         Input(ids.Y_AXIS_DROPDOWN, "value"),
         Input(ids.FILTER, "value"),
         Input(ids.LAYERS, "value")]  # Adding layers input
    )
    def update_scatter_plot(x_axis: str, y_axis: str, filter: int, selected_statistic: str) -> Figure:

        df["group"] = pd.Categorical(df["group"])

        filters = ["team", "group", ("pld_round_of_16", "won_round_of_16", "Round of 16"),
                   ("pld_quarter_finals", "won_quarter_finals", "Quarter Finals"),
                   ("pld_semi_finals", "won_semi_finals", "Semi Finals"),
                   ("pld_third_place", "won_third_place", "Third Place"), ("pld_finals", "won_finals", "Finals")]

        order_of_categories = [
            {"group": ["group 1", "group 2", " group 3", "group 4", "group 5", "group 6", "group 7", "group 8"]}]

        # Applying the filter and existing scatter plot logic
        if filter == 1:
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], color=filters[filter],  hover_data=['team'],
                             labels={filters[filter]: "Groups"}, category_orders=order_of_categories[0])

        elif (filter > 1) and (filter <= 6):
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], color=filters[filter][0], symbol=filters[filter][1],
                             hover_data=['team'], labels={filters[filter][0]: filters[filter][2], filters[filter][1]: "Result" } )

        else:
            # Apply shading logic for selected statistic
            quartiles = pd.qcut(df[selected_statistic], 4, labels=False)
            colors = ['lightblue', 'blue', 'darkblue', 'navy']  # Shades of blue
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], hover_data=['team'],
                             color=quartiles.apply(lambda x: colors[x]))

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

    @app.callback(
        Output(ids.POINT_COMPARISON, 'figure'),
        [Input(ids.SCATTER_PLOT, 'clickData')]
    )
    def display_click_data(click_data):
        if click_data is None:
            return {}

        global last_clicked_point
        if len(last_clicked_point) == 0:
            last_clicked_point.append(click_data['points'][0])
            return {}
        elif len(last_clicked_point) == 1:
            point1 = last_clicked_point.pop()
            point2 = click_data['points'][0]
            last_clicked_point.append(point2)
            point1_detail = df[df['team'] == point1['customdata'][0]]
            point2_detail = df[df['team'] == point2['customdata'][0]]

            attributes = [col for col in df.columns if col != 'team']
            values1 = point1_detail[attributes].values[0]
            values2 = point2_detail[attributes].values[0]

            fig = px.bar(
                x=list(values1) + list(values2),
                y=attributes * 2,
                color=[point1['customdata'][0]] * len(attributes) + [point2['customdata'][0]] * len(attributes),
                labels={'x': 'Value', 'y': 'Attribute', 'color': 'Point'},
                orientation='h',
                title=f"Comparison between {point1['customdata'][0]} and {point2['customdata'][0]}",
                width=1000,
                height=500,
            )

            return fig

    return dcc.Graph(id=ids.SCATTER_PLOT)
