from src.analysis.pos_analisis import pos_analisis

class visualizador_pos():
    def __init__(self, df):
        self._analisis = pos_analisis(df)

    def generar_grafico_distribucion(self):
        return self._analisis.generar_grafico_distribucion()