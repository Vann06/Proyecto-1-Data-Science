"""Diagnóstico inicial del conjunto unificado.

Este archivo se trabaja por turnos. Aquí NO se limpian datos.
Antes de comenzar, ejecutar primero: python src/unir_csv.py
"""

import re
import unicodedata
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ARCHIVO = ROOT / "data" / "interim" / "establecimientos_diversificado_raw_unificado.csv"


def cargar_datos() -> pd.DataFrame:
    """Carga el archivo unificado conservando todos los campos como texto."""
    return pd.read_csv(
        ARCHIVO,
        dtype="string",
        keep_default_na=False,
        encoding="utf-8-sig",
    )


# ================================================================
# TURNO 1 · VIANKA
# Variables: CODIGO, DISTRITO, DEPARTAMENTO, MUNICIPIO, DEPARTAMENTAL
# Completar aquí:
# - número de registros y variables;
# - tipos de datos;
# - valores faltantes y valores únicos;
# - códigos y distritos con formatos extraños;
# - departamentos o municipios fuera de catálogo;
# - contradicciones entre variables geográficas.
# ================================================================


# ================================================================
# TURNO 2 · RICARDO
# Variables: ESTABLECIMIENTO, DIRECCION, TELEFONO, SUPERVISOR, DIRECTOR
# Completar aquí:
# - espacios, mayúsculas, tildes, puntuación y caracteres especiales;
# - formatos de teléfonos, direcciones y nombres;
# - duplicados exactos;
# - posibles duplicados parciales usando similitud de texto;
# - ejemplos y cantidades de cada problema.
# No eliminar duplicados en esta fase.
# ================================================================


SEPARADOR_NUMEROS = re.compile(r"[,/;]|\s+[Yy]\s+")
MARCADOR_EXTENSION = re.compile(r"\b(?:EXT|EXTS|ESTX)\b\.?", re.IGNORECASE)
SUFIJO_ABREVIADO = re.compile(r"^(\d{7,8})-(\d{1,4})$")
LARGOS_VALIDOS = (8, 7)


def separar_numeros(texto: str) -> list[str]:
    """Extrae los teléfonos individuales contenidos en una celda.

    La columna mezcla varios números por celda con separadores
    inconsistentes (coma, guion, barra, espacio, la letra Y). El guion es
    ambiguo: en 24328801-24329098 separa dos números y en 232-1011 decora
    uno solo. Por eso la estructura se detecta con los separadores todavía
    presentes y solo después se descartan los caracteres no numéricos.
    """
    texto = MARCADOR_EXTENSION.split(texto)[0]

    numeros = []
    for fragmento in SEPARADOR_NUMEROS.split(texto):
        fragmento = fragmento.strip()

        abreviado = SUFIJO_ABREVIADO.fullmatch(fragmento)
        if abreviado:
            base, sufijo = abreviado.groups()
            numeros.extend([base, base[: -len(sufijo)] + sufijo])
            continue

        digitos = re.sub(r"\D", "", fragmento)
        if not digitos:
            continue

        for largo in LARGOS_VALIDOS:
            if len(digitos) % largo == 0 and len(digitos) <= largo * 4:
                numeros.extend(
                    digitos[i : i + largo]
                    for i in range(0, len(digitos), largo)
                )
                break
        else:
            if len(digitos) == 15:
                numeros.extend([digitos[:8], digitos[8:]])
            else:
                numeros.append(digitos)

    return [n for n in numeros if not re.fullmatch(r"0+", n)]


def clasificar_telefono(texto: str) -> str:
    """Asigna a una celda la primera categoría del plan de limpieza que cumple."""
    texto = texto.strip()
    if texto == "":
        return "vacio"
    if re.fullmatch(r"\d{8}", texto):
        return "valido"

    if MARCADOR_EXTENSION.search(texto):
        return "incluye extension"
    if re.search(r"0{6,}", texto):
        return "incluye placeholder de ceros"

    numeros = separar_numeros(texto)
    if not numeros:
        return "sin numeros recuperables"
    if any(len(n) not in LARGOS_VALIDOS for n in numeros):
        return "no interpretable"
    if len(numeros) > 1:
        return "varios numeros"
    if len(numeros[0]) == 7:
        return "numero legado de 7 digitos"
    return "un numero de 8 digitos mal formateado"


