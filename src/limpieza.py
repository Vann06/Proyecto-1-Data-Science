"""Limpieza reproducible del conjunto de datos.

IMPORTANTE:
No escribir transformaciones aquí hasta que la regla esté documentada y
aprobada en docs/plan_limpieza.md.

El archivo se trabaja por turnos: Vianka, Ricardo y Nadissa.
"""

import re

import pandas as pd

from src.diagnostico import (
    FRASE_AUSENCIA,
    _palabras_con_letra,
    normalizar_nombre,
    separar_numeros,
    sin_tildes,
)
from src.catalogos_geograficos import (
    DEPARTAMENTALES_CANONICAS,
    DEPARTAMENTOS_POR_CODIGO,
    PATRON_CODIGO,
    PATRON_DISTRITO_CORTO,
    PATRON_DISTRITO_EXTENDIDO,
    PATRON_DISTRITO_INCOMPLETO,
    PATRON_ZONA,
    VARIABLES_VIANKA,
    clave_comparacion,
    limpiar_celda_texto,
    nombre_geografico,
)


def limpiar_datos_preliminar(df: pd.DataFrame) -> pd.DataFrame:
    """Aplicará únicamente las reglas aprobadas en el plan de limpieza."""

    limpio_pre = df.copy()

    # ============================================================
    # TURNO 1 · VIANKA
    # CODIGO, DISTRITO, DEPARTAMENTO, MUNICIPIO, DEPARTAMENTAL
    # Los valores originales se conservan y los casos dudosos se marcan.
    # ============================================================

    limpio_pre = limpiar_codigo(limpio_pre)
    limpio_pre = limpiar_distrito(limpio_pre)
    limpio_pre = limpiar_departamento(limpio_pre)
    limpio_pre = limpiar_municipio(limpio_pre)
    limpio_pre = limpiar_departamental(limpio_pre)
    limpio_pre = marcar_consistencia_geografica(limpio_pre)

    # ============================================================
    # TURNO 2 · RICARDO
    # ESTABLECIMIENTO, DIRECCION, TELEFONO, SUPERVISOR, DIRECTOR
    # Los duplicados parciales se marcan, no se eliminan.
    # ============================================================

    limpio_pre = marcar_duplicados_establecimiento(limpio_pre)
    limpio_pre = limpiar_direccion(limpio_pre)
    limpio_pre = limpiar_telefono(limpio_pre)
    limpio_pre = limpiar_supervisor(limpio_pre)
    limpio_pre = limpiar_director(limpio_pre)

    # ============================================================
    # TURNO 3 · NADISSA
    # NIVEL, SECTOR, AREA, STATUS, MODALIDAD, JORNADA, PLAN
    # Agregar aquí solo las reglas previamente aprobadas.
    # ============================================================

    limpio_pre = limpiar_categorias_nadissa(limpio_pre)
    return limpio_pre


# ================================================================
# TURNO 3 - NADISSA - variables categoricas
# ================================================================


CATEGORIAS_NADISSA = {
    "NIVEL": ["DIVERSIFICADO"],
    "SECTOR": ["PRIVADO", "OFICIAL", "COOPERATIVA", "MUNICIPAL"],
    "AREA": ["URBANA", "RURAL"],
    "STATUS": ["ABIERTA", "CERRADA TEMPORALMENTE", "CERRADA DEFINITIVAMENTE", "TEMPORAL TITULOS", "TEMPORAL NOMBRAMIENTO"],
    "MODALIDAD": ["MONOLINGUE", "BILINGUE"],
    "JORNADA": ["DOBLE", "VESPERTINA", "MATUTINA", "SIN JORNADA", "NOCTURNA", "INTERMEDIA"],
    "PLAN": ["DIARIO(REGULAR)", "FIN DE SEMANA", "SEMIPRESENCIAL (FIN DE SEMANA)", "SEMIPRESENCIAL (UN D\u00cdA A LA SEMANA)", "A DISTANCIA", "SEMIPRESENCIAL", "VIRTUAL A DISTANCIA", "SEMIPRESENCIAL (DOS D\u00cdAS A LA SEMANA)", "SABATINO", "DOMINICAL", "MIXTO", "IRREGULAR", "INTERCALADO"],
}


