import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import plotly.express as px

dash.register_page(__name__, path="/viz1", name="Comparacion")

# ── Datos de ejemplo (reemplazar con datos reales del pipeline) ───────────────
palabras  = ["análisis", "texto", "modelo", "datos", "lenguaje",
             "corpus", "token", "entidad", "frase", "sentimiento"]
frecuencias = [120, 98, 87, 76, 65, 54, 43, 38, 30, 22]


# ── Diseño de la página ───────────────────────────────────────────────────────
layout = html.Div(
    [
        # Encabezado
        html.Div(
            [
                html.H1("Frecuencia de Términos", className="page-title"),
                html.P(
                    "Palabras más frecuentes detectadas en el corpus procesado.",
                    className="page-subtitle",
                ),
            ],
            className="page-header",
        ),

        # Control deslizante
        html.Div(
            [
                html.Label("Número de términos a mostrar:", className="control-label"),
                dcc.Slider(
                    id="deslizador-top-n",
                    min=5,
                    max=10,
                    step=1,
                    value=10,
                    marks={i: str(i) for i in range(5, 11)},
                    className="slider",
                ),
            ],
            className="card-section controls-row",
        ),

        # Gráficas
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="grafica-barras", className="chart"),
                    className="chart-card half",
                ),
                html.Div(
                    dcc.Graph(id="grafica-treemap", className="chart"),
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
    Output("grafica-barras", "figure"),
    Output("grafica-treemap", "figure"),
    Input("deslizador-top-n", "value"),
)
def actualizar_graficas(cantidad_terminos):
    """Actualiza las gráficas según el número de términos seleccionado."""
    palabras_filtradas   = palabras[:cantidad_terminos]
    frecuencias_filtradas = frecuencias[:cantidad_terminos]

    # Gráfica de barras horizontales
    grafica_barras = go.Figure(
        go.Bar(
            x=frecuencias_filtradas[::-1],
            y=palabras_filtradas[::-1],
            orientation="h",
            marker=dict(
                color=frecuencias_filtradas[::-1],
                colorscale="Teal",
                showscale=False,
            ),
        )
    )
    grafica_barras.update_layout(
        title="Términos más frecuentes",
        **diseno_oscuro(),
        xaxis_title="Frecuencia",
        yaxis_title="",
    )

    # Gráfica de treemap
    grafica_treemap = px.treemap(
        names=palabras_filtradas,
        parents=[""] * len(palabras_filtradas),
        values=frecuencias_filtradas,
        color=frecuencias_filtradas,
        color_continuous_scale="Teal",
    )
    grafica_treemap.update_layout(
        title="Treemap de frecuencias",
        **diseno_oscuro(),
    )

    return grafica_barras, grafica_treemap


def diseno_oscuro():
    """Retorna los parámetros de diseño oscuro comunes a todas las gráficas."""
    return dict(
        paper_bgcolor="#151c2c",
        plot_bgcolor="#1e2738",
        font=dict(color="#c9d4e8", family="'Courier New', monospace"),
        margin=dict(l=20, r=20, t=50, b=20),
    )