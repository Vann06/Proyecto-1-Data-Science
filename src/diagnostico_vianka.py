"""Diagnóstico reproducible de las variables geográficas asignadas.

Analiza CODIGO, DISTRITO, DEPARTAMENTO, MUNICIPIO y DEPARTAMENTAL sin
modificar el conjunto de datos. Los resultados se calculan directamente a
partir del archivo unificado para evitar conteos desactualizados.

Ejecutar desde la raíz del repositorio:
    python src/diagnostico_vianka.py
"""

from __future__ import annotations

import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ARCHIVO = (
    ROOT
    / "data"
    / "interim"
    / "establecimientos_diversificado_raw_unificado.csv"
)
REPORTE_DIR = ROOT / "reports" / "diagnostico_inicial"

VARIABLES_VIANKA = [
    "CODIGO",
    "DISTRITO",
    "DEPARTAMENTO",
    "MUNICIPIO",
    "DEPARTAMENTAL",
]

DEPARTAMENTOS_CANONICOS = {
    "ALTA VERAPAZ": "Alta Verapaz",
    "BAJA VERAPAZ": "Baja Verapaz",
    "CHIMALTENANGO": "Chimaltenango",
    "CHIQUIMULA": "Chiquimula",
    "EL PROGRESO": "El Progreso",
    "ESCUINTLA": "Escuintla",
    "GUATEMALA": "Guatemala",
    "HUEHUETENANGO": "Huehuetenango",
    "IZABAL": "Izabal",
    "JALAPA": "Jalapa",
    "JUTIAPA": "Jutiapa",
    "PETEN": "Petén",
    "QUETZALTENANGO": "Quetzaltenango",
    "QUICHE": "Quiché",
    "RETALHULEU": "Retalhuleu",
    "SACATEPEQUEZ": "Sacatepéquez",
    "SAN MARCOS": "San Marcos",
    "SANTA ROSA": "Santa Rosa",
    "SOLOLA": "Sololá",
    "SUCHITEPEQUEZ": "Suchitepéquez",
    "TOTONICAPAN": "Totonicapán",
    "ZACAPA": "Zacapa",
}

DEPARTAMENTOS_SIN_TILDE = {
    "PETEN",
    "QUICHE",
    "SACATEPEQUEZ",
    "SOLOLA",
    "SUCHITEPEQUEZ",
    "TOTONICAPAN",
}


def cargar_datos() -> pd.DataFrame:
    """Carga el archivo unificado y valida las variables requeridas."""
    if not ARCHIVO.exists():
        raise FileNotFoundError(
            "No existe el archivo unificado. Ejecute primero "
            "'python src/unir_csv.py'."
        )

    df = pd.read_csv(
        ARCHIVO,
        dtype="string",
        keep_default_na=False,
        encoding="utf-8-sig",
    )

    faltantes = [col for col in VARIABLES_VIANKA if col not in df.columns]
    if faltantes:
        raise ValueError(
            "Faltan variables requeridas para el diagnóstico: "
            + ", ".join(faltantes)
        )

    return df


def normalizar_comparacion(texto: str) -> str:
    """Normaliza solo para comparar; nunca sustituye el dato original."""
    descompuesto = unicodedata.normalize("NFKD", str(texto))
    sin_tildes = "".join(
        caracter
        for caracter in descompuesto
        if not unicodedata.combining(caracter)
    )
    return re.sub(r"\s+", " ", sin_tildes.upper()).strip()


def _texto(df: pd.DataFrame, variable: str) -> pd.Series:
    """Devuelve una serie textual recortada sin cambiar el DataFrame."""
    return df[variable].fillna("").astype("string").str.strip()


def resumen_variables(df: pd.DataFrame) -> pd.DataFrame:
    """Resume tipo, faltantes, unicidad y problemas básicos de formato."""
    filas: list[dict[str, object]] = []

    for variable in VARIABLES_VIANKA:
        original = df[variable].fillna("").astype("string")
        texto = original.str.strip()
        no_vacio = texto.ne("")

        filas.append(
            {
                "variable": variable,
                "tipo_leido": str(df[variable].dtype),
                "registros": len(df),
                "faltantes": int((~no_vacio).sum()),
                "porcentaje_faltantes": round(
                    float((~no_vacio).mean()) * 100,
                    2,
                ),
                "valores_unicos_no_vacios": int(texto[no_vacio].nunique()),
                "espacios_inicio_fin": int(original.ne(texto).sum()),
                "espacios_multiples": int(
                    texto.str.contains(r"\s{2,}", regex=True).sum()
                ),
            }
        )

    return pd.DataFrame(filas)


