import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, Patch, html
from dash.dependencies import Input, Output
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots
# from .pca import teams_from_pca

from . import ids


TEAM_DATA = pd.read_csv('Data/team_data.csv', delimiter=',')
# data used for creating data frames
df = TEAM_DATA 
# filtering options for the scatter plot
filters = ["team", "group", ("pld_round_of_16", "won_round_of_16", "Round of 16"),
           ("pld_quarter_finals", "won_quarter_finals", "Quarter Finals"),
           ("pld_semi_finals", "won_semi_finals", "Semi Finals"),
           ("pld_third_place", "won_third_place", "Third Place"), ("pld_finals", "won_finals", "Finals")]
# all teams names used, for modifing the size of points inside traces
all_teams = ['Argentina', 'Australia', 'Belgium', 'Brazil', 'Cameroon', 'Canada', 'Costa Rica', 'Croatia', 
             'Denmark', 'Ecuador', 'England', 'France', 'Germany', 'Ghana', 'Iran', 'Japan', 'Korea Republic', 
             'Mexico', 'Morocco', 'Netherlands', 'Poland', 'Portugal', 'Qatar', 'Saudi Arabia', 'Senegal', 'Serbia',
             'Spain', 'Switzerland', 'Tunisia', 'United States', 'Uruguay', 'Wales']

last_clicked_point = []

all_colors = (px.colors.qualitative.Bold[:9] + px.colors.qualitative.Pastel[:9]
              + px.colors.qualitative.Prism[:9] + px.colors.qualitative.Safe[:9])

def render(app: Dash):

  ############################################################ SCATTER PLOT #################################################### 
 # outputs the scatter plor
 
    @app.callback(
        Output(ids.SCATTER_PLOT, "figure"),          # outputs the scatter plor
        [Input(ids.X_AXIS_DROPDOWN, "value"),        # gets the input from X_AXIS_DROPDOWN
         Input(ids.Y_AXIS_DROPDOWN, "value"),        # gets the input from Y_AXIS_DROPDOWN
         Input(ids.FILTER, "value"),                 # gets the input from FILTER
         Input(ids.PCA, "clickData"),                # gets the teams from PCA
         Input(ids.SEARCH_BAR, "value"),             # gets the input form SEARCH_BAR
         Input(ids.CLEAR_SCATTER_BUTTON, "value")]   # get imput form clear CLEAR_SCATTER_BUTTON
    )
    def update_scatter_plot(x_axis: str, y_axis: str, filter: int, sv_clicked_data, teams: list[str], clicked) -> Figure:

        """
        function creates a scatter plot based on inputs from x_axis, y_axis, filter, sv_clicked_data, teams, search dropdown and 
        relation between PCA and Scatter plot
        input: 
               x_axis -> inputs attributes that will be ploted on x-axis of the scatterplot
               y_axis -> inputs attributes that will be ploted on y-axis of the scatterplot
               filter -> a value that indexes over the set of filters
               sv_clicked_data -> teams from the PCA graph
               teams  -> a list storing names of the sleceted teams that will have their size changed
               clicked -> if checkbox is clicked  the PCA clicks affect Scatter plot

        output:
               fig -> a figure objet ready for presenting in the layout
        """

        # changing the variable to categorical data in order to create more interactive legend
        df["group"] = pd.Categorical(df["group"])

        # creation of graphs based on the the selected filter
        if filter == 1:
            num_unique = len(df[filters[filter]].unique())
            colorscale = all_colors[0:num_unique]
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis],
                             color=filters[filter],  color_discrete_sequence=colorscale,
                             hover_data=['team'], labels={filters[filter]: "Groups"})  # specifing the name in the legend
            
            fig.update_traces(marker=dict(size=[10 for _ in range(4)])) # creates a dummy size list,
                                                                        # making every point on the graph of size 10

        elif (filter > 1) and (filter <= 6):# creates filters for ("pld_round_of_16", "won_round_of_16", "Round of 16"),
                                             #                     ("pld_quarter_finals", "won_quarter_finals", "Quarter Finals"),
                                             #                     ("pld_semi_finals", "won_semi_finals", "Semi Finals"),
                                             #                     ("pld_third_place", "won_third_place", "Third Place"), 
                                             #                     ("pld_finals", "won_finals", "Finals")
            num_unique = len(df[filters[filter][0]].unique())
            colorscale = all_colors[0:num_unique]
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis],
                             color=filters[filter][0], color_discrete_sequence=colorscale,
                             symbol=filters[filter][1], hover_data=['team'],
                             labels={filters[filter][0]: filters[filter][2], filters[filter][1]: "Result"})
            
            # used for modyfing the structure of the figure object
            figure_dict = fig.to_dict() 
            # gets the number of traces for a initialized figure
            points_per_trace = [(trace["name"], len(trace["customdata"])) for trace in figure_dict["data"]]
            # updates every trace with correct dummy sieze list
            for element in points_per_trace:
                fig.update_traces(marker=dict(size=[10 for _ in range(element[1])]), selector=dict(name=element[0]))

        else:
            num_unique = len(df[filters[filter]].unique())
            colorscale = all_colors[0:num_unique]
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], color=filters[filter], color_discrete_sequence=colorscale,
                             hover_data=['team'])
            
            fig.update_traces(marker=dict(size=[10 for _ in range(32)]))

        if sv_clicked_data is not None and 'points' in sv_clicked_data and clicked:
            team_indices = [point['pointNumber'] for point in sv_clicked_data['points']]
            team_names = [team for index, team in enumerate(teams_from_pca) if index in team_indices]

            for i, trace in enumerate(fig.data):
                trace_team = trace.customdata[0]
                # the following is done to make sure we do the highlighting for any in the group
                # all the time
                if any(x in trace_team for x in team_names):
                    fig.data[i].update(marker=dict(line=dict(width=3, color='DarkSlateGray')))
                    fig.data[i].update()

        fig_dict = fig.to_dict()
       
        # stores the {name of the team : (name of the trace, index of the trace, index of the team inside the trace)}
        traceback = dict()
        for trace in range(len(fig_dict["data"])):
            for indx in range(len(fig_dict["data"][trace]['customdata'])):
                chosen_team = fig_dict["data"][trace]['customdata'][indx]
                name = fig_dict["data"][trace]['name']
                traceback[chosen_team[0]] = (name, trace, indx)

        # this dictionary is going to store the intial value of the dummy size list, based on the selected team in search bar
        # format {name of the trace: dummy size list, list of indexes that need to be changed (indexes are taken from the traceback)}
        update_size_call = dict()
        if teams == None:
            # that way reset the update_size_call whan no teams are selected
            update_size_call = dict()
            return fig
        else: 
            for team in teams:
                label = traceback[team][0]
                indx_trace = traceback[team][1]
                indx_team = traceback[team][2]
                if label not in update_size_call.keys() and type(fig_dict["data"][indx_trace]["marker"]["size"]) == int:
                   update_size_call[label] = [[fig_dict["data"][indx_trace]["marker"]["size"]], [indx_team]] # case distinction 
                                                                                                             # for team filter

                elif label not in update_size_call.keys() and type(fig_dict["data"][indx_trace]["marker"]["size"]) == list:
                    update_size_call[label] = [fig_dict["data"][indx_trace]["marker"]["size"], [indx_team]]

                if label in update_size_call.keys() and indx_team not in update_size_call[label][1]:
                    update_size_call[label][1].append(indx_team) # appends the unique indexes that need modifing

            # print(update_size_call)
                    
            # stores only the name of the trace that has to be updated and the updated dummy size list
            # format {name of the trace : updated dummy size list}
            update_size_out = dict()
            for key in update_size_call.keys():
                indx_modify = update_size_call[key][1]
                updated_size = update_size_call[key][0]
                for index in indx_modify:
                    updated_size[index] = 20
                update_size_out[key] = updated_size
            # print(update_size_out)

            # updates traces that are inside the update_size_out
            for key in update_size_out:
                fig.update_traces(marker_size=update_size_out[key], selector=dict(name=key))  
        return fig

