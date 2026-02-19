import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go

dash.register_page(__name__, path="/viz2", name="Evolucion")

# ── Datos de ejemplo (reemplazar con datos reales del pipeline) ───────────────
entidades_por_tipo = {
    "PER":  {
        "etiquetas": ["García", "López", "Martínez", "Rodríguez", "González"],
        "conteos":   [45, 38, 30, 27, 21],
    },
    "ORG":  {
        "etiquetas": ["UNAM", "Google", "Banco Azteca", "PEMEX", "ONU"],
        "conteos":   [60, 52, 41, 35, 29],
    },
    "LOC":  {
        "etiquetas": ["México", "Guadalajara", "Monterrey", "Puebla", "CDMX"],
        "conteos":   [80, 55, 48, 40, 37],
    },
    "MISC": {
        "etiquetas": ["COVID-19", "IA", "Python", "Reforma", "Euro"],
        "conteos":   [30, 28, 22, 18, 15],
    },
}

colores_grafica = ["#00d4aa", "#00b4d8", "#0077b6", "#48cae4", "#90e0ef"]


# ── Diseño de la página ───────────────────────────────────────────────────────
layout = html.Div(
    [
        # Encabezado
        html.Div(
            [
                html.H1("Entidades Nombradas (NER)", className="page-title"),
                html.P(
                    "Distribución de entidades detectadas por el pipeline.",
                    className="page-subtitle",
                ),
            ],
            className="page-header",
        ),

        # Selector de tipo de entidad
        html.Div(
            [
                html.Label("Tipo de entidad:", className="control-label"),
                dcc.Dropdown(
                    id="selector-tipo-entidad",
                    options=[{"label": tipo, "value": tipo} for tipo in entidades_por_tipo],
                    value="PER",
                    clearable=False,
                    className="dropdown",
                ),
            ],
            className="card-section controls-row",
        ),

        # Gráficas de barras y pastel
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="grafica-barras-ner", className="chart"),
                    className="chart-card half",
                ),
                html.Div(
                    dcc.Graph(id="grafica-pastel-ner", className="chart"),
                    className="chart-card half",
                ),
            ],
            className="charts-row",
        ),

        # Tarjetas de resumen por tipo de entidad
        html.Div(
            [
                html.Div(
                    [
                        html.Div(str(sum(datos["conteos"])), className="stat-number"),
                        html.Div(tipo, className="stat-label"),
                    ],
                    className="stat-card",
                )
                for tipo, datos in entidades_por_tipo.items()
            ],
            className="stats-row",
        ),
    ],
    className="page-container",
)


# ── Callback ──────────────────────────────────────────────────────────────────

@callback(
    Output("grafica-barras-ner", "figure"),
    Output("grafica-pastel-ner", "figure"),
    Input("selector-tipo-entidad", "value"),
)
def actualizar_graficas_ner(tipo_entidad):
    """Actualiza las gráficas según el tipo de entidad seleccionado."""
    datos      = entidades_por_tipo[tipo_entidad]
    etiquetas  = datos["etiquetas"]
    conteos    = datos["conteos"]

    # Gráfica de barras
    grafica_barras = go.Figure(
        go.Bar(x=etiquetas, y=conteos, marker_color=colores_grafica)
    )
    grafica_barras.update_layout(
        title=f"Entidades más frecuentes — {tipo_entidad}",
        **diseno_oscuro(),
        xaxis_title="Entidad",
        yaxis_title="Frecuencia",
    )

    # Gráfica de pastel con hueco (donut)
    grafica_pastel = go.Figure(
        go.Pie(
            labels=etiquetas,
            values=conteos,
            marker=dict(colors=colores_grafica),
            hole=0.4,
        )
    )
    grafica_pastel.update_layout(
        title=f"Proporción por entidad — {tipo_entidad}",
        **diseno_oscuro(),
    )

    return grafica_barras, grafica_pastel


def diseno_oscuro():
    """Retorna los parámetros de diseño oscuro comunes a todas las gráficas."""
    return dict(
        paper_bgcolor="#151c2c",
        plot_bgcolor="#1e2738",
        font=dict(color="#c9d4e8", family="'Courier New', monospace"),
        margin=dict(l=20, r=20, t=50, b=20),
    )