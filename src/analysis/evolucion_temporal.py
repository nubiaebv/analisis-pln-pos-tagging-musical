import pandas as pd
import numpy as np
import re
import plotly.graph_objects as go
import plotly.express as px
from scipy.stats import pearsonr


class evolucion_temporal:
    def __init__(self, df):
        # Mantenemos el filtrado original del notebook
        self.df = df[df['Periodo'] >= 1980.0].copy()
        self.tendencias_anuales = None

    def extraer_pos_tags(self, pos_string):
        if pd.isna(pos_string): return []
        return re.findall(r",\s*'([^']+)'\)", str(pos_string))

    def extraer_palabras(self, tokens_string):
        if pd.isna(tokens_string): return []
        return re.findall(r"'([^']+)'", str(tokens_string))

    def calcular_complejidad_gramatical(self, pos_list):
        if not pos_list: return 0
        # Lógica original: (ADJ + ADV + SCONJ + CCONJ) / total
        complejas = sum(1 for tag in pos_list if tag in ['ADJ', 'ADV', 'SCONJ', 'CCONJ'])
        return complejas / len(pos_list)

    def calcular_diversidad_lexica(self, palabras):
        if not palabras: return 0
        return len(set(palabras)) / len(palabras)

    def calcular_longitud_promedio_oracion(self, pos_list):
        if not pos_list: return 0
        puntuaciones = sum(1 for tag in pos_list if tag == 'PUNCT')
        return len(pos_list) / puntuaciones if puntuaciones > 0 else len(pos_list)

    def categorizar_periodo(self, year):
        if pd.isna(year): return 'Desconocido'
        year = int(year)
        if year < 1990:
            return 'Pre-90s'
        elif 1990 <= year < 2000:
            return '90s'
        elif 2000 <= year < 2010:
            return '2000s'
        elif 2010 <= year < 2020:
            return '2010s'
        return '2020s'

    def preparar_datos(self):
        """Aplica las métricas al dataframe."""
        if self.df.empty: return None

        # Procesamiento idéntico al notebook
        self.df['pos_list'] = self.df['Lematizado'].apply(self.extraer_pos_tags)
        self.df['palabras_list'] = self.df['tokens'].apply(self.extraer_palabras)

        self.df['complejidad_gramatical'] = self.df['pos_list'].apply(self.calcular_complejidad_gramatical)
        self.df['diversidad_lexica'] = self.df['palabras_list'].apply(self.calcular_diversidad_lexica)
        self.df['longitud_oracion'] = self.df['pos_list'].apply(self.calcular_longitud_promedio_oracion)
        self.df['Periodo_Categoria'] = self.df['Periodo'].apply(self.categorizar_periodo)

        # Agrupación anual para tendencias
        self.tendencias_anuales = self.df.groupby('Periodo').agg({
            'complejidad_gramatical': 'mean',
            'diversidad_lexica': 'mean',
            'longitud_oracion': 'mean'
        }).reset_index().sort_values('Periodo')

        return self.df

    def grafico_evolucion_complejidad(self):
        """Replica el gráfico de líneas con tendencia de Pearson."""
        df_plot = self.tendencias_anuales
        x, y = df_plot['Periodo'], df_plot['complejidad_gramatical']
        corr, _ = pearsonr(x, y)
        z = np.polyfit(x, y, 1)
        p = np.poly1d(z)

        fig = go.Figure()
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers', name='Complejidad', line=dict(color='#00d1ff')))
        fig.add_trace(go.Scatter(x=x, y=p(x), mode='lines', name=f'Tendencia (r={corr:.3f})',
                                 line=dict(dash='dash', color='red')))

        fig.update_layout(title="Evolución de la Complejidad Gramatical")
        return fig

    def grafico_distribucion_longitud(self):
        """Genera un Boxplot por década."""
        orden = ['Pre-90s', '90s', '2000s', '2010s', '2020s']
        # Filtrar solo periodos presentes para evitar errores de eje
        periodos_presentes = [p for p in orden if p in self.df['Periodo_Categoria'].unique()]

        fig = px.box(
            self.df, x="Periodo_Categoria", y="longitud_oracion",
            category_orders={"Periodo_Categoria": periodos_presentes},
            title="Distribución de Longitud de Oración por Década",
            color="Periodo_Categoria"
        )
        return fig

    def grafico_heatmap_correlacion(self):
        """Genera el heatmap de correlación entre métricas."""
        cols = ['complejidad_gramatical', 'diversidad_lexica', 'longitud_oracion', 'Periodo']
        corr_matrix = self.df[cols].corr()

        fig = px.imshow(
            corr_matrix,
            text_auto=".2f",
            aspect="auto",
            title="Mapa de Calor de Correlaciones",
            color_continuous_scale='RdBu_r'
        )
        return fig