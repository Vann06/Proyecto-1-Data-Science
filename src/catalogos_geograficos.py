"""Catálogos y normalización determinista para la geografía de Guatemala.

Este módulo no ejecuta la limpieza. src.limpieza es la única fuente de
verdad del proceso y reutiliza aquí solamente dominios y funciones escalares.
"""

from __future__ import annotations

import math
import re
import unicodedata
from numbers import Real
from typing import Any

import pandas as pd


def es_faltante_escalar(valor: Any) -> bool:
    """Detecta faltantes escalares sin producir un resultado vectorial."""
    if valor is None or valor is pd.NA or valor is pd.NaT:
        return True
    return isinstance(valor, Real) and math.isnan(float(valor))


VARIABLES_VIANKA = [
    "CODIGO",
    "DISTRITO",
    "DEPARTAMENTO",
    "MUNICIPIO",
    "DEPARTAMENTAL",
]
MARCADORES_FALTANTE = {
    "",
    "N/A",
    "NA",
    "N.A.",
    "NULL",
    "NONE",
    "-",
    ".",
    "SIN DATO",
    "SIN DATOS",
    "NO DISPONIBLE",
}
PATRON_CODIGO = re.compile(r"^\d{2}-\d{2}-\d{4}-\d{2}$")
PATRON_DISTRITO_CORTO = re.compile(r"^\d{2}-\d{3}$")
PATRON_DISTRITO_EXTENDIDO = re.compile(r"^\d{2}-\d{2}-\d{4}$")
PATRON_DISTRITO_INCOMPLETO = re.compile(r"^\d{2}-$")
PATRON_ZONA = re.compile(r"^ZONA\s+(\d{1,2})$")
CARACTERES_INVISIBLES = re.compile(r"[\u200b-\u200d\u2060\ufeff]")

DEPARTAMENTOS_POR_CODIGO = {
    "01": "Guatemala",
    "02": "El Progreso",
    "03": "Sacatepéquez",
    "04": "Chimaltenango",
    "05": "Escuintla",
    "06": "Santa Rosa",
    "07": "Sololá",
    "08": "Totonicapán",
    "09": "Quetzaltenango",
    "10": "Suchitepéquez",
    "11": "Retalhuleu",
    "12": "San Marcos",
    "13": "Huehuetenango",
    "14": "Quiché",
    "15": "Baja Verapaz",
    "16": "Alta Verapaz",
    "17": "Petén",
    "18": "Izabal",
    "19": "Zacapa",
    "20": "Chiquimula",
    "21": "Jalapa",
    "22": "Jutiapa",
}

DEPARTAMENTALES_CANONICAS = {
    "ALTA VERAPAZ": "Alta Verapaz",
    "BAJA VERAPAZ": "Baja Verapaz",
    "CHIMALTENANGO": "Chimaltenango",
    "CHIQUIMULA": "Chiquimula",
    "EL PROGRESO": "El Progreso",
    "ESCUINTLA": "Escuintla",
    "GUATEMALA NORTE": "Guatemala Norte",
    "GUATEMALA OCCIDENTE": "Guatemala Occidente",
    "GUATEMALA ORIENTE": "Guatemala Oriente",
    "GUATEMALA SUR": "Guatemala Sur",
    "HUEHUETENANGO": "Huehuetenango",
    "IZABAL": "Izabal",
    "JALAPA": "Jalapa",
    "JUTIAPA": "Jutiapa",
    "PETEN": "Petén",
    "QUETZALTENANGO": "Quetzaltenango",
    "QUICHE": "Quiché",
    "QUICHE NORTE": "Quiché Norte",
    "RETALHULEU": "Retalhuleu",
    "SACATEPEQUEZ": "Sacatepéquez",
    "SAN MARCOS": "San Marcos",
    "SANTA ROSA": "Santa Rosa",
    "SOLOLA": "Sololá",
    "SUCHITEPEQUEZ": "Suchitepéquez",
    "TOTONICAPAN": "Totonicapán",
    "ZACAPA": "Zacapa",
}

