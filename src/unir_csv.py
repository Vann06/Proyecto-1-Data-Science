"""Une los 23 CSV crudos sin cambiarlos

Resultado:
- conserva únicamente las 17 columnas originales
- mantiene una sola fila de encabezados
- elimina solo filas completamente vacías
- no agrega columnas de trazabilidad
- no limpia, corrige ni normaliza ningún otro dato.

Ejecutar desde la raíz del repositorio:
    python src/unir_csv.py
"""

from pathlib import Path
import csv

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
OUTPUT_FILE = (
    ROOT
    / "data"
    / "interim"
    / "establecimientos_diversificado_raw_unificado.csv"
)

archivos = sorted(RAW_DIR.glob("*.csv"))

if len(archivos) != 23:
    raise ValueError(
        f"Se esperaban 23 CSV y se encontraron {len(archivos)}."
    )

encabezado_referencia = None
filas_unificadas = []
filas_vacias_eliminadas = 0

for archivo in archivos:
    with archivo.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as fuente:
        lector = csv.reader(fuente)
        encabezado = next(lector)

        if encabezado_referencia is None:
            encabezado_referencia = encabezado
        elif encabezado != encabezado_referencia:
            raise ValueError(
                f"El encabezado de {archivo.name} no coincide."
            )

        for fila in lector:
            if len(fila) != len(encabezado_referencia):
                raise ValueError(
                    f"{archivo.name} contiene una fila con "
                    f"{len(fila)} columnas; se esperaban "
                    f"{len(encabezado_referencia)}."
                )

            # Única exclusión: filas completamente vacías.
            if all(celda == "" for celda in fila):
                filas_vacias_eliminadas += 1
                continue

            filas_unificadas.append(fila)

# Verificar que sí se haya encontrado un encabezado.
if encabezado_referencia is None:
    raise ValueError(
        "No se encontró ningún encabezado en los archivos CSV."
    )

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_FILE.open(
    "w",
    encoding="utf-8-sig",
    newline="",
) as destino:
    escritor = csv.writer(destino)
    escritor.writerow(encabezado_referencia)
    escritor.writerows(filas_unificadas)

print(f"Archivos unidos: {len(archivos)}")
print(f"Variables originales: {len(encabezado_referencia)}")
print(f"Registros generados: {len(filas_unificadas):,}")
print(
    "Filas completamente vacías eliminadas: "
    f"{filas_vacias_eliminadas}"
)
print(f"Archivo generado: {OUTPUT_FILE}")