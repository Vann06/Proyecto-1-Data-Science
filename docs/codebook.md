# Libro de códigos

**Proyecto:** Obtención y Limpieza de Datos  
**Fuente:** Ministerio de Educación de Guatemala  
**Filtro:** Nivel escolar Diversificado  
**Fecha de extracción:** pendiente de confirmar  
**Versión actual:** 0.1 · datos crudos

Los tres integrantes completan este mismo archivo por turnos. Cada persona actualiza las variables que tiene asignadas.

| Responsable | Variable | Descripción inicial | Tipo esperado | Dominio o formato permitido | Tratamiento aplicado |
|---|---|---|---|---|---|
| Vianka | CODIGO | Código del establecimiento | Texto | Formato oficial de MINEDUC | Pendiente |
| Vianka | DISTRITO | Distrito educativo | Texto | Formato oficial observado | Pendiente |
| Vianka | DEPARTAMENTO | Departamento del establecimiento | Texto | Catálogo oficial de Guatemala | Pendiente |
| Vianka | MUNICIPIO | Municipio del establecimiento | Texto | Catálogo oficial según departamento | Pendiente |
| Vianka | DEPARTAMENTAL | Dirección departamental relacionada | Texto | Catálogo definido por MINEDUC | Pendiente |
| Ricardo | ESTABLECIMIENTO | Nombre del establecimiento | Texto | Nombre normalizado según regla aprobada | Pendiente |
| Ricardo | DIRECCION | Dirección física | Texto | Texto con formato uniforme | Pendiente |
| Ricardo | TELEFONO | Teléfono de contacto | Texto | Formato que apruebe el equipo | Pendiente |
| Ricardo | SUPERVISOR | Nombre del supervisor | Texto | Nombre con formato uniforme | Pendiente |
| Ricardo | DIRECTOR | Nombre del director | Texto | Nombre con formato uniforme | Pendiente |
| Nadissa | NIVEL | Nivel educativo | Texto categórico | DIVERSIFICADO | Pendiente |
| Nadissa | SECTOR | Sector del establecimiento | Texto categórico | Categorías observadas y aprobadas | Pendiente |
| Nadissa | AREA | Área geográfica | Texto categórico | Categorías observadas y aprobadas | Pendiente |
| Nadissa | STATUS | Estado del establecimiento | Texto categórico | Categorías observadas y aprobadas | Pendiente |
| Nadissa | MODALIDAD | Modalidad educativa | Texto categórico | Categorías observadas y aprobadas | Pendiente |
| Nadissa | JORNADA | Jornada de atención | Texto categórico | Categorías observadas y aprobadas | Pendiente |
| Nadissa | PLAN | Plan educativo | Texto categórico | Categorías observadas y aprobadas | Pendiente |

## Columnas técnicas del archivo unificado

| Variable | Descripción | Uso final |
|---|---|---|
| archivo_origen | Nombre del CSV del que salió el registro | Trazabilidad; decidir al final si se conserva |
| fila_origen | Número de fila dentro del archivo original | Trazabilidad; decidir al final si se conserva |

## Historial

| Versión | Fecha | Descripción |
|---|---|---|
| 0.1 | 17 de julio de 2026 | Estructura inicial y descripción preliminar de variables |
