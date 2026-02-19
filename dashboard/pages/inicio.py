import dash
from dash import html, dcc, callback, Input, Output, State
import dash_bootstrap_components as dbc

import threading
import io
import re
import sys

try:
    from src.pos_tagging.pipeline_spacy import pipeline_spacy
    _spacy_disponible = True
    _error_importacion_spacy = None
except Exception as excepcion_spacy:
    _spacy_disponible = False
    _error_importacion_spacy = str(excepcion_spacy)

try:
    from src.pos_tagging.pipeline_nltk import pipeline_nltk
    _nltk_disponible = True
    _error_importacion_nltk = None
except Exception as excepcion_nltk:
    _nltk_disponible = False
    _error_importacion_nltk = str(excepcion_nltk)

dash.register_page(__name__, path="/", name="Inicio")

# ── Estado compartido entre el hilo del pipeline y los callbacks ──────────────
# Guardamos los mensajes fijos (logs) y los progresos actuales por separado
# Mensajes de sistema (Cargando modelo, listo, etc.)
logs_sistema = []
# Diccionario para mantener SOLO la última versión de cada paso
# Ejemplo: {"Paso 1": "Barra al 20%", "Paso 2": "Barra al 5%"}
pasos_activos = {}
pipeline_en_ejecucion: bool = False
df_resultado_global = None


# ── Capturador de salida estándar (stdout/stderr) para tqdm ──────────────────

class CapturadorSalidaConsola(io.TextIOBase):
    def write(self, texto: str) -> int:
        global logs_sistema, pasos_activos
        if not texto or not texto.strip():
            return len(texto)

        # 1. Limpiar el desorden de tqdm (\r y múltiples líneas en un envío)
        lineas = re.split(r'[\r\n]+', texto)
        for linea in lineas:
            linea = linea.strip()
            if not linea: continue

            # 2. ¿Es una barra de progreso?
            # Buscamos "Paso X" al inicio de la línea
            match_paso = re.search(r'^(Paso \d+)', linea)

            if match_paso and ("%" in linea or "|" in linea):
                id_paso = match_paso.group(1)
                # Formateamos y GUARDAMOS/REEMPLAZAMOS en el diccionario
                pasos_activos[id_paso] = self._formatear_linea_tqdm(linea)
            else:
                # 3. Si es un mensaje normal, va a la lista de logs permanentes
                # Evitamos duplicar mensajes de "Cargando..." si llegan repetidos
                linea_fmt = self._formatear_linea_tqdm(linea)
                if not logs_sistema or logs_sistema[-1] != linea_fmt:
                    logs_sistema.append(linea_fmt)

        return len(texto)

    def flush(self):
        pass

    @staticmethod
    def _formatear_linea_tqdm(linea: str) -> str:
        """
        Detecta si la línea es una barra tqdm y aplica el HTML formateado.
        Ejemplo de línea tqdm:
          Paso 1 Tokenización: 100%|██████████| 500/500 [00:03<00:00, 142.it/s]
        """
        # Patrón: "<descripción>: <porcentaje>%|<barra>| <n>/<total> [tiempo]"
        patron_tqdm = re.compile(
            r'^(?P<desc>.+?):\s*(?P<pct>\d+)%\|(?P<barra>[█░▌ #]*)\|\s*'
            r'(?P<n>\d+)/(?P<total>\d+)'
            r'(?P<resto>.*)$'
        )
        coincidencia = patron_tqdm.match(linea)

        if coincidencia:
            descripcion = coincidencia.group("desc").strip()
            porcentaje  = coincidencia.group("pct")
            barra       = coincidencia.group("barra")
            conteo      = f'{coincidencia.group("n")}/{coincidencia.group("total")}'
            resto       = coincidencia.group("resto").strip()

            return (
                f'<span class="tqdm-etiqueta">{descripcion}:</span> '
                f'<span class="tqdm-porcentaje">{porcentaje:>3}%</span> '
                f'<span class="tqdm-barra">|{barra}|</span> '
                f'<span class="tqdm-conteo">{conteo}</span> '
                f'<span class="tqdm-resto">{resto}</span>'
            )

        # Líneas de print normales (mensajes de inicio, errores, etc.)
        if any(sym in linea for sym in ["✔", "✓", "Listo", "correctamente", "="]):
            return f'<span class="tqdm-completado">{linea}</span>'

        if any(sym in linea for sym in ["🎉", "finalizado", "Finalizado"]):
            return f'<span class="tqdm-finalizado">{linea}</span>'

        if any(sym in linea for sym in ["⚠", "Error", "error", "Traceback"]):
            return f'<span class="tqdm-error">{linea}</span>'

        return f'<span class="tqdm-info">{linea}</span>'


