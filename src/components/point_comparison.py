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
last_clicked_point_click_plot = []
filters = ["team", "group", ("pld_round_of_16", "won_round_of_16", "Round of 16"),
           ("pld_quarter_finals", "won_quarter_finals", "Quarter Finals"),
           ("pld_semi_finals", "won_semi_finals", "Semi Finals"),
           ("pld_third_place", "won_third_place", "Third Place"), ("pld_finals", "won_finals", "Finals")]

last_clicked_point = []

all_colors = (px.colors.qualitative.Bold[:9] + px.colors.qualitative.Pastel[:9]
              + px.colors.qualitative.Prism[:9] + px.colors.qualitative.Safe[:9])
locked = False
last_click_point_fig = None
last_button_click = None


def reset_last_clicked_point():
    global last_clicked_point
    last_clicked_point = []


# can be used to clear the last_clicked_point list

def render(app: Dash):

    @app.callback(
    Output(ids.DUMMY_OUTPUT, 'children'),
    Input(ids.LOCK_TEAMS_CHECKBOX, "value")
    )

    def update_lock_teams_checkbox(checkbox_value):
        global locked
        locked = checkbox_value
        return None
        
    @app.callback(
        Output(ids.POINT_COMPARISON, 'figure'),
        [Input(ids.CLEAR_TEAMS_BUTTON, "n_clicks"),
         Input(ids.SCATTER_PLOT, 'clickData')]
    )
    def display_click_data(button_click, click_data):
        global locked, last_click_point_fig, last_button_click, last_clicked_point
        if button_click != last_button_click:
            last_button_click = button_click
            reset_last_clicked_point()
            return {}

        if locked:
            return last_click_point_fig

        if click_data is None:
            return {}

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
            last_click_point_fig = fig
            
            return fig      
   

    return dcc.Graph(id=ids.POINT_COMPARISON)