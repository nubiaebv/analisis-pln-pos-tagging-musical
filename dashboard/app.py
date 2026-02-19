import dash
from dash import Dash, html, dcc
import dash_bootstrap_components as dbc
import sys
import os
# Obtiene la ruta absoluta de la carpeta raíz del proyecto
ruta_raiz = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ruta_raiz not in sys.path:
    sys.path.insert(0, ruta_raiz)

aplicacion = Dash(
    __name__,
    use_pages=True,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.css",
    ],
    suppress_callback_exceptions=True,
)

# ── Barra lateral de navegación ──────────────────────────────────────────────
barra_lateral = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.Span("NP Asociados", className="logo-accent"),
                        html.Span(" Estudio"),
                    ],
                    className="sidebar-title",
                ),
                html.P("Analizador de canciones", className="sidebar-subtitle"),
            ],
            className="sidebar-header",
        ),
        html.Hr(className="sidebar-divider"),
        dbc.Nav(
            [
                dbc.NavLink(
                    [html.I(className="bi bi-house-fill"), html.Span("Inicio")],
                    href="/",
                    active="exact",
                    className="nav-item-link",
                ),
                dbc.NavLink(
                    [html.I(className="bi bi-bar-chart-fill"), html.Span("Comparación")],
                    href="/viz1",
                    active="exact",
                    id="nav-comparacion", # ID añadido
                    className="nav-item-link",
                    disabled=True,
                ),
                dbc.NavLink(
                    [html.I(className="bi bi-diagram-3-fill"), html.Span("Evolución Temporal")],
                    href="/viz2",
                    active="exact",
                    id="nav-evolucion", # ID añadido
                    className="nav-item-link",
                    disabled=True,
                ),
                dbc.NavLink(
                    [html.I(className="bi bi-graph-up"), html.Span("Sentimientos")],
                    href="/viz3",
                    active="exact",
                    id="nav-sentimientos", # ID añadido
                    className="nav-item-link",
                    disabled=True,
                ),
                dbc.NavLink(
                    [html.I(className="bi i-graph-up"), html.Span("POS")],
                    href="/viz4",
                    active="exact",
                    id="nav-pos",  # ID añadido
                    className="nav-item-link",
                    disabled=True,
                ),
            ],
            vertical=True,
            pills=True,
        ),
        html.Div("v1.0.0", className="sidebar-version"),
    ],
    className="sidebar",
)

aplicacion.layout = html.Div(
    [
        dcc.Store(id='store-datos-pipeline', storage_type='memory'),
        barra_lateral,
        html.Div(dash.page_container, className="main-content"),
    ],
    className="app-wrapper",
)

if __name__ == "__main__":
    aplicacion.run(debug=True)