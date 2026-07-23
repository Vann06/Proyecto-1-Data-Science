"""Une los 23 CSV crudos sin limpiar sus variables originales.

Resultado:
- conserva las 17 variables originales;
- conserva todas las filas, incluso las completamente vacías;
- agrega archivo_origen y fila_origen para mantener trazabilidad;
- no corrige, normaliza ni elimina registros.

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
        f"Se esperaban 23 archivos CSV y se encontraron {len(archivos)}."
    )

encabezado_referencia = None
filas_unificadas = []
filas_completamente_vacias = 0

for archivo in archivos:
    with archivo.open(
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as fuente:
        lector = csv.reader(fuente)
        encabezado = next(lector, None)

        if encabezado is None:
            raise ValueError(
                f"El archivo {archivo.name} no contiene encabezado."
            )

        if encabezado_referencia is None:
            encabezado_referencia = encabezado

        elif encabezado != encabezado_referencia:
            raise ValueError(
                f"El encabezado de {archivo.name} no coincide "
                "con el resto de los archivos."
            )

        for numero_fila, fila in enumerate(lector, start=2):
            # Las líneas físicas completamente vacías no se consideran registros.
            if not fila:
                continue

            if len(fila) != len(encabezado_referencia):
                raise ValueError(
                    f"{archivo.name}, fila {numero_fila}, contiene "
                    f"{len(fila)} columnas; se esperaban "
                    f"{len(encabezado_referencia)}."
                )

            if all(not celda.strip() for celda in fila):
                filas_completamente_vacias += 1

            filas_unificadas.append(
                fila + [archivo.name, numero_fila]
            )

if encabezado_referencia is None:
    raise ValueError(
        "No se encontró ningún encabezado en los archivos CSV."
    )

encabezado_salida = encabezado_referencia + [
    "archivo_origen",
    "fila_origen",
]

OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

with OUTPUT_FILE.open(
    "w",
    encoding="utf-8-sig",
    newline="",
) as destino:
    escritor = csv.writer(destino)
    escritor.writerow(encabezado_salida)
    escritor.writerows(filas_unificadas)

registros_con_informacion = (
    len(filas_unificadas) - filas_completamente_vacias
)

print(f"Archivos unidos: {len(archivos)}")
print(f"Variables originales: {len(encabezado_referencia)}")
print("Columnas de trazabilidad: 2")
print(f"Registros crudos generados: {len(filas_unificadas):,}")
print(
    f"Registros con información: "
    f"{registros_con_informacion:,}"
)
print(
    "Filas completamente vacías conservadas: "
    f"{filas_completamente_vacias}"
)
print(f"Archivo generado: {OUTPUT_FILE}")