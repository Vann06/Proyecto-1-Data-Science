# Proyecto 1 · Obtención y Limpieza de Datos

**Curso:** CC3084 · Data Science  
**Universidad:** Universidad del Valle de Guatemala  
**Semestre:** II, 2026  
**Estado actual:** Estructura inicial del proyecto

## Descripción

Este repositorio contiene el trabajo del **Proyecto 1: Obtención y Limpieza de los Datos**.  
El objetivo será obtener los datos de establecimientos educativos de Guatemala que llegan
hasta el nivel diversificado, diagnosticar su calidad, definir un plan de limpieza,
aplicar transformaciones reproducibles, validar el resultado y generar un único conjunto
de datos limpio junto con su libro de códigos.

> En esta versión inicial todavía no se han descargado, analizado ni limpiado datos.

## Fuente prevista

Ministerio de Educación de Guatemala:

- Buscador de establecimientos educativos
- Nivel escolar requerido: **Diversificado**

## Estructura

```text
Proyecto-1-Data-Science/
├── data/
│   ├── raw/                 # Datos originales sin modificar
│   ├── interim/             # Datos temporales o intermedios
│   └── processed/           # Conjunto final limpio
├── notebooks/
│   └── proyecto_1.ipynb     # Cuaderno principal del proyecto
├── src/
│   ├── obtencion.py         # Funciones para obtener y unir datos
│   ├── diagnostico.py       # Diagnóstico del estado inicial
│   ├── limpieza.py          # Transformaciones de limpieza
│   ├── validacion.py        # Pruebas automáticas de calidad
│   └── utils.py             # Funciones auxiliares
├── docs/
│   ├── codebook.md
│   ├── plan_limpieza.md
│   ├── informe_calidad.md
│   └── registro_transformaciones.csv
├── reports/
│   └── figures/             # Gráficas y tablas exportadas
├── tests/
│   └── test_calidad.py
├── .github/workflows/
│   └── publish.yml          # Publicación del sitio con GitHub Pages
├── _quarto.yml
├── index.qmd
├── requirements.txt
└── README.md
```

## Flujo de trabajo previsto

1. Obtener y documentar los datos crudos.
2. Guardar cada archivo original en `data/raw/`.
3. Elaborar el diagnóstico inicial.
4. Preparar el plan de limpieza antes de modificar los datos.
5. Implementar las transformaciones en funciones reproducibles.
6. Registrar cada modificación.
7. Ejecutar pruebas automáticas de calidad.
8. Comparar el estado antes y después.
9. Generar un único archivo limpio en `data/processed/`.
10. Completar el libro de códigos y el informe final.

## Instalación

### Windows PowerShell

```powershell
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
jupyter notebook notebooks/proyecto_1.ipynb
```

### macOS o Linux

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
jupyter notebook notebooks/proyecto_1.ipynb
```

## Reglas del proyecto

- Los archivos de `data/raw/` no deben modificarse.
- Toda transformación debe poder reproducirse ejecutando el código.
- No se eliminarán posibles duplicados parciales sin analizar y documentar cada caso.
- Cada cambio debe quedar registrado en `docs/registro_transformaciones.csv`.
- Las variables y transformaciones deben documentarse en `docs/codebook.md`.
- El conjunto final se guardará únicamente en `data/processed/`.
- Cada integrante debe realizar contribuciones identificables mediante commits.

## Trabajo colaborativo sugerido

Cada integrante debe trabajar en una rama propia:

```bash
git checkout -b nombre-tarea
```

Después debe subir sus cambios y abrir un Pull Request hacia `main`.

## Publicación

El repositorio incluye una configuración base para publicar la documentación mediante
**Quarto + GitHub Pages**. La publicación podrá activarse en:

`Settings → Pages → Source → GitHub Actions`

La dirección esperada será:

`https://Vann06.github.io/NOMBRE-DEL-REPOSITORIO/`
