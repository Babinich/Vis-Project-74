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
- By running the 'main.py' file you receive a link which redirects you to the browser-version of the app, where you can adjust and select the data you want to view

- ### Attributes table

| Attributes                  | Categorical/Ordered | Ordering Type          |
|-----------------------------|---------------------|------------------------|
| goals_per90                 | Ordered             | Quantitative Sequential|
| assists_per90               | Ordered             | Quantitative Sequential|
| goals_pens_per90            | Ordered             | Quantitative Sequential|
| goals_assists_per90         | Ordered             | Quantitative Sequential|
| goals_assists_pens_per90    | Ordered             | Quantitative Sequential|
| shots_per90                 | Ordered             | Quantitative Sequential|
| shots_on_target_per90       | Ordered             | Quantitative Sequential|
| xg_per90                    | Ordered             | Quantitative Sequential|
| xg_assist_per90             | Ordered             | Quantitative Sequential|
| npxg_per90                  | Ordered             | Quantitative Sequential|
| xg_xg_assist_per90          | Ordered             | Quantitative Sequential|
| npxg_xg_assist_per90        | Ordered             | Quantitative Sequential|
| gk_shots_on_target_against  | Ordered             | Quantitative Sequential|
| gk_save_pct                 | Ordered             | Quantitative Sequential|
| games_complete              | Ordered             | Quantitative Sequential|
| gk_clean_sheets_pct         | Ordered             | Quantitative Sequential|
| pld_round_of_16             | Categorical         | Unordered              |
| won_round_of_16             | Categorical         | Unordered              |
| pld_quarter_finals          | Categorical         | Unordered              |
| won_quarter_finals          | Categorical         | Unordered              |
| pld_semi_finals             | Categorical         | Unordered              |
| won_semi_finals             | Categorical         | Unordered              |
| pld_third_place             | Categorical         | Unordered              |
| won_third_place             | Categorical         | Unordered              |
| pld_finals                  | Categorical         | Unordered              |
| won_finals                  | Categorical         | Unordered              |
| possession                  | Ordered             | Quantitative Sequential|
| passes_pct                  | Ordered             | Quantitative Sequential|
| dribbles_completed_pct      | Ordered             | Quantitative Sequential|
| tackles_won                 | Ordered             | Quantitative Sequential|
| fouled                      | Ordered             | Quantitative Sequential|
| avg_age                     | Ordered             | Quantitative Sequential|
| cards_yellow                | Ordered             | Quantitative Sequential|
