# Revisión de cumplimiento del Proyecto 1

## Resultado general

El repositorio contiene ingesta, diagnóstico, plan, limpieza, generación del
CSV procesado, validaciones automáticas, métricas comparativas y documentación
reproducible. Permanecen cinco asuntos que requieren una fuente externa o
revisión manual.

| Requisito de la guía | Estado | Evidencia o cambio necesario |
|---|---|---|
| Obtención, CSV crudos y unión | Parcialmente cumplido | Existen 23 CSV y `src/unir_csv.py` reproduce la unión. `src/obtencion.py` sigue como esqueleto y la fecha exacta de descarga está pendiente. |
| Diagnóstico inicial | Mayormente cumplido | El notebook principal incluye dimensiones, tipos, faltantes, únicos, duplicados, dominios y formatos. El notebook geográfico no tiene ejecución guardada y conviene consolidar todas las tablas finales. |
| Plan de limpieza previo | Cumplido con pendientes documentados | Cubre las 17 variables, la eliminación de filas vacías y el esquema final; cada regla incluye justificación y riesgo. |
| Limpieza de todas las variables | Mayormente cumplido | El CSV final no contiene filas vacías ni espacios múltiples. Permanecen distritos incompletos, teléfonos legados, validación municipal y duplicados parciales en revisión. |
| Registro de transformaciones | Cumplido | Las transformaciones de las 17 variables, la eliminación de filas y el esquema final incluyen cantidad y justificación. |
| Pruebas automáticas | Cumplido para las reglas implementadas | Cuatro pruebas validan esquema, dimensiones, duplicados, espacios, códigos, teléfonos, dominios y tipos; los pendientes manuales tienen controles de regresión. |
| Informe antes/después | Cumplido con pendientes documentados | `docs/informe_calidad.md` compara el conjunto crudo con el procesado mediante tablas generadas por código. |
| Conjunto limpio único | Cumplido | `src/generar_dataset.py` produce 11,867 registros y 18 variables en `data/processed/`. |
| Libro de códigos | Mayormente cumplido | Documenta las variables, tratamientos y columnas de auditoría; la fecha exacta de extracción continúa pendiente. |
| PDF del libro de códigos | No cumplido | No se encontró un PDF final del codebook en el repositorio. |
| Reproducibilidad | Cumplido | La unión, generación del CSV, métricas y pruebas se ejecutan mediante comandos documentados en `README.md`. |

## Hallazgos que conviene corregir primero

1. Revisar los 21 grupos confirmados de duplicados parciales y documentar una
   decisión por grupo. Marcar no sustituye la revisión caso por caso que exige
   la guía.
2. Resolver los 70 distritos incompletos o definirlos como faltantes/revisión
   aceptada con evidencia institucional. Mientras permanezcan, no puede
   afirmarse que no existen formatos inválidos.
3. Alinear el dominio de teléfonos: el plan acepta provisionalmente 7 u 8
   dígitos y hay 90 celdas con al menos un número de 7 dígitos.
4. Confirmar la fecha exacta de extracción y actualizar la versión final del
   libro de códigos.
5. Incorporar un catálogo oficial completo de municipios por departamento. El
   diccionario actual corrige ortografía, pero no demuestra pertenencia al
   catálogo correspondiente.
