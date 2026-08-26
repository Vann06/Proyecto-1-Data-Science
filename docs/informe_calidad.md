# Informe de calidad de los datos

**Conjunto:** establecimientos educativos de Guatemala con nivel Diversificado

**Fuente:** Buscador de establecimientos educativos del Ministerio de Educación

**Fecha de evaluación:** 26 de agosto de 2026

**Estado del resultado:** conjunto procesado y validado automáticamente, con
pendientes de revisión manual

## Alcance y método

La columna **Antes** corresponde a la unión sin limpieza de los 23 CSV y la
columna **Después** al resultado de `generar_conjunto_limpio()`. Los faltantes
se comparan sobre las mismas 17 variables originales. `ZONA_CAPITAL` se informa
como una variable derivada, pero no entra en el denominador de faltantes porque
no existía en la fuente.

Las tablas se regeneran con:

```bash
python src/unir_csv.py
python src/generar_dataset.py
python src/metricas_calidad.py
python -m pytest -q
```

Los resultados tabulares quedan en `reports/calidad/`. Se considera faltante
tanto `NA` como una cadena vacía. Los duplicados exactos se comparan sobre las
17 variables originales, sin `archivo_origen` ni `fila_origen`, porque esas
columnas harían que dos registros iguales aparentaran ser distintos.

## Comparación antes y después

| Métrica | Antes de limpiar | Después de limpiar |
|---|---:|---:|
| Registros | 11,890 | 11,867 |
| Variables | 17 | 18 |
| Valores faltantes | 4,217 (2.09%) | 4,447 (2.20%) |
| Variables con al menos un faltante | 17 | 7 |
| Duplicados exactos | 23 filas (22 repeticiones) | 0 |
| Posibles duplicados parciales | 4,045 filas candidatas | 42 filas confirmadas, todavía sin resolver |
| Variables con formato inconsistente | 9 | 1 |
| Variables con tipo incorrecto | 7 | 0 en memoria |
| Categorías inconsistentes | Pendiente de consolidar | Pendiente de validar |
| Celdas modificadas durante la limpieza | No aplica | 43,901 |

### ¿Cómo se interpreta la comparación?

- Se retiraron las 23 filas completamente vacías porque no representaban
  establecimientos. Con esto también desaparecieron los duplicados exactos.
- El conjunto pasó de 17 a 18 variables por la creación de `ZONA_CAPITAL`, que
  conserva la zona que originalmente estaba almacenada en `MUNICIPIO`.
- Los faltantes aumentaron porque la limpieza identificó valores que parecían
  texto normal, pero en realidad significaban ausencia de información. Por
  ejemplo, `SIN ESPECIFICAR`, guiones o teléfonos sin números recuperables se
  convirtieron en `NA`. Esto mejora la forma de representar los faltantes; no
  significa que se haya perdido información.
- Antes de limpiar, los 23 duplicados exactos eran las filas vacías. Al ser una
  misma fila repetida 23 veces, representaban 22 repeticiones adicionales.
- De las 4,045 filas inicialmente marcadas como candidatas a duplicado parcial,
  42 tienen además la misma dirección, jornada y plan. Estas 42 filas forman 21
  grupos y todavía deben revisarse antes de decidir si se conservan, corrigen o
  fusionan.
- La única variable que conserva un formato incompleto es `DISTRITO`, con 70
  valores `NN-` pendientes de revisión. Los espacios múltiples fueron
  normalizados en los demás campos de texto.
- Las 43,901 celdas modificadas no representan necesariamente 43,901 errores
  distintos. Una celda se cuenta una vez aunque haya pasado por varias reglas
  de limpieza.

La tabla presenta el resultado disponible al 26 de agosto de 2026. El CSV
procesado ya se genera y supera las validaciones automáticas, pero conserva los
casos que requieren revisión manual.

## Valores faltantes por variable