# ── Funciones que envuelven la ejecución real de cada pipeline ────────────────

def ejecutar_pipeline_spacy():
    """
    Lanza pipeline_spacy().ejecutar() redirigiendo stdout y stderr
    al capturador para mostrar el progreso de tqdm en la consola del dashboard.
    """
    global logs_sistema, pasos_activos, pipeline_en_ejecucion,df_resultado_global
    logs_sistema = []
    pasos_activos = {}
    pipeline_en_ejecucion = True

    # Guardar los flujos originales
    stdout_original = sys.stdout
    stderr_original = sys.stderr

    capturador = CapturadorSalidaConsola()

    try:
        # Redirigir ambos flujos (tqdm escribe en stderr)
        sys.stdout = capturador
        sys.stderr = capturador

        if not _spacy_disponible:
            registros_pipeline.append(
                f'<span class="tqdm-error">No se pudo importar pipeline_spacy: '
                f'{_error_importacion_spacy}</span>'
            )
        else:
            instancia_spacy = pipeline_spacy()
            df_resultado_global = instancia_spacy.ejecutar()
            print(f"DEBUG HILO: DataFrame creado con {len(df_resultado_global)} filas")

            registros_pipeline.append(
                '<span class="tqdm-finalizado">Pipeline spaCy finalizado correctamente</span>'
            )

    except Exception as error:
        registros_pipeline.append(
            f'<span class="tqdm-error">Error durante la ejecución de spaCy: {error}</span>'
        )
    finally:
        # Restaurar los flujos originales siempre
        sys.stdout = stdout_original
        sys.stderr = stderr_original
        pipeline_en_ejecucion = False


def ejecutar_pipeline_nltk():
    """
    Lanza pipeline_nltk().ejecutar() redirigiendo stdout y stderr
    al capturador para mostrar el progreso de tqdm en la consola del dashboard.
    """
    global logs_sistema, pasos_activos, pipeline_en_ejecucion, df_resultado_global
    logs_sistema = []
    pasos_activos = {}
    pipeline_en_ejecucion = True

    stdout_original = sys.stdout
    stderr_original = sys.stderr

    capturador = CapturadorSalidaConsola()

    try:
        sys.stdout = capturador
        sys.stderr = capturador

        if not _nltk_disponible:
            registros_pipeline.append(
                f'<span class="tqdm-error">No se pudo importar pipeline_nltk: '
                f'{_error_importacion_nltk}</span>'
            )
        else:
            instancia_nltk = pipeline_nltk()
            df_resultado_global = instancia_nltk.ejecutar()
            print(f"DEBUG HILO: DataFrame creado con {len(df_resultado_global)} filas")
            registros_pipeline.append(
                '<span class="tqdm-finalizado">Pipeline NLTK finalizado correctamente</span>'
            )

    except Exception as error:
        registros_pipeline.append(
            f'<span class="tqdm-error">Error durante la ejecución de NLTK: {error}</span>'
        )
    finally:
        sys.stdout = stdout_original
        sys.stderr = stderr_original
        pipeline_en_ejecucion = False


# ── Mensajes de estado de importación para mostrar en la consola al inicio ───

def _generar_mensajes_estado_importacion() -> list[str]:
    """Retorna mensajes HTML sobre si los pipelines se importaron correctamente."""
    mensajes = []
    if _spacy_disponible:
        mensajes.append('<span class="tqdm-completado">pipeline_spacy importado correctamente</span>')
    else:
        mensajes.append(
            f'<span class="tqdm-error">pipeline_spacy no disponible: {_error_importacion_spacy}</span>'
        )
    if _nltk_disponible:
        mensajes.append('<span class="tqdm-completado">pipeline_nltk importado correctamente</span>')
    else:
        mensajes.append(
            f'<span class="tqdm-error">pipeline_nltk no disponible: {_error_importacion_nltk}</span>'
        )
    return mensajes


# ── Diseño de la página ───────────────────────────────────────────────────────

