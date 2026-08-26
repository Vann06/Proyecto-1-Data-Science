# Libro de códigos

**Proyecto:** Obtención y Limpieza de Datos  
**Fuente:** Ministerio de Educación de Guatemala  
**Filtro:** Nivel escolar Diversificado  
**Fecha de extracción:** pendiente de confirmar  
**Versión actual:** 0.2 · limpieza automatizada con pendientes documentados

Los tres integrantes completan este mismo archivo por turnos. Cada persona actualiza las variables que tiene asignadas.

| Responsable | Variable | Descripción inicial | Tipo esperado | Dominio o formato permitido | Tratamiento aplicado |
|---|---|---|---|---|---|
| Vianka | CODIGO | Código del establecimiento | Texto | `NN-NN-NNNN-NN`; se conserva como texto y se valida | Implementada en `limpieza.py` |
| Vianka | DISTRITO | Distrito educativo | Texto anulable | `NN-NNN`, `NN-NN-NNNN` o valor incompleto marcado para revisión | Implementada en `limpieza.py` |
| Vianka | DEPARTAMENTO | Departamento del establecimiento | Texto categórico | 22 departamentos oficiales; Ciudad Capital se asigna a Guatemala | Implementada en `limpieza.py` |
| Vianka | MUNICIPIO | Municipio del establecimiento | Texto categórico | Escritura normalizada según departamento y prefijo del código | Implementada en `limpieza.py` |
| Vianka | DEPARTAMENTAL | Dirección departamental relacionada | Texto categórico | 26 categorías administrativas, incluidas las subdivisiones | Implementada en `limpieza.py` |
| Vianka | ZONA_CAPITAL | Zona de la Ciudad de Guatemala conservada al corregir el nivel geográfico de MUNICIPIO | Texto categórico anulable | `Zona 1` a `Zona 25`, según valores observados; `NA` fuera de la capital | Derivada por `limpieza.py` |
| Ricardo | ESTABLECIMIENTO | Nombre del establecimiento | Texto anulable | Texto sin espacios múltiples; se conservan tildes y puntuación | Se colapsan espacios y se crea una clave separada para detectar variantes y posibles duplicados. |
| Ricardo | DIRECCION | Dirección física | Texto anulable | Dirección sin espacios múltiples; `NA` cuando no existe información recuperable | Se retiran municipio y fechas redundantes al final, se corrige `O` por `0` únicamente en contexto numérico y se preservan direcciones rurales. |
| Ricardo | TELEFONO | Uno o varios teléfonos de contacto | Texto anulable | Uno o más números de 7 u 8 dígitos separados por `; `; `NA` si no hay número recuperable | Se eliminan decoraciones y se uniforman los separadores. Los números de 7 dígitos quedan pendientes de revisión. |
| Ricardo | SUPERVISOR | Nombre del supervisor | Texto anulable | Nombre sin espacios múltiples; `NA` cuando no es identificable | Se corrigen grafías puntuales y se unifican variantes dentro del mismo distrito. No se realizaron imputaciones por falta de una referencia segura. |
| Ricardo | DIRECTOR | Nombre del director | Texto anulable | Nombre sin título ni espacios múltiples; `NA` cuando no es identificable | Se separa el título profesional y se unifican variantes dentro del mismo municipio. |
| Nadissa | NIVEL | Nivel educativo; constante por el filtro de extracción | Categórico | `DIVERSIFICADO` | Se conserva como metadato del filtro y se fija el dominio. |
| Nadissa | SECTOR | Sector del establecimiento | Categórico | `PRIVADO`, `OFICIAL`, `COOPERATIVA`, `MUNICIPAL` | Se convierte a categórico; no se modifican valores. |
| Nadissa | AREA | Área geográfica | Categórico anulable | `URBANA`, `RURAL`, `NA` | `SIN ESPECIFICAR` se reclasifica a `NA`. Los 12 valores rurales de Ciudad Capital se conservan después de contrastar código, nombre y dirección con la fuente. |
| Nadissa | STATUS | Estado del establecimiento | Categórico | `ABIERTA`, `CERRADA TEMPORALMENTE`, `CERRADA DEFINITIVAMENTE`, `TEMPORAL TITULOS`, `TEMPORAL NOMBRAMIENTO` | Se preservan los estados temporales como categorías administrativas distintas. |
| Nadissa | MODALIDAD | Modalidad educativa | Categórico | `MONOLINGUE`, `BILINGUE` | Se convierte a categórico binario; no se modifican valores. |
| Nadissa | JORNADA | Jornada de atención | Categórico | `DOBLE`, `VESPERTINA`, `MATUTINA`, `SIN JORNADA`, `NOCTURNA`, `INTERMEDIA` | `SIN JORNADA` se conserva como categoría válida para ofertas sin horario fijo. |
| Nadissa | PLAN | Plan educativo | Categórico | 13 categorías observadas | Se preservan la categoría genérica `SEMIPRESENCIAL`, sus variantes y las categorías poco frecuentes ya revisadas. |

## Esquema del CSV limpio

