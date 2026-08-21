# Libro de códigos

**Proyecto:** Obtención y Limpieza de Datos  
**Fuente:** Ministerio de Educación de Guatemala  
**Filtro:** Nivel escolar Diversificado  
**Fecha de extracción:** pendiente de confirmar  
**Versión actual:** 0.1 · datos crudos

Los tres integrantes completan este mismo archivo por turnos. Cada persona actualiza las variables que tiene asignadas.

| Responsable | Variable | Descripción inicial | Tipo esperado | Dominio o formato permitido | Tratamiento aplicado |
|---|---|---|---|---|---|
| Vianka | CODIGO | Código del establecimiento | Texto | `NN-NN-NNNN-NN`; se conserva como texto y se valida | Implementada en `limpieza.py` |
| Vianka | DISTRITO | Distrito educativo | Texto anulable | `NN-NNN`, `NN-NN-NNNN` o valor incompleto marcado para revisión | Implementada en `limpieza.py` |
| Vianka | DEPARTAMENTO | Departamento del establecimiento | Texto categórico | 22 departamentos oficiales; Ciudad Capital se asigna a Guatemala | Implementada en `limpieza.py` |
| Vianka | MUNICIPIO | Municipio del establecimiento | Texto categórico | Escritura normalizada según departamento y prefijo del código | Implementada en `limpieza.py` |
| Vianka | DEPARTAMENTAL | Dirección departamental relacionada | Texto categórico | 26 categorías administrativas, incluidas las subdivisiones | Implementada en `limpieza.py` |
| Vianka | ZONA_CAPITAL | Zona de la Ciudad de Guatemala conservada al corregir el nivel geográfico de MUNICIPIO | Texto categórico anulable | `Zona 1` a `Zona 25`, según valores observados; `NA` fuera de la capital | Derivada por `limpieza.py` |
| Ricardo | ESTABLECIMIENTO | Nombre del establecimiento | Texto | Nombre normalizado según regla aprobada | Pendiente |
| Ricardo | DIRECCION | Dirección física | Texto | Texto con formato uniforme | Pendiente |
| Ricardo | TELEFONO | Teléfono de contacto | Texto | Formato que apruebe el equipo | Pendiente |
| Ricardo | SUPERVISOR | Nombre del supervisor | Texto | Nombre con formato uniforme | Pendiente |
| Ricardo | DIRECTOR | Nombre del director | Texto | Nombre con formato uniforme | Pendiente |
| Nadissa | NIVEL | Nivel educativo | Texto categórico | DIVERSIFICADO | Pendiente |
| Nadissa | SECTOR | Sector del establecimiento | Texto categórico | Categorías observadas y aprobadas | Pendiente |
| Nadissa | AREA | Área geográfica | Texto categórico | Categorías observadas y aprobadas | Pendiente |
| Nadissa | STATUS | Estado del establecimiento | Texto categórico | Categorías observadas y aprobadas | Pendiente |
| Nadissa | MODALIDAD | Modalidad educativa | Texto categórico | Categorías observadas y aprobadas | Pendiente |
| Nadissa | JORNADA | Jornada de atención | Texto categórico | Categorías observadas y aprobadas | Pendiente |
| Nadissa | PLAN | Plan educativo | Texto categórico | Categorías observadas y aprobadas | Pendiente |

## Columnas derivadas y de trazabilidad — turno 1

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

## Columnas técnicas del archivo unificado

| Variable | Descripción | Uso final |
|---|---|---|
| archivo_origen | Nombre del CSV del que salió el registro | Trazabilidad; decidir al final si se conserva |
| fila_origen | Número de fila dentro del archivo original | Trazabilidad; decidir al final si se conserva |

## Historial

| Versión | Fecha | Descripción |
|---|---|---|
| 0.1 | 17 de julio de 2026 | Estructura inicial y descripción preliminar de variables |
