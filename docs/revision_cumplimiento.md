# Revisión de cumplimiento del Proyecto 1

**Referencia revisada:** guía “Proyecto 1. Obtención y Limpieza de los datos”,
CC3084, semestre II de 2026.  
**Fecha de revisión:** 25 de agosto de 2026.

## Resultado general

El repositorio contiene una base sólida de ingesta, diagnóstico, plan y
limpieza reproducible, pero todavía no está listo para entrega final. Los
bloqueos principales son la ausencia de validaciones automáticas completas, la
falta del CSV procesado, los duplicados sin decisión y documentación final
incompleta.

| Requisito de la guía | Estado | Evidencia o cambio necesario |
|---|---|---|
| Obtención, CSV crudos y unión | Parcialmente cumplido | Existen 23 CSV y `src/unir_csv.py` reproduce la unión. `src/obtencion.py` sigue como esqueleto y la fecha exacta de descarga está pendiente. |
| Diagnóstico inicial | Mayormente cumplido | El notebook principal incluye dimensiones, tipos, faltantes, únicos, duplicados, dominios y formatos. El notebook geográfico no tiene ejecución guardada y conviene consolidar todas las tablas finales. |
| Plan de limpieza previo | Mayormente cumplido | Cubre las 17 variables con reglas y riesgos, pero la última fila de `PLAN` quedó desalineada y hay decisiones que el código no cumple exactamente. |
| Limpieza de todas las variables | Parcialmente cumplido | Hay reglas reproducibles y trazabilidad, pero quedan filas vacías, distritos incompletos, espacios múltiples, municipio sin catálogo completo y duplicados parciales sin decisión. |
| Registro de transformaciones | No cumplido por completo | Solo las variables geográficas tienen problema, transformación, cantidad y justificación; las filas de Ricardo y Nadissa están vacías. |
| Pruebas automáticas | No cumplido | `validar_datos()` lanza `NotImplementedError` y `tests/test_calidad.py` solo contiene un `TODO`. |
| Informe antes/después | Preliminar | `docs/informe_calidad.md` ya contiene métricas reproducibles del estado actual, pero no puede cerrar con ceros hasta tener el CSV final validado. |
| Conjunto limpio único | No cumplido | `data/processed/` no contiene el CSV final. El flujo actual conserva 11,890 filas y 48 columnas. |
| Libro de códigos | Parcialmente cumplido | Tiene estructura útil, pero conserva versión cruda 0.1, fecha pendiente, tratamientos de Ricardo como pendientes y no documenta todas las columnas derivadas. |
| PDF del libro de códigos | No cumplido | No se encontró un PDF final del codebook en el repositorio. |
| Reproducibilidad | Parcialmente cumplido | La unión y limpieza se pueden ejecutar, pero falta un comando final que genere CSV, validaciones, métricas e informe de principio a fin. |

## Hallazgos que conviene corregir primero

1. Implementar la finalización del conjunto: retirar las 23 filas vacías con
   una regla aprobada, definir las columnas del CSV final y escribirlo en
   `data/processed/`.
2. Revisar los 21 grupos confirmados de duplicados parciales y documentar una
   decisión por grupo. Marcar no sustituye la revisión caso por caso que exige
   la guía.
3. Completar `src/validacion.py` y `tests/test_calidad.py` con pruebas de
   duplicados, espacios, teléfonos, catálogos, tipos, categorías y todos los
   errores detectados inicialmente.
4. Completar `docs/registro_transformaciones.csv` para Ricardo y Nadissa. La
   cantidad afectada debe salir del código, no escribirse a mano sin respaldo.
5. Resolver los 70 distritos incompletos o definirlos como faltantes/revisión
   aceptada con evidencia institucional. Mientras permanezcan, no puede
   afirmarse que no existen formatos inválidos.
6. Normalizar espacios múltiples en los campos de texto destinados al CSV
   final, conservando las columnas originales solo en una salida de auditoría.
7. Incorporar un catálogo oficial completo de municipios por departamento. El
   diccionario actual corrige ortografía, pero no demuestra pertenencia al
   catálogo correspondiente.
8. Alinear el dominio de teléfonos: el plan habla de 8 dígitos y el código
   acepta 7 u 8. Hay 90 celdas limpias con al menos un número de 7 dígitos.
9. Corregir documentación desactualizada: `README.md` e `index.qmd` aún dicen
   que el proyecto está en diagnóstico, aunque ya existe limpieza preliminar.
10. Confirmar la fecha exacta de extracción y actualizar versión, fuente y
    tratamientos en el libro de códigos antes de exportarlo a PDF.

## Revisión del codebook de ejemplo

El archivo de ejemplo descargado pertenece a un proyecto de clasificación de
imágenes de cartas TCG. Su tema, variables, clases, fuentes y decisiones de
modelado no son reutilizables en este proyecto. Sí sirve como referencia de
presentación porque comienza con el propósito del dataset, enumera dominios y
explica transformaciones.

Para este proyecto, la guía exige mucho más detalle por cada variable:
descripción, tipo, dominio, valores posibles, tratamiento aplicado, variables
derivadas, fecha de extracción, fuente y versión del conjunto limpio. Por eso,
el ejemplo no debe copiarse como plantilla completa. El `docs/codebook.md` del
repositorio está mejor orientado, pero debe actualizarse con:

- la fecha exacta de extracción;
- la versión final del conjunto;
- los tratamientos reales de `ESTABLECIMIENTO`, `DIRECCION`, `TELEFONO`,
  `SUPERVISOR` y `DIRECTOR`;
- todas las columnas derivadas y su fórmula;
- la decisión sobre columnas técnicas y de auditoría;
- dominios completos o referencias a catálogos versionados;
- un historial que corresponda al CSV final.