def diagnostico_codigo(df: pd.DataFrame) -> pd.DataFrame:
    """Evalúa formato, unicidad y coherencia geográfica de CODIGO."""
    codigo = _texto(df, "CODIGO")
    patron = r"^\d{2}-\d{2}-\d{4}-\d{2}$"
    prefijo = codigo.str.slice(0, 5)

    base_prefijos = df[["DEPARTAMENTO", "MUNICIPIO"]].copy()
    base_prefijos["prefijo_codigo"] = prefijo

    prefijos_por_par = (
        base_prefijos.groupby(["DEPARTAMENTO", "MUNICIPIO"])[
            "prefijo_codigo"
        ]
        .nunique()
    )
    geografia_por_prefijo = (
        base_prefijos.groupby("prefijo_codigo")
        .agg(
            departamentos=("DEPARTAMENTO", "nunique"),
            municipios=("MUNICIPIO", "nunique"),
        )
    )

    return pd.DataFrame(
        [
            {
                "revision": "valores vacios",
                "cantidad": int(codigo.eq("").sum()),
                "resultado": "esperado 0",
            },
            {
                "revision": "formato NN-NN-NNNN-NN",
                "cantidad": int(codigo.str.fullmatch(patron).sum()),
                "resultado": "debe coincidir con los registros no vacios",
            },
            {
                "revision": "codigos duplicados",
                "cantidad": int(codigo[codigo.ne("")].duplicated().sum()),
                "resultado": "esperado 0",
            },
            {
                "revision": "pares departamento-municipio con más de un prefijo",
                "cantidad": int((prefijos_por_par > 1).sum()),
                "resultado": "esperado 0",
            },
            {
                "revision": "prefijos asociados a más de una geografia",
                "cantidad": int(
                    (
                        (geografia_por_prefijo["departamentos"] > 1)
                        | (geografia_por_prefijo["municipios"] > 1)
                    ).sum()
                ),
                "resultado": "esperado 0",
            },
        ]
    )


def clasificar_distrito(valor: str) -> str:
    """Clasifica la estructura observada de un código de distrito."""
    valor = str(valor).strip()
    if valor == "":
        return "vacio"
    if re.fullmatch(r"\d{2}-", valor):
        return "incompleto"
    if re.fullmatch(r"\d{2}-\d{3}", valor):
        return "formato corto NN-NNN"
    if re.fullmatch(r"\d{2}-\d{2}-\d{4}", valor):
        return "formato extendido NN-NN-NNNN"
    return "otro formato"


def diagnostico_distrito(df: pd.DataFrame) -> pd.DataFrame:
    """Cuenta formatos, faltantes y casos especiales de DISTRITO."""
    distrito = _texto(df, "DISTRITO")
    categoria = distrito.map(clasificar_distrito)

    resumen = (
        categoria.value_counts(dropna=False)
        .rename_axis("categoria")
        .reset_index(name="cantidad")
    )
    resumen["porcentaje"] = (
        resumen["cantidad"] / len(df) * 100
    ).round(2)

    ejemplos = (
        pd.DataFrame({"valor": distrito, "categoria": categoria})
        .groupby("categoria")["valor"]
        .agg(lambda serie: " | ".join(serie.drop_duplicates().head(4)))
    )
    resumen["ejemplos"] = resumen["categoria"].map(ejemplos)
    return resumen.sort_values("cantidad", ascending=False)