El archivo `data/processed/establecimientos_diversificado_limpio.csv` contiene
las 17 variables originales limpias y `ZONA_CAPITAL`. Las columnas técnicas,
copias originales, banderas y claves se utilizan durante la auditoría, pero no
forman parte del CSV analítico final.

## Columnas derivadas y de auditoría

Estas columnas permiten auditar la limpieza sin eliminar ni reconstruir casos
dudosos. Las columnas `_ORIGINAL` conservan exactamente el valor de entrada.

| Variable | Tipo | Cálculo y utilidad |
|---|---|---|
| `CODIGO_ORIGINAL` | Texto | Copia de `CODIGO` antes de normalizar espacios o marcadores. |
| `CODIGO_FORMATO_VALIDO` | Booleano | Indica cumplimiento de `NN-NN-NNNN-NN`. |
| `CODIGO_DUPLICADO` | Booleano | Marca todas las apariciones de un código repetido; no elimina filas. |
| `DISTRITO_ORIGINAL` | Texto | Copia del distrito antes de convertir vacíos a `NA`. |
| `DISTRITO_FORMATO` | Texto categórico | Clasifica como faltante, corto, extendido, incompleto u otro. |
| `DISTRITO_INCOMPLETO` | Booleano | Marca valores `NN-` que requieren consulta institucional. |
| `DISTRITO_FORMATO_VALIDO` | Booleano | Verdadero para los dos formatos completos conservados. |
| `DISTRITO_REQUIERE_REVISION` | Booleano | Une los formatos incompletos y no reconocidos. |
| `DEPARTAMENTO_ORIGINAL` | Texto | Copia previa a la escritura canónica y a la reclasificación de Ciudad Capital. |
| `DEPARTAMENTO_FUERA_CATALOGO` | Booleano | Marca valores no incluidos en los 22 departamentos ni en la excepción de la fuente. |
| `DEPARTAMENTO_ES_CIUDAD_CAPITAL` | Booleano | Identifica las filas cuya categoría original era `CIUDAD CAPITAL`. |
| `MUNICIPIO_ORIGINAL` | Texto | Copia previa a la normalización; también protege la lógica del turno de Ricardo. |
| `MUNICIPIO_ZONA_INVALIDA` | Booleano | Marca una fila capitalina cuyo municipio original no cumple `ZONA N`. |
| `MUNICIPIO_CORREGIDO_CATALOGO` | Booleano | Indica que cambió la escritura o el nivel geográfico del municipio. |
| `DEPARTAMENTAL_ORIGINAL` | Texto | Copia previa a la normalización del dominio administrativo. |
| `DEPARTAMENTAL_FUERA_CATALOGO` | Booleano | Marca valores fuera de las 26 categorías administrativas observadas. |
| `CODIGO_DEPARTAMENTO_CONSISTENTE` | Booleano anulable | Compara el prefijo del código con el departamento limpio; `NA` si no es comparable. |
| `PREFIJO_CODIGO_AMBIGUO` | Booleano | Marca prefijos `NN-NN` asociados con más de un municipio. |
| `DUPLICADO_EXACTO_VIANKA` | Booleano | Marca coincidencias exactas en las cinco variables asignadas; no elimina filas. |
| `ESTABLECIMIENTO_ORIGINAL` | Texto | Copia del nombre antes de normalizar espacios. |
| `ESTABLECIMIENTO_CLAVE` | Texto | Versión sin diferencias de tildes, puntuación o espacios utilizada únicamente para comparar. |
| `ESTABLECIMIENTO_GRUPO_DUPLICADO` | Entero anulable | Identificador del grupo candidato por clave y municipio. |
| `ESTABLECIMIENTO_DUPLICADO_CONFIRMADO` | Booleano | Marca candidatos que también comparten jornada, plan y dirección. |
| `DIRECCION_ORIGINAL` | Texto | Copia de la dirección antes de aplicar las reglas de limpieza. |
| `TELEFONO_ORIGINAL` | Texto | Copia de la celda telefónica antes de estructurar los contactos. |
| `SUPERVISOR_ORIGINAL` | Texto | Copia del nombre antes de corregirlo o reclasificarlo. |
| `SUPERVISOR_IMPUTADO` | Booleano | Indica si el supervisor fue imputado desde una referencia del mismo distrito. |
| `DIRECTOR_ORIGINAL` | Texto | Copia del nombre antes de separar el título y unificar variantes. |
| `DIRECTOR_TITULO` | Texto anulable | Título profesional extraído del inicio de `DIRECTOR`. |

## Columnas técnicas del archivo unificado

| Variable | Descripción | Uso final |
|---|---|---|
| archivo_origen | Nombre del CSV del que salió el registro | Trazabilidad durante la auditoría; se excluye del CSV final |
| fila_origen | Número de fila dentro del archivo original | Trazabilidad durante la auditoría; se excluye del CSV final |

## Historial

| Versión | Fecha | Descripción |
|---|---|---|
| 0.1 | 17 de julio de 2026 | Estructura inicial y descripción preliminar de variables |
| 0.2 | 26 de agosto de 2026 | Documentación de la limpieza automatizada, el esquema final y las columnas de auditoría |