# Las claves no llevan tildes porque se usan únicamente para comparar. Los
# reemplazos son cerrados y deterministas; no se usa similitud para modificar.
PALABRAS_GEOGRAFICAS = {
    "ACASAGUASTLAN": "Acasaguastlán",
    "ACATAN": "Acatán",
    "AGUACATAN": "Aguacatán",
    "AGUSTIN": "Agustín",
    "AMATITLAN": "Amatitlán",
    "ANDRES": "Andrés",
    "ASUNCION": "Asunción",
    "ATITAN": "Atitán",
    "BALANYA": "Balanyá",
    "BARBARA": "Bárbara",
    "BARTOLOME": "Bartolomé",
    "CABANAS": "Cabañas",
    "CABRICAN": "Cabricán",
    "CAHABON": "Cahabón",
    "CAJOLA": "Cajolá",
    "CAMOTAN": "Camotán",
    "CARCHA": "Carchá",
    "CHAPARRON": "Chaparrón",
    "CHICHE": "Chiché",
    "COBAN": "Cobán",
    "CONCEPCION": "Concepción",
    "CRISTOBAL": "Cristóbal",
    "CUNEN": "Cunén",
    "DUENAS": "Dueñas",
    "GENOVA": "Génova",
    "GUALAN": "Gualán",
    "GUAZACAPAN": "Guazacapán",
    "HUITE": "Huité",
    "HUITAN": "Huitán",
    "IXCAN": "Ixcán",
    "IXCHIGUAN": "Ixchiguán",
    "IXHUATAN": "Ixhuatán",
    "IXTAHUACAN": "Ixtahuacán",
    "IXTATAN": "Ixtatán",
    "JERONIMO": "Jerónimo",
    "JICARO": "Jícaro",
    "JOCOTAN": "Jocotán",
    "JOSE": "José",
    "LANQUIN": "Lanquín",
    "LUCIA": "Lucía",
    "MALACATAN": "Malacatán",
    "MAQUINA": "Máquina",
    "MARIA": "María",
    "MARTIN": "Martín",
    "MORAZAN": "Morazán",
    "MULUA": "Muluá",
    "NAHUALA": "Nahualá",
    "NENTON": "Nentón",
    "OCOS": "Ocós",
    "PALIN": "Palín",
    "PALOPO": "Palopó",
    "PANAM": "Panán",
    "PANZOS": "Panzós",
    "PATZICIA": "Patzicía",
    "PATZITE": "Patzité",
    "PATZUN": "Patzún",
    "PETATAN": "Petatán",
    "POPTUN": "Poptún",
    "PURULHA": "Purulhá",
    "QUICHE": "Quiché",
    "RAXRUHA": "Raxruhá",
    "RIO": "Río",
    "SACATEPEQUEZ": "Sacatepéquez",
    "SALAMA": "Salamá",
    "SALCAJA": "Salcajá",
    "SAYAXCHE": "Sayaxché",
    "SEBASTIAN": "Sebastián",
    "SENAHU": "Senahú",
    "SIGUILA": "Sigüilá",
    "SIQUINALA": "Siquinalá",
    "SOLOLA": "Sololá",
    "TACANA": "Tacaná",
    "TAMAHU": "Tamahú",
    "TECPAN": "Tecpán",
    "TECTITAN": "Tectitán",
    "TOLIMAN": "Tolimán",
    "TOMAS": "Tomás",
    "TOTONICAPAN": "Totonicapán",
    "TUCURU": "Tucurú",
    "UNION": "Unión",
    "USPANTAN": "Uspantán",
    "UTATLAN": "Utatlán",
    "VINAS": "Viñas",
    "VISITACION": "Visitación",
    "ZAPOTITLAN": "Zapotitlán",
}
PALABRAS_MINUSCULAS = {"DE", "DEL", "EL", "LA", "LAS", "LOS"}
NOMBRES_MUNICIPALES_CORREGIDOS = {
    # Error ortográfico confirmado por el código municipal 14-21.
    "PACHALUN": "Pachalum",
}


def clave_comparacion(valor: Any) -> str:
    """Crea una clave sin tildes, mayúscula y con espacios uniformes."""
    if es_faltante_escalar(valor):
        return ""
    texto = unicodedata.normalize("NFKD", str(valor))
    texto = "".join(c for c in texto if not unicodedata.combining(c))
    texto = CARACTERES_INVISIBLES.sub("", texto)
    return re.sub(r"\s+", " ", texto).strip().upper()


def limpiar_celda_texto(valor: Any) -> Any:
    """Normaliza Unicode/espacios y representa marcadores como ``pd.NA``."""
    if es_faltante_escalar(valor):
        return pd.NA
    texto = unicodedata.normalize("NFC", str(valor))
    texto = CARACTERES_INVISIBLES.sub("", texto)
    texto = re.sub(r"\s+", " ", texto).strip()
    if clave_comparacion(texto) in MARCADORES_FALTANTE:
        return pd.NA
    return texto


def nombre_geografico(valor: Any) -> Any:
    """Normaliza un nombre observado con un diccionario ortográfico cerrado."""
    clave = clave_comparacion(valor)
    if not clave:
        return pd.NA
    if clave in NOMBRES_MUNICIPALES_CORREGIDOS:
        return NOMBRES_MUNICIPALES_CORREGIDOS[clave]
    palabras = []
    for posicion, palabra in enumerate(clave.split()):
        if palabra in PALABRAS_GEOGRAFICAS:
            palabras.append(PALABRAS_GEOGRAFICAS[palabra])
        elif posicion > 0 and palabra in PALABRAS_MINUSCULAS:
            palabras.append(palabra.lower())
        else:
            palabras.append(palabra.title())
    return " ".join(palabras)
