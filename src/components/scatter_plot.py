from dash import Dash, html, dcc, Patch
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots
import plotly.graph_objs as go

from . import ids

TEAM_DATA = pd.read_csv('Data/team_data.csv', delimiter=',')
df = TEAM_DATA
last_clicked_point = []
filters = ["team", "group", ("pld_round_of_16", "won_round_of_16", "Round of 16"),
           ("pld_quarter_finals", "won_quarter_finals", "Quarter Finals"),
           ("pld_semi_finals", "won_semi_finals", "Semi Finals"),
           ("pld_third_place", "won_third_place", "Third Place"), ("pld_finals", "won_finals", "Finals")]


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

        order_of_categories = [
            {"group": ["group 1", "group 2", " group 3", "group 4", "group 5", "group 6", "group 7", "group 8"]}]

        # Applying the filter and existing scatter plot logic
        if filter == 1:
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], color=filters[filter], hover_data=['team'],
                             labels={filters[filter]: "Groups"}, category_orders=order_of_categories[0])

        elif (filter > 1) and (filter <= 6):
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], color=filters[filter][0], symbol=filters[filter][1],
                             hover_data=['team'],
                             labels={filters[filter][0]: filters[filter][2], filters[filter][1]: "Result"})

        else:
            # Apply shading logic for selected statistic
            quartiles = pd.qcut(df[selected_statistic], 4, labels=False)
            colors = ['lightblue', 'blue', 'darkblue', 'navy']  # Shades of blue
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], hover_data=['team'],
                             color=quartiles.apply(lambda x: colors[x]))

        fig.update_layout(
            height=600,
            width=600,
        )
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
        Output('second-view', 'figure'),
        [Input('cat-1', 'value'),
         Input('cat-2', 'value'),
         Input('cat-3', 'value'),
         Input('cat-4', 'value'),
         Input(ids.FILTER, "value")],
    )
    def update_second_view(selected_value_1, selected_value_2, selected_value_3, selected_value_4, filter):
        selected_values = [selected_value_1, selected_value_2, selected_value_3, selected_value_4, 'team']
        color = 'team'
        if filter == 1:
            color = filters[filter]
        elif 1 < filter <= 6:
            color = filters[filter][0]

        color_mapping = {value: i for i, value in enumerate(df[color].unique())}
        df['selected_filter'] = df[color].map(color_mapping)

        selected_columns = [sel_val_not_none for sel_val_not_none in selected_values if sel_val_not_none is not None] + ['selected_filter']
        df_sorted = df[selected_columns].sort_values(selected_columns)

        fig = px.parallel_categories(df_sorted, dimensions=selected_values, color='selected_filter')
        return fig

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

            attributes1 = ["goals_per90", "assists_per90", "goals_pens_per90", "goals_assists_per90",
                           "goals_assists_pens_per90", "shots_per90", "shots_on_target_per90"]
            attributes2 = ["gk_shots_on_target_against", "gk_save_pct", "possession", "passes_pct",
                           "average_shot_distance", "dribbles_completed_pct", "fouled", "avg_age"]

            fig = make_subplots(rows=1, cols=2)

            values1 = point1_detail[attributes1].values[0]
            values2 = point2_detail[attributes1].values[0]

            fig.add_trace(go.Bar(
                x=attributes1,
                y=values1,
                orientation='v',
                name=point1['customdata'][0],
                marker=dict(
                    color='rgba(58, 71, 80, 0.6)',
                    line=dict(color='rgba(58, 71, 80, 1.0)', width=1)
                ),
                showlegend=True
            ), row=1, col=1)
            fig.add_trace(go.Bar(
                x=attributes1,
                y=values2,
                orientation='v',
                name=point2['customdata'][0],
                marker=dict(
                    color='rgba(246, 78, 139, 0.6)',
                    line=dict(color='rgba(246, 78, 139, 1.0)', width=1)
                ),
                showlegend=True
            ), row=1, col=1)

            values3 = point1_detail[attributes2].values[0]
            values4 = point2_detail[attributes2].values[0]

            fig.add_trace(go.Bar(
                x=attributes2,
                y=values3,
                orientation='v',
                name=point1['customdata'][0],
                marker=dict(
                    color='rgba(58, 71, 80, 0.6)',
                    line=dict(color='rgba(58, 71, 80, 1.0)', width=1)
                ),
                showlegend=False
            ), row=1, col=2)
            fig.add_trace(go.Bar(
                x=attributes2,
                y=values4,
                orientation='v',
                name=point2['customdata'][0],
                marker=dict(
                    color='rgba(246, 78, 139, 0.6)',
                    line=dict(color='rgba(246, 78, 139, 1.0)', width=1)
                ),
                showlegend=False
            ), row=1, col=2)

            fig.update_layout(
                barmode='group',
                height=700,
                width=600,
            )
            return fig

    return dcc.Graph(id=ids.SCATTER_PLOT)
