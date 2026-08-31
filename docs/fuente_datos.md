# Fuente de los datos

## Información general

- **Fuente:** Ministerio de Educación de Guatemala.
- **Sistema:** Buscador de establecimientos educativos.
- **Enlace:** http://www.mineduc.gob.gt/BUSCAESTABLECIMIENTO_GE/
- **Filtro utilizado:** `NIVEL ESCOLAR: DIVERSIFICADO`.
- **Cobertura:** todo el país.
- **Archivos obtenidos:** 23 exportaciones.
- **Fecha de extracción y conversión documentada por el equipo:** 17 de julio de 2026.

## Archivos

Los 23 archivos representan los 22 departamentos y una exportación separada de Ciudad Capital.

Todos los archivos crudos se guardan en:

```text
data/raw/
```

## Conversión a CSV

El portal entregó archivos con extensión `.xls`, pero internamente contenían tablas HTML. Se convirtieron a CSV en codificación UTF-8 con BOM para que puedan abrirse correctamente en Excel y Python.

Durante la conversión:

- no se cambiaron nombres de columnas;
- no se eliminaron filas;
- no se corrigieron valores;
- no se normalizaron espacios, tildes, mayúsculas ni teléfonos;
- no se reemplazaron valores faltantes;
- se conservaron las filas vacías presentes en las exportaciones.

La conversión es reproducible con `python src/obtencion.py --source-dir RUTA`,
donde `RUTA` contiene las 23 exportaciones HTML guardadas con extensión `.xls`.
Si los CSV ya existen, `python src/obtencion.py` valida el esquema, comprueba el
filtro `DIVERSIFICADO` y genera la unión.

## Catálogo geográfico de referencia

La combinación de departamento y municipio se valida contra los 340 códigos
municipales publicados por SEGEPLAN en el conjunto *Cálculo Matemático para la
Asignación Constitucional a las Municipalidades 2026*. El recurso se consultó
el 31 de agosto de 2026 y el catálogo derivado se conserva en
`data/reference/municipios_guatemala.csv`.

Por esta razón, los CSV de `data/raw/` se consideran datos crudos y no deben editarse manualmente.

## Validación inicial

| Validación | Resultado |
|---|---:|
| Archivos esperados | 23 |
| Archivos recibidos | 23 |
| Variables originales por archivo | 17 |
| Archivos con la misma estructura | 23 |
| Filas totales al unir | 11,890 |
| Filas con información | 11,867 |
| Filas completamente vacías | 23 |

## Unión de archivos

La unión se genera con:

```bash
python src/unir_csv.py
```

El archivo resultante se guarda en:

```text
data/interim/establecimientos_diversificado_raw_unificado.csv
```

El archivo unificado conserva las 17 variables originales y agrega únicamente `archivo_origen` y `fila_origen` para poder rastrear cada registro. Estas dos columnas son técnicas y no deben contarse como variables originales en el diagnóstico.
