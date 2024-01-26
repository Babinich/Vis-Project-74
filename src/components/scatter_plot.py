import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from dash import Dash, dcc, Patch, html
from dash.dependencies import Input, Output
from plotly.graph_objs import Figure
from plotly.subplots import make_subplots
import json
import plotly.io as pio

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


def render(app: Dash):
        
    @app.callback(
    Output(ids.SCATTER_PLOT, "figure"),     # outputs the scatter plor
    Input(ids.X_AXIS_DROPDOWN, "value"),    # gets the input from X_AXIS_DROPDOWN
    Input(ids.Y_AXIS_DROPDOWN, "value"),    # gets the input from Y_AXIS_DROPDOWN
    Input(ids.FILTER,"value"),              # gets the input from FILTER
    Input(ids.SEARCH_BAR, "value")          # gets the input form SEARCH_BAR
    )

    def update_scatter_plot(x_axis: str, y_axis: str, filter: int, teams: list[str]) -> dcc.Graph:
        """
        function creates a scatter plot based on inputs from x_axis, y_axis, filter, and search dropdown
        input: 
               x_axis -> inputs attributes that will be ploted on x-axis of the scatterplot
               y_axis -> inputs attributes that will be ploted on y-axis of the scatterplot
               filter -> a value that indexes over the set of filters
               teams  -> a list storing names of the sleceted teams that will have their size changed
        output:
               fig -> a figure objet ready for presenting in the layout
        """

        # changing the variable to categorical data in order to create more interactive legend
        df["group"] = pd.Categorical(df["group"]) 

        # creation of graphs based on the the selected filter
        if filter == 1: # group filter
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], color=filters[filter], opacity=0.7,  hover_data=['team'],
                             labels={filters[filter]: "Groups"}) # specifing the name in the legend
            fig.update_traces(marker=dict(size=[8 for _ in range(4)])) # creates a dummy size list, 
                                                                       # making every point on the graph of size 8
           
        elif (filter > 1) and (filter <= 6): # creates filters for ("pld_round_of_16", "won_round_of_16", "Round of 16"),
                                             #                     ("pld_quarter_finals", "won_quarter_finals", "Quarter Finals"),
                                             #                     ("pld_semi_finals", "won_semi_finals", "Semi Finals"),
                                             #                     ("pld_third_place", "won_third_place", "Third Place"), 
                                             #                     ("pld_finals", "won_finals", "Finals")
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], color=filters[filter][0], opacity=0.7, symbol=filters[filter][1], 
                             hover_data=['team'], labels={filters[filter][0]: filters[filter][2], filters[filter][1]: "Result" })
            
            # used for modyfing the structure of the figure object
            figure_dict = fig.to_dict() 
            # gets the number of traces for a initialized figure
            number_of_traces= len(figure_dict["data"])
            # gets the number of points per trace, used to get the correct length of dummy size list for each trace, otherwise
            # size is not customizable 
            points_per_trace = [(trace["name"], len(trace["customdata"])) for trace in figure_dict["data"]]
            # updates every trace with correct dummy sieze list
            for element in points_per_trace:
                fig.update_traces(marker=dict(size=[8 for _ in range(element[1])]), selector=dict(name=element[0]))

        else:
            # creates a plot for team filter
            fig = px.scatter(df, x=df[x_axis], y=df[y_axis], opacity=0.7, hover_data=['team'])
            # creates the dummy size list
            fig.update_traces(marker=dict(size=[8 for _ in range(32)]))

        # used for mifin the strucure of the plot
        fig_dict = fig.to_dict()
       
        # stores the {name of the team : (name of the trace, index of the trace, index of the team inside the trace)}
        traceback = dict()
        for trace in range(len(fig_dict["data"])):
            for indx in range(len(fig_dict["data"][trace]['customdata'])):
                chosen_team = fig_dict["data"][trace]['customdata'][indx]
                name = fig_dict["data"][trace]['name']
                traceback[chosen_team[0]] = (name, trace, indx)

        # print(traceback)       
        
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
                    updated_size[index] = 16
                update_size_out[key] = updated_size
            # print(update_size_out)

            # updates traces that are inside the update_size_out
            for key in update_size_out:
                fig.update_traces(marker_size=update_size_out[key], selector=dict(name=key))
            
        return fig

    return dcc.Graph(id=ids.SCATTER_PLOT)
