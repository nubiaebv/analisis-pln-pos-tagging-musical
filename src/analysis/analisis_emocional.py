import pandas as pd
import numpy as np
import re
from collections import Counter, defaultdict
from scipy.stats import pearsonr, spearmanr, f_oneway
from scipy.stats import chi2_contingency
import spacy
from textblob import TextBlob
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import warnings


class analisis_emocional:
    """Encapsula toda la lógica de cálculo y generación de gráficos Plotly."""

    # Verbos de estado comunes en inglés
    _VERBOS_ESTADO = {
        "be", "am", "is", "are", "was", "were", "been", "being",
        "seem", "appear", "look", "feel", "sound", "taste", "smell",
        "remain", "stay", "become", "exist", "have", "own", "possess",
        "know", "believe", "think", "understand", "love", "hate", "want", "need",
    }

    _PALABRAS_POSITIVAS = {
        "love", "happy", "joy", "beautiful", "good", "amazing", "wonderful",
        "great", "perfect", "smile", "dream", "hope", "light", "heaven",
        "sweet", "forever", "together", "free", "peace", "bright",
    }

    _PALABRAS_NEGATIVAS = {
        "hate", "sad", "pain", "hurt", "broken", "cry", "dark", "lost",
        "alone", "empty", "fear", "death", "hell", "wrong", "bad",
        "never", "die", "goodbye", "end", "tear",
    }

    def __init__(self, df: pd.DataFrame):
        self._nlp = spacy.load("en_core_web_sm")
        self._df = df.copy()
        self._calcular_metricas()

    # ------------------------------------------------------------------
    # Helpers de cálculo (idénticos al notebook)
    # ------------------------------------------------------------------

    def _extraer_pos_tags(self, pos_string):
        """Extrae las etiquetas POS de una cadena de texto."""
        if pd.isna(pos_string):
            return []
        return re.findall(r",\s*'([^']+)'\)", str(pos_string))

    def _calcular_densidad_adjetivos(self, pos_list):
        """Calcula la densidad de adjetivos (Adjetivos / total tokens)."""
        if not pos_list:
            return 0
        adjetivos = sum(1 for tag in pos_list if tag == "ADJ")
        return (adjetivos / len(pos_list) * 100) if pos_list else 0

    def _calcular_ratio_verbos_accion_estado(self, texto):
        """Calcula el ratio entre verbos de acción y verbos de estado."""
        if pd.isna(texto):
            return 0
        doc = self._nlp(str(texto))
        accion, estado = 0, 0
        for token in doc:
            if token.pos_ in ["VERB", "AUX"]:
                if token.lemma_.lower() in self._VERBOS_ESTADO:
                    estado += 1
                else:
                    accion += 1
        return accion / estado if estado > 0 else accion

    def _calcular_complejidad_sintactica(self, pos_list):
        """Calcula un índice de complejidad sintáctica (ADJ + ADV + SCONJ)."""
        if not pos_list:
            return 0
        complejos = sum(1 for tag in pos_list if tag in ["ADJ", "ADV", "SCONJ"])
        return (complejos / len(pos_list) * 100) if pos_list else 0

    def _analizar_polaridad_emocional(self, texto):
        """Retorna (polaridad, subjetividad) usando TextBlob."""
        if pd.isna(texto):
            return 0, 0
        try:
            blob = TextBlob(str(texto))
            return blob.sentiment.polarity, blob.sentiment.subjectivity
        except Exception:
            return 0, 0

    def _categorizar_emocion(self, polaridad):
        """Categoriza la emoción en Positiva / Neutral / Negativa."""
        if polaridad > 0.3:
            return "Positiva"
        elif polaridad < -0.3:
            return "Negativa"
        return "Neutral"

    def _calcular_intensidad_emocional(self, subjetividad, densidad_adj):
        """Índice de intensidad emocional: subjetividad × 0.6 + densidad_adj × 0.4."""
        return subjetividad * 0.6 + (densidad_adj / 100) * 0.4

    def _contar_palabras_emocionales(self, texto, pos_list):
        """Cuenta palabras emocionales positivas y negativas (%)."""
        if pd.isna(texto):
            return 0, 0
        doc = self._nlp(str(texto).lower())
        positivas = sum(1 for t in doc if t.lemma_ in self._PALABRAS_POSITIVAS)
        negativas = sum(1 for t in doc if t.lemma_ in self._PALABRAS_NEGATIVAS)
        total = len(pos_list) if pos_list else 1
        return (positivas / total * 100), (negativas / total * 100)

    # ------------------------------------------------------------------
    # Pipeline principal de cálculo
    # ------------------------------------------------------------------

    def _calcular_metricas(self):
        df = self._df

        # POS tags
        df["pos_list"] = df["Lematizado"].apply(self._extraer_pos_tags)

        # Morfosintácticas
        df["densidad_adjetivos"] = df["pos_list"].apply(self._calcular_densidad_adjetivos)
        df["ratio_verbos_accion_estado"] = df["letra_cancion"].apply(
            self._calcular_ratio_verbos_accion_estado
        )
        df["complejidad_sintactica"] = df["pos_list"].apply(
            self._calcular_complejidad_sintactica
        )

        # Emocionales
        df[["polaridad", "subjetividad"]] = df["letra_cancion"].apply(
            lambda x: pd.Series(self._analizar_polaridad_emocional(x))
        )
        df["categoria_emocional"] = df["polaridad"].apply(self._categorizar_emocion)
        df["intensidad_emocional"] = df.apply(
            lambda r: self._calcular_intensidad_emocional(
                r["subjetividad"], r["densidad_adjetivos"]
            ),
            axis=1,
        )

        # Palabras emocionales
        df[["pct_palabras_positivas", "pct_palabras_negativas"]] = df.apply(
            lambda r: pd.Series(
                self._contar_palabras_emocionales(r["letra_cancion"], r["pos_list"])
            ),
            axis=1,
        )

        self._df = df
        self._variables_morfosintacticas = [
            "densidad_adjetivos",
            "ratio_verbos_accion_estado",
            "complejidad_sintactica",
        ]
        self._variables_emocionales = ["polaridad", "subjetividad", "intensidad_emocional"]
        self._categorias = ["Positiva", "Neutral", "Negativa"]

    # ------------------------------------------------------------------
    # Gráfico 1: Dispersión – relaciones bivariadas morfosintaxis ↔ emoción
    # ------------------------------------------------------------------

    def grafico_dispersion_sentimiento(self) -> go.Figure:
        """
        Scatter plots (2×3) de relaciones entre variables morfosintácticas
        y emocionales, coloreadas por categoría emocional.
        Equivalente al gráfico de matplotlib de la sección 8 del notebook.
        """
        df = self._df
        categorias = self._categorias
        colores = {"Positiva": "#2ecc71", "Neutral": "#f39c12", "Negativa": "#e74c3c"}

        relaciones = [
            ("densidad_adjetivos", "polaridad", "Densidad de Adjetivos", "Polaridad Emocional"),
            ("densidad_adjetivos", "subjetividad", "Densidad de Adjetivos", "Subjetividad"),
            (
                "ratio_verbos_accion_estado",
                "polaridad",
                "Ratio V.Acción/Estado",
                "Polaridad Emocional",
            ),
            (
                "ratio_verbos_accion_estado",
                "intensidad_emocional",
                "Ratio V.Acción/Estado",
                "Intensidad Emocional",
            ),
            (
                "complejidad_sintactica",
                "subjetividad",
                "Complejidad Sintáctica",
                "Subjetividad",
            ),
            (
                "complejidad_sintactica",
                "intensidad_emocional",
                "Complejidad Sintáctica",
                "Intensidad Emocional",
            ),
        ]

        fig = make_subplots(
            rows=2,
            cols=3,
            subplot_titles=[f"{lx} vs {ly}" for _, _, lx, ly in relaciones],
            horizontal_spacing=0.08,
            vertical_spacing=0.12,
        )

        categorias_ya_en_leyenda = set()

        for idx, (var_x, var_y, label_x, label_y) in enumerate(relaciones):
            row, col = divmod(idx, 3)
            row += 1
            col += 1

            df_plot = df[[var_x, var_y, "categoria_emocional"]].dropna()

            for cat in categorias:
                df_cat = df_plot[df_plot["categoria_emocional"] == cat]
                show_legend = cat not in categorias_ya_en_leyenda
                categorias_ya_en_leyenda.add(cat)

                fig.add_trace(
                    go.Scatter(
                        x=df_cat[var_x],
                        y=df_cat[var_y],
                        mode="markers",
                        marker=dict(color=colores[cat], size=4, opacity=0.5),
                        name=cat,
                        legendgroup=cat,
                        showlegend=show_legend,
                    ),
                    row=row,
                    col=col,
                )

            # Línea de tendencia
            z = np.polyfit(df_plot[var_x], df_plot[var_y], 1)
            x_line = np.linspace(df_plot[var_x].min(), df_plot[var_x].max(), 100)
            corr, p_val = pearsonr(df_plot[var_x], df_plot[var_y])

            fig.add_trace(
                go.Scatter(
                    x=x_line,
                    y=np.polyval(z, x_line),
                    mode="lines",
                    line=dict(color="red", dash="dash", width=2),
                    name=f"Tendencia (r={corr:.3f})",
                    showlegend=False,
                ),
                row=row,
                col=col,
            )

            # Actualizar ejes
            fig.update_xaxes(title_text=label_x, row=row, col=col)
            fig.update_yaxes(title_text=label_y, row=row, col=col)

            # Anotar correlación en el título del subplot
            fig.layout.annotations[idx].text = (
                f"{label_x} vs {label_y}<br>"
                f"<sub>r={corr:.3f}, p={'<0.001' if p_val < 0.001 else f'{p_val:.4f}'}</sub>"
            )

        fig.update_layout(
            title=dict(
                text="Relaciones Bivariadas: Morfosintaxis ↔ Sentimiento",
                font=dict(size=18, family="Arial Black"),
                x=0.5,
            ),
            height=700,
            template="plotly_white",
            legend=dict(
                title="Categoría emocional",
                orientation="h",
                yanchor="bottom",
                y=-0.15,
                xanchor="center",
                x=0.5,
            ),
        )

        return fig

    # ------------------------------------------------------------------
    # Gráfico 2: Barras – distribución emocional por género
    # ------------------------------------------------------------------

    def grafico_barras_emocion_genero(self) -> go.Figure:
        """
        Gráfico de barras apiladas (%) de categorías emocionales por género musical.
        Equivalente al heatmap de distribución de la sección 7 del notebook,
        reformulado como barras para mayor legibilidad.
        """
        df = self._df
        categorias = self._categorias
        colores = {"Positiva": "#2ecc71", "Neutral": "#f39c12", "Negativa": "#e74c3c"}

        distribucion = (
                pd.crosstab(df["Genero"], df["categoria_emocional"], normalize="index") * 100
        )
        # Asegurar orden de columnas
        for cat in categorias:
            if cat not in distribucion.columns:
                distribucion[cat] = 0
        distribucion = distribucion[categorias]
        distribucion = distribucion.sort_values("Positiva", ascending=True)

        fig = go.Figure()

        for cat in categorias:
            fig.add_trace(
                go.Bar(
                    name=cat,
                    y=distribucion.index,
                    x=distribucion[cat],
                    orientation="h",
                    marker_color=colores[cat],
                    text=distribucion[cat].round(1).astype(str) + "%",
                    textposition="inside",
                    insidetextanchor="middle",
                )
            )

        fig.update_layout(
            barmode="stack",
            title=dict(
                text="Distribución de Categorías Emocionales por Género Musical",
                font=dict(size=18, family="Arial Black"),
                x=0.5,
            ),
            xaxis=dict(title="Porcentaje (%)", range=[0, 100]),
            yaxis=dict(title="Género Musical"),
            legend=dict(
                title="Categoría emocional",
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5,
            ),
            height=480,
            template="plotly_white",
        )

        return fig

    # ------------------------------------------------------------------
    # Gráfico 3: Heatmap – correlación morfosintaxis ↔ emoción
    # ------------------------------------------------------------------

    def grafico_heatmap_emocional(self) -> go.Figure:
        """
        Heatmap de correlaciones de Pearson entre variables morfosintácticas
        y emocionales. Equivalente al heatmap de la sección 5 del notebook.
        """
        df = self._df
        vars_morfo = self._variables_morfosintacticas
        vars_emoc = self._variables_emocionales

        df_corr = df[vars_morfo + vars_emoc].dropna()
        matriz = df_corr.corr().loc[vars_morfo, vars_emoc]

        # Etiquetas más legibles
        labels_morfo = [
            "Densidad Adjetivos",
            "Ratio Verbos A/E",
            "Complejidad Sintáctica",
        ]
        labels_emoc = ["Polaridad", "Subjetividad", "Intensidad Emocional"]

        # Calcular p-values para anotaciones
        anotaciones = []
        for i, vm in enumerate(vars_morfo):
            for j, ve in enumerate(vars_emoc):
                data = df_corr[[vm, ve]].dropna()
                corr_val, p_val = pearsonr(data[vm], data[ve])
                sig = "***" if p_val < 0.001 else "**" if p_val < 0.01 else "*" if p_val < 0.05 else ""
                anotaciones.append(
                    dict(
                        x=labels_emoc[j],
                        y=labels_morfo[i],
                        text=f"{corr_val:.3f}{sig}",
                        showarrow=False,
                        font=dict(size=14, color="white" if abs(corr_val) > 0.3 else "black"),
                    )
                )

        fig = go.Figure(
            data=go.Heatmap(
                z=matriz.values,
                x=labels_emoc,
                y=labels_morfo,
                colorscale="RdBu_r",
                zmid=0,
                zmin=-1,
                zmax=1,
                colorbar=dict(title="r de Pearson"),
                hoverongaps=False,
                hovertemplate="<b>%{y}</b> ↔ <b>%{x}</b><br>r = %{z:.3f}<extra></extra>",
            )
        )

        fig.update_layout(
            title=dict(
                text="Correlación: Estructura Morfosintáctica ↔ Emocionalidad<br>"
                     "<sub>* p&lt;0.05  ** p&lt;0.01  *** p&lt;0.001</sub>",
                font=dict(size=17, family="Arial Black"),
                x=0.5,
            ),
            annotations=anotaciones,
            xaxis=dict(title="Variables Emocionales", tickfont=dict(size=13)),
            yaxis=dict(title="Variables Morfosintácticas", tickfont=dict(size=13)),
            height=420,
            template="plotly_white",
        )

        return fig

