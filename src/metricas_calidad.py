"""Genera las tablas reproducibles del informe de calidad.

La comparación usa únicamente las 17 variables sustantivas. Las columnas de
trazabilidad, copias ``*_ORIGINAL`` y banderas de auditoría se informan por
separado para no alterar artificialmente las métricas antes/después.

Ejecutar desde la raíz del repositorio::

    python src/unir_csv.py
    python src/metricas_calidad.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.catalogos_geograficos import (  # noqa: E402
    DEPARTAMENTALES_CANONICAS,
    DEPARTAMENTOS_POR_CODIGO,
    PATRON_CODIGO,
    PATRON_DISTRITO_CORTO,
    PATRON_DISTRITO_EXTENDIDO,
)
from src.diagnostico import cargar_datos  # noqa: E402
from src.limpieza import (  # noqa: E402
    VARIABLES_ORIGINALES,
    filas_completamente_vacias,
    generar_conjunto_limpio,
    limpiar_datos_preliminar,
)


OUTPUT_DIR = ROOT / "reports" / "calidad"


def mascara_faltante(serie: pd.Series) -> pd.Series:
    """Detecta NA y cadenas vacías después de recortar espacios."""
    texto = serie.astype("string")
    return texto.isna() | texto.str.strip().eq("")


def _contiene_espacios_multiples(serie: pd.Series) -> pd.Series:
    return serie.astype("string").fillna("").str.contains(r"\s{2,}", regex=True)


def _problemas_formato_antes(df: pd.DataFrame) -> dict[str, int]:
    """Cuenta celdas problemáticas con las reglas aprobadas en el plan."""
    no_vacio = lambda columna: ~mascara_faltante(df[columna])
    departamentos_canonicos = set(DEPARTAMENTOS_POR_CODIGO.values())
    departamentales_canonicas = set(DEPARTAMENTALES_CANONICAS.values())

    distrito_valido = (
        df["DISTRITO"].str.fullmatch(PATRON_DISTRITO_CORTO)
        | df["DISTRITO"].str.fullmatch(PATRON_DISTRITO_EXTENDIDO)
    )
    telefono_valido = df["TELEFONO"].str.fullmatch(r"\d{8}")

    return {
        "DISTRITO": int((no_vacio("DISTRITO") & ~distrito_valido).sum()),
        "DEPARTAMENTO": int(
            (no_vacio("DEPARTAMENTO") & ~df["DEPARTAMENTO"].isin(departamentos_canonicos)).sum()
        ),
        "MUNICIPIO": int(df["MUNICIPIO"].str.fullmatch(r"ZONA\s+\d{1,2}").sum()),
        "ESTABLECIMIENTO": int(_contiene_espacios_multiples(df["ESTABLECIMIENTO"]).sum()),
        "DIRECCION": int(_contiene_espacios_multiples(df["DIRECCION"]).sum()),
        "TELEFONO": int((no_vacio("TELEFONO") & ~telefono_valido).sum()),
        "SUPERVISOR": int(_contiene_espacios_multiples(df["SUPERVISOR"]).sum()),
        "DIRECTOR": int(_contiene_espacios_multiples(df["DIRECTOR"]).sum()),
        "DEPARTAMENTAL": int(
            (no_vacio("DEPARTAMENTAL") & ~df["DEPARTAMENTAL"].isin(departamentales_canonicas)).sum()
        ),
    }


def _problemas_formato_despues(df: pd.DataFrame) -> dict[str, int]:
    no_vacio = lambda columna: ~mascara_faltante(df[columna])
    distrito_valido = (
        df["DISTRITO"].str.fullmatch(PATRON_DISTRITO_CORTO)
        | df["DISTRITO"].str.fullmatch(PATRON_DISTRITO_EXTENDIDO)
    )
    telefono_valido = df["TELEFONO"].astype("string").str.fullmatch(
        r"\d{7,8}(?:; \d{7,8})*"
    )

    return {
        "DISTRITO": int((no_vacio("DISTRITO") & ~distrito_valido).sum()),
        "DEPARTAMENTO": int(
            (
                no_vacio("DEPARTAMENTO")
                & ~df["DEPARTAMENTO"].isin(DEPARTAMENTOS_POR_CODIGO.values())
            ).sum()
        ),
        "MUNICIPIO": int(
            df["MUNICIPIO"].astype("string").str.fullmatch(r"ZONA\s+\d{1,2}").sum()
        ),
        "ESTABLECIMIENTO": int(_contiene_espacios_multiples(df["ESTABLECIMIENTO"]).sum()),
        "DIRECCION": int(_contiene_espacios_multiples(df["DIRECCION"]).sum()),
        "TELEFONO": int((no_vacio("TELEFONO") & ~telefono_valido.fillna(False)).sum()),
        "SUPERVISOR": int(_contiene_espacios_multiples(df["SUPERVISOR"]).sum()),
        "DIRECTOR": int(_contiene_espacios_multiples(df["DIRECTOR"]).sum()),
        "DEPARTAMENTAL": int(
            (
                no_vacio("DEPARTAMENTAL")
                & ~df["DEPARTAMENTAL"].isin(DEPARTAMENTALES_CANONICAS.values())
            ).sum()
        ),
    }


def generar_tablas() -> None:
    crudo = cargar_datos()
    preliminar = limpiar_datos_preliminar(crudo)
    limpio = generar_conjunto_limpio(crudo)
    variables = VARIABLES_ORIGINALES
    filas_vacias = filas_completamente_vacias(crudo)

    faltantes = pd.DataFrame({
        "variable": variables,
        "antes_cantidad": [int(mascara_faltante(crudo[v]).sum()) for v in variables],
        "despues_cantidad": [int(mascara_faltante(limpio[v]).sum()) for v in variables],
    })
    faltantes["antes_porcentaje"] = (faltantes["antes_cantidad"] / len(crudo) * 100).round(4)
    faltantes["despues_porcentaje"] = (
        faltantes["despues_cantidad"] / len(limpio) * 100
    ).round(4)

    cambios = []
    for variable in variables:
        antes = (
            crudo.loc[~filas_vacias, variable]
            .astype("string")
            .fillna("<NA>")
            .reset_index(drop=True)
        )
        despues = limpio[variable].astype("string").fillna("<NA>")
        cambios.append({
            "variable": variable,
            "celdas_modificadas": int(antes.ne(despues).sum()),
        })
    cambios = pd.DataFrame(cambios)

    formato_antes = _problemas_formato_antes(crudo)
    formato_despues = _problemas_formato_despues(limpio)
    formato = pd.DataFrame({
        "variable": list(formato_antes),
        "celdas_problematicas_antes": list(formato_antes.values()),
        "celdas_problematicas_despues": [formato_despues[v] for v in formato_antes],
    })

    candidatos = preliminar["ESTABLECIMIENTO_GRUPO_DUPLICADO"].notna()
    confirmados = preliminar["ESTABLECIMIENTO_DUPLICADO_CONFIRMADO"]
    duplicados_parciales = pd.DataFrame([{
        "filas_candidatas": int(candidatos.sum()),
        "grupos_candidatos": int(preliminar.loc[candidatos, "ESTABLECIMIENTO_GRUPO_DUPLICADO"].nunique()),
        "filas_confirmadas": int(confirmados.sum()),
        "grupos_confirmados": int(preliminar.loc[confirmados, "ESTABLECIMIENTO_GRUPO_DUPLICADO"].nunique()),
        "filas_fusionadas_o_eliminadas": 0,
    }])

    columnas_duplicados = [
        "ESTABLECIMIENTO_GRUPO_DUPLICADO",
        "CODIGO",
        "ESTABLECIMIENTO_ORIGINAL",
        "MUNICIPIO",
        "DIRECCION_ORIGINAL",
        "JORNADA",
        "PLAN",
        "archivo_origen",
        "fila_origen",
    ]
    detalle_duplicados = preliminar.loc[
        confirmados,
        columnas_duplicados,
    ].sort_values("ESTABLECIMIENTO_GRUPO_DUPLICADO")

    total_celdas_antes = len(crudo) * len(variables)
    total_celdas_despues = len(limpio) * len(variables)
    faltantes_antes = int(faltantes["antes_cantidad"].sum())
    faltantes_despues = int(faltantes["despues_cantidad"].sum())
    duplicados_antes = int(crudo[variables].duplicated(keep=False).sum())
    duplicados_despues = int(limpio[variables].duplicated(keep=False).sum())
    resumen = pd.DataFrame([
        {"metrica": "Registros", "antes": len(crudo), "despues_actual": len(limpio), "observacion": "Se retiraron las 23 filas completamente vacías."},
        {"metrica": "Variables", "antes": len(variables), "despues_actual": len(limpio.columns), "observacion": "Se agregó ZONA_CAPITAL como variable derivada."},
        {"metrica": "Valores faltantes", "antes": f"{faltantes_antes} ({faltantes_antes / total_celdas_antes:.2%})", "despues_actual": f"{faltantes_despues} ({faltantes_despues / total_celdas_despues:.2%})", "observacion": "La comparación de faltantes usa las 17 variables originales en ambos estados."},
        {"metrica": "Variables con faltantes", "antes": int((faltantes["antes_cantidad"] > 0).sum()), "despues_actual": int((faltantes["despues_cantidad"] > 0).sum()), "observacion": "Después de retirar filas vacías, siete variables conservan faltantes reales."},
        {"metrica": "Duplicados exactos", "antes": duplicados_antes, "despues_actual": duplicados_despues, "observacion": "Las 23 filas participantes antes eran filas vacías; no quedan duplicados exactos."},
        {"metrica": "Posibles duplicados", "antes": int(candidatos.sum()), "despues_actual": int(confirmados.sum()), "observacion": "4,045 candidatas; 42 confirmadas en 21 grupos; ninguna resuelta todavía."},
        {"metrica": "Variables con formato inconsistente", "antes": sum(v > 0 for v in formato_antes.values()), "despues_actual": sum(v > 0 for v in formato_despues.values()), "observacion": "Solo DISTRITO conserva 70 formatos incompletos pendientes de revisión."},
        {"metrica": "Variables con tipo incorrecto", "antes": 7, "despues_actual": 0, "observacion": "Las siete categóricas quedan con dtype category en memoria; el CSV requerirá un esquema de carga."},
        {"metrica": "Categorías inconsistentes", "antes": "Pendiente de consolidar", "despues_actual": "Pendiente de validar", "observacion": "Falta acordar una regla de conteo y validar MUNICIPIO contra un catálogo oficial completo."},
        {"metrica": "Celdas modificadas", "antes": 0, "despues_actual": int(cambios["celdas_modificadas"].sum()), "observacion": "No equivale a errores distintos: una celda se cuenta una vez aunque reciba varias operaciones."},
    ])

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    faltantes.to_csv(OUTPUT_DIR / "faltantes_por_variable.csv", index=False, encoding="utf-8-sig")
    cambios.to_csv(OUTPUT_DIR / "cambios_por_variable.csv", index=False, encoding="utf-8-sig")
    formato.to_csv(OUTPUT_DIR / "problemas_formato.csv", index=False, encoding="utf-8-sig")
    duplicados_parciales.to_csv(OUTPUT_DIR / "duplicados_parciales.csv", index=False, encoding="utf-8-sig")
    detalle_duplicados.to_csv(
        OUTPUT_DIR / "duplicados_confirmados_pendientes.csv",
        index=False,
        encoding="utf-8-sig",
    )
    resumen.to_csv(OUTPUT_DIR / "resumen_metricas.csv", index=False, encoding="utf-8-sig")

    print(resumen.to_string(index=False))
    print(f"\nTablas guardadas en: {OUTPUT_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    generar_tablas()
