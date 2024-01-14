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
        Output(ids.HOVER_PLOT, 'figure'),
        [Input(ids.SCATTER_PLOT, 'hoverData')]
    )
    def display_hover_data(hover_data):
        if hover_data is None:
            return {}
    
        hovered_point = hover_data['points'][0]

        point_detail = df[df['team'] == hovered_point['customdata'][0]]

        attributes = [col for col in df.columns if col != 'team']
        values = point_detail[attributes].values[0]

        fig_bar = px.bar(
            x = list(values),
            y = attributes,
            # color=[point1['customdata'][0]] * len(attributes) + [point2['customdata'][0]] * len(attributes),
            labels={'x': 'Value', 'y': 'Attribute', 'color': 'Point'},
            orientation='h',
            title=f"Hover plot",
            width=1000,
            height=500,
        )

        return fig_bar
    return dcc.Graph(id=ids.HOVER_PLOT)