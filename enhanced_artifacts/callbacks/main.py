"""
callbacks/main.py

Author: Jason Fuller
Date: 2026-01-25

Main page callbacks.

This module populates the main landing page welcome message using the current
authenticated user stored in `store-auth`.
"""

from dash import Input, Output, no_update


def register_main_callbacks(app):
    """
    Register callbacks for the main page.

    Args:
        app: Dash app instance
    """

    @app.callback(
        Output("main-welcome", "children"),
        Input("store-auth", "data"),
    )
    def render_main_welcome(auth_data):
        if not auth_data:
            return no_update

        name = (auth_data.get("display_name") or "").strip()
        if not name:
            return "Welcome"

        return f"Welcome, {name}"
