from dash import Dash, html
from src.components.layout import create_layout
from dash_bootstrap_components.themes import BOOTSTRAP

if __name__ == "__main__":
    app = Dash(external_stylesheets=[BOOTSTRAP])
    app.title = "DataDribbler"
    app.layout = create_layout(app)
    app.run(debug=False)
