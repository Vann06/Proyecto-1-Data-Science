# Revisión final de cumplimiento del Proyecto 1

## Resultado general

La versión 1.0.0 cubre la obtención documentada, unión, diagnóstico, plan,
limpieza, registro de transformaciones, validación, comparación antes/después,
libro de códigos y generación del CSV limpio. El PDF del libro de códigos se
mantiene fuera del alcance de esta revisión por decisión del equipo.

| Requisito de la guía | Estado | Evidencia |
|---|---|---|
| Obtención, CSV crudos y unión | Cumplido | `src/obtencion.py` convierte exportaciones HTML/XLS, valida los 23 CSV y ejecuta la unión reproducible. |
| Diagnóstico inicial | Cumplido | Los notebooks y reportes incluyen dimensiones, tipos, faltantes, únicos, duplicados, dominios, formatos y problemas potenciales. |
| Plan de limpieza previo | Cumplido | `docs/plan_limpieza.md` cubre las 17 variables, la variable derivada, justificación y riesgos. |
| Limpieza de todas las variables | Cumplido | Los formatos inválidos detectados se corrigen o pasan a `NA` sin imputación especulativa. |
| Registro de transformaciones | Cumplido | `docs/registro_transformaciones.csv` contiene problema, transformación, cantidad, justificación y responsable. |
| Duplicados exactos y parciales | Cumplido | No quedan duplicados exactos; 1,085 pares parciales fueron revisados con RapidFuzz y documentados individualmente. |
| Pruebas automáticas | Cumplido | Las pruebas validan el DataFrame generado y el CSV persistido, incluyendo geografía oficial y dominios. |
| Informe antes/después | Cumplido | Todas las métricas requeridas tienen valores finales reproducibles. |
| Conjunto limpio único | Cumplido | `data/processed/establecimientos_diversificado_limpio.csv` contiene 11,867 registros y 18 variables. |
| Libro de códigos en Markdown | Cumplido | La versión 1.0.0 enumera descripción, tipo, dominio, valores, tratamiento, fuente, fecha y variable derivada. |
| PDF del libro de códigos | Fuera de alcance | No se genera en esta fase por decisión explícita del equipo. |
| Reproducibilidad | Cumplido | El README contiene una secuencia única desde la validación de los datos crudos hasta las pruebas. |
| Contribuciones del equipo | Cumplido | Los cuatro integrantes tienen contribuciones en el repositorio y el codebook final se actualiza en la rama de limpieza de Ricardo. |

## Controles finales

- 23 CSV crudos y 17 variables originales.
- 11,890 filas crudas; 11,867 filas con información.
- 11,867 registros y 18 variables en el CSV final.
- Cero duplicados exactos.
- Cero formatos inválidos detectados.
- Cero pares de duplicados parciales pendientes de decisión.
- 340 municipios disponibles en el catálogo oficial de referencia.
- CSV final incluido explícitamente en el repositorio.
