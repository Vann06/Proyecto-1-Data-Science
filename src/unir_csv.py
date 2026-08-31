"""Une los 23 CSV crudos sin modificar sus 17 variables originales."""

from __future__ import annotations

import csv
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUTPUT_FILE = ROOT / "data" / "interim" / "establecimientos_diversificado_raw_unificado.csv"


def unir_csv(raw_dir: Path = RAW_DIR, output_file: Path = OUTPUT_FILE) -> dict[str, int]:
    """Valida y une los CSV, conservando filas vacías y trazabilidad."""
    archivos = sorted(raw_dir.glob("*.csv"))
    if len(archivos) != 23:
        raise ValueError(f"Se esperaban 23 archivos CSV y se encontraron {len(archivos)}.")

    encabezado_referencia = None
    filas_unificadas = []
    filas_completamente_vacias = 0

    for archivo in archivos:
        with archivo.open("r", encoding="utf-8-sig", newline="") as fuente:
            lector = csv.reader(fuente)
            encabezado = next(lector, None)
            if encabezado is None:
                raise ValueError(f"El archivo {archivo.name} no contiene encabezado.")
            if encabezado_referencia is None:
                encabezado_referencia = encabezado
            elif encabezado != encabezado_referencia:
                raise ValueError(f"El encabezado de {archivo.name} no coincide con el resto.")

            for numero_fila, fila in enumerate(lector, start=2):
                if not fila:
                    continue
                if len(fila) != len(encabezado_referencia):
                    raise ValueError(
                        f"{archivo.name}, fila {numero_fila}, contiene {len(fila)} "
                        f"columnas; se esperaban {len(encabezado_referencia)}."
                    )
                if all(not celda.strip() for celda in fila):
                    filas_completamente_vacias += 1
                filas_unificadas.append(fila + [archivo.name, numero_fila])

    if encabezado_referencia is None:
        raise ValueError("No se encontró ningún encabezado en los archivos CSV.")

    output_file.parent.mkdir(parents=True, exist_ok=True)
    with output_file.open("w", encoding="utf-8-sig", newline="") as destino:
        escritor = csv.writer(destino)
        escritor.writerow(encabezado_referencia + ["archivo_origen", "fila_origen"])
        escritor.writerows(filas_unificadas)

    return {
        "archivos": len(archivos),
        "variables_originales": len(encabezado_referencia),
        "registros_crudos": len(filas_unificadas),
        "registros_con_informacion": len(filas_unificadas) - filas_completamente_vacias,
        "filas_completamente_vacias": filas_completamente_vacias,
    }


def main() -> None:
    resumen = unir_csv()
    print(f"Archivos unidos: {resumen['archivos']}")
    print(f"Variables originales: {resumen['variables_originales']}")
    print("Columnas de trazabilidad: 2")
    print(f"Registros crudos generados: {resumen['registros_crudos']:,}")
    print(f"Registros con información: {resumen['registros_con_informacion']:,}")
    print(f"Filas completamente vacías conservadas: {resumen['filas_completamente_vacias']}")
    print(f"Archivo generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
