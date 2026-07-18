"""Diagnóstico inicial del conjunto unificado.

Este archivo se trabaja por turnos. Aquí NO se limpian datos.
Antes de comenzar, ejecutar primero: python src/unir_csv.py
"""

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ARCHIVO = ROOT / "data" / "interim" / "establecimientos_diversificado_raw_unificado.csv"


def cargar_datos() -> pd.DataFrame:
    """Carga el archivo unificado conservando todos los campos como texto."""
    return pd.read_csv(
        ARCHIVO,
        dtype="string",
        keep_default_na=False,
        encoding="utf-8-sig",
    )


# ================================================================
# TURNO 1 · VIANKA
# Variables: CODIGO, DISTRITO, DEPARTAMENTO, MUNICIPIO, DEPARTAMENTAL
# Completar aquí:
# - número de registros y variables;
# - tipos de datos;
# - valores faltantes y valores únicos;
# - códigos y distritos con formatos extraños;
# - departamentos o municipios fuera de catálogo;
# - contradicciones entre variables geográficas.
# ================================================================


# ================================================================
# TURNO 2 · RICARDO
# Variables: ESTABLECIMIENTO, DIRECCION, TELEFONO, SUPERVISOR, DIRECTOR
# Completar aquí:
# - espacios, mayúsculas, tildes, puntuación y caracteres especiales;
# - formatos de teléfonos, direcciones y nombres;
# - duplicados exactos;
# - posibles duplicados parciales usando similitud de texto;
# - ejemplos y cantidades de cada problema.
# No eliminar duplicados en esta fase.
# ================================================================


# ================================================================
# TURNO 3 · NADISSA
# Variables: NIVEL, SECTOR, AREA, STATUS, MODALIDAD, JORNADA, PLAN
# Completar aquí:
# - inventario de categorías;
# - categorías vacías o fuera del dominio esperado;
# - diferencias por escritura, tildes, mayúsculas o puntuación;
# - resumen final de los problemas potenciales de calidad.
# ================================================================


if __name__ == "__main__":
    df = cargar_datos()
    print(f"Registros cargados: {len(df):,}")
    print(f"Columnas totales: {len(df.columns)}")
    print("Pendiente: completar las secciones por turnos.")
