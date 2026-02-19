from src.analysis.comparacion_generos import comparacion_generos

class visualizador_generos:
    def __init__(self, df):
        self._analisis = comparacion_generos(df)
        self._analisis.preparar_datos()


    def grafico_barras_comparativo(self, top_n=10):
        return self._analisis.grafico_barras_comparativo()

    def grafico_dispersion_densidad(self):
        return self._analisis.grafico_dispersion_densidad()
    def grafico_distribucion_tokens(self):
        return self._analisis.grafico_distribucion_tokens()
