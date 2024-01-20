# Visteam
## Visualisation project - Goup 74

### Repository structure
This section explains the structure of this repository, and all the code in it.

#### Directory structure
- Data: It contains two data sets, "filter_data.csv" and "team_data.csv". "team_data.csv" is the main file with all necessary data for visulisation.
- src/components: Inside this folder we store every components and layouts used for visualisation. All callbacks are being coded inside given component. That's the only place where we can implement callbacks. Every component has it's own ID. Every ID is listed in "ids.py".

#### Code structure
- scatter_plot.py: creates main scatter plot
- x_axis_dropdown.py: dropdown reponsible for x axis
- y_axis_dropdown.py: dropdown reponsible for y axis
- filter.py: filters the data by the groups stage, teams and knockout stage
- search_bar.py: allows for detecting given data point in scatter plot (needs more development)
- ids.py: contains all ids of every component
- layout.py: specifies the layout of the app

                     
                     
