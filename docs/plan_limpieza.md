# Plan de limpieza

Este archivo se completa **antes de modificar los datos**. Los tres trabajan aquí por turnos y únicamente llenan las filas de sus variables.

Estados sugeridos: `Pendiente`, `Propuesta`, `Aprobada`, `Implementada`, `Validada`.

| Responsable | Variable | Problema encontrado | Regla propuesta | Por qué funcionará | Riesgo asociado | Estado |
|---|---|---|---|---|---|---|
| Vianka | CODIGO | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Vianka | DISTRITO | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Vianka | DEPARTAMENTO | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Vianka | MUNICIPIO | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Vianka | DEPARTAMENTAL | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Ricardo | ESTABLECIMIENTO | Escritura inconsistente: tildes (27%), comillas (25%), espacios múltiples (12%), abreviaturas con punto | Normalizar tildes/comillas/espacios en una clave de comparación; conservar el nombre original en los datos | Aquí la puntuación es adorno, no sintaxis; la normalización solo afecta la clave, no el dato final | La NFKD funde Ñ→N (CAÑAS=CANAS) al comparar; sirve para agrupar, no para reemplazar | Propuesta |
| Ricardo | ESTABLECIMIENTO | Posibles duplicados: 848 grupos con >1 escritura en un mismo municipio (1,483 nombres fusionan) | Agrupar por nombre normalizado + municipio; confirmar con JORNADA/PLAN/DIRECCION antes de marcar. No eliminar | CODIGO es la llave primaria (11,867 únicos); el nombre no identifica una entidad por sí solo | Fundir homónimos (mismo nombre, otro municipio) o distinta oferta en un mismo edificio | Propuesta |
| Ricardo | DIRECCION | Faltante disfrazado: 99 vacías + 169 que solo repiten el municipio | Reclasificar a NA la dirección que iguala al municipio; tratar como faltante | Informa lo mismo que un vacío y ningún conteo de nulos la detecta | Es un piso, no un total: CIUDAD GUATEMALA ≠ GUATEMALA por igualdad exacta | Propuesta |
| Ricardo | DIRECCION | Municipio redundante al final (948; 892 son direcciones completas) | Recortar el sufijo del municipio cuando la dirección trae más contenido | Es redundante con MUNICIPIO y no aporta localización nueva | No recortar cuando el municipio es parte de un topónimo del lugar | Propuesta |
| Ricardo | DIRECCION | Fecha incrustada al final (26), a veces repetida (22/0209/02/20) | Recortar el patrón de fecha final; exigir dos separadores para detectarlo | Es un campo desbordado al exportar, no algo tecleado | Confundir con número de casa (3-50, un solo guion): por eso dos separadores | Propuesta |
| Ricardo | DIRECCION | Letra O por cero (10): O-71, OC-150, O AV. 0-06 | Corregir O→0 solo en contexto numérico | Es un typo que produce una cadena válida, invisible a los filtros de formato | Falso positivo sobre una O legítima; revisar en contexto | Propuesta |
| Ricardo | DIRECCION | Dos dominios: urbana postal (vía/número/zona) vs rural nombre-de-lugar (ALDEA, CASERÍO) | NO tratar "falta número de casa" como defecto en el área rural | No es defecto de captura: la dirección rural no puede tener esa estructura | Sobre-limpiar direcciones rurales válidas por medirlas con regla urbana | Documentado |
| Ricardo | TELEFONO | Vacío (969, 8.1%) | Dejar NA | Faltante legítimo: un teléfono no se deduce de otra columna | Ninguno | Propuesta |
| Ricardo | TELEFONO | Formato no estándar (251): varios números por celda, legado de 7 díg, extensión | separar_numeros() → lista de números de 8 díg; el sufijo -XX es correlativo (NNNNNNNN-XX) | La celda es una lista de contactos en texto libre, no un solo teléfono | Guion ambiguo (separa vs decora); resolver por estructura antes de quitar no-dígitos | Propuesta |
| Ricardo | SUPERVISOR | Ausencia real (561, 4.7%) | Imputar por DISTRITO (un distrito → un supervisor); NA si no hay referencia | Es recuperable desde otra columna del propio dataset | Un distrito pudo cambiar de supervisor a lo largo del tiempo | Propuesta |
| Ricardo | SUPERVISOR | Variantes por tildes/espacios del mismo nombre (192 escrituras) | Fusionar con normalizar_nombre(); confirmar con corte geográfico (DEPARTAMENTAL/DISTRITO) | Un supervisor es una persona real atada a una jurisdicción | Homónimos reales en distinta jurisdicción | Propuesta |
| Ricardo | SUPERVISOR | Contaminación (16): O/0 (ACEVED0), tilde grave (ORTÌZ), apóstrofo tipográfico (O´NELL), coma final | Corregir grafías y quitar puntuación final | Producen cadenas válidas que ningún filtro sintáctico atrapa | Bajo; revisar caso a caso | Propuesta |
| Ricardo | DIRECTOR | Ausencia real 2,174 (18.3%): 1,755 vacías + 360 disfrazadas (---, 000000, X, SIN DATOS) | Convertir los disfrazados a NA (regla "<2 palabras con letra"), luego dejar NA | No es imputable (propio del establecimiento); el conteo de nulos era un piso | Descartar un nombre real de una sola palabra (ninguno observado) | Propuesta |
| Ricardo | DIRECTOR | Variantes por tildes/espacios del mismo nombre (198 escrituras) | Fusionar con normalizar_nombre() | Nombre de persona; misma lógica que SUPERVISOR | Homónimos; nombres truncados (VASQUEZ vs VASQUEZ REYES) | Propuesta |
| Ricardo | DIRECTOR | Título incrustado (18): LIC., PEM. | Separar el título del nombre | La celda es un nombre real, solo decorado | Confundir un título con parte del nombre | Propuesta |
| Nadissa | NIVEL | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Nadissa | SECTOR | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Nadissa | AREA | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Nadissa | STATUS | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Nadissa | MODALIDAD | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Nadissa | JORNADA | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |
| Nadissa | PLAN | Pendiente | Pendiente | Pendiente | Pendiente | Pendiente |

## Aspectos que deben revisarse cuando correspondan

- Valores faltantes, cadenas vacías y marcadores como `N/A`, `NULL`, `-`, `.`, `Sin dato`.
- Tipos de datos.
- Espacios, mayúsculas, tildes, caracteres especiales y puntuación.
- Categorías escritas de distintas maneras.
- Formatos de teléfonos, códigos, direcciones y nombres.
- Valores fuera del dominio permitido.
- Duplicados exactos y parciales.
- Contradicciones entre variables.
- Variables derivadas, únicamente cuando sean necesarias y estén justificadas.

Una variable puede necesitar más de una fila si presenta problemas diferentes.
