


"""Stays commented, beacuse of the global variables being used"""






# import pandas as pd
# import plotly.express as px
# import plotly.graph_objs as go
# from dash import Dash, dcc, Patch, html
# from dash.dependencies import Input, Output
# from plotly.graph_objs import Figure
# from plotly.subplots import make_subplots

# from . import ids

# TEAM_DATA = pd.read_csv('Data/team_data.csv', delimiter=',')

# df = TEAM_DATA

# filters = ["team", "group", ("pld_round_of_16", "won_round_of_16", "Round of 16"),
#            ("pld_quarter_finals", "won_quarter_finals", "Quarter Finals"),
#            ("pld_semi_finals", "won_semi_finals", "Semi Finals"),
#            ("pld_third_place", "won_third_place", "Third Place"), ("pld_finals", "won_finals", "Finals")]

# all_colors = (px.colors.qualitative.Bold[:9] + px.colors.qualitative.Pastel[:9]
#               + px.colors.qualitative.Prism[:9] + px.colors.qualitative.Safe[:9])

# teams_from_pca = []


# def render(app: Dash):

#     @app.callback(
#     Output(ids.PCA, 'figure'),
#     [Input(ids.CATEGORY_DROPDOWN_1, 'value'),
#     Input(ids.CATEGORY_DROPDOWN_2, 'value'),
#     Input(ids.CATEGORY_DROPDOWN_3, 'value'),
#     Input(ids.CATEGORY_DROPDOWN_4, 'value'),
#     Input(ids.FILTER, "value"),
#     Input(ids.SCATTER_PLOT, "clickData"),
#     Input(ids.CLEAR_PCA_BUTTON, "value")])

#     def update_second_view(selected_value_1, selected_value_2, selected_value_3, selected_value_4, filter,
#                            sp_clicked_data, clicked):
#         selected_values = [selected_value_1, selected_value_2, selected_value_3, selected_value_4]
#         filter_name = 'team'

#         if filter == 1:
#             filter_name = filters[filter]
#         elif 1 < filter <= 6:
#             filter_name = filters[filter][0]

#         color_mapping = {value: i for i, value in enumerate(df[filter_name].unique())}
#         filter_key = 'filter_' + filter_name
#         df[filter_key] = df[filter_name].map(color_mapping)

#         selected_columns = [filter_key] + (
#             [sel_val_not_none for sel_val_not_none in selected_values if sel_val_not_none is not None])
#         selected_columns += ['team']
#         num_unique = len(df[filter_name].unique())
#         colorscale = all_colors[0:num_unique]
#         df_sorted = df[selected_columns].sort_values(selected_columns)
#         fig = px.parallel_categories(df_sorted, dimensions=selected_columns, color=filter_key,
#                                      color_continuous_scale=colorscale)
#         fig.update_layout(coloraxis_colorbar=dict(tickvals=[i for i in range(0, num_unique)],
#                                                   ticktext=df[filter_name].unique(),
#                                                   tickmode='array'), height=900, width=1100)
#         global teams_from_pca
#         teams_from_pca = df_sorted['team'].values

#         if sp_clicked_data is not None and 'points' in sp_clicked_data and clicked:
#             clicked_team = sp_clicked_data['points'][0]['customdata'][0]
#             fig.update_traces(line=dict(color=[
#                 'black' if team == clicked_team else color
#                 for team, color in zip(df_sorted['team'], fig.data[0]['line']['color'])
#             ]))
            
#         print(teams_from_pca)
#         return fig

    
#     return dcc.Graph(id=ids.PCA)

