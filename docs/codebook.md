# Libro de códigos

**Proyecto:** Obtención y Limpieza de Datos
**Fuente:** Buscador de establecimientos educativos del Ministerio de Educación de Guatemala
**Filtro:** `NIVEL ESCOLAR: DIVERSIFICADO`
**Fecha de extracción documentada por el equipo:** 17 de julio de 2026
**Fecha de cierre de calidad:** 31 de agosto de 2026
**Versión del conjunto limpio:** 1.0.0

Los cuatro integrantes contribuyeron al repositorio y al libro de códigos. El
CSV final contiene las 17 variables de la fuente y la variable derivada
`ZONA_CAPITAL`.

## Variables del conjunto limpio

| Responsable | Variable | Descripción | Tipo | Dominio permitido | Valores posibles | Tratamiento aplicado |
|---|---|---|---|---|---|---|
| Vianka | `CODIGO` | Identificador oficial del establecimiento | Texto no anulable | `NN-NN-NNNN-NN`, único | 11,867 códigos observados | Se conserva como texto y se validan formato, unicidad y consistencia geográfica. |
| Vianka | `DISTRITO` | Distrito educativo | Texto anulable | `NN-NNN`, `NN-NN-NNNN` o `NA` | Códigos completos observados y `NA` | Vacíos y 70 códigos incompletos `NN-` pasan a `NA`; el original queda en auditoría. |
| Vianka | `DEPARTAMENTO` | Departamento del establecimiento | Categórico | 22 departamentos oficiales | Guatemala, El Progreso, Sacatepéquez, Chimaltenango, Escuintla, Santa Rosa, Sololá, Totonicapán, Quetzaltenango, Suchitepéquez, Retalhuleu, San Marcos, Huehuetenango, Quiché, Baja Verapaz, Alta Verapaz, Petén, Izabal, Zacapa, Chiquimula, Jalapa y Jutiapa | Se normalizan tildes y `CIUDAD CAPITAL` se asigna a Guatemala. |
| Vianka | `MUNICIPIO` | Municipio del establecimiento | Categórico | 340 códigos municipales de SEGEPLAN | Valores de `data/reference/municipios_guatemala.csv` | Se determina por el prefijo municipal de `CODIGO`; la etiqueta MINEDUC se conserva cuando difiere legítimamente de la forma corta de SEGEPLAN. |
| Vianka | `ZONA_CAPITAL` | Zona de la Ciudad de Guatemala | Categórico anulable | `Zona 1` a `Zona 25` o `NA` | 22 zonas observadas; `NA` fuera de Ciudad Capital | Variable derivada de `MUNICIPIO_ORIGINAL = ZONA N`; preserva la sububicación al corregir el nivel municipal. |
| Ricardo | `ESTABLECIMIENTO` | Nombre del establecimiento | Texto anulable | Texto sin espacios iniciales, finales o múltiples | Texto libre o `NA` | Se normalizan espacios y se conserva la escritura visible. Las comparaciones de duplicados usan una clave separada. |
| Ricardo | `DIRECCION` | Dirección física | Texto anulable | Texto uniforme o `NA` | Texto libre o `NA` | Se reclasifican faltantes disfrazados, se retiran municipio y fechas redundantes, y se corrige `O` por `0` solo en contexto numérico. |
| Ricardo | `TELEFONO` | Uno o varios teléfonos de contacto | Texto anulable | Uno o más números de 8 dígitos separados por `; ` | `NNNNNNNN`, listas con `; ` o `NA` | Se recuperan únicamente números de ocho dígitos; los componentes de siete dígitos no se completan y permanecen en `TELEFONO_ORIGINAL`. |
| Ricardo | `SUPERVISOR` | Nombre del supervisor | Texto anulable | Nombre sin espacios múltiples o `NA` | Texto libre o `NA` | Se corrigen grafías puntuales y variantes dentro del distrito. No se imputa sin fecha de vigencia. |
| Ricardo | `DIRECTOR` | Nombre del director | Texto anulable | Nombre sin título ni espacios múltiples o `NA` | Texto libre o `NA` | Se separa el título profesional, se normalizan variantes dentro del municipio y se conservan faltantes no imputables. |
| Nadissa | `NIVEL` | Nivel educativo usado como filtro | Categórico | Una categoría | `DIVERSIFICADO` | Se conserva como metadato del filtro. |
| Nadissa | `SECTOR` | Sector del establecimiento | Categórico | Cuatro categorías | `PRIVADO`, `OFICIAL`, `COOPERATIVA`, `MUNICIPAL` | Se fija un dominio cerrado. |
| Nadissa | `AREA` | Área geográfica | Categórico anulable | Dos categorías o `NA` | `URBANA`, `RURAL`, `NA` | `SIN ESPECIFICAR` pasa a `NA`; los casos rurales de Ciudad Capital se conservan tras revisión. |
| Nadissa | `STATUS` | Estado administrativo | Categórico | Cinco categorías | `ABIERTA`, `CERRADA TEMPORALMENTE`, `CERRADA DEFINITIVAMENTE`, `TEMPORAL TITULOS`, `TEMPORAL NOMBRAMIENTO` | Los estados temporales se conservan como categorías distintas. |
| Nadissa | `MODALIDAD` | Modalidad educativa | Categórico | Dos categorías | `MONOLINGUE`, `BILINGUE` | Se fija un dominio cerrado. |
| Nadissa | `JORNADA` | Jornada de atención | Categórico | Seis categorías | `DOBLE`, `VESPERTINA`, `MATUTINA`, `SIN JORNADA`, `NOCTURNA`, `INTERMEDIA` | `SIN JORNADA` se conserva para ofertas sin horario fijo. |
| Nadissa | `PLAN` | Plan educativo | Categórico | Trece categorías | `DIARIO(REGULAR)`, `FIN DE SEMANA`, `SEMIPRESENCIAL (FIN DE SEMANA)`, `SEMIPRESENCIAL (UN DÍA A LA SEMANA)`, `A DISTANCIA`, `SEMIPRESENCIAL`, `VIRTUAL A DISTANCIA`, `SEMIPRESENCIAL (DOS DÍAS A LA SEMANA)`, `SABATINO`, `DOMINICAL`, `MIXTO`, `IRREGULAR`, `INTERCALADO` | Se preserva la categoría genérica semipresencial, sus variantes específicas y las categorías válidas de baja frecuencia. |
| Vianka | `DEPARTAMENTAL` | Dirección departamental educativa | Categórico | 26 categorías administrativas | Alta Verapaz, Baja Verapaz, Chimaltenango, Chiquimula, El Progreso, Escuintla, Guatemala Norte, Guatemala Occidente, Guatemala Oriente, Guatemala Sur, Huehuetenango, Izabal, Jalapa, Jutiapa, Petén, Quetzaltenango, Quiché, Quiché Norte, Retalhuleu, Sacatepéquez, San Marcos, Santa Rosa, Sololá, Suchitepéquez, Totonicapán y Zacapa | Se normaliza con un catálogo administrativo independiente del departamento geográfico. |

