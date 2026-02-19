from src.analysis.evolucion_temporal import evolucion_temporal

class visualizador_evolucion:
    def __init__(self, df):
        self._analisis = evolucion_temporal(df)
        self._analisis.preparar_datos()

    def grafico_evolucion_complejidad(self):
        return self._analisis.grafico_evolucion_complejidad()

    def grafico_distribucion_longitud(self):
        return self._analisis.grafico_distribucion_longitud()
    def grafico_heatmap_correlacion(self):
        return self._analisis.grafico_heatmap_correlacion()