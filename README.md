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
- point_comparison.py: Manages the interactive point comparison chart, updating the visualization based on user selections and interactions within the scatter plot.
- cat_1_pca.py: Sets up a dropdown for selecting the first category for PCA analysis.
- cat_2_pca.py: Sets up a dropdown for selecting the second category for PCA analysis.
- cat_3_pca.py: Sets up a dropdown for selecting the third category for PCA analysis.
- cat_4_pca.py: Sets up a dropdown for selecting the fourth category for PCA analysis.
- main.py: Initializes the Dash application, sets the page title, applies the Bootstrap theme for styling, and defines the layout with the create_layout function. Runs the app in debug mode.

- ### How to launch the app
By running the 'main.py' file you receive a link which redirects you to the browser-version of the app, where you can adjust and select the data you want to view

- ### Attributes description
Here are the attributes used in our code, including a short description for each attribute

- **goals_per90**: Average number of goals scored by a team per 90 minutes of play.
- **assists_per90**: Average number of assists made by a team per 90 minutes.
- **goals_pens_per90**: Average number of goals scored excluding penalties per 90 minutes.
- **goals_assists_per90**: Sum of goals and assists per 90 minutes.
- **goals_assists_pens_per90**: Combined number of goals and assists, excluding penalties, per 90 minutes.
- **shots_per90**: Average number of shots taken by a team per 90 minutes.
- **shots_on_target_per90**: Average number of shots on goal per 90 minutes.
- **xg_per90**: Expected goals metric calculated per 90 minutes.
- **xg_assist_per90**: Expected goals from assists per 90 minutes.
- **npxg_per90**: Non-penalty expected goals per 90 minutes.
- **xg_xg_assist_per90**: Sum of expected goals and expected assists per 90 minutes.
- **npxg_xg_assist_per90**: Combined non-penalty expected goals and expected assists per 90 minutes.
- **gk_shots_on_target_against**: Average number of shots on target faced by the goalkeeper per 90 minutes.
- **gk_save_pct**: Goalkeeper's save percentage.
- **games_complete**: Number of complete games played.
- **gk_clean_sheets_pct**: Percentage of games where the goalkeeper kept a clean sheet.
- **pld_round_of_16**: Indicates if and against who the team has played in the round of 16.
- **won_round_of_16**: Indicator of whether the round of 16 match was won or not.
- **pld_quarter_finals**: Indicates if and against who the team has played in the quarter finals.
- **won_quarter_finals**: Indicator of whether the quarter-final match was won or not.
- **pld_semi_finals**: Indicates if and against who the team has played in the semi finals.
- **won_semi_finals**: Indicator of whether the semi-final match was won or not.
- **pld_third_place**: Indicates if and against who the team has played for the third place.
- **won_third_place**: Indicator of whether the third-place match was won or not.
- **pld_finals**: Indicates if and against who the team has played in the finals.
- **won_finals**: Indicator of whether the final match was won or not.
- **possession**: Average percentage of time a team controls the ball during a game.
- **passes_pct**: Average pass completion percentage.
- **dribbles_completed_pct**: Percentage of successful dribbles.
- **tackles_won**: Number of tackles won by a team.
- **fouled**: Number of times players of the team have been fouled.
- **avg_age**: Average age of the team's players.
- **cards_yellow**: Number of yellow cards received by the team.

### Screenshots
#### Scatter plot
<img width="1370" alt="Screen Shot 2024-02-02 at 11 44 47" src="https://github.com/Babinich/Vis-Project-74/assets/41565823/e4e012e7-35ea-498f-9718-883a5bb0b4bb">

#### Parallel categories plot
<img width="1410" alt="Screen Shot 2024-02-02 at 11 46 11" src="https://github.com/Babinich/Vis-Project-74/assets/41565823/00c04cda-0da4-4331-a97b-cb6ed6c3bcf4">

#### Point comparison plot
<img width="1276" alt="Screen Shot 2024-02-02 at 11 46 30" src="https://github.com/Babinich/Vis-Project-74/assets/41565823/4332d04b-d151-47c1-bf75-704e3ea6a0f5">

