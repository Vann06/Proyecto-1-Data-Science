"""Une los 23 CSV crudos sin limpiar ni modificar sus valores.

Uso desde la raíz del repositorio:
    python src/unir_csv.py

Resultado:
    data/interim/establecimientos_diversificado_raw_unificado.csv
"""

from pathlib import Path

import pandas as pd

# Las rutas se calculan desde este archivo para que el programa funcione
# aunque se ejecute desde otra carpeta.
ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
INTERIM_DIR = ROOT / "data" / "interim"
OUTPUT_FILE = INTERIM_DIR / "establecimientos_diversificado_raw_unificado.csv"


def unir_archivos() -> pd.DataFrame:
    """Lee, valida y concatena los 23 CSV crudos."""

    archivos = sorted(RAW_DIR.glob("*.csv"))

    if len(archivos) != 23:
        raise ValueError(
            f"Se esperaban 23 CSV en {RAW_DIR} y se encontraron {len(archivos)}."
        )

    dataframes = []
    columnas_referencia = None

    for archivo in archivos:
        # Todo se lee como texto para no alterar códigos ni teléfonos.
        df_archivo = pd.read_csv(
            archivo,
            dtype="string",
            keep_default_na=False,
            encoding="utf-8-sig",
        )

        if columnas_referencia is None:
            columnas_referencia = list(df_archivo.columns)
        elif list(df_archivo.columns) != columnas_referencia:
            raise ValueError(f"El esquema de {archivo.name} no coincide.")

        # Estas dos columnas solo permiten rastrear el origen del registro.
        df_archivo["archivo_origen"] = archivo.name
        df_archivo["fila_origen"] = range(2, len(df_archivo) + 2)
        dataframes.append(df_archivo)

    df_unificado = pd.concat(dataframes, ignore_index=True)

    INTERIM_DIR.mkdir(parents=True, exist_ok=True)
    df_unificado.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    return df_unificado


if __name__ == "__main__":
    datos = unir_archivos()
    print("Archivos unidos: 23")
    print(f"Registros: {len(datos):,}")
    print("Variables originales: 17")
    print(f"Archivo generado: {OUTPUT_FILE}")
