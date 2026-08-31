# Estructura de limpieza geográfica — Vianka

## Alcance

Esta parte del flujo cubre `CODIGO`, `DISTRITO`, `DEPARTAMENTO`, `MUNICIPIO`,
`DEPARTAMENTAL` y la consistencia entre estas variables. Las transformaciones
se ejecutan desde `src/limpieza.py`; el notebook conserva la evidencia y los
resultados reproducibles.

## Ejecución

Desde la raíz del repositorio:

```bash
python src/unir_csv.py
python src/generar_catalogo_municipios.py
python src/metricas_calidad.py
python -m pytest -q
```

## Componentes

| Archivo | Propósito |
|---|---|
| `src/limpieza.py` | Flujo integrado de limpieza |
| `src/catalogos_geograficos.py` | Dominios y funciones geográficas |
| `data/reference/municipios_guatemala.csv` | Catálogo de 340 municipios y códigos oficiales |
| `docs/registro_transformaciones.csv` | Registro de reglas, cantidades y justificación |
| `notebooks/03_limpieza_datos_turno1_vianka.ipynb` | Evidencia del turno geográfico |

## Reglas finales

| Variable | Tipo final | Tratamiento |
|---|---|---|
| `CODIGO` | Texto | Normaliza espacios y caracteres invisibles; valida `NN-NN-NNNN-NN` y unicidad. |
| `DISTRITO` | Texto anulable | Conserva `NN-NNN` y `NN-NN-NNNN`; convierte vacíos, marcadores e incompletos `NN-` a `NA`. |
| `DEPARTAMENTO` | Categórico | Usa los 22 departamentos; `CIUDAD CAPITAL` se asigna a Guatemala. |
| `MUNICIPIO` | Categórico | Valida y normaliza el nombre mediante el código municipal y el catálogo de 340 municipios. |
| `DEPARTAMENTAL` | Categórico | Usa un dominio administrativo independiente de 26 categorías. |
| `ZONA_CAPITAL` | Texto anulable | Conserva como variable derivada la zona presente en el municipio original. |

Los valores originales y las banderas de auditoría permiten rastrear cada
decisión. Los códigos fuera de formato no se reconstruyen y los valores sin una
referencia suficiente se representan como `NA`.
