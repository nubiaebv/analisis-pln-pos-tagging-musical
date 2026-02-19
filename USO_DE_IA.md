# USO DE INTELIGENCIA ARTIFICIAL

> ** Documentación del uso de IA**  
> Este archivo documenta el uso de herramientas
> de Inteligencia Artificial durante el desarrollo de este proyecto.

---

## 1. Herramientas de IA Utilizadas

| Herramienta    | Tareas en las que se usó                              |
|----------------|-------------------------------------------------------|
| Claude         | _Ej: documentación, explicación de conceptos_         |
| Gemini         | _Ej: generación de funciones, depuración de errores_  |
| GitHub Copilot | _Ej: autocompletado de código, sugerencias en línea_  |

---
## 2. Ejemplos de Prompts Utilizados

### Prompt 1
**Herramienta:** _Claude_  
**Contexto / tarea:** _Desarrollar una interfaz multipágina en Dash para procesamiento de texto (spaCy/NLTK)  <br> con indicadores de progreso tipo tqdm y estilos CSS externos._
```
tengo esta estructura para crear una pagina web con ploty  dash, dame un cascarason que tenga un inicio,
3 paginas de visualizacio, en la de inicio debo selecionar que opcion de pipeline quiero ejecutar spacy 
o nltk ya el archivo esta en una, no hay que cargarlo y me gustaria que muestre en pantalla lo
tqdm.pandas(desc="Paso 1 Tokenización") como esa etiqueta, todo lo que sea css debe ir en el archivo de style
```

**Resultado obtenido:** _Código base de un dashboard con selector de pipeline, consola de progreso visual y tres módulos de visualización pre-configurados_  

---
### Prompt 2
**Herramienta:** _Claude_  
**Contexto / tarea:** _Intentaba obtener datos de múltiples canciones desde la API de Genius en Python, pero el proceso
se detiene tras 100 llamadas debido al límite de solicitudes del API._
```
Tengo el siguiente script "
def obtener_datos_cancion(titulo, artista=None):
    try:
        song = genius.search_song(titulo, artista or "")

        if not song:
            return None, None, None, None

        datos = song.to_dict()

        release = datos.get("release_date_components")
        año = release.get("year") if release else None
        fecha = datos.get("release_date_for_display")
        lyric = song.lyrics

Genius no devuelve género directamente
        genero = None

        return fecha, lyric, año, genero

    except Exception as e:
        print(f"Error con '{titulo}': {e}")
        return None, None, None, None "
        
pero solo me lo genera 100 veces por restriccion de llamados al api que solucion podemos realizar para hacer n llamados

```
**Resultado obtenido:** _Script de automatización para Genius API con lógica de rotación de múltiples API keys y 
  manejo de errores (429) para la recuperación masiva de metadatos de canciones._

---

### Prompt 3
**Herramienta:** _Claude_  
**Contexto / tarea:** _Implementar manejo de errores para evitar que los script se detenga cuando ocurra una excepción_
```
Tengo una app en Dash que ejecuta pipelines spaCy o NLTK en un hilo y muestra el progreso de tqdm en una consola HTML.
Necesito implementar un manejo de errores en los diversos archivos .py del proyecto, para así se evite que la UI se bloquee y no habilite las páginas si el pipeline falla. Te comparto el primer código para iniciar la aplicación de manejo de errores de forma simple pero funcional. 
" "
```

**Resultado obtenido:** _se aplica try/except en cada función atrapa cualquier excepción del pipeline,_

---

## 3. Reflexión sobre el Aprendizaje

_El uso de IA (Claude) me permitió acelerar el desarrollo del proyecto, especialmente en la creación de la arquitectura multipágina en Dash y en la implementación de un sistema de visualización de progreso con tqdm dentro de la interfaz web. Además, me ayudó a reforzar conceptos clave como el uso de threading, la redirección de stdout/stderr, el manejo de límites de API y la aplicación estratégica de try/except para evitar bloqueos en aplicaciones interactivas._

_No obstante, algunas respuestas requirieron ajustes para adaptarse a mi implementación específica, ya que no siempre contemplaban detalles como variables globales o dependencias entre callbacks. Fue necesario aplicar criterio propio para depurar errores, reorganizar estados del dashboard y validar correctamente los resultados antes de habilitar las páginas. La IA facilitó el proceso, pero la integración final demandó análisis técnico y varias pruebas._

---

## 4. Modificaciones al Código / Análisis Generado por IA

- **Modificación 1:** _Reorganicé variables globales (logs_sistema, pasos_activos, df_resultado_global) para evitar conflictos entre hilos y callbacks._
- **Modificación 2:** _Agregué validaciones adicionales para impedir que las páginas de visualización se habiliten si el DataFrame del pipeline es None o si ocurrió una excepción._
- **Modificación 3:** _Ajusté la lógica de captura de tqdm para que solo se actualice la última versión de cada paso, evitando duplicación de barras de progreso en la consola._

---
*Última actualización: Jueves 19 de febrero del 2026*