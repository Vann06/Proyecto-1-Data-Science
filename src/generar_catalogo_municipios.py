"""Genera el catálogo municipal usado para validar la geografía del proyecto."""

from __future__ import annotations

import argparse
import sys
from io import BytesIO
from pathlib import Path
from urllib.request import urlopen

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.catalogos_geograficos import DEPARTAMENTOS_POR_CODIGO, nombre_geografico  # noqa: E402


URL_SEGEPLAN = (
    "https://datos.segeplan.gob.gt/dataset/"
    "f4ee4102-b724-4617-8343-95a03e7fe34b/resource/"
    "8df77811-4e24-4fe8-af78-6e40153850f8/download/"
    "calculo-matematico-para-la-asignacion-constitucional-a-las-"
    "municipalidades-del-ano-2026.csv"
)
SALIDA = ROOT / "data" / "reference" / "municipios_guatemala.csv"


def _leer_fuente(ruta: Path | None = None) -> pd.DataFrame:
    if ruta is None:
        with urlopen(URL_SEGEPLAN, timeout=120) as respuesta:
            fuente = BytesIO(respuesta.read())
    else:
        fuente = ruta

    tabla = pd.read_csv(fuente, encoding="cp1252", sep=";").iloc[:, :3]
    tabla.columns = ["codigo", "municipio_segeplan", "abreviatura_departamento"]
    tabla = tabla.dropna(subset=["codigo", "municipio_segeplan"]).copy()
    tabla["codigo"] = tabla["codigo"].astype(int).astype(str).str.zfill(4)
    if len(tabla) != 340 or tabla["codigo"].nunique() != 340:
        raise ValueError("La fuente de SEGEPLAN no contiene 340 códigos municipales únicos.")
    return tabla


def _nombres_observados_mineduc() -> dict[str, str]:
    filas = []
    for archivo in sorted((ROOT / "data" / "raw").glob("*.csv")):
        df = pd.read_csv(
            archivo,
            dtype="string",
            keep_default_na=False,
            encoding="utf-8-sig",
            usecols=["CODIGO", "MUNICIPIO"],
        )
        filas.append(df)

    raw = pd.concat(filas, ignore_index=True)
    raw = raw.loc[raw["CODIGO"].str.fullmatch(r"\d{2}-\d{2}-\d{4}-\d{2}")].copy()
    raw["codigo_municipio"] = raw["CODIGO"].str.slice(0, 5).str.replace("-", "", regex=False)
    raw.loc[raw["codigo_municipio"].str.startswith("00"), "codigo_municipio"] = "0101"
    raw["municipio"] = raw["MUNICIPIO"].map(nombre_geografico)
    raw.loc[raw["codigo_municipio"].eq("0101"), "municipio"] = "Guatemala"

    unicos = raw.dropna(subset=["municipio"]).groupby("codigo_municipio")["municipio"].nunique()
    ambiguos = unicos[unicos > 1]
    if not ambiguos.empty:
        raise ValueError(f"Códigos municipales ambiguos en MINEDUC: {ambiguos.index.tolist()}")
    return raw.dropna(subset=["municipio"]).groupby("codigo_municipio")["municipio"].first().to_dict()


def generar_catalogo(fuente: Path | None = None, salida: Path = SALIDA) -> pd.DataFrame:
    tabla = _leer_fuente(fuente)
    observados = _nombres_observados_mineduc()
    tabla["codigo_departamento"] = tabla["codigo"].str[:2]
    tabla["codigo_municipio"] = tabla["codigo"]
    tabla["departamento"] = tabla["codigo_departamento"].map(DEPARTAMENTOS_POR_CODIGO)
    tabla["municipio_segeplan"] = tabla["municipio_segeplan"].str.strip().map(nombre_geografico)
    tabla["municipio_mineduc"] = tabla["codigo"].map(observados).fillna(tabla["municipio_segeplan"])
    catalogo = tabla[
        [
            "codigo_departamento",
            "codigo_municipio",
            "departamento",
            "municipio_segeplan",
            "municipio_mineduc",
        ]
    ].sort_values("codigo_municipio")
    salida.parent.mkdir(parents=True, exist_ok=True)
    catalogo.to_csv(salida, index=False, encoding="utf-8-sig")
    return catalogo


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path)
    parser.add_argument("--output", type=Path, default=SALIDA)
    args = parser.parse_args()
    catalogo = generar_catalogo(args.source, args.output)
    print(f"Municipios: {len(catalogo)}")
    print(f"Archivo generado: {args.output}")


if __name__ == "__main__":
    main()