def diagnostico_departamento(df: pd.DataFrame) -> pd.DataFrame:
    """Distingue departamentos oficiales de la partición Ciudad Capital."""
    departamento = _texto(df, "DEPARTAMENTO")
    no_vacio = departamento.ne("")
    es_capital = departamento.eq("CIUDAD CAPITAL")
    fuera_catalogo = (
        no_vacio
        & ~departamento.isin(DEPARTAMENTOS_CANONICOS)
        & ~es_capital
    )

    categorias_oficiales = departamento[
        departamento.isin(DEPARTAMENTOS_CANONICOS)
    ].nunique()

    return pd.DataFrame(
        [
            {
                "revision": "categorias observadas",
                "cantidad": int(departamento[no_vacio].nunique()),
                "detalle": (
                    f"{categorias_oficiales} departamentos oficiales y "
                    "una categoria especial de la fuente"
                ),
            },
            {
                "revision": "registros en CIUDAD CAPITAL",
                "cantidad": int(es_capital.sum()),
                "detalle": "particion de la fuente; no es departamento oficial",
            },
            {
                "revision": "departamentos sin tilde normativa",
                "cantidad": int(
                    departamento.isin(DEPARTAMENTOS_SIN_TILDE).sum()
                ),
                "detalle": ", ".join(sorted(DEPARTAMENTOS_SIN_TILDE)),
            },
            {
                "revision": "valores fuera del catalogo preliminar",
                "cantidad": int(fuera_catalogo.sum()),
                "detalle": "excluye la categoria especial CIUDAD CAPITAL",
            },
        ]
    )


def diagnostico_municipio(df: pd.DataFrame) -> pd.DataFrame:
    """Evalúa MUNICIPIO sin confundir zonas capitalinas con municipios."""
    departamento = _texto(df, "DEPARTAMENTO")
    municipio = _texto(df, "MUNICIPIO")
    es_capital = departamento.eq("CIUDAD CAPITAL")
    es_zona = municipio.str.fullmatch(r"ZONA \d{1,2}")

    base_geo = pd.DataFrame(
        {"DEPARTAMENTO": departamento, "MUNICIPIO": municipio}
    )
    pares = (
        base_geo.loc[municipio.ne(""), ["DEPARTAMENTO", "MUNICIPIO"]]
        .drop_duplicates()
    )
    pares_no_capital = (
        base_geo.loc[
            (~es_capital) & municipio.ne(""),
            ["DEPARTAMENTO", "MUNICIPIO"],
        ]
        .drop_duplicates()
    )

    municipios_no_capital = base_geo.loc[
        (~es_capital) & municipio.ne(""),
        ["DEPARTAMENTO", "MUNICIPIO"],
    ]
    nombres_en_varios_departamentos = (
        municipios_no_capital.groupby("MUNICIPIO")["DEPARTAMENTO"]
        .nunique()
        .gt(1)
    )
    con_vocal_acentuada = municipio.str.contains(
        r"[ÁÉÍÓÚÜ]",
        regex=True,
    )
    zonas_capitalinas = municipio[es_capital & municipio.ne("")].nunique()

    return pd.DataFrame(
        [
            {
                "revision": "valores vacios",
                "cantidad": int(municipio.eq("").sum()),
                "detalle": "esperado 0",
            },
            {
                "revision": "nombres unicos",
                "cantidad": int(municipio[municipio.ne("")].nunique()),
                "detalle": "incluye las zonas registradas por la fuente",
            },
            {
                "revision": "pares departamento-municipio",
                "cantidad": int(pares.shape[0]),
                "detalle": "conteo derivado de pares únicos observados",
            },
            {
                "revision": "pares fuera de CIUDAD CAPITAL",
                "cantidad": int(pares_no_capital.shape[0]),
                "detalle": "municipios con establecimientos de Diversificado",
            },
            {
                "revision": "zonas de Ciudad Capital",
                "cantidad": int(zonas_capitalinas),
                "detalle": "etiquetas ZONA que deben conservarse como sububicacion",
            },
            {
                "revision": "filas capitalinas que no tienen formato ZONA",
                "cantidad": int((es_capital & ~es_zona).sum()),
                "detalle": "esperado 0",
            },
            {
                "revision": "nombres repetidos en distintos departamentos",
                "cantidad": int(nombres_en_varios_departamentos.sum()),
                "detalle": (
                    "homonimos posibles; validar siempre junto a DEPARTAMENTO"
                ),
            },
            {
                "revision": "filas con vocal acentuada",
                "cantidad": int(con_vocal_acentuada.sum()),
                "detalle": (
                    "permite medir si la exportacion conserva tildes en municipios"
                ),
            },
        ]
    )


