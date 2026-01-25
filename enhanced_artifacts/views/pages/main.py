"""
views/pages/main.py

Author: Jason Fuller
Date: 2026-01-25

Main page layout.

This page is the landing screen after a successful login. For now, it is kept
intentionally simple and only displays a welcome message.

The user's name is populated by a callback using the logged-in session data
(e.g., store-auth) and written into the "main-welcome" div.
"""

import dash_bootstrap_components as dbc
from dash import html


def layout_main():
    return dbc.Container(
        [
            html.H2("Welcome", className="mb-2"),
            html.Div(id="main-welcome", className="text-muted mb-3"),
        ],
        className="py-4",
    )
