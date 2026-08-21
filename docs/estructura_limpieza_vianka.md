# Estructura independiente de limpieza — Vianka

## Alcance

Mis responsabilidades comprenden el uso de limpieza para:
`CODIGO`, `DISTRITO`, `DEPARTAMENTO`,`MUNICIPIO` y `DEPARTAMENTAL`, además de la consistencia geográfica entre
estas variables.

## Ejecución reproducible

Desde la raíz del repositorio:

```bash
python src/unir_csv.py
pytest -q tests/test_limpieza_integrada.py
```

El notebook `notebooks/03_limpieza_datos_turno1_vianka.ipynb` presenta las
cantidades, ejemplos y conclusiones, pero no contiene reglas duplicadas: todas
las transformaciones se importan desde `src/limpieza.py`, igual que en el
notebook de Ricardo.

La limpieza compartida es preliminar y conserva las 11,890 filas, incluidas
las 23 filas vacías, porque en esta fase no se elimina nada. `src/limpieza.py`
es el único flujo de limpieza; `src/catalogos_geograficos.py` contiene solo
dominios y funciones escalares de normalización.

Se generan:

| Salida | Propósito |
|---|---|
| `src/limpieza.py` | Único flujo ejecutable de limpieza preliminar para Vianka y Ricardo |
| `src/catalogos_geograficos.py` | Dominios y normalización geográfica; no ejecuta transformaciones |
| `docs/registro_transformaciones.csv` | Tabla de problema, transformación, registros afectados y justificación |
| `notebooks/03_limpieza_datos_turno1_vianka.ipynb` | Evidencia reproducible, ejemplos y cantidades del turno 1 |

## Reglas por variable

| Variable | Tipo final | Tratamiento |
|---|---|---|
| `CODIGO` | Texto | Normaliza espacios y caracteres invisibles; conserva ceros; valida `NN-NN-NNNN-NN` y unicidad. No reconstruye códigos. |
| `DISTRITO` | Texto anulable | Convierte vacío y marcadores exactos a `NA`; conserva los formatos `NN-NNN` y `NN-NN-NNNN`; los valores `NN-` quedan en revisión manual. |
| `DEPARTAMENTO` | Texto categórico | Usa el dominio oficial de 22 departamentos, con tildes y escritura consistente. `CIUDAD CAPITAL` se asigna a `Guatemala`. |
| `MUNICIPIO` | Texto categórico | Normaliza mayúsculas, artículos y tildes de forma determinista. En Ciudad Capital se asigna `Guatemala`; `PACHALUN` se corrige a `Pachalum` por el código municipal 14-21. |
| `DEPARTAMENTAL` | Texto categórico | Usa un catálogo administrativo independiente de 26 categorías. Conserva las cuatro regiones de Guatemala y `Quiché Norte`. |
| `ZONA_CAPITAL` | Texto categórico anulable | Variable derivada desde el `MUNICIPIO` original cuando `DEPARTAMENTO = CIUDAD CAPITAL`; conserva valores como `Zona 1`. |

## Cobertura de los criterios de calidad

- Faltantes, cadenas vacías y marcadores: se unifican como `NA` después de
  normalizar espacios, Unicode y caracteres invisibles.
- Tipos: los códigos permanecen como texto; las variables geográficas se
  escriben como texto canónico compatible con CSV.
- Categorías y formatos: se usan diccionarios cerrados para departamentos y
  departamentales. No se usa coincidencia aproximada para reemplazar valores.
- Valores inválidos: se marcan con columnas booleanas y conservan
  `archivo_origen` y `fila_origen` para su revisión.
- Duplicados: se buscan códigos duplicados y coincidencias exactas en las cinco
  variables; ningún registro se elimina automáticamente. La similitud de
  nombres de establecimientos corresponde a la parte de Ricardo y no debe
  aplicarse sobre códigos geográficos secuenciales.
- Consistencia: el prefijo de `CODIGO` se compara con `DEPARTAMENTO`; también
  se comprueba que un mismo prefijo `NN-NN` no apunte a municipios distintos.
  La zona capitalina se separa del municipio.
- Variables derivadas: `ZONA_CAPITAL` evita perder la sububicación al corregir
  el nivel geográfico.


Los distritos incompletos se conservan y se marcan porque no existe evidencia
suficiente para completar sus dígitos. Del mismo modo, cualquier valor fuera de
los catálogos o código duplicado queda en el reporte y no se elimina. La fuente
ortográfica de referencia es la [lista de códigos de departamentos y municipios
del Instituto Nacional de Estadística (INE)](https://www.ine.gob.gt/sistema/uploads/2015/12/11/DDrIEuLOPuEcXTcLXab1yOkiOV2HQreq.pdf);
si se incorpora una versión más reciente del catálogo, los diccionarios y las
pruebas deben versionarse juntos.