def clasificar_relacion_departamental(
    departamento: str,
    departamental: str,
) -> str:
    """Clasifica la relación sin exigir igualdad entre variables distintas."""
    dep = str(departamento).strip()
    dptal = str(departamental).strip()
    dep_normalizado = normalizar_comparacion(dep)
    dptal_normalizado = normalizar_comparacion(dptal)

    if dep == dptal:
        return "coincidencia exacta"
    if dep_normalizado == dptal_normalizado:
        return "solo difiere por tildes"
    if (
        dep in {"GUATEMALA", "CIUDAD CAPITAL"}
        and dptal_normalizado.startswith("GUATEMALA ")
    ):
        return "subdivision administrativa"
    if (
        dep_normalizado == "QUICHE"
        and dptal_normalizado == "QUICHE NORTE"
    ):
        return "subdivision administrativa"
    return "otra relacion"


def diagnostico_departamental(df: pd.DataFrame) -> pd.DataFrame:
    """Resume las categorías y su relación con DEPARTAMENTO."""
    relacion = pd.Series(
        [
            clasificar_relacion_departamental(dep, dptal)
            for dep, dptal in zip(
                df["DEPARTAMENTO"],
                df["DEPARTAMENTAL"],
            )
        ],
        index=df.index,
        dtype="string",
    )

    resumen = (
        relacion.value_counts()
        .rename_axis("relacion")
        .reset_index(name="cantidad")
    )
    resumen["porcentaje"] = (
        resumen["cantidad"] / len(df) * 100
    ).round(2)
    resumen["categorias_departamentales"] = int(
        _texto(df, "DEPARTAMENTAL").nunique()
    )
    return resumen


