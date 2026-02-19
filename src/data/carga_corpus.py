"""
Clase: carga_corpus

Objetivo: Py con funciones para cargar corpus

Cambios:

"""
import pandas as pd

from src.utils import path

class carga_corpus:
    def __init__(self):
        self._directorio_proyecto = path.obtener_ruta_local()

    def cargar_corpus(self, ruta):
        return pd.read_csv(self._directorio_proyecto+ruta,delimiter = ',',decimal = ".", encoding='utf-8')
    def guardar_corpus(self,ruta, df):
        df.to_csv(self._directorio_proyecto + ruta, index=False)