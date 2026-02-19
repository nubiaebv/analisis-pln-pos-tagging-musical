# 🎵 Análisis Morfosintáctico de Letras Musicales con POS Tagging

> Proyecto académico de Procesamiento de Lenguaje Natural (PLN) que aplica técnicas de **Part-of-Speech (POS) Tagging** sobre letras de canciones para identificar patrones gramaticales según el género musical, complementado con un **dashboard analítico interactivo** y análisis exploratorio de datos (EDA).

![Python](https://img.shields.io/badge/Python-3.9+-blue?logo=python&logoColor=white)
![NLTK](https://img.shields.io/badge/NLTK-3.8+-green)
![spaCy](https://img.shields.io/badge/spaCy-3.x-09A3D5?logo=spacy&logoColor=white)
![Estado](https://img.shields.io/badge/Estado-En%20desarrollo-yellow)
![Uso de IA](https://img.shields.io/badge/IA%20utilizada-Claude%20%7C%20Gemini%20%7C%20Copilot-blueviolet)

---

##  Tabla de Contenidos

- [Descripción del Proyecto](#-descripción-del-proyecto)
- [Objetivos](#-objetivos)
- [Tecnologías Utilizadas](#-tecnologías-utilizadas)
- [Estructura del Repositorio](#-estructura-del-repositorio)
- [Instalación y Configuración](#-instalación-y-configuración)
- [Uso](#-uso)
- [Metodología](#-metodología)
- [Dashboard Analítico](#-dashboard-analítico)
- [Resultados Esperados](#-resultados-esperados)
- [Uso de Inteligencia Artificial](#-uso-de-inteligencia-artificial)
- [Autor](#-autor)


---

##  Descripción del Proyecto

Este proyecto forma parte de un análisis lingüístico computacional orientado a explorar cómo varía el uso gramatical en distintos géneros musicales. A través del **etiquetado morfosintáctico (POS Tagging)**, se identifican y comparan categorías gramaticales como sustantivos, verbos, adjetivos, pronombres y adverbios presentes en las letras de canciones.

El análisis se lleva a cabo utilizando dos de las bibliotecas más reconocidas en el campo del PLN:

- **NLTK** (*Natural Language Toolkit*) — para tokenización y etiquetado clásico.
- **spaCy** — para un etiquetado más moderno, eficiente y con soporte multilingüe.

Los resultados se presentan a través de un **dashboard analítico interactivo** que facilita la exploración visual de los patrones encontrados.

---

##  Objetivos

- Aplicar técnicas de POS Tagging sobre corpus de letras musicales.
- Realizar un análisis exploratorio de datos (EDA) sobre las características lingüísticas del corpus.
- Comparar los resultados entre NLTK y spaCy en términos de precisión y cobertura.
- Identificar patrones gramaticales diferenciadores entre géneros musicales.
- Visualizar los hallazgos a través de un dashboard analítico interactivo.
- Documentar de forma transparente el uso de herramientas de IA durante el desarrollo del proyecto.

---

##  Tecnologías Utilizadas

| Herramienta | Versión recomendada | Propósito |
|-------------|---------------------|-----------|
| Python | 3.9+ | Lenguaje base del proyecto |
| NLTK | 3.8+ | Tokenización y POS Tagging clásico |
| spaCy | 3.x | POS Tagging avanzado y multilingüe |
| Pandas | 2.x | Manipulación y análisis de datos |
| Matplotlib / Seaborn | — | Visualización estática de resultados |
| Plotly / Dash | — | Dashboard analítico interactivo |
| Jupyter Notebook | — | Entorno de desarrollo interactivo |

---

##  Estructura del Repositorio

```
analisis-pln-pos-tagging-musical/
│
├── dashboard/                            # Dashboard analítico con Streamlit
│   ├── assets/
│   │   └── Style.css                     # Estilos personalizados
│   ├── pages/
│   │   ├── Comparacion.py                # Vista: comparación entre géneros
│   │   ├── Emociones.py                  # Vista: análisis emocional
│   │   ├── Evolucion.py                  # Vista: evolución temporal
│   │   └── inicio.py                     # Vista: resumen general
│   └── app.py                            # Punto de entrada del dashboard
│
├── data/
│   ├── processed/
│   │   └── corpus_canciones.csv          # Corpus procesado de letras
│   ├── raw/                              # Letras originales sin procesar
│   └── results/
│       ├── corpus_canciones_nltk.csv     # Resultados POS Tagging con NLTK
│       ├── corpus_canciones_spacy.csv    # Resultados POS Tagging con spaCy
│       └── corpus_canciones_spicy.csv    # Resultados complementarios
│
├── notebooks/
│   ├── 01_exploracion_datos.ipynb        # Exploración inicial del corpus (EDA)
│   ├── 02_pos_tagging_nltk.ipynb         # POS Tagging con NLTK
│   ├── 03_pos_tagging_spacy.ipynb        # POS Tagging con spaCy
│   ├── 04.1_analisis_morfologico.ipynb   # Análisis morfológico (resumen)
│   ├── 04_analisis_morfologico_nltk.ipynb# Análisis morfológico detallado con NLTK
│   ├── 05_comparacion_generos.ipynb      # Comparación de patrones por género
│   ├── 06_evolucion_temporal.ipynb       # Evolución temporal del lenguaje musical
│   └── 07_emocionalidad_gramatical.ipynb # Análisis de emocionalidad gramatical
│
├── src/
│   ├── analysis/
│   │   ├── analisis_emocional.py         # Módulo de análisis emocional
│   │   ├── comparacion_generos.py        # Módulo de comparación por género
│   │   ├── evolucion_temporal.py         # Módulo de evolución temporal
│   │   └── pos_analisis.py               # Módulo principal de análisis POS
│   ├── data/
│   │   └── carga_corpus.py               # Carga y preprocesamiento del corpus
│   ├── pos_tagging/
│   │   ├── pipeline_nltk.py              # Pipeline de POS Tagging con NLTK
│   │   └── pipeline_spacy.py             # Pipeline de POS Tagging con spaCy
│   ├── utils/
│   │   └── path.py                       # Utilidades de rutas del proyecto
│   └── visualization/
│       ├── visualizador_emocional.py     # Visualizaciones del análisis emocional
│       ├── visualizador_evolucion.py     # Visualizaciones de evolución temporal
│       ├── visualizador_generos.py       # Visualizaciones por género
│       └── visualizador_pos.py           # Visualizaciones del POS Tagging
│
├── tests/                                # Pruebas unitarias del proyecto
│
├── .gitignore
├── README.md
├── USO_DE_IA.md                          # Registro de uso de IA (Claude, Gemini, Copilot)
└── requirements.txt
```

---

## ️ Instalación y Configuración

### 1. Clonar el repositorio

```bash
git clone https://github.com/nubiaebv/analisis-pln-pos-tagging-musical.git
cd analisis-pln-pos-tagging-musical
```

### 2. Crear un entorno virtual (recomendado)

```bash
python -m venv venv
source venv/bin/activate        # macOS / Linux
venv\Scripts\activate           # Windows
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

### 4. Descargar los modelos de NLTK y spaCy

```python
# En Python o en una celda de Jupyter
import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('stopwords')
```

```bash
# Modelo en español de spaCy
python -m spacy download es_core_news_sm

# Modelo en inglés (opcional)
python -m spacy download en_core_web_sm
```

---

##  Uso

### Ejecutar los notebooks de análisis

```bash
jupyter notebook
```

Navega a la carpeta `notebooks/` y ejecuta los archivos para reproducir el EDA y el análisis POS completo.

### Ejecutar el dashboard

```bash
 run dashboard/app.py
```

Abre tu navegador en http://127.0.0.1:8050/ para explorar el dashboard analítico de forma interactiva.

### Ejecutar los scripts de análisis directamente

```bash
python src/nltk_analysis.py
python src/spacy_analysis.py
```

---

##  Metodología

El proyecto sigue las siguientes etapas:

1. **Recopilación del corpus** 
2. **Análisis Exploratorio de Datos (EDA)** 
3. **Preprocesamiento** 
4. **POS Tagging con NLTK** 
5. **POS Tagging con spaCy** 
6. **Análisis comparativo** 
7. **Visualización e interpretación** 
---

##  Dashboard Analítico

El proyecto incluye un **dashboard analítico interactivo** desarrollado en la carpeta `dashboard/`, que permite explorar visualmente los resultados del análisis PLN sin necesidad de ejecutar los notebooks.


Para ejecutarlo, sigue las instrucciones en la sección [Uso](#-uso).

---

##  Resultados Esperados

- Comparación entre Géneros Musicales: Identificar diferencias morfosintácticas entre Rock, Pop, Hip-Hop, Reggaetón y Baladas mediante análisis de POS, densidad léxica y uso de pronombres.

- Evolución Temporal del Lenguaje Musical: Analizar si el lenguaje de las letras se ha simplificado o sofisticado desde los 90s hasta la actualidad usando métricas de complejidad y variedad léxica.

- Emocionalidad Gramatical: Evaluar la relación entre estructura gramatical y carga emocional a partir de adjetivos, tipos de verbos y complejidad sintáctica.

- Dominio Técnico: NLTK vs spaCy: Comparar técnicamente ambas herramientas según etiquetado POS, precisión en español y adecuación al análisis.

- Dashboard Analítico Interactivo: Integrar y visualizar todos los hallazgos en un panel interactivo para facilitar la exploración e interpretación de resultados.

---

##  Uso de Inteligencia Artificial

Este proyecto utilizó herramientas de inteligencia artificial como apoyo durante su desarrollo. Las tareas específicas asistidas por cada herramienta se encuentran documentadas en el archivo:

📄 **[`USO_DE_IA.md`](./USO_DE_IA.md)**

Las herramientas utilizadas incluyen:

| Herramienta |
|-------------|
| **Claude** (Anthropic) |
| **Gemini** (Google) |
| **GitHub Copilot** |

> El uso de IA se documenta con fines de transparencia académica. Todas las decisiones de diseño, análisis e interpretación son responsabilidad de los autores.

---

##  Autores
**Nubia Elena  Brenes Valerín**

**Pablo Andrés Marín Castillo**

---
Proyecto desarrollado como parte del curso Mineria de Textos del diplomado en Big Data CUC

---