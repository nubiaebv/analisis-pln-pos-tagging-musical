import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go
import plotly.express as px


class analisis_emocional:
    def __init__(self, df):
        # Hacemos una copia profunda para no afectar otros componentes
        self.df = df.copy()
        self.normalizar_columnas_criticas()

    def normalizar_columnas_criticas(self):
        """
        Esta función es la clave. Busca las columnas sin importar si tienen
        mayúsculas, minúsculas o nombres del pipeline.
        """
        # Mapeo de posibles nombres que vienen del notebook o del CSV
        mapa = {
            'Subjetividad': 'subjetividad',
            'Polaridad': 'polaridad',
            'sentiment_subjectivity': 'subjetividad',
            'sentiment_polarity': 'polaridad',
            'Genero': 'genero'
        }

        # Renombrar columnas existentes
        self.df = self.df.rename(columns=lambda x: mapa.get(x, x))

        # Asegurar que sean tipos numéricos (crucial para .corr() y .mean())
        for col in ['polaridad', 'subjetividad']:
            if col in self.df.columns:
                self.df[col] = pd.to_numeric(self.df[col], errors='coerce').fillna(0)
            else:
                # Si no existe, la creamos vacía para que el código no explote
                self.df[col] = 0.0

    def extraer_pos_tags(self, pos_string):
        if pd.isna(pos_string): return []
        return re.findall(r",\s*'([^']+)'\)", str(pos_string))

    def preparar_datos(self):
        if self.df.empty: return None

        # Procesamiento de POS
        self.df['pos_list'] = self.df['Lematizado'].apply(self.extraer_pos_tags)

        def calcular_metricas_emocionales(pos_list):
            if not pos_list: return pd.Series([0.0, 0.0, 0.0])
            n_tokens = len(pos_list)
            n_adj = sum(1 for tag in pos_list if tag == 'ADJ')
            n_verb = sum(1 for tag in pos_list if tag == 'VERB')
            n_adv = sum(1 for tag in pos_list if tag == 'ADV')

            densidad_adj = (n_adj / n_tokens) * 100 if n_tokens > 0 else 0
            complejidad_sin = ((n_adj + n_adv) / n_tokens) * 100 if n_tokens > 0 else 0
            return pd.Series([densidad_adj, float(n_verb), complejidad_sin])

        # Aplicamos cálculos
        self.df[['densidad_adj', 'n_verbos', 'complejidad_sintactica']] = \
            self.df['pos_list'].apply(calcular_metricas_emocionales)

        # Filtrado por volumen de datos (igual que tu notebook)
        col_gen = 'genero' if 'genero' in self.df.columns else 'Genero'
        if col_gen in self.df.columns:
            conteo = self.df[col_gen].value_counts()
            generos_top = conteo[conteo > 50].index
            self.df = self.df[self.df[col_gen].isin(generos_top)]

        return self.df

    def grafico_barras_emocion_genero(self):
        col_gen = 'genero' if 'genero' in self.df.columns else 'Genero'

        # El error KeyError: 'subjetividad' morirá aquí gracias a normalizar_columnas_criticas()
        resumen = self.df.groupby(col_gen)[['subjetividad', 'densidad_adj']].mean().reset_index()
        resumen = resumen.sort_values('subjetividad', ascending=False)

        fig = px.bar(
            resumen, x=col_gen, y='subjetividad',
            color='densidad_adj',
            title='Subjetividad Media por Género vs. Uso de Adjetivos',
            color_continuous_scale='Viridis'
        )
        return fig

    def grafico_heatmap_emocional(self):
        cols = ['polaridad', 'subjetividad', 'densidad_adj', 'n_verbos', 'complejidad_sintactica']
        # Solo usamos las que existen realmente
        existing_cols = [c for c in cols if c in self.df.columns]

        if len(existing_cols) < 2:
            return go.Figure().update_layout(title="Datos insuficientes para correlación")

        corr_matrix = self.df[existing_cols].corr()
        return px.imshow(corr_matrix, text_auto=".3f", title="Correlaciones Gramático-Emocionales",
                         color_continuous_scale='RdBu_r')

    def grafico_dispersion_sentimiento(self):
        return px.scatter(self.df, x='polaridad', y='subjetividad', color='densidad_adj',
                          title="Sentimiento vs Adjetivación")