layout = html.Div(
    [
        # Encabezado
        html.Div(
            [
                html.H1("Panel de Control", className="page-title"),
                html.P(
                    "Selecciona el pipeline NLP que deseas ejecutar sobre el corpus cargado.",
                    className="page-subtitle",
                ),
            ],
            className="page-header",
        ),

        # ── Selector de pipeline ──────────────────────────────────────────────
        html.Div(
            [
                html.H5("Seleccionar Pipeline", className="section-title"),

                html.Div(
                    [
                        # Tarjeta spaCy
                        html.Div(
                            [
                                html.I(className="bi bi-stars pipeline-icono"),
                                html.H6("spaCy"),
                                html.P(
                                    "Tokenización · POS Tagging · Stopwords · Minúsculas · Lematización",
                                ),
                                # Indicador de disponibilidad
                                html.Span(
                                    "● Disponible" if _spacy_disponible else "● No disponible",
                                    className=(
                                        "indicador-disponible"
                                        if _spacy_disponible
                                        else "indicador-no-disponible"
                                    ),
                                ),
                            ],
                            className="pipeline-tarjeta pipeline-tarjeta-activa",
                            id="tarjeta-spacy",
                        ),

                        # Tarjeta NLTK
                        html.Div(
                            [
                                html.I(className="bi bi-puzzle-fill pipeline-icono"),
                                html.H6("NLTK"),
                                html.P(
                                    "Tokenización · POS Tagging · Stopwords · Minúsculas · Lematización",
                                ),
                                html.Span(
                                    "● Disponible" if _nltk_disponible else "● No disponible",
                                    className=(
                                        "indicador-disponible"
                                        if _nltk_disponible
                                        else "indicador-no-disponible"
                                    ),
                                ),
                            ],
                            className="pipeline-tarjeta",
                            id="tarjeta-nltk",
                        ),
                    ],
                    className="pipeline-fila-tarjetas",
                ),

                # Detalle de pasos del pipeline seleccionado
                html.Div(id="detalle-pasos-pipeline", className="detalle-pasos"),

                # Botones de acción
                html.Div(
                    [
                        dbc.Button(
                            [html.I(className="bi bi-play-fill me-2"), "Ejecutar Pipeline"],
                            id="boton-ejecutar",
                            className="btn-ejecutar",
                            n_clicks=0,
                        ),
                        dbc.Button(
                            [html.I(className="bi bi-x-circle me-2"), "Limpiar Consola"],
                            id="boton-limpiar",
                            className="btn-limpiar",
                            n_clicks=0,
                        ),
                    ],
                    className="fila-botones",
                ),
            ],
            className="card-section",
        ),

        # ── Consola de progreso estilo terminal ───────────────────────────────
        html.Div(
            [
                html.Div(
                    [
                        # Barra superior estilo macOS
                        html.Div(
                            [
                                html.Span("●", className="punto punto-rojo"),
                                html.Span("●", className="punto punto-amarillo"),
                                html.Span("●", className="punto punto-verde"),
                                html.Span(
                                    "Progreso del Pipeline — tqdm",
                                    className="consola-titulo",
                                ),
                            ],
                            className="consola-barra-superior",
                        ),
                        # Cuerpo de la consola (se actualiza por polling)
                        html.Div(
                            html.P("Esperando ejecución...", className="consola-placeholder"),
                            id="salida-consola",
                            className="consola-cuerpo",
                        ),
                    ],
                    className="ventana-consola",
                ),

                # Almacenes de estado ocultos
                dcc.Store(id="estado-pipeline",       data="inactivo"),
                dcc.Store(id="pipeline-seleccionado", data="spacy"),

                # Intervalo de sondeo: activo solo mientras corre el pipeline
                dcc.Interval(id="intervalo-progreso", interval=300, disabled=True),
            ],
            className="card-section",
        ),
    ],
    className="page-container",
)


# ── Callbacks ─────────────────────────────────────────────────────────────────

