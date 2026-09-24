<div align="center">
<picture>
    <source srcset="https://imgur.com/5bYAzsb.png" media="(prefers-color-scheme: dark)">
    <source srcset="https://imgur.com/Os03JoE.png" media="(prefers-color-scheme: light)">
    <img src="https://imgur.com/Os03JoE.png" alt="Escudo UNAL" width="350px">
</picture>

<h3>Curso de Robótica 2026-II</h3>

<h1>Introducción a ROS 2 Lyrical</h1>

<h2>Guía 02 - Instalación de ROS 2 Lyrical en Ubuntu 26.04</h2>

<h4>Pedro Fabián Cárdenas Herrera<br>
    Manuel Felipe Carranza Montenegro</h4>

<p>
  <img alt="Ubuntu 26.04 LTS" src="https://img.shields.io/badge/Ubuntu-26.04%20LTS-E95420?logo=ubuntu&logoColor=white">
  <img alt="ROS 2 Lyrical" src="https://img.shields.io/badge/ROS%202-Lyrical-22314E?logo=ros&logoColor=white">
  <img alt="Nivel" src="https://img.shields.io/badge/Nivel-Introductorio-2ea44f">
</p>

</div>

<div align="justify">

## Tabla de contenidos

- [Introducción](#introducción)
- [Objetivos](#objetivos)
- [Requisitos previos](#requisitos-previos)
- [Instalación de herramientas previas](#instalación-de-herramientas-previas)
  - [1. Visual Studio Code](#1-visual-studio-code)
  - [2. Terminator](#2-terminator-terminal-recomendado)
- [Instalación de ROS 2 Lyrical](#instalación-de-ros-2-lyrical)
  - [0. Recomendación antes de empezar](#0-recomendación-antes-de-empezar-si-tenías-otra-versión-de-ros)
  - [1. Configuración del Locale (UTF-8)](#1-configuración-del-locale-utf-8)
  - [2. Configurar las fuentes oficiales de ROS 2](#2-configurar-las-fuentes-oficiales-de-ros-2)
  - [3. Instalación de ROS 2 Lyrical](#3-instalación-de-ros-2-lyrical)
- [Configuración del entorno](#configuración-del-entorno)
- [Herramientas de desarrollo recomendadas](#herramientas-de-desarrollo-recomendadas-para-el-curso)
  - [1. rosdep](#1-rosdep-resolver-dependencias)
  - [2. colcon](#2-colcon-compilación-de-workspaces)
- [Probar ROS 2 (talker-listener)](#probar-ros-2-ejemplo-talker-listener)
- [Workspace inicial (opcional)](#opcional-primera-estructura-de-workspace-colcon)
- [Verificación de la instalación](#verificación-de-la-instalación)
- [Solución de problemas comunes](#solución-de-problemas-comunes)
- [Recursos útiles](#recursos-útiles-para-seguir-aprendiendo)
- [Referencias](#referencias)

---

## Introducción

ROS 2 (Robot Operating System 2) es una infraestructura de software modular y abierta diseñada para el desarrollo de aplicaciones robóticas. Esta guía está dirigida a estudiantes y docentes de la Universidad Nacional de Colombia, especialmente aquellos vinculados a cursos de robótica, que deseen configurar un entorno de desarrollo con **ROS 2 Lyrical Luth (LTS)** sobre **Ubuntu 26.04 LTS (Resolute Raccoon)**.

**ROS 2 Lyrical Luth** fue publicado en mayo de 2026 y corresponde a una versión de soporte extendido (LTS), con soporte previsto hasta mayo de 2031. Ubuntu 26.04 es su plataforma Ubuntu principal y cuenta con soporte oficial para arquitecturas **amd64 (x86-64)** y **arm64 (aarch64)**.

En esta guía se detallan paso a paso los comandos necesarios para instalar ROS 2, configurar el entorno, instalar herramientas útiles como Visual Studio Code y Terminator, y realizar una primera prueba utilizando los nodos de ejemplo `talker` y `listener`.

> **Importante:** esta guía utiliza la instalación mediante paquetes Debian (`apt`), que es el método recomendado para una instalación normal de ROS 2 sobre Ubuntu 26.04.

---

## Objetivos

- Proporcionar una guía clara y funcional para instalar **ROS 2 Lyrical** sobre **Ubuntu 26.04 LTS**.
- Asegurar que el entorno de desarrollo esté correctamente configurado para trabajar con ROS 2.
- Introducir herramientas útiles como Terminator y Visual Studio Code para facilitar el desarrollo y la organización del trabajo.
- Verificar la instalación de ROS 2 mediante la ejecución de nodos de ejemplo (`talker` y `listener`).
- Dejar preparado un entorno base para desarrollar y compilar paquetes mediante `colcon`.
- Configurar `rosdep` para resolver automáticamente las dependencias de los paquetes ROS 2.

---

## Requisitos previos

- Tener instalado **Ubuntu 26.04 LTS (Resolute Raccoon)** de 64 bits.
- Arquitectura compatible:
  - `amd64` / `x86_64`.
  - `arm64` / `aarch64`.
- Conexión a internet estable.
- Usuario con permisos `sudo`.
- Recomendado: realizar una instalación nativa o dual boot para los equipos principales del curso.
- Mantener el sistema actualizado antes de instalar ROS 2.

Primero actualiza el sistema:

```bash
sudo apt update
sudo apt upgrade -y
```

Para verificar tu versión de Ubuntu:

```bash
lsb_release -a
```

También puedes utilizar:

```bash
cat /etc/os-release
```

Deberías encontrar una referencia similar a:

```text
Ubuntu 26.04 LTS
Resolute Raccoon
```

---

## Instalación de herramientas previas

### 1. Visual Studio Code

Visual Studio Code es un editor de código moderno y ligero, con extensiones útiles para C++, Python, CMake, Git y ROS 2.

> Este procedimiento instala Visual Studio Code desde el repositorio oficial de Microsoft, permitiendo recibir actualizaciones mediante `apt`.

Instala primero las herramientas necesarias:

```bash
sudo apt update
sudo apt install wget gpg apt-transport-https -y
```

Descarga e instala la llave del repositorio de Microsoft:

```bash
wget -qO- https://packages.microsoft.com/keys/microsoft.asc \
| gpg --dearmor > packages.microsoft.gpg

sudo install -D -o root -g root -m 644 packages.microsoft.gpg \
/usr/share/keyrings/packages.microsoft.gpg
```

Agrega el repositorio de Visual Studio Code:

```bash
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/packages.microsoft.gpg] \
https://packages.microsoft.com/repos/code stable main" \
| sudo tee /etc/apt/sources.list.d/vscode.list > /dev/null
```

Actualiza los repositorios e instala VS Code:

```bash
sudo apt update
sudo apt install code -y
```

Puedes iniciarlo ejecutando:

```bash
code
```

#### Extensiones recomendadas

Dentro de Visual Studio Code se recomienda instalar:

- C/C++.
- Python.
- CMake Tools.
- ROS.
- GitLens (opcional).

---

### 2. Terminator (Terminal recomendado)

Terminator permite dividir una misma ventana de terminal en múltiples paneles. Esto resulta especialmente útil en ROS 2, donde normalmente se ejecutan varios nodos de manera simultánea.

```bash
sudo apt update
sudo apt install terminator -y
```

Para abrirlo:

```bash
terminator
```

---

# Instalación de ROS 2 Lyrical

## 0. Recomendación antes de empezar (si tenías otra versión de ROS)

Si ya tenías instalada otra distribución de ROS 2, por ejemplo Humble, Jazzy o Kilted, evita mezclar entornos dentro de una misma terminal.

Puedes verificar los paquetes ROS instalados mediante:

```bash
dpkg -l | grep '^ii  ros-' | head -n 30
```

También puedes revisar las distribuciones presentes en `/opt/ros`:

```bash
ls /opt/ros/
```

En los equipos utilizados para el curso se recomienda trabajar principalmente con una única distribución de ROS 2 para evitar errores producidos por variables de entorno o dependencias incompatibles.

---

## 1. Configuración del Locale (UTF-8)

ROS 2 requiere un entorno con soporte UTF-8.

Comprueba primero la configuración actual:

```bash
locale
```

Instala y configura el locale si es necesario:

```bash
sudo apt update
sudo apt install locales -y
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8
```

Verifica nuevamente:

```bash
locale
```

Debes observar que `LANG` o `LC_ALL` utilicen una configuración UTF-8.

---

## 2. Configurar las fuentes oficiales de ROS 2

ROS 2 utiliza sus propios repositorios de paquetes. En las versiones actuales, la configuración recomendada se realiza mediante el paquete **`ros2-apt-source`**, que administra automáticamente la llave y la configuración del repositorio oficial.

### 2.1 Habilitar el repositorio Universe

```bash
sudo apt update
sudo apt install software-properties-common -y
sudo add-apt-repository universe
```

---

### 2.2 Instalar el paquete `ros2-apt-source`

Instala `curl`:

```bash
sudo apt update
sudo apt install curl -y
```

Obtén automáticamente la versión más reciente de `ros2-apt-source`:

```bash
export ROS_APT_SOURCE_VERSION=$(curl -s \
https://api.github.com/repos/ros-infrastructure/ros-apt-source/releases/latest \
| grep -F "tag_name" | awk -F'"' '{print $4}')
```

Descarga el paquete correspondiente a tu versión de Ubuntu:

```bash
curl -L -o /tmp/ros2-apt-source.deb \
"https://github.com/ros-infrastructure/ros-apt-source/releases/download/${ROS_APT_SOURCE_VERSION}/ros2-apt-source_${ROS_APT_SOURCE_VERSION}.$(. /etc/os-release && echo ${UBUNTU_CODENAME:-${VERSION_CODENAME}})_all.deb"
```

Instálalo:

```bash
sudo dpkg -i /tmp/ros2-apt-source.deb
```

Actualiza la información de paquetes:

```bash
sudo apt update
```

---

## 3. Instalación de ROS 2 Lyrical

Antes de instalar ROS 2, es recomendable asegurarse de que Ubuntu esté completamente actualizado:

```bash
sudo apt update
sudo apt upgrade -y
```

### Opción A: ROS 2 Desktop — recomendada para el curso

Incluye ROS 2, RViz, herramientas gráficas, demos y paquetes de uso frecuente.

```bash
sudo apt install ros-lyrical-desktop -y
```

Esta es la opción recomendada para los computadores de escritorio y portátiles utilizados durante las prácticas.

---

### Opción B: ROS Base — instalación ligera

Incluye las librerías de comunicación, herramientas de línea de comandos y componentes básicos de ROS 2, pero no instala las principales herramientas gráficas.

```bash
sudo apt install ros-lyrical-ros-base -y
```

Esta opción puede ser útil en:

- Computadores embebidos.
- Servidores.
- Robots sin interfaz gráfica.
- Sistemas con recursos limitados.

---

### Herramientas de desarrollo de ROS 2

Para los estudiantes que desarrollarán paquetes ROS 2 se recomienda instalar también:

```bash
sudo apt install ros-dev-tools -y
```

---

# Configuración del entorno

## 1. Activar ROS 2 en la sesión actual

Después de instalar ROS 2 Lyrical, carga las variables de entorno mediante:

```bash
source /opt/ros/lyrical/setup.bash
```

Comprueba que el comando `ros2` se encuentre disponible:

```bash
ros2 --help
```

---

## 2. Activar ROS 2 automáticamente al abrir una terminal

Para no ejecutar manualmente el comando `source` cada vez que abras una nueva terminal:

```bash
echo "source /opt/ros/lyrical/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

A partir de este momento, ROS 2 Lyrical quedará configurado automáticamente cada vez que abras una terminal Bash.

> Si utilizas `zsh`, agrega la línea correspondiente en `~/.zshrc` en lugar de `~/.bashrc`.

---

## 3. Verificar la distribución ROS activa

```bash
echo $ROS_DISTRO
```

La salida esperada es:

```text
lyrical
```

También puedes revisar:

```bash
env | grep ROS
```

---

# Herramientas de desarrollo recomendadas para el curso

## 1. rosdep (resolver dependencias)

`rosdep` permite identificar e instalar automáticamente dependencias requeridas por los paquetes ROS.

Instálalo si todavía no se encuentra disponible:

```bash
sudo apt install python3-rosdep -y
```

Inicialízalo:

```bash
sudo rosdep init
```

Actualiza su base de datos:

```bash
rosdep update
```

> Si `rosdep` indica que ya fue inicializado, no es necesario repetir `sudo rosdep init`; ejecuta únicamente `rosdep update`.

---

## 2. colcon (compilación de workspaces)

`colcon` es la herramienta utilizada para compilar workspaces de ROS 2.

```bash
sudo apt install python3-colcon-common-extensions python3-argcomplete -y
```

Verifica la instalación:

```bash
colcon --help
```

---

# Probar ROS 2 (Ejemplo talker-listener)

ROS 2 incluye nodos de demostración que permiten comprobar rápidamente que la comunicación entre procesos funciona correctamente.

## Terminal 1 — Talker

Abre una terminal y ejecuta:

```bash
source /opt/ros/lyrical/setup.bash
ros2 run demo_nodes_cpp talker
```

Deberías observar mensajes similares a:

```text
Publishing: 'Hello World: 1'
Publishing: 'Hello World: 2'
Publishing: 'Hello World: 3'
```

---

## Terminal 2 — Listener

Abre una segunda terminal y ejecuta:

```bash
source /opt/ros/lyrical/setup.bash
ros2 run demo_nodes_py listener
```

Deberías observar mensajes similares a:

```text
I heard: [Hello World: 1]
I heard: [Hello World: 2]
I heard: [Hello World: 3]
```

Si el `listener` recibe correctamente los mensajes publicados por el `talker`, la instalación básica de ROS 2 está funcionando.

Detén los nodos con:

```text
Ctrl + C
```

---

# (Opcional) Primera estructura de workspace (colcon)

En ROS 2 se recomienda organizar los paquetes propios dentro de un workspace.

Crea el workspace inicial:

```bash
mkdir -p ~/colcon_ws/src
cd ~/colcon_ws
```

Carga primero ROS 2:

```bash
source /opt/ros/lyrical/setup.bash
```

Compila el workspace:

```bash
colcon build --symlink-install
```

Carga el entorno generado:

```bash
source install/setup.bash
```

La estructura será aproximadamente:

```text
colcon_ws/
├── build/
├── install/
├── log/
└── src/
```

Los paquetes desarrollados por el estudiante deberán ubicarse dentro de:

```text
~/colcon_ws/src/
```

---

## Instalar dependencias de paquetes dentro del workspace

Después de agregar paquetes dentro de `src/`, ejecuta:

```bash
cd ~/colcon_ws
rosdep install --from-paths src --ignore-src -r -y
```

Luego vuelve a compilar:

```bash
colcon build --symlink-install
```

Y carga el workspace:

```bash
source install/setup.bash
```

---

# Verificación de la instalación

Puedes realizar las siguientes comprobaciones rápidas.

### Ver distribución ROS activa

```bash
echo $ROS_DISTRO
```

Salida esperada:

```text
lyrical
```

### Ver versión de Ubuntu

```bash
lsb_release -ds
```

Salida esperada similar a:

```text
Ubuntu 26.04 LTS
```

### Ver paquetes ROS instalados

```bash
apt list --installed 2>/dev/null | grep '^ros-lyrical' | head -n 20
```

### Ver nodos activos

Con el ejemplo `talker-listener` ejecutándose:

```bash
ros2 node list
```

### Ver tópicos disponibles

```bash
ros2 topic list
```

Debería aparecer, entre otros:

```text
/chatter
```

Puedes inspeccionar directamente los mensajes del tópico:

```bash
ros2 topic echo /chatter
```

---

# Solución de problemas comunes

## 1. `ros2: command not found`

Asegúrate de haber cargado el entorno:

```bash
source /opt/ros/lyrical/setup.bash
```

Verifica que Lyrical exista dentro de `/opt/ros`:

```bash
ls /opt/ros/
```

Deberías observar:

```text
lyrical
```

---

## 2. `Unable to locate package ros-lyrical-desktop`

Primero comprueba la versión de Ubuntu:

```bash
cat /etc/os-release
```

Luego verifica que `ros2-apt-source` se encuentre instalado:

```bash
dpkg -l | grep ros2-apt-source
```

Actualiza los repositorios:

```bash
sudo apt update
```

Y verifica si el paquete es visible:

```bash
apt-cache policy ros-lyrical-desktop
```

---

## 3. Error durante `rosdep init`

Si aparece un mensaje indicando que el archivo ya existe, `rosdep` probablemente ya fue inicializado.

Ejecuta únicamente:

```bash
rosdep update
```

---

## 4. `$ROS_DISTRO` muestra otra versión

Comprueba tu archivo `~/.bashrc`:

```bash
nano ~/.bashrc
```

Busca líneas antiguas como:

```bash
source /opt/ros/humble/setup.bash
```

```bash
source /opt/ros/jazzy/setup.bash
```

```bash
source /opt/ros/kilted/setup.bash
```

Si deseas utilizar Lyrical como distribución principal, evita cargar automáticamente varias distribuciones ROS en la misma terminal y deja activa la línea:

```bash
source /opt/ros/lyrical/setup.bash
```

Después ejecuta:

```bash
source ~/.bashrc
```

Y verifica:

```bash
echo $ROS_DISTRO
```

---

## 5. El `talker` funciona pero el `listener` no recibe mensajes

Comprueba que ambos nodos estén activos:

```bash
ros2 node list
```

Comprueba el tópico:

```bash
ros2 topic list
```

Inspecciona la información de `/chatter`:

```bash
ros2 topic info /chatter -v
```

Para las pruebas iniciales utiliza ambos nodos en el mismo computador antes de realizar pruebas entre máquinas diferentes.

---

## 6. Comprobar la arquitectura del equipo

```bash
dpkg --print-architecture
```

Valores esperados:

```text
amd64
```

o:

```text
arm64
```

---

# Recursos útiles para seguir aprendiendo

Una vez terminada la instalación, se recomienda continuar con los tutoriales oficiales de ROS 2 Lyrical, especialmente los temas relacionados con:

- Nodos.
- Tópicos.
- Servicios.
- Acciones.
- Parámetros.
- Interfaces (`msg`, `srv`, `action`).
- Creación de paquetes Python.
- Creación de paquetes C++.
- `colcon`.
- `rosdep`.
- Archivos `launch`.
- TF2.
- URDF.
- RViz.
- Gazebo.

---

# Referencias

1. ROS 2 Lyrical — Documentation:  
   https://docs.ros.org/en/lyrical/

2. ROS 2 Lyrical — Installation:  
   https://docs.ros.org/en/lyrical/Installation.html

3. ROS 2 Lyrical — Ubuntu installation using Debian packages:  
   https://docs.ros.org/en/lyrical/Installation/Ubuntu-Install-Debs.html

4. ROS 2 Lyrical — Ubuntu binary installation and system requirements:  
   https://docs.ros.org/en/lyrical/Installation/Alternatives/Ubuntu-Install-Binary.html

5. ROS 2 — Lyrical Luth Release:  
   https://docs.ros.org/en/rolling/Releases/Release-Lyrical-Luth.html

6. ROS 2 — Release schedule:  
   https://docs.ros.org/en/rolling/The-ROS2-Project/Release-Schedule.html

7. Ubuntu 26.04 LTS — Resolute Raccoon:  
   https://ubuntu.com/

8. ROS apt source repository:  
   https://github.com/ros-infrastructure/ros-apt-source

9. Visual Studio Code — Linux installation:  
   https://code.visualstudio.com/docs/setup/linux

10. ROS 2 Tutorials:  
    https://docs.ros.org/en/lyrical/Tutorials.html

---

<div align="center">

### Universidad Nacional de Colombia
### Curso de Robótica

**ROS 2 Lyrical Luth + Ubuntu 26.04 LTS**

</div>

</div>
