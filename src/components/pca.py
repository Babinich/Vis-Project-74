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
filters = ["team", "group", ("pld_round_of_16", "won_round_of_16", "Round of 16"),
           ("pld_quarter_finals", "won_quarter_finals", "Quarter Finals"),
           ("pld_semi_finals", "won_semi_finals", "Semi Finals"),
           ("pld_third_place", "won_third_place", "Third Place"), ("pld_finals", "won_finals", "Finals")]


def render(app: Dash):
    @app.callback(
        Output(ids.PCA, 'figure'),
        [Input(ids.CATEGORY_DROPDOWN_1, 'value'),
         Input(ids.CATEGORY_DROPDOWN_2, 'value'),
         Input(ids.CATEGORY_DROPDOWN_3, 'value'),
         Input(ids.CATEGORY_DROPDOWN_4, 'value'),
         Input(ids.FILTER, "value")],
    )
    def update_second_view(selected_value_1, selected_value_2, selected_value_3, selected_value_4, filter):
        selected_values = [selected_value_1, selected_value_2, selected_value_3, selected_value_4]
        filter_name = 'team'
        if filter == 1:
            filter_name = filters[filter]
        elif 1 < filter <= 6:
            filter_name = filters[filter][0]

        color_mapping = {value: i for i, value in enumerate(df[filter_name].unique())}
        filter_key = 'filter_' + filter_name
        num_unique = len(df[filter_name].unique())
        colorscale = px.colors.qualitative.Set1
        df[filter_key] = df[filter_name].map(color_mapping)

        selected_columns = [filter_key] + ([sel_val_not_none for sel_val_not_none in selected_values if sel_val_not_none is not None])
        selected_columns += ['team']
        df_sorted = df[selected_columns].sort_values(selected_columns)

        fig = px.parallel_categories(df_sorted, dimensions=selected_columns, color=filter_key,
                                     color_continuous_scale=colorscale[0:num_unique])
        fig.update_layout(coloraxis_colorbar=dict(tickvals=[i for i in range(0, num_unique)],
                                                  ticktext=df[filter_name].unique(),
                                                  tickmode='array'), height=800, width=1100)
        return fig
    
    return dcc.Graph(id=ids.PCA)