@callback(
    Output("tarjeta-spacy",           "className"),
    Output("tarjeta-nltk",            "className"),
    Output("pipeline-seleccionado",   "data"),
    Output("detalle-pasos-pipeline",  "children"),
    Input("tarjeta-spacy", "n_clicks"),
    Input("tarjeta-nltk",  "n_clicks"),
    prevent_initial_call=False,
)
def resaltar_tarjeta_seleccionada(clics_spacy, clics_nltk):
    """Resalta la tarjeta activa, guarda la selección y muestra los pasos del pipeline."""
    contexto = dash.callback_context
    seleccionado = "spacy"

    if contexto.triggered:
        id_disparador = contexto.triggered[0]["prop_id"].split(".")[0]
        if id_disparador == "tarjeta-nltk":
            seleccionado = "nltk"

    clase_spacy = "pipeline-tarjeta" + (" pipeline-tarjeta-activa" if seleccionado == "spacy" else "")
    clase_nltk  = "pipeline-tarjeta" + (" pipeline-tarjeta-activa" if seleccionado == "nltk"  else "")

    # Pasos reales de cada pipeline según su código fuente
    pasos_spacy = [
        ("Paso 1", "Tokenización",    "Aplica spaCy para extraer tokens de cada letra de canción."),
        ("Paso 2", "Etiquetado POS",  "Asigna categoría gramatical a cada token (sustantivo, verbo…)."),
        ("Paso 3", "Stopwords",       "Elimina palabras vacías usando el vocabulario de spaCy."),
        ("Paso 4", "Minúsculas",      "Convierte todos los tokens a minúsculas."),
        ("Paso 5", "Lematización",    "Reduce cada token a su forma base con el lematizador de spaCy."),
    ]
    pasos_nltk = [
        ("Paso 1", "Tokenización",    "Divide cada letra en oraciones y luego en tokens con NLTK."),
        ("Paso 2", "Etiquetado POS",  "Etiqueta gramaticalmente cada token con pos_tag de NLTK."),
        ("Paso 3", "Stopwords",       "Filtra stopwords del corpus en inglés de NLTK."),
        ("Paso 4", "Minúsculas",      "Convierte todos los tokens a minúsculas."),
        ("Paso 5", "Lematización",    "Lematiza con WordNetLemmatizer usando el POS tag como guía."),
    ]

    pasos = pasos_spacy if seleccionado == "spacy" else pasos_nltk

    detalle = html.Div(
        [
            html.Div(
                [
                    html.Span(numero, className="paso-numero"),
                    html.Div(
                        [
                            html.Strong(nombre, className="paso-nombre"),
                            html.Span(descripcion, className="paso-descripcion"),
                        ],
                        className="paso-texto",
                    ),
                ],
                className="paso-item",
            )
            for numero, nombre, descripcion in pasos
        ],
        className="lista-pasos",
    )

    return clase_spacy, clase_nltk, seleccionado, detalle


@callback(
    Output("intervalo-progreso", "disabled"),
    Output("estado-pipeline",    "data"),
    Input("boton-ejecutar", "n_clicks"),
    Input("boton-limpiar",  "n_clicks"),
    State("pipeline-seleccionado", "data"),
    prevent_initial_call=True,
)
def lanzar_pipeline(clics_ejecutar, clics_limpiar, pipeline_elegido):
    """Lanza el pipeline real en un hilo aparte y activa el sondeo de la consola."""
    global registros_pipeline, pipeline_en_ejecucion, df_resultado_global

    contexto = dash.callback_context
    if not contexto.triggered:
        return True, "inactivo"

    disparador = contexto.triggered[0]["prop_id"].split(".")[0]

    if disparador == "boton-limpiar":
        registros_pipeline = []
        pipeline_en_ejecucion = False
        return True, "inactivo"

    if disparador == "boton-ejecutar" and not pipeline_en_ejecucion:
        # Mostrar estado de importación antes de lanzar
        registros_pipeline = _generar_mensajes_estado_importacion()

        funcion_pipeline = (
            ejecutar_pipeline_spacy if pipeline_elegido == "spacy"
            else ejecutar_pipeline_nltk
        )
        hilo = threading.Thread(target=funcion_pipeline, daemon=True)
        hilo.start()
        return False, "ejecutando"

    return True, "inactivo"


@callback(
    Output("salida-consola", "children"),
    Output("intervalo-progreso", "disabled", allow_duplicate=True),
    Input("intervalo-progreso", "n_intervals"),
    State("estado-pipeline", "data"),
    prevent_initial_call=True,
)
def actualizar_consola(_, estado_actual):
    global logs_sistema, pasos_activos, pipeline_en_ejecucion,df_resultado_global

    # Ordenamos los pasos para que el Paso 1 siempre esté arriba del Paso 2
    claves_ordenadas = sorted(pasos_activos.keys())
    barras_progresivas = [pasos_activos[k] for k in claves_ordenadas]

    # Unimos todo
    todo_el_contenido = logs_sistema + barras_progresivas

    if not todo_el_contenido:
        return html.P("Esperando...", className="consola-placeholder"), False

    # Renderizado final
    contenido_final = "\n".join(todo_el_contenido)

    return dcc.Markdown(
        contenido_final,
        dangerously_allow_html=True,
        className="linea-consola"
    ), not pipeline_en_ejecucion


# inicio.py
@callback(
    Output("nav-comparacion", "disabled"),
    Output("nav-evolucion", "disabled"),
    Output("nav-sentimientos", "disabled"),
    Output("nav-pos", "disabled"),                        # ← 4to output
    Output("store-datos-pipeline", "data"),               # ← 5to output
    Input("intervalo-progreso", "disabled"),
    prevent_initial_call=True
)
def habilitar_menu_y_datos(intervalo_deshabilitado):
    global df_resultado_global

    if intervalo_deshabilitado and df_resultado_global is not None:
        print("Habilitando interfaz ahora...")
        return False, False, False, False, df_resultado_global.to_dict('records')
        #

    return dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update
    #