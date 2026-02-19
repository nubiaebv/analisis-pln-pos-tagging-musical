import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import pandas as pd
# Importamos la clase que creamos basada en el notebook 05
from src.analysis.comparacion_generos import comparacion_generos

dash.register_page(__name__, path="/viz1", name="Comparación de Géneros")

# ── Diseño de la página ───────────────────────────────────────────────────────
layout = html.Div(
    [
        # Encabezado
        html.Div(
            [
                html.H1("Análisis Comparativo por Género", className="page-title"),
                html.P(
                    "Contraste de patrones morfosintácticos y densidad léxica (Géneros con > 50 canciones).",
                    className="page-subtitle",
                ),
            ],
            className="page-header",
        ),

        # Gráfica Principal: Ratio S/V (Ancho completo)
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="grafica-barras-sv", className="chart", config={'responsive': True},
                              style={"height": "500px"}),
                    className="chart-card full-width",
                ),
            ],
            className="charts-row",
        ),

        # Gráficas Inferiores: Dispersión y Boxplot (Mitad y mitad)
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="grafica-dispersion-densidad", className="chart", style={"height": "450px"}),
                    className="chart-card half",
                ),
                html.Div(
                    dcc.Graph(id="grafica-boxplot-tokens", className="chart", style={"height": "450px"}),
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
    Output("grafica-barras-sv", "figure"),
    Output("grafica-dispersion-densidad", "figure"),
    Output("grafica-boxplot-tokens", "figure"),
    Input("store-datos-pipeline", "data"),
    prevent_initial_call=False
)
def actualizar_graficas(data):
    if not data:
        fig_vacia = go.Figure().update_layout(**diseno_oscuro())
        return fig_vacia, fig_vacia, fig_vacia

    # 1. Instanciamos la clase con los datos del pipeline
    df = pd.DataFrame(data)
    analizador = comparacion_generos(df)

    # 2. Ejecutamos el procesamiento (filtrado > 50 y métricas)
    analizador.preparar_datos()

    # 3. Obtenemos las figuras de la clase
    fig_barras = analizador.grafico_barras_comparativo()
    fig_scatter = analizador.grafico_dispersion_densidad()
    fig_box = analizador.grafico_distribucion_tokens()

    # 4. Aplicar diseño oscuro y ajustes de ejes a cada una
    estilo = diseno_oscuro()

    for fig in [fig_barras, fig_scatter, fig_box]:
        fig.update_layout(**estilo)
        # Ajuste específico para que las etiquetas de géneros se lean bien
        fig.update_xaxes(tickangle=45)

    return fig_barras, fig_scatter, fig_box


def diseno_oscuro():
    """Mantenemos tu configuración de diseño oscuro"""
    return dict(
        template="plotly_dark",
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font=dict(color="#c9d4e8"),
        margin=dict(l=40, r=20, t=60, b=80),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.4,
            xanchor="center",
            x=0.5
        )
    )