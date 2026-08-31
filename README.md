# Proyecto 1 · Obtención y Limpieza de Datos

**Curso:** CC3084 · Data Science
**Universidad:** Universidad del Valle de Guatemala
**Semestre:** II, 2026
**Versión del conjunto:** 1.0.0

## Objetivo

Obtener, diagnosticar, limpiar y validar los establecimientos educativos de
Guatemala que llegan al nivel Diversificado. El resultado es un único CSV
analítico acompañado por código reproducible, diagnóstico, plan, registro de
transformaciones, pruebas, informe de calidad y libro de códigos.

## Resultado final

- 23 CSV crudos correspondientes a 22 departamentos y Ciudad Capital.
- 11,890 filas crudas, incluidas 23 filas completamente vacías.
- 11,867 establecimientos en el conjunto final.
- 17 variables originales y `ZONA_CAPITAL` como variable derivada.
- Cero filas vacías y cero duplicados exactos.
- Cero formatos inválidos detectados por las reglas finales.
- 340 municipios en el catálogo oficial de referencia.
- 1,085 pares de posibles duplicados parciales revisados y documentados, sin
  decisiones pendientes.

El CSV final está en:

```text
data/processed/establecimientos_diversificado_limpio.csv
```

## Reproducción completa

Desde la raíz del repositorio:

```bash
python -m pip install -r requirements.txt
python src/obtencion.py
python src/generar_dataset.py
python src/metricas_calidad.py
python -m pytest -q
```

`src/obtencion.py` valida los CSV crudos y genera el archivo intermedio. Cuando
se dispone de las 23 exportaciones HTML guardadas con extensión `.xls`, también
puede reproducirse su conversión:

```bash
python src/obtencion.py --source-dir RUTA_A_EXPORTACIONES
```

El catálogo municipal incluido puede actualizarse desde el recurso público de
SEGEPLAN con:

```bash
python src/generar_catalogo_municipios.py
```

## Estructura principal

```text
data/raw/                              23 CSV originales
data/reference/municipios_guatemala.csv
data/interim/                          unión reproducible no versionada
data/processed/establecimientos_diversificado_limpio.csv
notebooks/                             diagnóstico y presentación de la limpieza
src/obtencion.py                       conversión, validación y unión
src/diagnostico.py                     diagnóstico de texto y categorías
src/diagnostico_vianka.py              diagnóstico geográfico
src/limpieza.py                        transformaciones aprobadas
src/generar_dataset.py                 generación del CSV final
src/metricas_calidad.py                métricas antes/después
src/validacion.py                      esquema y validaciones automáticas
tests/test_calidad.py                  pruebas del DataFrame y CSV persistido
docs/plan_limpieza.md                  reglas, justificaciones y riesgos
docs/registro_transformaciones.csv     cambios y cantidades afectadas
docs/informe_calidad.md                comparación final
docs/codebook.md                       libro de códigos versión 1.0.0
reports/calidad/                        evidencias tabulares reproducibles
```

## Decisiones de calidad

- Los códigos y teléfonos se conservan como texto para no perder ceros.
- Los 70 distritos incompletos pasan a `NA`; no se inventan sus dígitos.
- El teléfono final admite únicamente números de ocho dígitos separados por
  `; `. El valor original permanece disponible durante la auditoría.
- Código, departamento y municipio se validan contra los 340 códigos
  municipales de SEGEPLAN 2026.
- Los posibles duplicados se comparan con RapidFuzz dentro de bloques
  geográficos y operativos. Un código MINEDUC distinto se conserva si no hay
  evidencia oficial para fusionarlo o eliminarlo.
- Los faltantes de supervisor y director no se imputan sin una referencia con
  vigencia comprobable.

## Integrantes y contribuciones

| Persona | Variables principales | Contribución adicional |
|---|---|---|
| Vianka | `CODIGO`, `DISTRITO`, `DEPARTAMENTO`, `MUNICIPIO`, `DEPARTAMENTAL` | Ingesta y geografía |
| Ricardo | `ESTABLECIMIENTO`, `DIRECCION`, `TELEFONO`, `SUPERVISOR`, `DIRECTOR` | Duplicados parciales y documentación final |
| Nadissa | `NIVEL`, `SECTOR`, `AREA`, `STATUS`, `MODALIDAD`, `JORNADA`, `PLAN` | Dominios categóricos |
| Nina | Todas las variables | QA, métricas, pruebas y consolidación |

Los cuatro integrantes contribuyen al repositorio y al libro de códigos.

## Fuente

Los datos provienen del Buscador de establecimientos educativos del Ministerio
de Educación de Guatemala, usando el filtro
`NIVEL ESCOLAR: DIVERSIFICADO`. La extracción documentada corresponde al 17 de
julio de 2026. Los detalles están en `docs/fuente_datos.md`.
