import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go
import plotly.express as px


class comparacion_generos:
    def __init__(self, df):
        self.df = df.copy()
        self.resumen_generos = None

    def extraer_pos_tags(self, pos_string):
        if pd.isna(pos_string): return []
        return re.findall(r",\s*'([^']+)'\)", str(pos_string))

    def preparar_datos(self):
        """Replica la lógica de filtrado y cálculo del notebook 05."""
        if self.df.empty: return None

        # 1. Extraer POS tags
        self.df['pos_list'] = self.df['Lematizado'].apply(self.extraer_pos_tags)

        # 2. Cálculos de métricas por canción (Lógica original)
        def calcular_metricas_row(pos_list):
            if not pos_list: return pd.Series([0, 0, 0, 0])

            n_tokens = len(pos_list)
            n_subs = sum(1 for tag in pos_list if tag == 'NOUN')
            n_verbs = sum(1 for tag in pos_list if tag == 'VERB')
            n_pron = sum(1 for tag in pos_list if tag == 'PRON')
            n_adj_adv = sum(1 for tag in pos_list if tag in ['ADJ', 'ADV'])

            ratio_sv = n_subs / n_verbs if n_verbs > 0 else n_subs
            densidad = (n_subs + n_verbs + n_adj_adv) / n_tokens if n_tokens > 0 else 0
            pct_pron = (n_pron / n_tokens) * 100 if n_tokens > 0 else 0

            return pd.Series([n_tokens, ratio_sv, densidad, pct_pron])

        self.df[['n_tokens', 'ratio_sv', 'densidad_lexica', 'pct_pronombres']] = \
            self.df['pos_list'].apply(calcular_metricas_row)

        # 3. Filtrar géneros con más de 50 canciones (Tu criterio original)
        conteo_generos = self.df['Genero'].value_counts()
        generos_top = conteo_generos[conteo_generos > 50].index
        self.df = self.df[self.df['Genero'].isin(generos_top)]

        # 4. Agregación para tabla resumen
        self.resumen_generos = self.df.groupby('Genero').agg({
            'nombre_cancion': 'count',
            'n_tokens': 'mean',
            'ratio_sv': 'mean',
            'densidad_lexica': 'mean',
            'pct_pronombres': 'mean'
        }).reset_index()

        return self.df

    def grafico_barras_comparativo(self):
        """Gráfico de barras para Ratio Sustantivo/Verbo por Género."""
        df_sorted = self.resumen_generos.sort_values('ratio_sv', ascending=False)
        fig = px.bar(
            df_sorted, x='Genero', y='ratio_sv',
            title='Ratio Sustantivo/Verbo por Género',
            labels={'ratio_sv': 'Ratio S/V'},
            color='ratio_sv',
            color_continuous_scale='Viridis'
        )
        return fig

    def grafico_dispersion_densidad(self):
        """Gráfico de dispersión: Densidad Léxica vs % Pronombres."""
        fig = px.scatter(
            self.resumen_generos,
            x='densidad_lexica',
            y='pct_pronombres',
            text='Genero',
            size='nombre_cancion',
            color='Genero',
            title='Densidad Léxica vs. Uso de Pronombres (Tamaño = N° Canciones)'
        )
        fig.update_traces(textposition='top center')
        return fig

    def grafico_distribucion_tokens(self):
        """Boxplot de longitud de canciones por género."""
        fig = px.box(
            self.df, x='Genero', y='n_tokens',
            title='Distribución de Longitud (Tokens) por Género',
            color='Genero'
        )
        return fig