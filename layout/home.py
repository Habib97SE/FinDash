from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash import dash_table
from dash.dash_table.Format import Group
import dash


def build_hamburger_line() -> html.Div:
    return html.Div([
    ], className="line")


def build_hamburger_button():
    return html.Div([
        html.Div([
            build_hamburger_line(),
            build_hamburger_line(),
            build_hamburger_line(),
        ], className="hamburger")
    ], className="navbar")


def build_nav_item(text: str) -> html.Li:
    return html.Li([
        html.A([
            html.I(className="fas fa-home"),
            html.Span(text)
        ], href="#")
    ])


def build_sidebar():
    return html.Div([
        html.Ul([
            build_nav_item("Home"),
            build_nav_item("About"),
            build_nav_item("Services"),
            build_nav_item("Contact"),
        ])
    ], className="sidebar")


def build_logo_section() -> html.Div:
    return html.Div([
        html.A([
            html.H1("Findash"),
            html.H3("Stock Market Dashboard")
        ], href="/")
    ], className="col-11")


def build_header():
    return html.Header([
        html.Div([
            build_hamburger_button(),
            build_sidebar()
        ], className="col-1"),
        build_logo_section()
    ])


def build_home_page():
    return html.Div([
        build_header(),
    ], className="container")
