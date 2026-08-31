"""Genera y valida el único CSV limpio del proyecto.

Ejecutar desde la raíz del repositorio después de ``src/unir_csv.py``::

    python src/generar_dataset.py
"""

from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.diagnostico import cargar_datos  # noqa: E402
from src.limpieza import generar_conjunto_limpio  # noqa: E402
from src.validacion import validar_datos  # noqa: E402


OUTPUT_FILE = (
    ROOT
    / "data"
    / "processed"
    / "establecimientos_diversificado_limpio.csv"
)


def main() -> None:
    crudo = cargar_datos()
    limpio = generar_conjunto_limpio(crudo)
    validar_datos(limpio)

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    limpio.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print(f"Registros limpios: {len(limpio):,}")
    print(f"Variables finales: {len(limpio.columns)}")
    print(f"Archivo generado: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
