import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import pandas as pd
from src.visualization.visualizador_emocional import visualizador_emocional

dash.register_page(__name__, path="/viz3", name="Emociones")

# ── Diseño de la página ───────────────────────────────────────────────────────
layout = html.Div(
    [
        html.Div(
            [
                html.H1("Emocionalidad Gramatical", className="page-title"),
                html.P(
                    "Relación entre el uso de adjetivos, verbos y la carga emocional de las letras.",
                    className="page-subtitle",
                ),
            ],
            className="page-header",
        ),
        # Barras y Dispersión
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="grafica-barras-emocion", className="chart", style={"height": "450px"}),
                    className="chart-card half",
                ),
                html.Div(
                    dcc.Graph(id="grafica-scatter-emocion", className="chart", style={"height": "450px"}),
                    className="chart-card half",
                ),
            ],
            className="charts-row",
        ),
    ],
    className="page-container",
)

# ── Callback ──────────────────────────────────────────────────────────────────

@callback(
    Output("grafica-barras-emocion", "figure"),
    Output("grafica-scatter-emocion", "figure"),
    Input("store-datos-pipeline", "data"),
    prevent_initial_call=False
)
def actualizar_graficas_emocion(data):
    if not data:
        fig_v = go.Figure().update_layout(**diseno_oscuro())
        return fig_v, fig_v, fig_v

    df = pd.DataFrame(data)
    analizador = visualizador_emocional(df)


    # Generar figuras
    #fig_heat = analizador.grafico_heatmap_emocional()
    fig_barras = analizador.grafico_barras_emocion_genero()
    fig_scatter = analizador.grafico_dispersion_sentimiento()

    # Estética
    estilo = diseno_oscuro()
    for fig in [ fig_barras, fig_scatter]:
        fig.update_layout(**estilo)


    return  fig_barras, fig_scatter

def diseno_oscuro():
    return dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=40, r=20, t=60, b=100)
    )