def limpiar_categorias_nadissa(df: pd.DataFrame) -> pd.DataFrame:
    """Reclasifica el faltante de AREA y fija dominios categoricos aprobados."""
    df = df.copy()
    for columna, dominio in CATEGORIAS_NADISSA.items():
        texto = df[columna].astype("string").str.strip().replace("", pd.NA)
        if columna == "AREA":
            texto = texto.mask(texto.eq("SIN ESPECIFICAR"), pd.NA)
        fuera_dominio = texto.dropna()[~texto.dropna().isin(dominio)].unique()
        if len(fuera_dominio):
            valores = ", ".join(map(str, fuera_dominio))
            raise ValueError(f"{columna} contiene categorias no aprobadas: {valores}.")
        df[columna] = texto.astype(pd.CategoricalDtype(categories=dominio))

    return df


# ================================================================
# TURNO 1 · VIANKA — funciones de limpieza
# ================================================================


def limpiar_codigo(df: pd.DataFrame) -> pd.DataFrame:
    """Conserva CODIGO como texto y agrega controles; no reconstruye valores."""
    df = df.copy()
    df["CODIGO_ORIGINAL"] = df["CODIGO"]
    codigo = df["CODIGO"].map(limpiar_celda_texto).astype("string")
    df["CODIGO"] = codigo
    df["CODIGO_FORMATO_VALIDO"] = codigo.str.fullmatch(PATRON_CODIGO).fillna(False)
    df["CODIGO_DUPLICADO"] = codigo.notna() & codigo.duplicated(keep=False)
    return df


def limpiar_distrito(df: pd.DataFrame) -> pd.DataFrame:
    """Unifica faltantes y clasifica DISTRITO sin completar códigos parciales."""
    df = df.copy()
    df["DISTRITO_ORIGINAL"] = df["DISTRITO"]
    distrito = df["DISTRITO"].map(limpiar_celda_texto).astype("string")
    corto = distrito.str.fullmatch(PATRON_DISTRITO_CORTO).fillna(False)
    extendido = distrito.str.fullmatch(PATRON_DISTRITO_EXTENDIDO).fillna(False)
    incompleto = distrito.str.fullmatch(PATRON_DISTRITO_INCOMPLETO).fillna(False)

    formato = pd.Series("otro", index=df.index, dtype="string")
    formato.loc[distrito.isna()] = "faltante"
    formato.loc[corto] = "corto NN-NNN"
    formato.loc[extendido] = "extendido NN-NN-NNNN"
    formato.loc[incompleto] = "incompleto NN-"

    df["DISTRITO"] = distrito
    df["DISTRITO_FORMATO"] = formato
    df["DISTRITO_INCOMPLETO"] = incompleto
    df["DISTRITO_FORMATO_VALIDO"] = corto | extendido
    df["DISTRITO_REQUIERE_REVISION"] = incompleto | formato.eq("otro")
    return df


