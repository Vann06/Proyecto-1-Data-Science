# Catálogos de referencia

`municipios_guatemala.csv` contiene los 340 códigos municipales usados para
validar la combinación de código, departamento y municipio del conjunto final.

- Fuente oficial: Secretaría de Planificación y Programación de la Presidencia
  (SEGEPLAN).
- Conjunto: *Cálculo Matemático para la Asignación Constitucional a las
  Municipalidades 2026*.
- Fecha de consulta: 31 de agosto de 2026.
- Recurso original: <https://datos.segeplan.gob.gt/dataset/calculo-matematico-para-la-asignacion-constitucional-a-las-municipalidades-2026>

La columna `municipio_segeplan` conserva la etiqueta publicada por SEGEPLAN.
`municipio_mineduc` conserva la etiqueta canónica usada por el conjunto de
MINEDUC cuando ambas instituciones emplean formas legítimas diferentes. El
catálogo se regenera con:

```bash
python src/generar_catalogo_municipios.py
```