################################################################### PCA ##############################################################

    @app.callback(
        Output(ids.PCA, 'figure'),
        [Input(ids.CATEGORY_DROPDOWN_1, 'value'),
         Input(ids.CATEGORY_DROPDOWN_2, 'value'),
         Input(ids.CATEGORY_DROPDOWN_3, 'value'),
         Input(ids.CATEGORY_DROPDOWN_4, 'value'),
         Input(ids.FILTER, "value"),
         Input(ids.SCATTER_PLOT, "clickData"),
         Input(ids.CLEAR_PCA_BUTTON, "value")]
    )
    def update_second_view(selected_value_1, selected_value_2, selected_value_3, selected_value_4, filter,
                           sp_clicked_data, clicked):
        selected_values = [selected_value_1, selected_value_2, selected_value_3, selected_value_4]
        filter_name = 'team'

        if filter == 1:
            filter_name = filters[filter]
        elif 1 < filter <= 6:
            filter_name = filters[filter][0]

        color_mapping = {value: i for i, value in enumerate(df[filter_name].unique())}
        filter_key = 'filter_' + filter_name
        df[filter_key] = df[filter_name].map(color_mapping)

        selected_columns = [filter_key] + (
            [sel_val_not_none for sel_val_not_none in selected_values if sel_val_not_none is not None])
        selected_columns += ['team']
        num_unique = len(df[filter_name].unique())
        colorscale = all_colors[0:num_unique]
        df_sorted = df[selected_columns].sort_values(selected_columns)
        fig = px.parallel_categories(df_sorted, dimensions=selected_columns, color=filter_key,
                                     color_continuous_scale=colorscale)
        fig.update_layout(coloraxis_colorbar=dict(tickvals=[i for i in range(0, num_unique)],
                                                  ticktext=df[filter_name].unique(),
                                                  tickmode='array'), height=900, width=1100)
        global teams_from_pca
        teams_from_pca = df_sorted['team'].values

        if sp_clicked_data is not None and 'points' in sp_clicked_data and clicked:
            clicked_team = sp_clicked_data['points'][0]['customdata'][0]
            fig.update_traces(line=dict(color=[
                'black' if team == clicked_team else color
                for team, color in zip(df_sorted['team'], fig.data[0]['line']['color'])
            ]))
        
        # fig.update_layout(title_text="PCA")

        return fig

    return dcc.Graph(id=ids.SCATTER_PLOT)