def telefonos_no_estandar(df: pd.DataFrame) -> pd.DataFrame:
    """Detalla las celdas de TELEFONO que no son exactamente 8 dígitos.

    Devuelve una fila por celda problemática con su categoría y los números
    que se lograron recuperar, conservando el origen para trazabilidad.
    """
    telefono = df["TELEFONO"].fillna("").str.strip()
    mascara = telefono.ne("") & ~telefono.str.fullmatch(r"\d{8}")

    detalle = df.loc[mascara, ["TELEFONO", "ESTABLECIMIENTO"]].copy()
    detalle["categoria"] = telefono[mascara].map(clasificar_telefono)
    detalle["numeros_recuperados"] = telefono[mascara].map(separar_numeros)
    detalle["cantidad_recuperada"] = detalle["numeros_recuperados"].str.len()

    for columna in ["archivo_origen", "fila_origen"]:
        if columna in df.columns:
            detalle[columna] = df.loc[mascara, columna]

    return detalle


PATRONES_ESCRITURA = {
    "espacios multiples": r"\s{2,}",
    "termina en punto": r"\.\s*$",
    "comillas": r"[\"'“”]",
    "parentesis": r"[()]",
    "tiene minusculas": r"[a-z]",
    "tiene tildes": r"[ÁÉÍÓÚÜÑáéíóúüñ]",
    "abreviatura con punto": r"\b[A-ZÑ]{1,4}\.",
    "contiene digitos": r"\d",
    "caracter inusual": r"[^A-ZÑÁÉÍÓÚÜ0-9\s.,\"'()\-/&]",
}


def inventario_escritura(serie: pd.Series) -> pd.DataFrame:
    """Cuenta las variaciones de escritura presentes en una columna de texto.

    Las categorías no son excluyentes: una celda puede aparecer en varias.
    El patrón "caracter inusual" niega el conjunto esperado, de modo que
    revela símbolos que no se anticiparon al escribir esta tabla.
    """
    texto = serie.fillna("").str.strip()

    filas = []
    for nombre, patron in PATRONES_ESCRITURA.items():
        mascara = texto.str.contains(patron, regex=True)
        filas.append({
            "patron": nombre,
            "celdas": int(mascara.sum()),
            "porcentaje": round(float(mascara.mean()) * 100, 2),
            "ejemplos": " ¦ ".join(texto[mascara].unique()[:3]),
        })

    return pd.DataFrame(filas).sort_values("celdas", ascending=False)


def normalizar_nombre(texto: str) -> str:
    """Reduce un nombre a su forma comparable: solo letras y dígitos.

    Sirve para AGRUPAR escrituras equivalentes, no para reemplazar el
    nombre en los datos limpios: la descomposición NFKD también separa la
    Ñ de su virgulilla, así que CAÑAS y CANAS caen en la misma clave.
    Esa fusión conviene al comparar, porque la columna ya mezcla ambas
    escrituras, pero altera el nombre real de la institución.
    """
    texto = unicodedata.normalize("NFKD", texto)
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    return re.sub(r"[^A-Z0-9]+", " ", texto.upper()).strip()


def variantes_establecimiento(df: pd.DataFrame) -> pd.DataFrame:
    """Agrupa los nombres que solo difieren en su escritura.

    Compartir nombre no implica ser la misma entidad: los institutos
    públicos carecen de nombre propio y cientos se llaman igual en
    municipios distintos. CODIGO no sirve para separarlos porque es llave
    primaria (11,867 códigos para 11,867 registros), así que dos escrituras
    implican dos códigos por construcción. El contraste útil es geográfico:
    las variantes concentradas en un solo municipio son candidatas a
    duplicado, las repartidas entre municipios son homónimos esperables.
    """
    nombre = df["ESTABLECIMIENTO"].fillna("").str.strip()
    con_nombre = nombre.ne("")

    grupos = pd.DataFrame({
        "nombre": nombre[con_nombre],
        "clave": nombre[con_nombre].map(normalizar_nombre),
        "codigo": df.loc[con_nombre, "CODIGO"],
        "municipio": df.loc[con_nombre, "MUNICIPIO"],
    })

    resumen = grupos.groupby("clave").agg(
        escrituras=("nombre", "nunique"),
        codigos=("codigo", "nunique"),
        municipios=("municipio", "nunique"),
        registros=("nombre", "size"),
        formas=("nombre", lambda s: sorted(set(s))),
    )

    resumen = resumen[resumen["escrituras"] > 1].copy()
    resumen["categoria"] = resumen["municipios"].map(
        lambda n: "posible duplicado" if n == 1 else "homonimos"
    )

    return resumen.sort_values(["categoria", "escrituras"], ascending=[True, False])


