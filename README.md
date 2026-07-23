# Proyecto 1 · Obtención y Limpieza de Datos

**Curso:** CC3084 · Data Science  
**Universidad:** Universidad del Valle de Guatemala  
**Semestre:** II, 2026

## Objetivo

Obtener, diagnosticar, limpiar y validar los datos de establecimientos educativos de Guatemala que llegan al nivel **Diversificado**. El resultado final será un único CSV limpio, acompañado por el código reproducible, el plan de limpieza, el registro de transformaciones, el informe de calidad y el libro de códigos.

## Estado actual

Ya se cuenta con los **23 archivos CSV crudos** dentro de `data/raw/`. Estos archivos corresponden a los 22 departamentos de Guatemala y a una exportación adicional de Ciudad Capital.

La unión de los archivos se realiza con:

```bash
python src/unir_csv.py
```

El resultado se guarda en:

```text
data/interim/establecimientos_diversificado_raw_unificado.csv
```

La unión no limpia ni corrige los datos. El proceso conserva las 11,890 filas crudas, incluyendo las 23 filas completamente vacías, debido a que estas todavía forman parte del diagnóstico inicial.

De las 11,890 filas:

    - 11,867 contienen información.
    - 23 están completamente vacías.

El conjunto contiene 17 variables originales. Además, el archivo unificado agrega dos columnas técnicas para mantener la trazabilidad:

archivo_origen: indica de qué archivo CSV proviene el registro.
fila_origen: indica la posición del registro dentro del archivo original.

Por lo tanto, el archivo unificado contiene 19 columnas en total: 17 variables originales y 2 columnas de trazabilidad.

## Archivos principales

```text
data/raw/                              23 CSV originales; nunca se editan
data/interim/                          archivo unificado generado por código
notebooks/01_ingesta_diagnostico_inicial.ipynb
src/unir_csv.py                        unión de los 23 CSV
src/diagnostico.py                     diagnóstico inicial
src/limpieza.py                        limpieza aprobada
src/validacion.py                      pruebas del conjunto limpio
docs/fuente_datos.md                   fuente y conversión
docs/plan_limpieza.md                  plan compartido
docs/registro_transformaciones.csv     cambios realizados
docs/informe_calidad.md                comparación antes y después
docs/codebook.md                       libro de códigos compartido
```

## Forma sencilla de trabajar

No se trabajará en paralelo sobre los mismos archivos. Cada persona termina su parte, hace un commit y avisa a la siguiente para que primero descargue la versión más reciente.

### Orden de trabajo

1. **Vianka** comienza.
2. Cuando termine y suba sus cambios, avisa a **Ricardo**.
3. Ricardo ejecuta `git pull`, continúa el mismo archivo y sube su parte.
4. Ricardo avisa a **Nadissa**.
5. Nadissa ejecuta `git pull`, completa su parte y revisa que la fase esté terminada.

Este mismo orden se repite en cada fase: diagnóstico, plan de limpieza, limpieza, validación y documentación final.

## Responsabilidades

| Persona | Variables principales | Responsabilidad adicional |
|---|---|---|
| **Vianka** | `CODIGO`, `DISTRITO`, `DEPARTAMENTO`, `MUNICIPIO`, `DEPARTAMENTAL` | Verificar la unión y la consistencia geográfica |
| **Ricardo** | `ESTABLECIMIENTO`, `DIRECCION`, `TELEFONO`, `SUPERVISOR`, `DIRECTOR` | Revisar formatos de texto y duplicados exactos o parciales |
| **Nadissa** | `NIVEL`, `SECTOR`, `AREA`, `STATUS`, `MODALIDAD`, `JORNADA`, `PLAN` | Revisar categorías y consolidar el resultado de cada fase |

## Fases del proyecto

### 1. Diagnóstico inicial

Todos trabajan, por turnos, en:

```text
src/diagnostico.py
notebooks/01_ingesta_diagnostico_inicial.ipynb
```

El diagnóstico debe incluir registros, variables, tipos, faltantes, valores únicos, duplicados, valores fuera de dominio, formatos inconsistentes y problemas potenciales.

### 2. Plan de limpieza

Antes de modificar datos, cada persona completa las filas de sus variables en:

```text
docs/plan_limpieza.md
```

Cada problema debe tener regla propuesta, justificación y riesgo. Solo después de revisar el plan entre los tres se comienza la limpieza.

### 3. Limpieza

Los tres continúan, por turnos, en:

```text
src/limpieza.py
```

Cada cambio debe anotarse también en:

```text
docs/registro_transformaciones.csv
```

### 4. Validación y cierre

Los tres completan, por turnos:

```text
src/validacion.py
docs/informe_calidad.md
docs/codebook.md
```

## Regla para cada turno

Antes de comenzar:

```bash
git pull
```

Al terminar una parte completa:

```bash
git add .
git commit -m "Descripción clara del trabajo realizado"
git push
```

Luego se avisa a la siguiente persona. No se deben hacer commits por cada línea o cada archivo pequeño; un commit debe representar una parte completa y entendible.

## Reglas importantes

- Nunca editar manualmente los archivos de `data/raw/`.
- No limpiar datos dentro del diagnóstico.
- No aplicar una transformación que no esté escrita antes en el plan.
- No eliminar posibles duplicados automáticamente.
- Documentar cada transformación y la cantidad de registros afectados.
- Todos deben contribuir al código y al libro de códigos.

## Fuente

Los datos provienen del buscador de establecimientos educativos del Ministerio de Educación de Guatemala, usando el filtro `NIVEL ESCOLAR: DIVERSIFICADO`.

Más información en [`docs/fuente_datos.md`](docs/fuente_datos.md).
