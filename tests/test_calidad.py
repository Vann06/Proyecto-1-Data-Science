"""Pruebas automáticas del conjunto limpio y sus pendientes documentados."""

import pandas as pd
import pytest

from src.diagnostico import cargar_datos
from src.limpieza import (
    COLUMNAS_FINALES,
    generar_conjunto_limpio,
    limpiar_datos_preliminar,
)
from src.validacion import validar_datos


@pytest.fixture(scope="module")
def crudo() -> pd.DataFrame:
    return cargar_datos()


@pytest.fixture(scope="module")
def preliminar(crudo: pd.DataFrame) -> pd.DataFrame:
    return limpiar_datos_preliminar(crudo)


@pytest.fixture(scope="module")
def limpio(crudo: pd.DataFrame) -> pd.DataFrame:
    return generar_conjunto_limpio(crudo)


def test_esquema_y_dimension_final(limpio: pd.DataFrame) -> None:
    assert limpio.shape == (11_867, 18)
    assert list(limpio.columns) == COLUMNAS_FINALES


def test_validaciones_automaticas(limpio: pd.DataFrame) -> None:
    validar_datos(limpio)


def test_no_hay_filas_vacias_ni_duplicados(limpio: pd.DataFrame) -> None:
    assert not limpio.isna().all(axis=1).any()
    assert not limpio.duplicated().any()
    assert limpio["CODIGO"].is_unique


def test_pendientes_manual_se_conservan(preliminar: pd.DataFrame) -> None:
    assert int(preliminar["ESTABLECIMIENTO_DUPLICADO_CONFIRMADO"].sum()) == 42
    assert int(preliminar["DISTRITO_INCOMPLETO"].sum()) == 70

    telefono = preliminar["TELEFONO"].dropna().astype("string")
    contiene_siete = telefono.str.contains(
        r"(?:^|; )\d{7}(?:$|; )",
        regex=True,
    )
    assert int(contiene_siete.sum()) == 90
