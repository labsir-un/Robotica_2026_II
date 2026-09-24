<div align="center">

# Curso de Robótica 2026-II

## Universidad Nacional de Colombia

**Pedro Fabián Cárdenas Herrera**  
**Manuel Felipe Carranza Montenegro**

</div>

---

# Repositorio general del curso

Este repositorio organiza el material del **Curso de Robótica 2026-II** en tres bloques:

- `Profesor/`: guías y material docente suministrado para el curso.
- `Estudiantes/`: espacio de trabajo de cada grupo de laboratorio.
- `Proyecto_Final/`: espacio de trabajo de los equipos del proyecto final.

La estructura está preparada para que los estudiantes editen directamente su carpeta y documenten cada laboratorio mediante un archivo `README.md`.

## Laboratorios

Cada grupo de laboratorio contiene exactamente estas seis carpetas:

| Laboratorio | Tema |
|---|---|
| Lab 01 | Robótica Industrial ABB IRB140 y RobotStudio |
| Lab 02 | Robótica Industrial Motoman MH6 y RoboDK |
| Lab 03 | Robótica Industrial EPSON T3 401S y EPSON RC+ |
| Lab 04 | Robótica de Desarrollo ROS Lyrical y Turtlesim |
| Lab 05 | Robótica de Desarrollo ROS Lyrical y Phantom Pincher X100 |
| Lab 06 | Robótica de Desarrollo ROS Lyrical y Robot 7DoF |

En cada carpeta se dejó un `README.md` base para que el grupo lo reemplace o complete con su informe.

## Grupos de laboratorio

| Grupo SIA | Grupo | Integrantes |
|---:|:---:|---|
| 1 | [1A](Estudiantes/Grupo_1A/) | Jose Manuel Rodríguez Sandoval<br>Leonardo Acevedo Monroy |
| 1 | [2A](Estudiantes/Grupo_2A/) | David Ruiz<br>Alexandra Garavito |
| 1 | [3A](Estudiantes/Grupo_3A/) | Felipe Vargas<br>Isaac Jordán |
| 1 | [4A](Estudiantes/Grupo_4A/) | Alejandro Zapata<br>Daniel Suarez |
| 1 | [5A](Estudiantes/Grupo_5A/) | Edwin Franco<br>Diego Fernandez |
| 1 | [6A](Estudiantes/Grupo_6A/) | Julieth Manuela Rojas Castro<br>Diego Andrés Barragán Martínez |
| 2 | [1B](Estudiantes/Grupo_1B/) | Alejandro Ramirez Gomez<br>Ronan Anquetin<br>Nirvana Ceron |
| 2 | [2B](Estudiantes/Grupo_2B/) | Daniel Rodriguez<br>Juan David Saldaña Estupiñán<br>Yeison Esteban Ortega |
| 2 | [3B](Estudiantes/Grupo_3B/) | Emmanuel Bonilla Mitrotti<br>Samuel David Negrete Lancheros |
| 2 | [4B](Estudiantes/Grupo_4B/) | Juan Diego Ruiz Trejo |
| 2 | [5B](Estudiantes/Grupo_5B/) | Ariel Cárdenas<br>Kennet Jared Cruz |
| 2 | [6B](Estudiantes/Grupo_6B/) | Yeison Esteban Ortega |
| 2 | [7B](Estudiantes/Grupo_7B/) | Samuel David Osorio Gutierrez<br>Santiago Gómez Camargo |
| 3 | [1C](Estudiantes/Grupo_1C/) | Miguel Angel Martinez Torres<br>Diego José Navarro López |
| 3 | [2C](Estudiantes/Grupo_2C/) | Andrés Felipe Osorio Ortiz<br>Jesus Manuel Aragon Buitrago |
| 3 | [3C](Estudiantes/Grupo_3C/) | Daniel Alejandro Torres Sanabria<br>Janpier Sebastian Zuñiga Ramos |
| 3 | [4C](Estudiantes/Grupo_4C/) | Sharon Michel Lobo Vergara<br>Cristian Esteban Agualimpia Torres<br>Fabian Stiven Abreo |
| 3 | [5C](Estudiantes/Grupo_5C/) | Alejandro Jiménez Zabala |
| 3 | [6C](Estudiantes/Grupo_6C/) | Por asignar |

> El grupo `6C` se conserva aunque actualmente no tiene integrantes registrados.

## Equipos de proyecto final

| Equipo | Robot asignado | Integrantes |
|---:|---|---|
| 1 | [ABB IRB 140 (Caín)](Proyecto_Final/Equipo_01_ABB_IRB140_Cain/) | Daniel Alejandro Torres Sanabria<br>Janpier Sebastian Zuñiga Ramos<br>Sharon Michel Lobo Vergara<br>Fabian Stiven Abreo |
| 2 | [ABB IRB 140 (Abel)](Proyecto_Final/Equipo_02_ABB_IRB140_Abel/) | Jose Manuel Rodríguez Sandoval<br>Leonardo Acevedo Monroy<br>Ariel Cárdenas<br>Kennet Jared Cruz |
| 3 | [Yaskawa Motoman MH6](Proyecto_Final/Equipo_03_Yaskawa_Motoman_MH6/) | Isaac Jordán<br>Felipe Vargas<br>Julieth Rojas<br>Diego Barragán |
| 4 | [Por asignar](Proyecto_Final/Equipo_04_Por_asignar/) | Por asignar |
| 5 | [Por asignar](Proyecto_Final/Equipo_05_Por_asignar/) | Por asignar |
| 6 | [Por asignar](Proyecto_Final/Equipo_06_Por_asignar/) | Por asignar |
| 7 | [Por asignar](Proyecto_Final/Equipo_07_Por_asignar/) | Por asignar |
| 8 | [Por asignar](Proyecto_Final/Equipo_08_Por_asignar/) | Por asignar |

Los equipos 4 a 8 quedan creados como espacios disponibles para asignaciones posteriores.

## Estructura general

```text
Robotica_2026_II/
├── Profesor/
├── Estudiantes/
│   ├── Grupo_1A/
│   ├── Grupo_2A/
│   └── ...
├── Proyecto_Final/
│   ├── Equipo_01_ABB_IRB140_Cain/
│   ├── Equipo_02_ABB_IRB140_Abel/
│   ├── Equipo_03_Yaskawa_Motoman_MH6/
│   └── Equipo_04...Equipo_08/
├── MANIFEST.md
├── manifest.json
├── CONTRIBUTING.md
├── LICENSE
└── README.md
```

## Flujo recomendado de trabajo

1. Actualizar la copia local con `git pull`.
2. Entrar únicamente a la carpeta correspondiente al grupo o equipo.
3. Agregar el informe, imágenes, código y evidencias necesarias.
4. Revisar `git status`.
5. Crear un commit descriptivo.
6. Hacer `git push`.

Ejemplo:

```bash
git pull
git status
git add .
git commit -m "Lab 01 - Informe grupo 1A"
git push
```

## Convención para los informes

Cada laboratorio debe conservar como punto de entrada un archivo:

```text
README.md
```

Los archivos adicionales pueden organizarse dentro de subcarpetas como:

```text
media/
src/
code/
docs/
```

según las necesidades de cada práctica.

---
