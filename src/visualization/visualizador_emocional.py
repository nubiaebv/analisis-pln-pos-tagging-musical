from src.analysis.analisis_emocional import analisis_emocional

class visualizador_emocional:
    def __init__(self, df):
        self._analisis = analisis_emocional(df)
        self._analisis.preparar_datos()

    def grafico_dispersion_sentimiento(self):
        return self._analisis.grafico_dispersion_sentimiento()

    def grafico_barras_emocion_genero(self):
        return self._analisis.grafico_barras_emocion_genero()

    def grafico_heatmap_emocional(self):
       return self._analisis.grafico_heatmap_emocional()
