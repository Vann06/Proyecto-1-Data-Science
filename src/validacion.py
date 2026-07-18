"""Validaciones automáticas del conjunto limpio.

Este archivo se completa después de implementar la limpieza.
Cada persona agrega pruebas para sus variables, siguiendo el mismo orden.
"""

import pandas as pd


def validar_datos(df: pd.DataFrame) -> None:
    """Ejecutará las reglas de calidad definidas por el equipo."""

    # ============================================================
    # TURNO 1 · VIANKA
    # Validar códigos, distritos, departamentos, municipios y coherencia geográfica.
    # ============================================================

    # ============================================================
    # TURNO 2 · RICARDO
    # Validar espacios, teléfonos, nombres, direcciones y duplicados.
    # ============================================================

    # ============================================================
    # TURNO 3 · NADISSA
    # Validar categorías, tipos de datos y resumen general de calidad.
    # ============================================================

    # Validaciones generales que deberán quedar completas al final:
    # - cero duplicados exactos;
    # - cero espacios al inicio o final de textos;
    # - teléfonos con el formato aprobado;
    # - departamentos y municipios dentro del catálogo;
    # - tipos de datos correctos;
    # - categorías sin variantes equivalentes;
    # - valores inválidos detectados en el diagnóstico igual a cero.

    raise NotImplementedError("Las validaciones se completarán después de la limpieza.")
