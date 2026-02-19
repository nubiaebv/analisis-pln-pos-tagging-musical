import dash
from dash import html, dcc, callback, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
# Asegúrate de que la ruta de importación sea la correcta según tu estructura
from src.analysis.evolucion_temporal import evolucion_temporal

dash.register_page(__name__, path="/viz2", name="Evolucion")

# ── Diseño de la página ───────────────────────────────────────────────────────
layout = html.Div(
    [
        # Encabezado
        html.Div(
            [
                html.H1("Evolución Temporal de la Complejidad", className="page-title"),
                html.P(
                    "Análisis de métricas gramaticales y léxicas a través de las décadas.",
                    className="page-subtitle",
                ),
            ],
            className="page-header",
        ),

        # Gráfica de Líneas (Ocupa el ancho completo para ver mejor la tendencia)
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="grafica-evolucion-lineas", className="chart", style={"height": "500px"}),
                    className="chart-card full-width",  # Usamos full-width para tendencia
                ),
            ],
            className="charts-row",
        ),

        # Gráficas inferiores (Boxplot y Heatmap)
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="grafica-distribucion-box", className="chart", style={"height": "450px"}),
                    className="chart-card half",
                ),
                html.Div(
                    dcc.Graph(id="grafica-correlacion-heat", className="chart", style={"height": "450px"}),
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
    Output("grafica-evolucion-lineas", "figure"),
    Output("grafica-distribucion-box", "figure"),
    Output("grafica-correlacion-heat", "figure"),
    Input("store-datos-pipeline", "data"),  # Conexión al almacén de datos
    prevent_initial_call=False
)
def actualizar_graficas_evolucion(data):
    """Procesa los datos del store y genera las visualizaciones temporales."""

    # Manejo de caso sin datos
    if not data or len(data) == 0:
        fig_vacia = go.Figure().update_layout(
            title="Esperando datos del pipeline...",
            **diseno_oscuro()
        )
        return fig_vacia, fig_vacia, fig_vacia

    # 1. Cargar datos en la clase
    df = pd.DataFrame(data)
    analizador = evolucion_temporal(df)

    # 2. Preparar métricas (décadas, densidad, etc.)
    df_procesado = analizador.preparar_datos()

    if df_procesado is None:
        return go.Figure(), go.Figure(), go.Figure()

    # 3. Generar Figuras desde la clase
    fig_lineas = analizador.grafico_evolucion_complejidad()
    fig_box = analizador.grafico_distribucion_longitud()
    fig_heat = analizador.grafico_heatmap_correlacion()

    # 4. Aplicar diseño estético común
    estilo = diseno_oscuro()

    # Personalización adicional para cada gráfico
    fig_lineas.update_layout(**estilo)
    fig_lineas.update_xaxes(tickangle=0)  # Décadas se leen bien horizontales

    fig_box.update_layout(**estilo)
    fig_box.update_xaxes(tickangle=45)

    fig_heat.update_layout(**estilo)

    return fig_lineas, fig_box, fig_heat


def diseno_oscuro():
    """Configuración visual para coherencia con el dashboard."""
    return dict(
        template="plotly_dark",
        paper_bgcolor="#151c2c",
        plot_bgcolor="#1e2738",
        font=dict(color="#c9d4e8", family="'Courier New', monospace"),
        margin=dict(l=50, r=20, t=60, b=50),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        )
    )