def sin_tildes(texto: str) -> str:
    """Quita tildes y pasa a mayúsculas CONSERVANDO la puntuación.

    Es la diferencia con normalizar_nombre(), que también borra guiones y
    comillas. En una dirección esos signos son sintaxis, no adorno: el
    guion separa el número de casa (3-50) y la comilla delimita el nombre
    de la vía (CALLE "A"). Detectar primero, normalizar después.
    """
    texto = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in texto if not unicodedata.combining(c)).upper()


# Marcadores de lo que una dirección alcanza a localizar. No son
# excluyentes: una dirección urbana completa cae en cuatro a la vez.
MARCADORES_DIRECCION = {
    "numero de casa (N-N)": r"\d+\s*-\s*\d+",
    "via urbana": (
        r"\b(?:CALLE|CALLEJON|AVENIDA|AVDA|AV|CALZADA|CALZ|DIAGONAL|DIAG"
        r"|BULEVAR|BOULEVARD|BLVD|RUTA|VIA)\b"
    ),
    "kilometro": r"\bKM\b|\bKM\.|\bKILOMETRO\b",
    "zona": r"\bZONA\b|\bZ\.?\s*\d",
    "rural": (
        r"\b(?:ALDEA|CASERIO|CASERO|CANTON|PARAJE|FINCA|COMUNIDAD"
        r"|PARCELAMIENTO|MICROPARCELA|PARCELA|SECTOR|COOPERATIVA)\b"
    ),
    "barrio/colonia": r"\b(?:BARRIO|COLONIA|COL\.|RESIDENCIAL|LOTIFICACION|CONDOMINIO)\b",
    "cabecera/casco": r"\bCABECERA\b|\bCASCO\b|\bCENTRO URBANO\b",
    "solo puntuacion": r"^[\W_]+$",
}


def marcadores_direccion(serie: pd.Series) -> pd.DataFrame:
    """Cuenta qué nivel de detalle alcanza cada dirección.

    DIRECCION no tiene un dominio sino dos. En el área urbana la dirección
    es postal y estructurada (número de casa, vía, zona); en el área rural
    es el nombre del lugar (ALDEA, CASERIO, CANTON, COOPERATIVA), que no
    tiene ni puede tener esa estructura. No es un defecto de captura, así
    que "falta el número de casa" no es un criterio válido de completitud
    para todo el conjunto.

    La lista de marcadores es una hipótesis y el residuo la corrige:
    COOPERATIVA, KILOMETRO escrito completo y el typo CASERO entraron aquí
    después de leer las celdas que no clasificaba ninguna categoría.
    """
    texto = serie.fillna("").str.strip().map(sin_tildes)
    no_vacia = texto.ne("")

    filas = []
    union = pd.Series(False, index=texto.index)
    for nombre, patron in MARCADORES_DIRECCION.items():
        mascara = (no_vacia & texto.str.contains(patron, regex=True)).fillna(False)
        union |= mascara
        filas.append({
            "marcador": nombre,
            "celdas": int(mascara.sum()),
            "porcentaje": round(float(mascara.mean()) * 100, 2),
            "ejemplos": " ¦ ".join(texto[mascara].unique()[:3]),
        })

    residuo = (no_vacia & ~union).fillna(False)
    filas.append({
        "marcador": "sin ningun marcador",
        "celdas": int(residuo.sum()),
        "porcentaje": round(float(residuo.mean()) * 100, 2),
        "ejemplos": " ¦ ".join(texto[residuo].unique()[:3]),
    })

    return pd.DataFrame(filas).sort_values("celdas", ascending=False)


