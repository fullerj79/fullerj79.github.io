"""
app.py

Author: Jason Fuller
Date: 2026-01-25

Application entry point.

This is the one place we wire the whole app together at startup:
- Create the Dash app + shared layout shell
- Initialize MongoDB collections (db/mongo.py)
- Construct Models (models/) that perform DB commands
- Construct Controllers (controllers/) that coordinate application logic
- Register the router + all Dash callbacks

Why we do this here:
- MongoDB connections should be created once (not inside callbacks)
- Controllers should be long-lived and reuse the same models
- Keeps responsibilities separated and prevents circular imports

Deploy note (Render):
- Render expects `server = app.server` at module scope.
"""

from dotenv import load_dotenv
load_dotenv()

import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

from db.mongo import users_collection
from models.user import UserModel
from controllers.user import UserController

from views.router import register_router
from callbacks import register_callbacks


def create_app() -> dash.Dash:
    """
    Create and configure the Dash application.

    Returns:
        A fully wired Dash app instance ready to run.
    """
    app = dash.Dash(
        __name__,
        external_stylesheets=[dbc.themes.CYBORG],
        suppress_callback_exceptions=True,
    )
    app.title = "The Fuller Monty: Relic Rush"

    # Minimal app shell. Router swaps page content into "page".
    # Stores live here so any page/callback can access session state.
    app.layout = html.Div(
        [
            dcc.Location(id="url"),
            dcc.Store(id="store-auth", storage_type="session"),
            dcc.Store(id="store-game", storage_type="session"),
            html.Div(id="page"),
        ]
    )

    # Build Model layer (DB access lives here)
    user_model = UserModel(users_collection)

    # Build Controller layer (auth/game flows live here)
    user_controller = UserController(user_model)

    # Wire router + callbacks (UI event handlers)
    register_router(app)
    register_callbacks(app, user_controller=user_controller)

    return app


app = create_app()

# Render expects this name at module scope
server = app.server


if __name__ == "__main__":
    app.run(debug=True)
