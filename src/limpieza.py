"""Limpieza reproducible del conjunto de datos.

IMPORTANTE:
No escribir transformaciones aquí hasta que la regla esté documentada y
aprobada en docs/plan_limpieza.md.

El archivo se trabaja por turnos: Vianka, Ricardo y Nadissa.
"""

import pandas as pd


def limpiar_datos(df: pd.DataFrame) -> pd.DataFrame:
    """Aplicará únicamente las reglas aprobadas en el plan de limpieza."""

    limpio = df.copy()

    # ============================================================
    # TURNO 1 · VIANKA
    # CODIGO, DISTRITO, DEPARTAMENTO, MUNICIPIO, DEPARTAMENTAL
    # Agregar aquí solo las reglas previamente aprobadas.
    # ============================================================

    # ============================================================
    # TURNO 2 · RICARDO
    # ESTABLECIMIENTO, DIRECCION, TELEFONO, SUPERVISOR, DIRECTOR
    # Agregar aquí solo las reglas previamente aprobadas.
    # Los duplicados parciales deben revisarse antes de decidir.
    # ============================================================

    # ============================================================
    # TURNO 3 · NADISSA
    # NIVEL, SECTOR, AREA, STATUS, MODALIDAD, JORNADA, PLAN
    # Agregar aquí solo las reglas previamente aprobadas.
    # ============================================================

    return limpio
