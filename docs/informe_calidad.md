# Informe de calidad de los datos

**Conjunto:** establecimientos educativos de Guatemala con nivel Diversificado

**Fuente:** Buscador de establecimientos educativos del Ministerio de Educación

**Fecha de evaluación:** 25 de agosto de 2026

**Estado del resultado:** Aún no está listo. todavía no debe presentarse como conjunto limpio final

## Alcance y método

La columna **Antes** corresponde a la unión sin limpieza de los 23 CSV y la
columna **Después (actual)** al resultado en memoria de
`limpiar_datos_preliminar()`. La comparación se limita a las 17 variables
sustantivas. Las dos columnas de trazabilidad y las 29 columnas derivadas de
auditoría no entran en los denominadores porque no existían en la fuente.

Las tablas se regeneran con:

```bash
python src/unir_csv.py
python src/metricas_calidad.py
```

Los resultados tabulares quedan en `reports/calidad/`. Se considera faltante
tanto `NA` como una cadena vacía. Los duplicados exactos se comparan sobre las
17 variables originales, sin `archivo_origen` ni `fila_origen`, porque esas
columnas harían que dos registros iguales aparentaran ser distintos.

## Comparación antes y después

| Métrica | Antes de limpiar | Después de la limpieza preliminar |
|---|---:|---:|
| Registros | 11,890 | 11,890 |
| Variables originales | 17 | 17 |
| Valores faltantes | 4,217 (2.09%) | 4,838 (2.39%) |
| Variables con al menos un faltante | 17 | 17 |
| Duplicados exactos | 23 filas (22 repeticiones) | 23 filas (22 repeticiones) |
| Posibles duplicados parciales | 4,045 filas candidatas | 42 filas confirmadas, todavía sin resolver |
| Variables con formato inconsistente | 9 | 5 |
| Variables con tipo incorrecto | 7 | 0 en memoria |
| Categorías inconsistentes | Pendiente de consolidar | Pendiente de validar |
| Celdas modificadas durante la limpieza | No aplica | 41,164 |

### ¿Cómo se interpreta la comparación?

- La cantidad de registros no cambió porque todavía se conservan las 23 filas
  completamente vacías. Si el equipo aprueba eliminarlas, el resultado final
  tendría 11,867 registros.
- Los faltantes aumentaron porque la limpieza identificó valores que parecían
  texto normal, pero en realidad significaban ausencia de información. Por
  ejemplo, `SIN ESPECIFICAR`, guiones o teléfonos sin números recuperables se
  convirtieron en `NA`. Esto mejora la forma de representar los faltantes; no
  significa que se haya perdido información.
- Los 23 duplicados exactos son las filas vacías. Al ser una misma fila repetida
  23 veces, se cuentan 22 repeticiones adicionales.
- De las 4,045 filas inicialmente marcadas como candidatas a duplicado parcial,
  42 tienen además la misma dirección, jornada y plan. Estas 42 filas forman 21
  grupos y todavía deben revisarse antes de decidir si se conservan, corrigen o
  fusionan.
- Las cinco variables que aún presentan problemas de formato son `DISTRITO`,
  `ESTABLECIMIENTO`, `DIRECCION`, `SUPERVISOR` y `DIRECTOR`.
- Las 17 variables originales se mantienen. El DataFrame también contiene dos
  columnas de trazabilidad y 29 columnas de auditoría, para un total de 48. Esas
  columnas adicionales no se contaron como variables originales.
- Las 41,164 celdas modificadas no representan necesariamente 41,164 errores
  distintos. Una celda se cuenta una vez aunque haya pasado por varias reglas
  de limpieza.

La tabla presenta el resultado disponible al 25 de agosto de 2026. Sigue siendo
una comparación preliminar porque todavía no se ha generado ni validado el CSV
limpio final.

## Valores faltantes por variable

