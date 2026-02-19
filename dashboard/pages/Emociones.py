import dash
from dash import html, dcc, callback, Input, Output
import plotly.graph_objects as go
import pandas as pd
import numpy as np

dash.register_page(__name__, path="/viz3", name="Emociones")

# ── Datos de ejemplo (reemplazar con datos reales del pipeline) ───────────────
np.random.seed(42)
fechas        = pd.date_range("2024-01-01", periods=30, freq="D")
conteo_pos    = np.random.randint(20, 80, 30)
conteo_neg    = np.random.randint(10, 50, 30)
conteo_neu    = 100 - conteo_pos - conteo_neg

resumen_general = {"Positivo": 420, "Negativo": 280, "Neutro": 300}


# ── Diseño de la página ───────────────────────────────────────────────────────
layout = html.Div(
    [
        # Encabezado
        html.Div(
            [
                html.H1("Análisis de Sentimientos", className="page-title"),
                html.P(
                    "Evolución temporal y distribución de polaridad en el corpus.",
                    className="page-subtitle",
                ),
            ],
            className="page-header",
        ),

        # Tarjetas KPI
        html.Div(
            [
                html.Div(
                    [
                        html.Div("420", className="stat-number positivo"),
                        html.Div("😊 Positivos", className="stat-label"),
                    ],
                    className="stat-card",
                ),
                html.Div(
                    [
                        html.Div("280", className="stat-number negativo"),
                        html.Div("😠 Negativos", className="stat-label"),
                    ],
                    className="stat-card",
                ),
                html.Div(
                    [
                        html.Div("300", className="stat-number neutro"),
                        html.Div("😐 Neutros", className="stat-label"),
                    ],
                    className="stat-card",
                ),
                html.Div(
                    [
                        html.Div("42%", className="stat-number acento"),
                        html.Div("📊 % Positivo", className="stat-label"),
                    ],
                    className="stat-card",
                ),
            ],
            className="stats-row",
        ),

        # Gráfica de área (fila completa)
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="grafica-area-sentimientos", className="chart"),
                    className="chart-card full",
                ),
            ],
            className="charts-row",
        ),

        # Gráfica donut + dispersión
        html.Div(
            [
                html.Div(
                    dcc.Graph(id="grafica-donut-sentimientos", className="chart"),
                    className="chart-card half",
                ),
                html.Div(
                    dcc.Graph(id="grafica-dispersion-sentimientos", className="chart"),
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
    Output("grafica-area-sentimientos", "figure"),
    Output("grafica-donut-sentimientos", "figure"),
    Output("grafica-dispersion-sentimientos", "figure"),
    Input("grafica-area-sentimientos", "id"),   # disparador inicial automático
)
def construir_graficas_sentimientos(_):
    """Construye las tres gráficas de la página de sentimientos."""

    # Área apilada — evolución temporal
    grafica_area = go.Figure()
    grafica_area.add_trace(go.Scatter(
        x=fechas, y=conteo_pos,
        name="Positivo",
        stackgroup="uno",
        fill="tonexty",
        line=dict(color="#00d4aa"),
    ))
    grafica_area.add_trace(go.Scatter(
        x=fechas, y=conteo_neg,
        name="Negativo",
        stackgroup="uno",
        fill="tonexty",
        line=dict(color="#ff6b6b"),
    ))
    grafica_area.add_trace(go.Scatter(
        x=fechas, y=conteo_neu,
        name="Neutro",
        stackgroup="uno",
        fill="tonexty",
        line=dict(color="#ffd166"),
    ))
    grafica_area.update_layout(
        title="Evolución de Sentimientos (últimos 30 días)",
        **diseno_oscuro(),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
    )

    # Donut — distribución general
    grafica_donut = go.Figure(
        go.Pie(
            labels=list(resumen_general.keys()),
            values=list(resumen_general.values()),
            hole=0.5,
            marker=dict(colors=["#00d4aa", "#ff6b6b", "#ffd166"]),
        )
    )
    grafica_donut.update_layout(
        title="Distribución General de Polaridad",
        **diseno_oscuro(),
    )

    # Dispersión — positivo vs negativo por día
    grafica_dispersion = go.Figure(
        go.Scatter(
            x=conteo_pos,
            y=conteo_neg,
            mode="markers",
            marker=dict(
                color=conteo_neu,
                colorscale="RdYlGn",
                size=10,
                showscale=True,
                colorbar=dict(title="Neutro"),
            ),
            text=[str(fecha.date()) for fecha in fechas],
        )
    )
    grafica_dispersion.update_layout(
        title="Positivo vs Negativo por día",
        **diseno_oscuro(),
        xaxis_title="% Positivo",
        yaxis_title="% Negativo",
    )

    return grafica_area, grafica_donut, grafica_dispersion


def diseno_oscuro():
    """Retorna los parámetros de diseño oscuro comunes a todas las gráficas."""
    return dict(
        paper_bgcolor="#151c2c",
        plot_bgcolor="#1e2738",
        font=dict(color="#c9d4e8", family="'Courier New', monospace"),
        margin=dict(l=20, r=20, t=50, b=20),
    )