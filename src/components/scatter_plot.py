import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, Patch, html
from dash.dependencies import Input, Output
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots

from . import ids

TEAM_DATA = pd.read_csv('Data/team_data.csv', delimiter=',')
df = TEAM_DATA
last_clicked_point = []
filters = ["team", "group", ("pld_round_of_16", "won_round_of_16", "Round of 16"),
           ("pld_quarter_finals", "won_quarter_finals", "Quarter Finals"),
           ("pld_semi_finals", "won_semi_finals", "Semi Finals"),
           ("pld_third_place", "won_third_place", "Third Place"), ("pld_finals", "won_finals", "Finals")]
all_colors = (px.colors.qualitative.Bold[:9] + px.colors.qualitative.Pastel[:9]
              + px.colors.qualitative.Prism[:9] + px.colors.qualitative.Safe[:9])
last_filter = 0


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
         Input(ids.LAYERS, "value"),
         Input(ids.SCATTER_PLOT, "clickData")]
    )
    def update_scatter_plot(x_axis: str, y_axis: str, filter: int, selected_statistic: str, sp_clicked_data) -> Figure:
        df["group"] = pd.Categorical(df["group"])
        print(filter, sp_clicked_data)
        global last_filter

        if filter != last_filter and sp_clicked_data is not None:
            sp_clicked_data = None

        if filter == 1:
            num_unique = len(df[filters[filter]].unique())
            colorscale = all_colors[0:num_unique]
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis],
                             color=filters[filter], color_discrete_sequence=colorscale,
                             hover_data=['team'], labels={filters[filter]: "Groups"})

        elif (filter > 1) and (filter <= 6):
            num_unique = len(df[filters[filter][0]].unique())
            colorscale = all_colors[0:num_unique]
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis],
                             color=filters[filter][0], color_discrete_sequence=colorscale,
                             symbol=filters[filter][1], hover_data=['team'],
                             labels={filters[filter][0]: filters[filter][2], filters[filter][1]: "Result"})

        else:
            num_unique = len(df[filters[filter]].unique())
            colorscale = all_colors[0:num_unique]
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], color=filters[filter], color_discrete_sequence=colorscale,
                             hover_data=['team'])

        if sp_clicked_data is not None and 'points' in sp_clicked_data:
            clicked_team = sp_clicked_data['points'][0]['customdata'][0]
            team_selector = (df['team'] == clicked_team)
            fig.update_traces(
                marker=dict(size=12, line=dict(width=2, color='DarkSlateGray')),
                selector=dict(mode='markers', customdata=clicked_team)
            )

        last_filter = filter
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
        Output(ids.SECOND_VIEW, 'figure'),
        [Input(ids.CATEGORY_DROPDOWN_1, 'value'),
         Input(ids.CATEGORY_DROPDOWN_2, 'value'),
         Input(ids.CATEGORY_DROPDOWN_3, 'value'),
         Input(ids.CATEGORY_DROPDOWN_4, 'value'),
         Input(ids.FILTER, "value"),
         Input(ids.SCATTER_PLOT, "clickData")],
    )
    def update_second_view(selected_value_1, selected_value_2, selected_value_3, selected_value_4, filter, sp_clicked_data):
        selected_values = [selected_value_1, selected_value_2, selected_value_3, selected_value_4]
        filter_name = 'team'
        global last_filter

        if filter != last_filter and sp_clicked_data is not None:
            sp_clicked_data = None

        if filter == 1:
            filter_name = filters[filter]
        elif 1 < filter <= 6:
            filter_name = filters[filter][0]

        color_mapping = {value: i for i, value in enumerate(df[filter_name].unique())}
        filter_key = 'filter_' + filter_name
        df[filter_key] = df[filter_name].map(color_mapping)

        selected_columns = [filter_key] + ([sel_val_not_none for sel_val_not_none in selected_values if sel_val_not_none is not None])
        selected_columns += ['team']
        num_unique = len(df[filter_name].unique())
        colorscale = all_colors[0:num_unique]
        df_sorted = df[selected_columns].sort_values(selected_columns)
        fig = px.parallel_categories(df_sorted, dimensions=selected_columns, color=filter_key,
                                     color_continuous_scale=colorscale)
        fig.update_layout(coloraxis_colorbar=dict(tickvals=[i for i in range(0, num_unique)],
                                                  ticktext=df[filter_name].unique(),
                                                  tickmode='array'), height=900, width=1100)

        if sp_clicked_data is not None and 'points' in sp_clicked_data:
            clicked_team = sp_clicked_data['points'][0]['customdata'][0]
            fig.update_traces(line=dict(color=[
                'black' if team == clicked_team else color
                for team, color in zip(df_sorted['team'], fig.data[0]['line']['color'])
            ]))

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
            return fig

    @app.callback(
        Output('color-bar', 'children'),  # Output to the color-bar div
        [Input(ids.LAYERS, 'value')]  # Input from layers dropdown
    )
    def update_color_bar(selected_statistic):
        if not selected_statistic or selected_statistic not in df.columns:
            return html.Div()  # Return empty div if no valid statistic is selected

        # Define your color shades (same as used in scatter plot)
        color_discrete_map = {
            'lightblue': '#67D3F3',  # Lighter blue
            'blue': '#0177D9',  # Regular blue
            'darkblue': '#01298B',  # Darker blue
            'navy': '#000F52'  # Navy blue
        }

        # Create a horizontal bar divided into four color sections
        color_bar_style = {'display': 'flex', 'height': '20px'}
        color_sections = [html.Div(style={'background-color': color, 'flex': '1'}) for color in
                          color_discrete_map.values()]

        return html.Div(color_sections, style=color_bar_style)

    return dcc.Graph(id=ids.SCATTER_PLOT)