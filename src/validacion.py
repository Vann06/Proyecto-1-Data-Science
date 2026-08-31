"""Validaciones automáticas del conjunto limpio y del CSV persistido."""

import re
from pathlib import Path

import pandas as pd

from src.catalogos_geograficos import (
    DEPARTAMENTALES_CANONICAS,
    DEPARTAMENTOS_POR_CODIGO,
    PATRON_CODIGO,
    PATRON_DISTRITO_CORTO,
    PATRON_DISTRITO_EXTENDIDO,
    cargar_catalogo_municipios,
    codigo_municipal_desde_establecimiento,
)
from src.limpieza import CATEGORIAS_NADISSA, COLUMNAS_FINALES


ROOT = Path(__file__).resolve().parents[1]
CSV_LIMPIO = ROOT / "data" / "processed" / "establecimientos_diversificado_limpio.csv"


def cargar_csv_limpio(ruta: Path = CSV_LIMPIO) -> pd.DataFrame:
    """Carga el CSV final aplicando el esquema documentado en el codebook."""
    df = pd.read_csv(ruta, dtype="string", encoding="utf-8-sig")
    for columna, dominio in CATEGORIAS_NADISSA.items():
        df[columna] = df[columna].astype(pd.CategoricalDtype(categories=dominio))
    return df


def validar_categorias_nadissa(df: pd.DataFrame) -> None:
    """Comprueba tipo, dominio y decisiones de limpieza categoricas."""
    for columna, dominio in CATEGORIAS_NADISSA.items():
        if not isinstance(df[columna].dtype, pd.CategoricalDtype):
            raise AssertionError(f"{columna} debe tener tipo categorico.")
        if not set(df[columna].dropna().astype("string")).issubset(dominio):
            raise AssertionError(f"{columna} contiene valores fuera del dominio aprobado.")
    if df["AREA"].astype("string").eq("SIN ESPECIFICAR").any():
        raise AssertionError("AREA no debe conservar SIN ESPECIFICAR.")
    if df["JORNADA"].astype("string").eq("SIN JORNADA").sum() == 0:
        raise AssertionError("JORNADA debe conservar SIN JORNADA.")


def validar_datos(df: pd.DataFrame) -> None:
    """Comprueba el esquema y las reglas automáticas del conjunto final."""
    if list(df.columns) != COLUMNAS_FINALES:
        raise AssertionError(
            "El esquema final no coincide con las 18 variables aprobadas."
        )
    if df.empty:
        raise AssertionError("El conjunto limpio no puede estar vacío.")
    if df.duplicated().any():
        raise AssertionError("El conjunto limpio contiene duplicados exactos.")

    texto = df.select_dtypes(include=["string", "object"])
    for columna in texto.columns:
        serie = texto[columna].astype("string")
        con_valor = serie.notna()
        if (con_valor & serie.ne(serie.str.strip())).any():
            raise AssertionError(f"{columna} contiene espacios en los extremos.")
        if serie.str.contains(r"\s{2,}", regex=True).fillna(False).any():
            raise AssertionError(f"{columna} contiene espacios múltiples.")

    codigo = df["CODIGO"].astype("string")
    if codigo.isna().any() or ~codigo.str.fullmatch(PATRON_CODIGO).all():
        raise AssertionError("CODIGO contiene faltantes o formatos inválidos.")
    if codigo.duplicated().any():
        raise AssertionError("CODIGO debe ser único.")

    distrito = df["DISTRITO"].astype("string")
    distrito_valido = (
        distrito.isna()
        | distrito.str.fullmatch(PATRON_DISTRITO_CORTO).fillna(False)
        | distrito.str.fullmatch(PATRON_DISTRITO_EXTENDIDO).fillna(False)
    )
    if not distrito_valido.all():
        raise AssertionError("DISTRITO contiene un formato no documentado.")

    departamentos = set(DEPARTAMENTOS_POR_CODIGO.values())
    if not set(df["DEPARTAMENTO"].dropna()).issubset(departamentos):
        raise AssertionError("DEPARTAMENTO contiene valores fuera del catálogo.")

    departamentales = set(DEPARTAMENTALES_CANONICAS.values())
    if not set(df["DEPARTAMENTAL"].dropna()).issubset(departamentales):
        raise AssertionError("DEPARTAMENTAL contiene valores fuera del catálogo.")

    catalogo = cargar_catalogo_municipios().set_index("codigo_municipio")
    codigo_municipal = codigo_municipal_desde_establecimiento(df["CODIGO"])
    municipio_esperado = codigo_municipal.map(catalogo["municipio_mineduc"])
    departamento_esperado = codigo_municipal.map(catalogo["departamento"])
    if municipio_esperado.isna().any():
        raise AssertionError("CODIGO contiene un código municipal fuera del catálogo.")
    if not df["MUNICIPIO"].astype("string").eq(municipio_esperado).all():
        raise AssertionError("MUNICIPIO no corresponde al código municipal oficial.")
    if not df["DEPARTAMENTO"].astype("string").eq(departamento_esperado).all():
        raise AssertionError("DEPARTAMENTO no corresponde al código municipal oficial.")

    zona = df["ZONA_CAPITAL"].astype("string")
    zona_valida = zona.isna() | zona.str.fullmatch(r"Zona \d{1,2}").fillna(False)
    if not zona_valida.all():
        raise AssertionError("ZONA_CAPITAL contiene un formato inválido.")

    telefono = df["TELEFONO"].astype("string")
    telefono_valido = (
        telefono.isna()
        | telefono.str.fullmatch(r"\d{8}(?:; \d{8})*").fillna(False)
    )
    if not telefono_valido.all():
        raise AssertionError("TELEFONO contiene un formato no documentado.")

    validar_categorias_nadissa(df)