## Variable derivada

`ZONA_CAPITAL` se creó porque los archivos de Ciudad Capital almacenaban una
zona en `MUNICIPIO`. Se calcula extrayendo `N` de `ZONA N`, antes de reemplazar
el municipio por `Guatemala`. Permite analizar la distribución dentro de la
capital sin conservar un valor que no pertenece al dominio municipal.

## Columnas de auditoría

Las siguientes columnas se producen durante la limpieza preliminar y se
excluyen del CSV analítico final:

| Grupo | Columnas | Uso |
|---|---|---|
| Trazabilidad | `archivo_origen`, `fila_origen` | Identifican el CSV y la fila de origen. |
| Copias originales | `CODIGO_ORIGINAL`, `DISTRITO_ORIGINAL`, `DEPARTAMENTO_ORIGINAL`, `MUNICIPIO_ORIGINAL`, `DEPARTAMENTAL_ORIGINAL`, `ESTABLECIMIENTO_ORIGINAL`, `DIRECCION_ORIGINAL`, `TELEFONO_ORIGINAL`, `SUPERVISOR_ORIGINAL`, `DIRECTOR_ORIGINAL` | Conservan el valor anterior a la transformación. |
| Geografía | `CODIGO_FORMATO_VALIDO`, `CODIGO_DUPLICADO`, `DISTRITO_FORMATO`, `DISTRITO_INCOMPLETO`, `DISTRITO_CONVERTIDO_A_NA`, `DISTRITO_FORMATO_VALIDO`, `DISTRITO_REQUIERE_REVISION`, `DEPARTAMENTO_FUERA_CATALOGO`, `DEPARTAMENTO_ES_CIUDAD_CAPITAL`, `MUNICIPIO_ZONA_INVALIDA`, `MUNICIPIO_CORREGIDO_CATALOGO`, `MUNICIPIO_CODIGO_CATALOGO_VALIDO`, `DEPARTAMENTAL_FUERA_CATALOGO`, `CODIGO_DEPARTAMENTO_CONSISTENTE`, `PREFIJO_CODIGO_AMBIGUO` | Validan formato, catálogo y consistencia entre campos. |
| Duplicados | `ESTABLECIMIENTO_CLAVE`, `ESTABLECIMIENTO_GRUPO_DUPLICADO`, `ESTABLECIMIENTO_DUPLICADO_CONFIRMADO`, `DUPLICADO_EXACTO_VIANKA` | Localizan candidatos sin eliminar registros automáticamente. |
| Texto y personas | `TELEFONO_DESCARTO_7_DIGITOS`, `SUPERVISOR_IMPUTADO`, `DIRECTOR_TITULO` | Documentan decisiones específicas de limpieza. |

## Esquema de carga

CSV no almacena tipos categóricos. Para recuperar el esquema documentado y
validar el archivo persistido se utiliza:

```python
from src.validacion import cargar_csv_limpio, validar_datos

df = cargar_csv_limpio()
validar_datos(df)
```

## Historial

| Versión | Fecha | Descripción |
|---|---|---|
| 0.1 | 17 de julio de 2026 | Estructura y descripciones iniciales. |
| 0.2 | 26 de agosto de 2026 | Limpieza automatizada y columnas de auditoría. |
| 1.0.0 | 31 de agosto de 2026 | Catálogo oficial, decisiones de duplicados, dominios finales y validación del CSV persistido. |
