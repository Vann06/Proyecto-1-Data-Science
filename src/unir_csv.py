"""Unión reproducible de los CSV crudos, sin limpieza.

Los archivos originales deben permanecer en data/raw/.
El resultado se guarda en data/interim/ y agrega únicamente:
- archivo_origen
- fila_origen
"""

from pathlib import Path
import pandas as pd

RAW_DIR = Path("../data/raw")
INTERIM_DIR = Path("../data/interim")
OUTPUT_FILE = INTERIM_DIR / "establecimientos_diversificado_raw_unificado.csv"

INTERIM_DIR.mkdir(parents=True, exist_ok=True)

archivos = sorted(RAW_DIR.glob("*.csv"))

if len(archivos) != 23:
    raise ValueError(
        f"Se esperaban 23 CSV crudos y se encontraron {len(archivos)}."
    )

dataframes = []

for archivo in archivos:
    df_archivo = pd.read_csv(
        archivo,
        dtype="string",
        keep_default_na=False,
        encoding="utf-8-sig",
    )

    df_archivo["archivo_origen"] = archivo.name
    df_archivo["fila_origen"] = range(2, len(df_archivo) + 2)
    dataframes.append(df_archivo)

columnas_base = list(dataframes[0].columns[:-2])

for archivo, df_archivo in zip(archivos, dataframes):
    if list(df_archivo.columns[:-2]) != columnas_base:
        raise ValueError(f"El esquema de {archivo.name} no coincide.")

df_unificado = pd.concat(dataframes, ignore_index=True)

df_unificado.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8-sig",
)

print(f"Archivos unidos: {len(archivos)}")
print(f"Registros: {len(df_unificado):,}")
print(f"Variables originales: {len(columnas_base)}")
print(f"Archivo generado: {OUTPUT_FILE}")