def direccion_redundante(df: pd.DataFrame) -> pd.DataFrame:
    """Mide cuánta DIRECCION repite lo que MUNICIPIO ya dice.

    Dos grados del mismo fenómeno. En el extremo, la dirección ES el
    municipio (COBAN, CHISEC): informa lo mismo que una celda vacía, pero
    ningún conteo de nulos la detecta. En el caso frecuente, una dirección
    completa y bien formada trae el municipio pegado al final, y ahí es
    sufijo redundante a recortar en la limpieza.

    El conteo del caso extremo es un piso, no un total: CIUDAD GUATEMALA y
    CIUDAD CAPITAL son el municipio GUATEMALA y la igualdad exacta no los ve.
    """
    direccion = df["DIRECCION"].fillna("").str.strip().map(sin_tildes)
    municipio = df["MUNICIPIO"].fillna("").str.strip().map(sin_tildes)
    no_vacia = direccion.ne("")

    # El municipio cambia en cada fila, así que str.contains no sirve: la
    # comparación es par a par. La guarda va dentro, porque "" in v es
    # cierto para toda cadena y contaría cada fila sin municipio.
    contiene = pd.Series(
        [m != "" and m in v for v, m in zip(direccion, municipio)],
        index=direccion.index,
    )

    igual = (no_vacia & direccion.eq(municipio)).fillna(False)
    parcial = (no_vacia & contiene & direccion.ne(municipio)).fillna(False)

    return pd.DataFrame([
        {"caso": "direccion == municipio", "celdas": int(igual.sum()),
         "porcentaje": round(float(igual.mean()) * 100, 2),
         "ejemplos": " ¦ ".join(direccion[igual].unique()[:3])},
        {"caso": "direccion contiene municipio", "celdas": int(parcial.sum()),
         "porcentaje": round(float(parcial.mean()) * 100, 2),
         "ejemplos": " ¦ ".join(direccion[parcial].unique()[:3])},
    ])


# Defectos que producen cadenas bien formadas, invisibles a los marcadores.
PATRONES_CONTAMINACION = {
    # Dos separadores, no uno: en 3-50 el guion es número de casa. La misma
    # ambigüedad del guion que ya apareció en los teléfonos.
    "fecha incrustada": r"\d{1,2}[/-]\d{1,2}[/-]\d{2,4}",
    "letra O por cero": r"^O\s+(?:CALLE|AV)|\bO[A-Z]?-\d",
}


def direccion_contaminada(serie: pd.Series) -> pd.DataFrame:
    """Busca los defectos que ningún filtro sintáctico atrapa.

    Las fechas aparecen siempre al final de la cadena y una llega repetida
    sobre sí misma (22/0209/02/20209): es un campo desbordado al exportar,
    no algo que alguien tecleara. La letra O por cero se confirma en una
    sola celda que trae las dos formas, O AV. 0-06: si fuera convención
    local sería consistente dentro de la fila.

    Son pocas celdas, pero las únicas que pasan intactas cualquier
    validación de formato, porque el resultado es una cadena válida.
    """
    texto = serie.fillna("").str.strip().map(sin_tildes)

    filas = []
    for nombre, patron in PATRONES_CONTAMINACION.items():
        mascara = texto.str.contains(patron, regex=True).fillna(False)
        filas.append({
            "patron": nombre,
            "celdas": int(mascara.sum()),
            "ejemplos": " ¦ ".join(texto[mascara].unique()[:3]),
        })

    return pd.DataFrame(filas).sort_values("celdas", ascending=False)


# ---------------------------------------------------------------
# SUPERVISOR y DIRECTOR — nombres de persona
# ---------------------------------------------------------------

FRASE_AUSENCIA = re.compile(r"\bSIN\s+DAT", re.IGNORECASE)
_LETRA = re.compile(r"[A-Za-zÑÁÉÍÓÚÜáéíóúñ]")


def _palabras_con_letra(texto: str) -> int:
    """Cuenta las palabras que contienen al menos una letra.

    Un nombre de persona en estos datos siempre trae dos o más: SUPERVISOR
    lo confirma, ni una celda de un solo token. Por eso "menos de dos"
    delata la ausencia sin enumerar cada largo de guion, que es la debilidad
    de una lista fija de marcadores: cuenta '--' pero se le escapa '---'.
    """
    return sum(bool(_LETRA.search(t)) for t in texto.split())