| Variable | Antes, n (%) | Después actual, n (%) | Cambio observado |
|---|---:|---:|---|
| `CODIGO` | 23 (0.19%) | 0 (0.00%) | Los faltantes pertenecían a las filas vacías eliminadas. |
| `DISTRITO` | 555 (4.67%) | 532 (4.48%) | Se representan como `NA`; no se imputan. |
| `DEPARTAMENTO` | 23 (0.19%) | 0 (0.00%) | Los faltantes pertenecían a las filas vacías eliminadas. |
| `MUNICIPIO` | 23 (0.19%) | 0 (0.00%) | Los faltantes pertenecían a las filas vacías eliminadas. |
| `ESTABLECIMIENTO` | 28 (0.24%) | 5 (0.04%) | Cinco establecimientos con código conservan el nombre faltante. |
| `DIRECCION` | 99 (0.83%) | 248 (2.09%) | Se reconocen valores que solo repetían el municipio como faltantes. |
| `TELEFONO` | 969 (8.15%) | 970 (8.17%) | Se reclasifican valores sin número recuperable. |
| `SUPERVISOR` | 558 (4.69%) | 538 (4.53%) | Se reconocen marcadores adicionales; no hubo imputaciones seguras. |
| `DIRECTOR` | 1,755 (14.76%) | 2,151 (18.13%) | Se reconocen marcadores o nombres no identificables adicionales. |
| `NIVEL` | 23 (0.19%) | 0 (0.00%) | Los faltantes pertenecían a las filas vacías eliminadas. |
| `SECTOR` | 23 (0.19%) | 0 (0.00%) | Los faltantes pertenecían a las filas vacías eliminadas. |
| `AREA` | 23 (0.19%) | 3 (0.03%) | Tres valores `SIN ESPECIFICAR` pasan a `NA`. |
| `STATUS` | 23 (0.19%) | 0 (0.00%) | Los faltantes pertenecían a las filas vacías eliminadas. |
| `MODALIDAD` | 23 (0.19%) | 0 (0.00%) | Los faltantes pertenecían a las filas vacías eliminadas. |
| `JORNADA` | 23 (0.19%) | 0 (0.00%) | `SIN JORNADA` se conserva como categoría válida. |
| `PLAN` | 23 (0.19%) | 0 (0.00%) | Los faltantes pertenecían a las filas vacías eliminadas. |
| `DEPARTAMENTAL` | 23 (0.19%) | 0 (0.00%) | Los faltantes pertenecían a las filas vacías eliminadas. |

Que aumente el número de `NA` puede ser una mejora de calidad: ahora la
ausencia se representa de manera uniforme y deja de confundirse con una
categoría o con texto libre. No se imputaron datos sin evidencia.

## Transformaciones observadas

En las 11,867 filas con información cambiaron 43,901 celdas de las variables
originales. Los cambios se concentran en la escritura geográfica canónica
(`DEPARTAMENTO`, `MUNICIPIO` y `DEPARTAMENTAL`), además del tratamiento de
direcciones, teléfonos y nombres de personas. Las columnas `*_ORIGINAL`
permiten auditar el valor anterior.

El formato de `TELEFONO` queda estructuralmente uniforme como uno o varios
números de 7 u 8 dígitos separados por `; `. No obstante, 90 celdas conservan
al menos un número de 7 dígitos; el equipo debe decidir y documentar si ese
formato legado pertenece al dominio válido o si requiere revisión manual.

## Duplicados

Los 23 duplicados exactos iniciales eran filas completamente vacías: una por
archivo de origen. Al generar el conjunto procesado se eliminan únicamente las
filas vacías en las 17 variables originales. El resultado no contiene
duplicados exactos.

La comparación por nombre normalizado y municipio produce 1,112 grupos
candidatos (4,045 filas). Al exigir además la misma jornada, plan y dirección,
quedan 21 grupos confirmados (42 filas). Los códigos son distintos, por lo que
no se deben fusionar automáticamente. Para cada grupo debe registrarse una de
estas decisiones: conservar ambos por ser ofertas distintas, corregir un valor,
fusionar registros o eliminar un duplicado, junto con la evidencia consultada.

## Validación y limitaciones actuales

Las cuatro pruebas automáticas implementadas comprueban el esquema, la
dimensión, los duplicados exactos, los espacios, códigos, teléfonos, catálogos
disponibles, tipos y dominios categóricos. Todas finalizan correctamente.

Permanecen estas limitaciones:

- Hay 70 valores de `DISTRITO` con formato incompleto `NN-`.
- Se conservan 90 celdas telefónicas con al menos un número de 7 dígitos.
- `MUNICIPIO` se corrige con un diccionario ortográfico, pero no se valida
  contra un catálogo oficial completo de combinaciones departamento-municipio.
- Los 21 grupos de posibles duplicados confirmados no tienen decisión final.
- La fecha exacta de extracción continúa pendiente de confirmación.

## Conclusión

La limpieza implementada normaliza la geografía y los campos de texto,
estructura los teléfonos, elimina las filas vacías y genera un CSV de 11,867
registros y 18 variables. Las pruebas automáticas confirman que no contiene
duplicados exactos ni espacios inconsistentes. Los casos enumerados en la
sección anterior permanecen documentados para su revisión manual.
