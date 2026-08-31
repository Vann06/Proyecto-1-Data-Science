"""Convierte las exportaciones del portal MINEDUC, valida los CSV y los une."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.unir_csv import OUTPUT_FILE, RAW_DIR, unir_csv  # noqa: E402


VARIABLES_ESPERADAS = [
    "CODIGO",
    "DISTRITO",
    "DEPARTAMENTO",
    "MUNICIPIO",
    "ESTABLECIMIENTO",
    "DIRECCION",
    "TELEFONO",
    "SUPERVISOR",
    "DIRECTOR",
    "NIVEL",
    "SECTOR",
    "AREA",
    "STATUS",
    "MODALIDAD",
    "JORNADA",
    "PLAN",
    "DEPARTAMENTAL",
]


def convertir_exportaciones_html(origen: Path, destino: Path = RAW_DIR) -> list[Path]:
    """Convierte tablas HTML descargadas con extensión XLS a CSV UTF-8."""
    archivos = sorted([*origen.glob("*.xls"), *origen.glob("*.html")])
    if len(archivos) != 23:
        raise ValueError(f"Se esperaban 23 exportaciones y se encontraron {len(archivos)}.")
    destino.mkdir(parents=True, exist_ok=True)
    salidas = []
    for archivo in archivos:
        tablas = pd.read_html(archivo, keep_default_na=False)
        candidatas = [tabla for tabla in tablas if list(tabla.columns) == VARIABLES_ESPERADAS]
        if len(candidatas) != 1:
            raise ValueError(f"{archivo.name} no contiene una tabla con el esquema esperado.")
        salida = destino / f"{archivo.stem.upper()}.csv"
        candidatas[0].to_csv(salida, index=False, encoding="utf-8-sig")
        salidas.append(salida)
    return salidas


def validar_csv_crudos(raw_dir: Path = RAW_DIR) -> dict[str, int]:
    """Comprueba cantidad, estructura y filtro de las exportaciones crudas."""
    archivos = sorted(raw_dir.glob("*.csv"))
    if len(archivos) != 23:
        raise ValueError(f"Se esperaban 23 CSV y se encontraron {len(archivos)}.")
    registros = 0
    for archivo in archivos:
        df = pd.read_csv(
            archivo,
            dtype="string",
            keep_default_na=False,
            encoding="utf-8-sig",
        )
        if list(df.columns) != VARIABLES_ESPERADAS:
            raise ValueError(f"El esquema de {archivo.name} no coincide con las 17 variables.")
        nivel = df["NIVEL"].str.strip()
        if not nivel[nivel.ne("")].eq("DIVERSIFICADO").all():
            raise ValueError(f"{archivo.name} contiene registros fuera del filtro DIVERSIFICADO.")
        registros += len(df)
    return {"archivos": len(archivos), "variables": 17, "registros": registros}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-dir", type=Path)
    args = parser.parse_args()
    if args.source_dir:
        convertir_exportaciones_html(args.source_dir)
    validacion = validar_csv_crudos()
    union = unir_csv()
    print(f"CSV crudos validados: {validacion['archivos']}")
    print(f"Registros crudos: {union['registros_crudos']:,}")
    print(f"Archivo unificado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
