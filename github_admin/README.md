<div align="center">

# 🔐 Control de acceso — Robótica 2026-II

**Repositorio:** `labsir-un/Robotica_2026_II`

</div>

## Qué incluye esta versión

Este paquete deja preparado un esquema para que:

- cada **grupo de laboratorio** pueda modificar únicamente los `README.md` de su grupo;
- cada **equipo de proyecto final** pueda modificar únicamente su `README.md`;
- el equipo **Profesores** pueda modificar todos esos README y los archivos administrativos;
- los README generales, `Profesor/`, `docs/`, `.github/` y `github_admin/` queden reservados para profesores.

El bloqueo real se realiza con **GitHub Push Rulesets**. El archivo `.github/CODEOWNERS` se incluye como capa adicional de propiedad/revisión, pero por sí solo no impide un push.

## Antes de aplicar

Edita:

```text
github_admin/access_control.json
```

y reemplaza:

```text
REEMPLAZAR_CON_USUARIO_GITHUB_PEDRO
REEMPLAZAR_CON_USUARIO_GITHUB_MANUEL
```

por los usuarios GitHub reales de los profesores.

También revisa:

```text
github_admin/usuarios_github_pendientes.csv
```

porque algunos estudiantes todavía no tienen usuario GitHub conocido. Hasta que se agregue su usuario, esos estudiantes no podrán recibir acceso automático al Team correspondiente.

## Aplicación

Instala GitHub CLI si todavía no lo tienes y autentícate:

```bash
gh auth login
```

Desde la raíz del repositorio ejecuta primero una validación:

```bash
python3 github_admin/setup_access_control.py
```

Cuando el plan sea correcto:

```bash
python3 github_admin/setup_access_control.py --apply
```

Si conscientemente deseas continuar aunque falten algunos usuarios GitHub:

```bash
python3 github_admin/setup_access_control.py --apply --allow-missing-users
```

## Teams que se crearán

- `profesores`
- `lab-1a`, `lab-2a`, ..., `lab-6c`
- `proyecto-01`, ..., `proyecto-08`

Todos los equipos de estudiantes reciben permiso `push` sobre el repositorio, pero los **Push Rulesets por ruta** bloquean cambios a los README que no les pertenecen.

## Archivos protegidos para profesores

```text
Profesor/**/*
docs/**/*
.github/**/*
github_admin/**/*
README.md
Estudiantes/README.md
Proyecto_Final/README.md
CONTRIBUTING.md
MANIFEST.md
manifest.json
LICENSE
ESTRUCTURA.txt
```

## Importante

Los permisos de carpeta no se activan simplemente por subir este ZIP. Los Teams y Rulesets viven en la configuración del servidor de GitHub, por eso hay que ejecutar el script una sola vez con una cuenta que tenga permisos administrativos.

Si GitHub rechaza la creación de **Push Rulesets**, revisa el plan de la organización y el tipo de repositorio. En ese caso, conserva `CODEOWNERS` y configura una regla de `main` que obligue a usar Pull Requests y revisiones de Code Owners.