def problemas_vianka(df: pd.DataFrame) -> pd.DataFrame:
    """Consolida los hallazgos que alimentan el plan de limpieza."""
    distrito = _texto(df, "DISTRITO")
    departamento = _texto(df, "DEPARTAMENTO")
    municipio = _texto(df, "MUNICIPIO")
    cantidad_municipios = int(municipio[municipio.ne("")].nunique())

    mascara_distrito_incompleto = distrito.str.fullmatch(r"\d{2}-")
    mascara_capital = departamento.eq("CIUDAD CAPITAL")
    mascara_sin_tilde = departamento.isin(DEPARTAMENTOS_SIN_TILDE)

    filas = [
        {
            "variable": "CODIGO",
            "problema": "Riesgo de tipado de un identificador numerico",
            "categoria": "tipo",
            "cantidad": len(df),
            "porcentaje": 100.00,
            "requiere_limpieza": "No",
            "estrategia_sugerida": (
                "Conservar como texto y validar formato/unicidad; "
                "no convertir a numero"
            ),
            "ejemplo": "16-01-0001-46",
        },
        {
            "variable": "DISTRITO",
            "problema": "Valor vacio",
            "categoria": "faltante",
            "cantidad": int(distrito.eq("").sum()),
            "porcentaje": round(float(distrito.eq("").mean()) * 100, 2),
            "requiere_limpieza": "Si",
            "estrategia_sugerida": (
                "Representar como NA; no imputar sin catalogo oficial"
            ),
            "ejemplo": "",
        },
        {
            "variable": "DISTRITO",
            "problema": "Codigo incompleto que termina en guion",
            "categoria": "formato",
            "cantidad": int(mascara_distrito_incompleto.sum()),
            "porcentaje": round(
                float(mascara_distrito_incompleto.mean()) * 100,
                2,
            ),
            "requiere_limpieza": "Si",
            "estrategia_sugerida": (
                "Marcar para revision; no completar digitos automaticamente"
            ),
            "ejemplo": "01- | 17- | 10-",
        },
        {
            "variable": "DISTRITO",
            "problema": "Dos estructuras ampliamente usadas",
            "categoria": "formato",
            "cantidad": int(distrito.ne("").sum()),
            "porcentaje": round(float(distrito.ne("").mean()) * 100, 2),
            "requiere_limpieza": "Revisar",
            "estrategia_sugerida": (
                "Conservar ambos formatos hasta contrastar el catalogo MINEDUC"
            ),
            "ejemplo": "16-006 | 16-01-0924",
        },
        {
            "variable": "DEPARTAMENTO",
            "problema": "Categoria especial CIUDAD CAPITAL",
            "categoria": "dominio",
            "cantidad": int(mascara_capital.sum()),
            "porcentaje": round(float(mascara_capital.mean()) * 100, 2),
            "requiere_limpieza": "Si",
            "estrategia_sugerida": (
                "Mapear geograficamente a Guatemala sin perder la condicion "
                "de capital"
            ),
            "ejemplo": "CIUDAD CAPITAL",
        },
        {
            "variable": "DEPARTAMENTO",
            "problema": (
                "Tildes omitidas en departamentos con acento normativo"
            ),
            "categoria": "ortografia",
            "cantidad": int(mascara_sin_tilde.sum()),
            "porcentaje": round(float(mascara_sin_tilde.mean()) * 100, 2),
            "requiere_limpieza": "Si",
            "estrategia_sugerida": (
                "Usar nombres oficiales bien escritos para el dato final"
            ),
            "ejemplo": "PETEN -> Petén | QUICHE -> Quiché",
        },
        {
            "variable": "MUNICIPIO",
            "problema": "Zonas capitalinas almacenadas como municipio",
            "categoria": "consistencia",
            "cantidad": int(mascara_capital.sum()),
            "porcentaje": round(float(mascara_capital.mean()) * 100, 2),
            "requiere_limpieza": "Si",
            "estrategia_sugerida": (
                "Conservar la zona como sububicacion y asignar municipio "
                "Guatemala"
            ),
            "ejemplo": "ZONA 1 | ZONA 10 | ZONA 25",
        },
        {
            "variable": "MUNICIPIO",
            "problema": (
                "Etiquetas pendientes de validacion ortografica contra catalogo"
            ),
            "categoria": "catalogo",
            "cantidad": cantidad_municipios,
            "porcentaje": 100.00,
            "requiere_limpieza": "Si",
            "estrategia_sugerida": (
                "Cruzar cada etiqueta con el catalogo oficial y conservar "
                "la escritura correcta"
            ),
            "ejemplo": "COBAN -> Cobán | AMATITLAN -> Amatitlán",
        },
        {
            "variable": "DEPARTAMENTAL",
            "problema": "No siempre coincide textualmente con DEPARTAMENTO",
            "categoria": "consistencia",
            "cantidad": int(
                (df["DEPARTAMENTO"] != df["DEPARTAMENTAL"]).sum()
            ),
            "porcentaje": round(
                float(
                    (df["DEPARTAMENTO"] != df["DEPARTAMENTAL"]).mean()
                )
                * 100,
                2,
            ),
            "requiere_limpieza": "Revisar",
            "estrategia_sugerida": (
                "Tratarla como division administrativa propia; "
                "normalizar tildes sin forzar igualdad"
            ),
            "ejemplo": (
                "GUATEMALA NORTE | GUATEMALA SUR | QUICHÉ NORTE"
            ),
        },
    ]

    return pd.DataFrame(filas)


def generar_reportes(df: pd.DataFrame) -> None:
    """Guarda tablas reproducibles para el notebook y la documentación."""
    REPORTE_DIR.mkdir(parents=True, exist_ok=True)

    tablas = {
        "resumen_variables_vianka.csv": resumen_variables(df),
        "diagnostico_codigo_vianka.csv": diagnostico_codigo(df),
        "diagnostico_distrito_vianka.csv": diagnostico_distrito(df),
        "diagnostico_departamento_vianka.csv": diagnostico_departamento(df),
        "diagnostico_municipio_vianka.csv": diagnostico_municipio(df),
        "diagnostico_departamental_vianka.csv": diagnostico_departamental(df),
        "problemas_geograficos_vianka.csv": problemas_vianka(df),
    }

    for nombre, tabla in tablas.items():
        tabla.to_csv(
            REPORTE_DIR / nombre,
            index=False,
            encoding="utf-8-sig",
        )


if __name__ == "__main__":
    datos = cargar_datos()
    generar_reportes(datos)

    print("Diagnóstico geográfico")
    print(f"Registros: {len(datos):,}")
    print(f"Variables originales: {len(datos.columns)}")
    print(resumen_variables(datos).to_string(index=False))
    print(
        "\nReportes guardados en: "
        f"{REPORTE_DIR.relative_to(ROOT)}"
    )
