# Informe de calidad de los datos

**Conjunto:** establecimientos educativos de Guatemala con nivel Diversificado
**Fuente:** Buscador de establecimientos educativos del Ministerio de Educación
**Fecha de evaluación final:** 31 de agosto de 2026
**Versión:** 1.0.0

## Alcance y método

La columna **Antes** corresponde a la unión sin limpieza de los 23 CSV. La
columna **Después** corresponde al CSV final. Las métricas se regeneran con:

```bash
python src/obtencion.py
python src/generar_dataset.py
python src/metricas_calidad.py
python -m pytest -q
```

Los faltantes se comparan sobre las 17 variables originales. `ZONA_CAPITAL` se
informa como variable derivada y no se incorpora al denominador de faltantes.
Los duplicados exactos también se calculan sobre las 17 variables originales,
sin las columnas técnicas de procedencia.

## Comparación antes y después

| Métrica | Antes de limpiar | Después de limpiar |
|---|---:|---:|
| Registros | 11,890 | 11,867 |
| Variables | 17 | 18 |
| Valores faltantes | 4,217 (2.09%) | 4,602 (2.28%) |
| Variables con al menos un faltante | 17 | 7 |
| Duplicados exactos | 23 filas participantes (22 repeticiones) | 0 |
| Posibles duplicados parciales | 1,085 pares candidatos | 0 decisiones pendientes; 1,085 pares conservados |
| Variables con formato inconsistente | 9 | 0 |
| Variables con tipo incorrecto | 7 | 0 al aplicar el esquema de carga |
| Categorías inconsistentes por escritura | 0 | 0 |
| Errores corregidos | 0 | 44,005 celdas modificadas |

### Interpretación

- Se eliminaron 23 filas completamente vacías que no representaban
  establecimientos. Esto también eliminó los duplicados exactos iniciales.
- Se creó `ZONA_CAPITAL` para conservar la zona que estaba almacenada en
  `MUNICIPIO` dentro de la exportación de Ciudad Capital.
- Los faltantes aumentaron porque los marcadores de ausencia, los 70 distritos
  incompletos y los teléfonos sin un número válido de ocho dígitos se
  representan ahora como `NA` sin inventar información.
- Las siete variables categóricas se cargan con dominios explícitos mediante
  `cargar_csv_limpio()`; la prueba de integración valida el CSV persistido.
- Las 44,005 celdas modificadas cuentan una celda una sola vez, aunque haya
  pasado por más de una regla. El detalle se encuentra en
  `reports/calidad/cambios_por_variable.csv`.

## Valores faltantes por variable

| Variable | Antes, n (%) | Después, n (%) | Decisión final |
|---|---:|---:|---|
| `CODIGO` | 23 (0.19%) | 0 (0.00%) | Los faltantes pertenecían a filas vacías eliminadas. |
| `DISTRITO` | 555 (4.67%) | 602 (5.07%) | Vacíos y 70 códigos `NN-` se representan como `NA`. |
| `DEPARTAMENTO` | 23 (0.19%) | 0 (0.00%) | Se eliminan únicamente las filas vacías. |
| `MUNICIPIO` | 23 (0.19%) | 0 (0.00%) | Se valida por código municipal oficial. |
| `ESTABLECIMIENTO` | 28 (0.24%) | 5 (0.04%) | Cinco códigos conservan nombre faltante. |
| `DIRECCION` | 99 (0.83%) | 248 (2.09%) | Repeticiones del municipio pasan a `NA`. |
| `TELEFONO` | 969 (8.15%) | 1,055 (8.89%) | Solo se conservan números recuperables de ocho dígitos. |
| `SUPERVISOR` | 558 (4.69%) | 538 (4.53%) | Se unifican variantes; no se imputa sin vigencia. |
| `DIRECTOR` | 1,755 (14.76%) | 2,151 (18.13%) | Marcadores y nombres no identificables pasan a `NA`. |
| `NIVEL` | 23 (0.19%) | 0 (0.00%) | Se eliminan únicamente las filas vacías. |
| `SECTOR` | 23 (0.19%) | 0 (0.00%) | Se fija el dominio categórico. |
| `AREA` | 23 (0.19%) | 3 (0.03%) | `SIN ESPECIFICAR` pasa a `NA`. |
| `STATUS` | 23 (0.19%) | 0 (0.00%) | Se fija el dominio categórico. |
| `MODALIDAD` | 23 (0.19%) | 0 (0.00%) | Se fija el dominio categórico. |
| `JORNADA` | 23 (0.19%) | 0 (0.00%) | `SIN JORNADA` se conserva como categoría válida. |
| `PLAN` | 23 (0.19%) | 0 (0.00%) | Se conservan las trece categorías validadas. |
| `DEPARTAMENTAL` | 23 (0.19%) | 0 (0.00%) | Se normaliza con un dominio administrativo propio. |

## Geografía

Los departamentos se validan contra los 22 valores oficiales. Los municipios
se validan por el prefijo municipal de `CODIGO` contra el catálogo de 340
municipios de SEGEPLAN 2026. La prueba comprueba que código, departamento y
municipio coincidan en las 11,867 filas. Las etiquetas de MINEDUC se conservan
cuando difieren legítimamente de la denominación corta publicada por SEGEPLAN.

Los 70 distritos incompletos no se reconstruyen por semejanza: pasan a `NA` y
su contenido queda en `DISTRITO_ORIGINAL`. No permanece ningún distrito con
formato inválido en el CSV final.

## Teléfonos

El formato final es `NNNNNNNN` o una lista separada por `; `. En 90 celdas se
detectó al menos un número legado de siete dígitos. Esos componentes se
descartaron del valor analítico porque no existe evidencia para completar el
dígito faltante; el texto crudo se conserva en `TELEFONO_ORIGINAL`. No queda
ningún teléfono final con letras o con una longitud distinta de ocho dígitos.

## Duplicados

La revisión parcial usa RapidFuzz con similitud mínima de 95 dentro de bloques
que comparten municipio, dirección, jornada y plan. Se evaluaron 1,085 pares y
cada decisión se documenta en
`reports/calidad/duplicados_parciales_revisados.csv`.

Los 1,085 pares se conservan porque cada integrante del par tiene un código
MINEDUC distinto. Un mismo plantel puede contener varias ofertas o registros
administrativos; sin evidencia oficial de baja no corresponde fusionar ni
eliminar códigos. No queda ninguna decisión pendiente y el CSV final conserva
cero duplicados exactos.

## Validación automática

Las pruebas comprueban:

- dimensión y esquema final;
- ausencia de filas vacías y duplicados exactos;
- unicidad y formato de `CODIGO`;
- ausencia de espacios iniciales, finales o múltiples;
- teléfonos de ocho dígitos;
- departamentos, municipios y códigos municipales oficiales;
- dominios y tipos categóricos;
- resolución documentada de distritos, teléfonos y duplicados parciales;
- equivalencia entre el DataFrame generado y el CSV guardado.

## Conclusión

El conjunto versión 1.0.0 contiene 11,867 registros y 18 variables, no tiene
duplicados exactos ni formatos inválidos detectados, y puede reconstruirse
desde los CSV crudos mediante los comandos documentados. Los valores ausentes
se conservan como `NA` cuando no existe evidencia suficiente para corregirlos.
