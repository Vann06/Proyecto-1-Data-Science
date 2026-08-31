"""Pruebas automáticas del conjunto limpio y las decisiones documentadas."""

import pandas as pd
import pytest

from src.diagnostico import cargar_datos
from src.limpieza import (
    COLUMNAS_FINALES,
    generar_conjunto_limpio,
    limpiar_datos_preliminar,
    revisar_duplicados_parciales,
)
from src.validacion import cargar_csv_limpio, validar_datos
from src.unir_csv import OUTPUT_FILE, unir_csv


@pytest.fixture(scope="module")
def crudo() -> pd.DataFrame:
    if not OUTPUT_FILE.exists():
        unir_csv()
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


def test_casos_documentados_quedan_resueltos(preliminar: pd.DataFrame) -> None:
    assert int(preliminar["ESTABLECIMIENTO_DUPLICADO_CONFIRMADO"].sum()) == 42
    assert int(preliminar["DISTRITO_INCOMPLETO"].sum()) == 70
    assert int(preliminar["DISTRITO_REQUIERE_REVISION"].sum()) == 0
    assert not preliminar["DISTRITO"].dropna().str.fullmatch(r"\d{2}-").any()
    assert int(preliminar["TELEFONO_DESCARTO_7_DIGITOS"].sum()) == 90
    assert not preliminar["TELEFONO"].dropna().str.contains(
        r"(?:^|; )\d{7}(?:$|; )", regex=True
    ).any()
    revisados = revisar_duplicados_parciales(preliminar)
    assert len(revisados) > 0
    assert set(revisados["decision"]) == {"CONSERVAR"}


def test_csv_persistido_cumple_el_esquema(limpio: pd.DataFrame) -> None:
    persistido = cargar_csv_limpio()
    validar_datos(persistido)
    pd.testing.assert_frame_equal(
        persistido.reset_index(drop=True),
        limpio.reset_index(drop=True),
        check_dtype=True,
    )
