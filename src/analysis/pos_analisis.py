import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


class pos_analisis:
    def __init__(self, df):
        self.df = df
        self.todos_pos_tags = []
        self.pos_counts_sorted = {}

    def extraer_todos_pos_tags(self, columna_pos='Lematizado'):
        """
        Extrae los tags asumiendo que la columna contiene una lista de tuplas
        o estructuras donde el segundo elemento es el tag.
        """
        print("Extrayendo POS tags de todas las canciones...")
        tags_recolectados = []

        for lista_tuplas in self.df[columna_pos]:
            # Verificación de seguridad para evitar errores si hay nulos
            if isinstance(lista_tuplas, list):
                for tupla in lista_tuplas:
                    # Según tu código: el segundo elemento es el tag (tupla[1])
                    if len(tupla) >= 2:
                        tags_recolectados.append(tupla[1])

        self.todos_pos_tags = tags_recolectados

        # Contar y ordenar frecuencias
        pos_counts = Counter(self.todos_pos_tags)
        self.pos_counts_sorted = dict(sorted(pos_counts.items(), key=lambda x: x[1], reverse=True))

        print(f"✓ Total de palabras analizadas: {len(self.todos_pos_tags):,}")
        print(f"✓ Tipos de POS tags encontrados: {len(self.pos_counts_sorted)}")

        return self.todos_pos_tags

    def generar_grafico_distribucion(self):
        """
        Crea la visualización de barras y retorna el objeto Figure.
        """
        if not self.pos_counts_sorted:
            self.extraer_todos_pos_tags()

        # Configuración de la figura
        fig, ax = plt.subplots(figsize=(14, 7))

        pos_names = list(self.pos_counts_sorted.keys())
        pos_values = list(self.pos_counts_sorted.values())

        # Colores y barras
        colors = plt.cm.Set3(range(len(pos_names)))
        bars = ax.bar(pos_names, pos_values, color=colors, edgecolor='black', linewidth=1.5)

        # Agregar etiquetas de valor sobre las barras
        for bar in bars:
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width() / 2., height,
                    f'{int(height):,}',
                    ha='center', va='bottom', fontweight='bold', fontsize=9)

        # Formateo de etiquetas y títulos
        ax.set_xlabel('Categoría Gramatical (POS)', fontsize=12, fontweight='bold')
        ax.set_ylabel('Frecuencia', fontsize=12, fontweight='bold')
        ax.set_title(f'Distribución de Etiquetas POS en {len(self.df):,} Canciones',
                     fontsize=14, fontweight='bold')

        ax.grid(axis='y', alpha=0.3, linestyle='--')
        plt.xticks(rotation=45, ha='right')
        plt.tight_layout()

        # Cerramos el plot para que no se muestre automáticamente
        plt.close(fig)
        return fig