def nombres_ausentes(serie: pd.Series) -> pd.DataFrame:
    """Desglosa la ausencia real en una columna de nombres.

    El conteo de nulos por lista fija es un piso: en DIRECTOR ve 1,814
    faltantes pero se le escapan 360 celdas que no son un nombre y tampoco
    están vacías —guiones de cualquier largo, '000000', 'X', 'SIN DATOS
    (...)'—. Es el mismo hueco que la dirección que solo repite el municipio:
    informa lo mismo que un vacío y ningún conteo de nulos la registra.

    Las categorías son excluyentes y van de la más vacía a la más parecida a
    un nombre; la ausencia total es la suma de las primeras cuatro filas.
    """
    texto = serie.fillna("").str.strip()
    n_alpha = texto.map(_palabras_con_letra)
    vacia = texto.eq("")
    frase = texto.str.contains(FRASE_AUSENCIA).fillna(False)

    categorias = {
        "vacia": vacia,
        "solo simbolos": ~vacia & n_alpha.eq(0),
        "un solo token": ~vacia & n_alpha.eq(1),
        "frase de ausencia": ~vacia & n_alpha.ge(2) & frase,
    }
    ausente = (
        categorias["vacia"] | categorias["solo simbolos"]
        | categorias["un solo token"] | categorias["frase de ausencia"]
    )
    categorias["nombre aparente"] = ~ausente

    filas = [
        {
            "categoria": nombre,
            "celdas": int(mascara.sum()),
            "porcentaje": round(float(mascara.mean()) * 100, 2),
            "ejemplos": " ¦ ".join(texto[mascara].unique()[:3]),
        }
        for nombre, mascara in categorias.items()
    ]
    return pd.DataFrame(filas)


def variantes_nombre(nombre: pd.Series, geo: pd.Series) -> pd.DataFrame:
    """Agrupa los nombres que solo difieren en su escritura.

    Misma idea que variantes_establecimiento, con otro corte. Un supervisor
    es una persona real atada a una jurisdicción, así que dos escrituras del
    mismo nombre normalizado concentradas en una sola son casi siempre la
    misma persona (CARLOS HUMBERTO GONZALEZ DE LEON y ...GONZÁLEZ DE LEÓN,
    393 registros partidos por las tildes). El mismo nombre repartido entre
    jurisdicciones ya pide revisión: puede ser un homónimo. Se ignoran las
    celdas ausentes —no son nombres que fusionar— con la misma regla que
    nombres_ausentes.
    """
    texto = nombre.fillna("").str.strip()
    frase = texto.str.contains(FRASE_AUSENCIA).fillna(False)
    es_nombre = texto.ne("") & texto.map(_palabras_con_letra).ge(2) & ~frase

    grupos = pd.DataFrame({
        "nombre": texto[es_nombre],
        "clave": texto[es_nombre].map(normalizar_nombre),
        "jurisdiccion": geo[es_nombre],
    })

    resumen = grupos.groupby("clave").agg(
        escrituras=("nombre", "nunique"),
        jurisdicciones=("jurisdiccion", "nunique"),
        registros=("nombre", "size"),
        formas=("nombre", lambda s: sorted(set(s))),
    )

    resumen = resumen[resumen["escrituras"] > 1].copy()
    resumen["categoria"] = resumen["jurisdicciones"].map(
        lambda n: "misma persona" if n == 1 else "revisar (homonimo?)"
    )
    return resumen.sort_values(
        ["categoria", "escrituras"], ascending=[True, False]
    )


# ================================================================
# TURNO 3 · NADISSA
# Variables: NIVEL, SECTOR, AREA, STATUS, MODALIDAD, JORNADA, PLAN
# Completar aquí:
# - inventario de categorías;
# - categorías vacías o fuera del dominio esperado;
# - diferencias por escritura, tildes, mayúsculas o puntuación;
# - resumen final de los problemas potenciales de calidad.
# ================================================================


if __name__ == "__main__":
    df = cargar_datos()
    print(f"Registros cargados: {len(df):,}")
    print(f"Columnas totales: {len(df.columns)}")
    print("Pendiente: completar las secciones por turnos.")