| Variable | Antes, n (%) | Después actual, n (%) | Cambio observado |
|---|---:|---:|---|
| `CODIGO` | 23 (0.19%) | 23 (0.19%) | Solo corresponden a filas completamente vacías. |
| `DISTRITO` | 555 (4.67%) | 555 (4.67%) | Se representan como `NA`; no se imputan. |
| `DEPARTAMENTO` | 23 (0.19%) | 23 (0.19%) | Solo filas vacías. |
| `MUNICIPIO` | 23 (0.19%) | 23 (0.19%) | Solo filas vacías. |
| `ESTABLECIMIENTO` | 28 (0.24%) | 28 (0.24%) | Continúan como cadenas vacías; deben convertirse a `NA` o resolverse. |
| `DIRECCION` | 99 (0.83%) | 271 (2.28%) | Se detectan 172 faltantes disfrazados adicionales. |
| `TELEFONO` | 969 (8.15%) | 993 (8.35%) | Se reclasifican 24 valores sin número recuperable. |
| `SUPERVISOR` | 558 (4.69%) | 561 (4.72%) | Se reconocen 3 marcadores adicionales; no hubo imputaciones efectivas. |
| `DIRECTOR` | 1,755 (14.76%) | 2,174 (18.28%) | Se reconocen 419 marcadores o nombres no identificables adicionales. |
| `NIVEL` | 23 (0.19%) | 23 (0.19%) | Solo filas vacías. |
| `SECTOR` | 23 (0.19%) | 23 (0.19%) | Solo filas vacías. |
| `AREA` | 23 (0.19%) | 26 (0.22%) | Tres valores `SIN ESPECIFICAR` pasan a `NA`. |
| `STATUS` | 23 (0.19%) | 23 (0.19%) | Solo filas vacías. |
| `MODALIDAD` | 23 (0.19%) | 23 (0.19%) | Solo filas vacías. |
| `JORNADA` | 23 (0.19%) | 23 (0.19%) | `SIN JORNADA` se conserva como categoría válida. |
| `PLAN` | 23 (0.19%) | 23 (0.19%) | Solo filas vacías. |
| `DEPARTAMENTAL` | 23 (0.19%) | 23 (0.19%) | Solo filas vacías. |

Que aumente el número de `NA` puede ser una mejora de calidad: ahora la
ausencia se representa de manera uniforme y deja de confundirse con una
categoría o con texto libre. No se imputaron datos sin evidencia.

## Transformaciones observadas

En las 11,867 filas con información cambiaron 41,164 celdas de las variables
originales. Los cambios se concentran en la escritura geográfica canónica
(`DEPARTAMENTO`, `MUNICIPIO` y `DEPARTAMENTAL`), además del tratamiento de
direcciones, teléfonos y nombres de personas. Las columnas `*_ORIGINAL`
permiten auditar el valor anterior.

El formato de `TELEFONO` queda estructuralmente uniforme como uno o varios
números de 7 u 8 dígitos separados por `; `. No obstante, 90 celdas conservan
al menos un número de 7 dígitos; el equipo debe decidir y documentar si ese
formato legado pertenece al dominio válido o si requiere revisión manual.

## Duplicados

Los 23 duplicados exactos son filas completamente vacías: una por archivo de
origen. No representan establecimientos y explican las 22 copias adicionales
de una misma fila vacía. Su eliminación todavía no está implementada ni
registrada como transformación.

La comparación por nombre normalizado y municipio produce 1,112 grupos
candidatos (4,045 filas). Al exigir además la misma jornada, plan y dirección,
quedan 21 grupos confirmados (42 filas). Los códigos son distintos, por lo que
no se deben fusionar automáticamente. Para cada grupo debe registrarse una de
estas decisiones: conservar ambos por ser ofertas distintas, corregir un valor,
fusionar registros o eliminar un duplicado, junto con la evidencia consultada.

## Validación y limitaciones actuales

El pipeline todavía no satisface todas las pruebas finales solicitadas:

- `validar_datos()` termina deliberadamente en `NotImplementedError`.
- `tests/test_calidad.py` no contiene pruebas ejecutables.
- Permanecen 23 filas vacías y, por ello, duplicados exactos sustantivos.
- Permanecen 70 valores de `DISTRITO` con formato incompleto `NN-`.
- Hay 1,395 establecimientos, 485 direcciones, 102 supervisores y 905
  directores con espacios múltiples después de la limpieza.
- `MUNICIPIO` se corrige con un diccionario ortográfico, pero no se valida
  contra un catálogo oficial completo de combinaciones departamento-municipio.
- Los 21 grupos de posibles duplicados confirmados no tienen decisión final.
- No existe todavía un CSV en `data/processed/` ni una definición aprobada de
  las columnas que debe contener.

## Conclusión

La limpieza implementada mejora la representación de faltantes, normaliza la
geografía, estructura los teléfonos y conserva trazabilidad. Sin embargo, el
resultado debe considerarse preliminar. Para poder informar ceros en las
métricas de errores finales primero deben resolverse los casos pendientes,
generarse el CSV procesado y ejecutarse pruebas automáticas completas.
