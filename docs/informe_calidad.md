# Informe de calidad de datos

Este documento se completa al finalizar la limpieza. Las métricas de **Antes** salen del diagnóstico inicial y las de **Después** se calculan sobre el CSV limpio.

| Métrica | Antes | Después | Explicación |
|---|---:|---:|---|
| Registros | 11,890 | Pendiente | Explicar cualquier cambio de filas |
| Variables originales | 17 | Pendiente | Explicar variables agregadas o eliminadas |
| Valores faltantes | Pendiente | Pendiente | Cantidad y porcentaje total |
| Variables con NA | Pendiente | Pendiente | Variables con al menos un faltante |
| Duplicados exactos | Pendiente | 0 esperado | Justificar eliminaciones |
| Posibles duplicados parciales | Pendiente | Pendiente | Indicar conservados, corregidos o fusionados |
| Variables con formato inconsistente | Pendiente | 0 esperado | Espacios, teléfonos, nombres y otros formatos |
| Variables con tipo incorrecto | Pendiente | 0 esperado | Comparar con el tipo esperado |
| Categorías inconsistentes | Pendiente | 0 esperado | Variantes que representaban lo mismo |
| Errores corregidos | 0 | Pendiente | Total o resumen por tipo de error |

## Observación inicial conocida

Los 23 archivos aportan una fila completamente vacía cada uno. Este hallazgo debe confirmarse con código dentro del diagnóstico y su tratamiento debe quedar aprobado en el plan de limpieza antes de eliminar esas filas.