def limpiar_departamento(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza DEPARTAMENTO al catálogo oficial y preserva el valor crudo."""
    df = df.copy()
    df["DEPARTAMENTO_ORIGINAL"] = df["DEPARTAMENTO"]
    original_limpio = df["DEPARTAMENTO"].map(limpiar_celda_texto).astype("string")
    clave = original_limpio.map(clave_comparacion)
    catalogo = {
        clave_comparacion(nombre): nombre
        for nombre in DEPARTAMENTOS_POR_CODIGO.values()
    }
    catalogo["CIUDAD CAPITAL"] = "Guatemala"
    normalizado = clave.map(catalogo).astype("string")

    df["DEPARTAMENTO"] = normalizado.fillna(original_limpio)
    df["DEPARTAMENTO_FUERA_CATALOGO"] = original_limpio.notna() & normalizado.isna()
    df["DEPARTAMENTO_ES_CIUDAD_CAPITAL"] = clave.eq("CIUDAD CAPITAL")
    return df


def limpiar_municipio(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza MUNICIPIO y separa la zona de los registros capitalinos."""
    df = df.copy()
    df["MUNICIPIO_ORIGINAL"] = df["MUNICIPIO"]
    municipio_original = df["MUNICIPIO"].map(limpiar_celda_texto).astype("string")
    departamento_original = df["DEPARTAMENTO_ORIGINAL"].map(clave_comparacion)
    es_capital = departamento_original.eq("CIUDAD CAPITAL")
    zona = municipio_original.fillna("").str.extract(PATRON_ZONA, expand=False)

    df["ZONA_CAPITAL"] = pd.Series(pd.NA, index=df.index, dtype="string")
    con_zona = es_capital & zona.notna()
    df.loc[con_zona, "ZONA_CAPITAL"] = "Zona " + zona[con_zona]

    municipio = municipio_original.map(nombre_geografico).astype("string")
    municipio.loc[es_capital] = "Guatemala"
    df["MUNICIPIO"] = municipio
    df["MUNICIPIO_ZONA_INVALIDA"] = es_capital & zona.isna()
    df["MUNICIPIO_CORREGIDO_CATALOGO"] = (
        municipio_original.notna()
        & municipio.notna()
        & municipio_original.ne(municipio)
    )
    return df


def limpiar_departamental(df: pd.DataFrame) -> pd.DataFrame:
    """Normaliza DEPARTAMENTAL con su dominio administrativo independiente."""
    df = df.copy()
    df["DEPARTAMENTAL_ORIGINAL"] = df["DEPARTAMENTAL"]
    original_limpio = df["DEPARTAMENTAL"].map(limpiar_celda_texto).astype("string")
    clave = original_limpio.map(clave_comparacion)
    normalizada = clave.map(DEPARTAMENTALES_CANONICAS).astype("string")
    df["DEPARTAMENTAL"] = normalizada.fillna(original_limpio)
    df["DEPARTAMENTAL_FUERA_CATALOGO"] = original_limpio.notna() & normalizada.isna()
    return df


def marcar_consistencia_geografica(df: pd.DataFrame) -> pd.DataFrame:
    """Marca contradicciones, prefijos ambiguos y duplicados; no elimina filas."""
    df = df.copy()
    codigo = df["CODIGO"].fillna("")
    prefijo_departamento = codigo.str.slice(0, 2)
    esperado = prefijo_departamento.map(DEPARTAMENTOS_POR_CODIGO)
    esperado.loc[prefijo_departamento.eq("00")] = "Guatemala"

    consistente = pd.Series(pd.NA, index=df.index, dtype="boolean")
    comparable = esperado.notna() & df["DEPARTAMENTO"].notna()
    consistente.loc[comparable] = df.loc[comparable, "DEPARTAMENTO"].eq(
        esperado.loc[comparable]
    )
    df["CODIGO_DEPARTAMENTO_CONSISTENTE"] = consistente

    prefijo_municipio = codigo.str.slice(0, 5)
    municipios_por_prefijo = (
        pd.DataFrame({"prefijo": prefijo_municipio, "municipio": df["MUNICIPIO"]})
        .loc[codigo.ne("")]
        .groupby("prefijo")["municipio"]
        .nunique()
    )
    ambiguos = set(municipios_por_prefijo[municipios_por_prefijo > 1].index)
    df["PREFIJO_CODIGO_AMBIGUO"] = codigo.ne("") & prefijo_municipio.isin(ambiguos)

    completo = df[VARIABLES_VIANKA].notna().all(axis=1)
    df["DUPLICADO_EXACTO_VIANKA"] = completo & df[VARIABLES_VIANKA].duplicated(
        keep=False
    )
    return df


# ================================================================
# TURNO 2 · RICARDO — funciones de limpieza
# ================================================================


def marcar_duplicados_establecimiento(df: pd.DataFrame) -> pd.DataFrame:
    """Agrega una clave de comparación y marca posibles duplicados de ESTABLECIMIENTO.

    El plan pide conservar el nombre original ("no transformar el valor"),
    así que ESTABLECIMIENTO no se toca: solo se agrega ESTABLECIMIENTO_CLAVE
    (normalizar_nombre) para agrupar. Un grupo es sospechoso cuando, dentro
    del mismo MUNICIPIO, la clave coincide pero hay más de una escritura
    distinta del nombre -mismo criterio que variantes_establecimiento() de
    diagnostico.py-: agrupar por clave+municipio sin exigir escrituras>1
    marcaría también a los cientos de institutos públicos que comparten un
    nombre genérico idéntico en el mismo municipio pero son planteles
    distintos, que no son duplicados. CODIGO sigue siendo la única llave
    primaria, así que esto no fusiona ni elimina nada, solo marca. Un grupo
    queda "confirmado" cuando además coinciden JORNADA, PLAN y DIRECCION (la
    dirección cruda, tal como llega, antes de limpiar_direccion), que es la
    evidencia adicional que pide el plan antes de tratarlos como el mismo
    establecimiento.
    """
    df = df.copy()

    nombre = df["ESTABLECIMIENTO"].fillna("").str.strip()
    clave = nombre.map(normalizar_nombre)
    df["ESTABLECIMIENTO_CLAVE"] = clave

    columna_municipio = (
        "MUNICIPIO_ORIGINAL" if "MUNICIPIO_ORIGINAL" in df.columns else "MUNICIPIO"
    )
    municipio = df[columna_municipio].fillna("").str.strip()
    grupo = clave + "||" + municipio
    con_clave = clave.ne("")

    escrituras = pd.DataFrame({"grupo": grupo, "nombre": nombre})[con_clave]
    escrituras_por_grupo = escrituras.groupby("grupo")["nombre"].nunique()
    claves_duplicadas = escrituras_por_grupo[escrituras_por_grupo > 1].index
    pertenece = con_clave & grupo.isin(claves_duplicadas)

    ids = {c: i + 1 for i, c in enumerate(sorted(claves_duplicadas))}
    df["ESTABLECIMIENTO_GRUPO_DUPLICADO"] = pd.array(
        [ids[c] if p else pd.NA for c, p in zip(grupo, pertenece)],
        dtype="Int64",
    )

    detalle = pd.DataFrame({
        "grupo": grupo,
        "jornada": df["JORNADA"].fillna("").str.strip(),
        "plan": df["PLAN"].fillna("").str.strip(),
        "direccion": df["DIRECCION"].fillna("").str.strip().map(sin_tildes),
    })[pertenece]

    confirmado = pd.Series(False, index=df.index)
    if not detalle.empty:
        coincide = detalle.groupby("grupo")[["jornada", "plan", "direccion"]].transform("nunique")
        confirmado.loc[detalle.index] = (coincide == 1).all(axis=1)
    df["ESTABLECIMIENTO_DUPLICADO_CONFIRMADO"] = confirmado

    return df


# --- DIRECCION ---------------------------------------------------------

# Dos separadores iguales (\1 exige que sean el mismo carácter): distingue una
# fecha DD/MM/AAAA de un rango de números de casa como 0-55/0-92, que mezcla
# guion y barra y por eso nunca coincide en el backreference.
_FECHA_FINAL = re.compile(r"(?:\s*\d{1,2}([/-])\d{1,2}\1\d{2,4})+\s*$")

# "O" sola al inicio, seguida de una vía (CALLE/AVENIDA/AV.): típico de
# direcciones que deberían empezar con "0" (cero) y no con la letra.
_O_INICIAL = re.compile(r"^O(?=\s+(?:CALLE|AVENIDA|AV\.?)(?:\s|$))")
# "O" seguida de una letra opcional y un guion+dígito: OC-150, O-71.
_O_GUION_DIGITO = re.compile(r"\bO([A-Z]?)-(\d)")


def _recortar_municipio(direccion: str, municipio: str) -> str:
    """Recorta el municipio del final de una dirección, solo si sobra contenido.

    No recorta si el municipio está en medio de la cadena (posible topónimo)
    ni si el carácter justo antes del sufijo es alfanumérico (el municipio
    sería parte de otra palabra, no un sufijo real).
    """
    if not municipio:
        return direccion

    dn = sin_tildes(direccion)
    mn = sin_tildes(municipio)
    if not dn.endswith(mn):
        return direccion

    pos = len(dn) - len(mn)
    if pos <= 0:
        return direccion
    if dn[pos - 1].isalnum():
        return direccion

    recorte = re.sub(r"[\s,.\-]+$", "", direccion[:pos])
    return recorte if recorte else direccion


def limpiar_direccion(df: pd.DataFrame) -> pd.DataFrame:
    """Aplica en cascada las 4 reglas de DIRECCION del plan de limpieza.

    Orden: primero se reclasifican a NA los faltantes disfrazados (así no se
    recorta nada de una celda que ya no dice nada); sobre lo que queda se
    recorta la fecha incrustada al final -la capa más externa, agregada al
    exportar-; luego el sufijo de municipio, que recién ahí queda expuesto al
    final de la cadena; por último la letra "O" por cero, que es
    independiente de las demás. El dominio rural (ALDEA/CASERÍO) no se toca:
    la ausencia de número de casa ahí no es un defecto (regla 26 del plan).
    """
    df = df.copy()
    df["DIRECCION_ORIGINAL"] = df["DIRECCION"]

    direccion = df["DIRECCION"].fillna("").str.strip()
    columna_municipio = (
        "MUNICIPIO_ORIGINAL" if "MUNICIPIO_ORIGINAL" in df.columns else "MUNICIPIO"
    )
    municipio = df[columna_municipio].fillna("").str.strip()

    # 1) faltante disfrazado: vacía o igual al municipio (sin_tildes + strip)
    dn = direccion.map(sin_tildes)
    mn = municipio.map(sin_tildes)
    faltante = direccion.eq("") | (mn.ne("") & dn.eq(mn))
    direccion = direccion.mask(faltante, pd.NA)

    # 2) fecha incrustada al final
    con_fecha = direccion.map(lambda s: isinstance(s, str) and _FECHA_FINAL.search(s) is not None)
    direccion = direccion.mask(
        con_fecha,
        direccion.str.replace(_FECHA_FINAL, "", regex=True).str.rstrip(" ,.-"),
    )
    direccion = direccion.mask(direccion.eq(""), pd.NA)

    # 3) municipio redundante al final, solo si la dirección trae más contenido
    direccion = pd.Series(
        [
            _recortar_municipio(d, m) if pd.notna(d) else d
            for d, m in zip(direccion, municipio)
        ],
        index=direccion.index,
        dtype="string",
    )

    # 4) letra "O" por cero en contexto numérico
    direccion = direccion.str.replace(_O_INICIAL, "0", regex=True)
    direccion = direccion.str.replace(_O_GUION_DIGITO, r"0\1-\2", regex=True)

    df["DIRECCION"] = direccion
    return df


# --- TELEFONO ------------------------------------------------------------


def limpiar_telefono(df: pd.DataFrame) -> pd.DataFrame:
    """Deja NA en los teléfonos vacíos y convierte el resto en una lista de contactos.

    La celda mezcla varios números con separadores inconsistentes; reutiliza
    separar_numeros() (diagnostico.py) para partirla y se queda solo con los
    números de 7 u 8 dígitos recuperados, unidos con "; ". Si no se recupera
    ningún número válido, también queda NA.
    """
    df = df.copy()
    df["TELEFONO_ORIGINAL"] = df["TELEFONO"]

    def _limpiar(celda: str):
        celda = (celda or "").strip()
        if celda == "":
            return pd.NA
        numeros = [n for n in separar_numeros(celda) if len(n) in (7, 8)]
        return "; ".join(numeros) if numeros else pd.NA

    df["TELEFONO"] = df["TELEFONO"].fillna("").map(_limpiar).astype("string")
    return df


# --- SUPERVISOR y DIRECTOR — nombres de persona ---------------------------


def _mascara_ausente(texto: pd.Series) -> pd.Series:
    """Mismo criterio que nombres_ausentes() de diagnostico.py, como máscara por fila."""
    n_alpha = texto.map(_palabras_con_letra)
    frase = texto.str.contains(FRASE_AUSENCIA).fillna(False)
    return n_alpha.lt(2) | (n_alpha.ge(2) & frase)


def _forma_mas_frecuente(serie: pd.Series) -> str:
    conteo = serie.value_counts()
    return sorted(conteo[conteo == conteo.max()].index)[0]


def _fusionar_variantes(texto: pd.Series, geo: pd.Series) -> pd.Series:
    """Unifica escrituras que comparten (geo, normalizar_nombre) a la forma más frecuente.

    Las celdas ausentes no participan del agrupamiento (no son nombres que
    fusionar). El corte geográfico es lo que evita fusionar homónimos reales
    de distinta jurisdicción.
    """
    ausente = _mascara_ausente(texto)
    clave = texto.map(normalizar_nombre)
    grupo = geo.fillna("").str.strip() + "||" + clave
    aplicable = ~ausente & clave.ne("")

    resultado = texto.copy()
    if aplicable.any():
        mapa = (
            pd.DataFrame({"grupo": grupo[aplicable], "texto": texto[aplicable]})
            .groupby("grupo")["texto"]
            .agg(_forma_mas_frecuente)
        )
        resultado.loc[aplicable] = grupo[aplicable].map(mapa)
    return resultado


# 0 entre letras dentro de la misma palabra: ACEVED0 -> ACEVEDO.
_CERO_EN_PALABRA = re.compile(r"\b([A-Z]+)0([A-Z]*)\b")
# Acentos graves (ajenos al español) hacia su forma aguda correcta.
_GRAVE_A_AGUDA = str.maketrans({
    "À": "Á", "È": "É", "Ì": "Í", "Ò": "Ó", "Ù": "Ú",
    "à": "á", "è": "é", "ì": "í", "ò": "ó", "ù": "ú",
})
# Apóstrofos tipográficos (´ ` ʼ ’) hacia un apóstrofo recto.
_APOSTROFOS = re.compile(r"[´`ʼ’]")


def _corregir_contaminacion_nombre(texto: str) -> str:
    """Corrige grafías puntuales de SUPERVISOR: O/0, tilde grave, apóstrofo, puntuación final."""
    texto = _CERO_EN_PALABRA.sub(r"\1O\2", texto)
    texto = texto.translate(_GRAVE_A_AGUDA)
    texto = _APOSTROFOS.sub("'", texto)
    texto = re.sub(r"[,.;]+\s*$", "", texto).strip()
    return texto


def limpiar_supervisor(df: pd.DataFrame) -> pd.DataFrame:
    """Corrige, fusiona, reclasifica e imputa SUPERVISOR, en ese orden.

    1) Corrige la contaminación puntual (grafías). 2) Fusiona variantes de
    tildes/espacios dentro del mismo DISTRITO. 3) Lo que sigue sin ser un
    nombre real queda NA. 4) Cada NA se imputa con el supervisor más
    frecuente de su DISTRITO (un distrito, un supervisor); si el distrito no
    tiene ninguna referencia, se deja NA.
    """
    df = df.copy()
    df["SUPERVISOR_ORIGINAL"] = df["SUPERVISOR"]

    distrito = df["DISTRITO"].fillna("").str.strip()
    texto = df["SUPERVISOR"].fillna("").str.strip().map(_corregir_contaminacion_nombre)
    texto = _fusionar_variantes(texto, distrito)

    ausente = _mascara_ausente(texto)
    texto = texto.mask(ausente, pd.NA)

    referencia = (
        texto[~ausente].groupby(distrito[~ausente]).agg(_forma_mas_frecuente)
    )
    imputado = ausente & distrito.isin(referencia.index)
    texto = texto.mask(imputado, distrito.map(referencia))

    df["SUPERVISOR"] = texto
    df["SUPERVISOR_IMPUTADO"] = imputado
    return df


# Títulos académicos/profesionales observados al inicio de DIRECTOR.
_TITULO = re.compile(
    r"^(LIC|LICDA|ING|INGA|ARQ|DR|DRA|PEM|PROFR|PROFA|MTRO|MTRA|BR|TEC)\.?\s+",
    re.IGNORECASE,
)


def limpiar_director(df: pd.DataFrame) -> pd.DataFrame:
    """Separa el título, reclasifica la ausencia real y fusiona variantes de DIRECTOR.

    El corte geográfico para fusionar variantes es MUNICIPIO (no DISTRITO
    como en SUPERVISOR): un director no es un cargo territorial, así que
    fusionar por distrito arriesgaría más homónimos. normalizar_nombre ya
    conserva distinto el número de palabras, así que "VASQUEZ" y "VASQUEZ
    REYES" nunca caen en el mismo grupo.
    """
    df = df.copy()
    df["DIRECTOR_ORIGINAL"] = df["DIRECTOR"]

    texto = df["DIRECTOR"].fillna("").str.strip()
    titulo = texto.str.extract(_TITULO, expand=False)
    texto = texto.str.replace(_TITULO, "", regex=True).str.strip()

    ausente = _mascara_ausente(texto)
    columna_municipio = (
        "MUNICIPIO_ORIGINAL" if "MUNICIPIO_ORIGINAL" in df.columns else "MUNICIPIO"
    )
    municipio = df[columna_municipio].fillna("").str.strip()
    texto = _fusionar_variantes(texto, municipio)
    texto = texto.mask(ausente, pd.NA)

    df["DIRECTOR_TITULO"] = titulo.where(titulo.isna(), titulo.str.upper() + ".")
    df["DIRECTOR"] = texto
    return df
