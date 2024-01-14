from dash import Dash, html
from src.components.layout import create_layout
import dash_bootstrap_components as dbc

if __name__ == "__main__":
    app = Dash(external_stylesheets=[dbc])
    app.title = "Visteam"
    app.layout = create_layout(app)
    app.run(debug=True)
