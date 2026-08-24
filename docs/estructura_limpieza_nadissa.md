# Estructura de limpieza - Nadissa

## Alcance

Variables asignadas: `NIVEL`, `SECTOR`, `AREA`, `STATUS`, `MODALIDAD`,
`JORNADA` y `PLAN`.

## Flujo reproducible

1. Ejecutar `python src/unir_csv.py` para reconstruir el archivo unificado.
2. Ejecutar `notebooks/03_limpieza_datos_turno3_nadissa.ipynb`.
3. El notebook llama a `limpiar_datos_preliminar()` desde `src/limpieza.py`,
   valida las categorías y genera
   `data/interim/establecimientos_diversificado_limpio_preliminar.csv`.

El notebook no duplica reglas y nunca modifica `data/raw/`.

## Decisiones documentadas

- `NIVEL` se conserva como categoría constante por el filtro de extracción.
- `SECTOR`, `STATUS`, `MODALIDAD`, `JORNADA` y `PLAN` se convierten a tipo
  categórico con sus dominios aprobados.
- `AREA = SIN ESPECIFICAR` se reclasifica a `NA`.
- Los doce registros `RURAL` de Ciudad Capital se conservan. Nadissa verificó
  manualmente los códigos `00-01-0512-46`, `00-02-0137-46` y `00-07-0007-46`:
  código, nombre y dirección coincidieron exactamente con la fuente; los tres
  pertenecen al área rural.
