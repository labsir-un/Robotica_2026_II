<div align="center">
<picture>
    <source srcset="https://imgur.com/5bYAzsb.png" media="(prefers-color-scheme: dark)">
    <source srcset="https://imgur.com/Os03JoE.png" media="(prefers-color-scheme: light)">
    <img src="https://imgur.com/Os03JoE.png" alt="Escudo UNAL" width="350px">
</picture>

<h3>Curso de Robótica 2026-II</h3>

<h1>Manipulador de 7 GDL con 9 Servomotores DYNAMIXEL</h1>

<h2>Guía 07 - Control Articular, RViz2, DYNAMIXEL e Intel RealSense D435 con ROS 2 Lyrical</h2>

<h4>Pedro Fabián Cárdenas Herrera<br>
    Manuel Felipe Carranza Montenegro</h4>

<p>
  <img alt="Ubuntu 26.04 LTS" src="https://img.shields.io/badge/Ubuntu-26.04%20LTS-E95420?logo=ubuntu&logoColor=white">
  <img alt="ROS 2 Lyrical" src="https://img.shields.io/badge/ROS%202-Lyrical-22314E?logo=ros&logoColor=white">
  <img alt="DYNAMIXEL Protocol" src="https://img.shields.io/badge/DYNAMIXEL-Protocol%201.0-00979D">
  <img alt="Baudrate" src="https://img.shields.io/badge/Baudrate-1%20Mbps-2ea44f">
  <img alt="Motores" src="https://img.shields.io/badge/Motores-9-f39c12">
  <img alt="Articulaciones" src="https://img.shields.io/badge/Controles%20lógicos-8-0969da">
  <img alt="RealSense" src="https://img.shields.io/badge/Intel%20RealSense-D435-0071C5">
  <img alt="Percepción" src="https://img.shields.io/badge/RGB%20%2B%20Depth%20%2B%20PointCloud-RViz2-6f42c1">
</p>
</div>

<div align="justify">

## Tabla de contenidos

- [1. Propósito de la guía](#1-propósito-de-la-guía)
- [2. Configuración real del manipulador](#2-configuración-real-del-manipulador)
- [3. Relación entre motores físicos y articulaciones lógicas](#3-relación-entre-motores-físicos-y-articulaciones-lógicas)
- [4. Funcionamiento especial de `joint2`](#4-funcionamiento-especial-de-joint2)
- [5. Arquitectura del sistema](#5-arquitectura-del-sistema)
- [6. Tópicos y servicios](#6-tópicos-y-servicios)
- [7. Registros DYNAMIXEL utilizados](#7-registros-dynamixel-utilizados)
- [8. Advertencias de seguridad](#8-advertencias-de-seguridad)
- [9. Requisitos](#9-requisitos)
- [10. Instalación de ROS 2 Lyrical y dependencias](#10-instalación-de-ros-2-lyrical-y-dependencias)
- [11. Preparación del puerto serie](#11-preparación-del-puerto-serie)
- [12. Creación del workspace y del paquete](#12-creación-del-workspace-y-del-paquete)
- [13. Estructura completa del repositorio](#13-estructura-completa-del-repositorio)
- [14. Código completo del repositorio](#14-código-completo-del-repositorio)
- [15. Compilación del workspace](#15-compilación-del-workspace)
- [16. Práctica 1: validación completa sin hardware](#16-práctica-1-validación-completa-sin-hardware)
- [17. Práctica 2: uso de la interfaz gráfica](#17-práctica-2-uso-de-la-interfaz-gráfica)
- [18. Práctica 3: verificar el comportamiento de `joint2`](#18-práctica-3-verificar-el-comportamiento-de-joint2)
- [19. Práctica 4: inspección de ROS 2](#19-práctica-4-inspección-de-ros-2)
- [20. Práctica 5: detectar el puerto e IDs DYNAMIXEL](#20-práctica-5-detectar-el-puerto-e-ids-dynamixel)
- [21. Práctica 6: primera conexión con el robot real](#21-práctica-6-primera-conexión-con-el-robot-real)
- [22. Práctica 7: movimiento individual de articulaciones](#22-práctica-7-movimiento-individual-de-articulaciones)
- [23. Práctica 8: HOME, velocidad, torque y parada](#23-práctica-8-home-velocidad-torque-y-parada)
- [24. Práctica 9: trayectoria automática](#24-práctica-9-trayectoria-automática)
- [25. Calibración del manipulador](#25-calibración-del-manipulador)
- [26. Diagnóstico y verificación](#26-diagnóstico-y-verificación)
- [27. Solución de problemas](#27-solución-de-problemas)
- [28. Actividad propuesta para estudiantes](#28-actividad-propuesta-para-estudiantes)
- [29. Publicación en GitHub](#29-publicación-en-github)
- [30. Cambios respecto a la versión Jazzy](#30-cambios-respecto-a-la-versión-jazzy)
- [31. Visualización sincronizada en RViz2](#31-visualización-sincronizada-en-rviz2)
- [32. Paquete `arm7_description`](#32-paquete-arm7_description)
- [33. Ejecución: GUI + robot físico + RViz2](#33-ejecución-gui--robot-físico--rviz2)
- [34. Ajuste y validación del modelo en RViz](#34-ajuste-y-validación-del-modelo-en-rviz)
- [35. Integración de la Intel RealSense D435](#35-integración-de-la-intel-realsense-d435)
- [36. Instalación y prueba independiente de la D435](#36-instalación-y-prueba-independiente-de-la-d435)
- [37. TF entre la D435 y el robot](#37-tf-entre-la-d435-y-el-robot)
- [38. Ejecución del sistema completo con cámara](#38-ejecución-del-sistema-completo-con-cámara)
- [39. Diagnóstico de la RealSense en ROS 2 y RViz2](#39-diagnóstico-de-la-realsense-en-ros-2-y-rviz2)
- [40. Actividad de percepción propuesta](#40-actividad-de-percepción-propuesta)
- [41. Bibliografía](#41-bibliografía)

---

# 1. Propósito de la guía

Esta guía desarrolla un proyecto completo para controlar un manipulador robótico de **7 grados de libertad más gripper**, accionado por **9 servomotores DYNAMIXEL**, utilizando **Ubuntu 26.04 LTS**, **ROS 2 Lyrical Luth**, Python y DynamixelSDK.

El sistema está compuesto por:

- 3 motores **MX-64**;
- 3 motores **MX-28**;
- 3 motores **AX-12A**;
- todos configurados con **DYNAMIXEL Protocol 1.0**;
- todos configurados a **1,000,000 baud**;
- 9 actuadores físicos;
- 8 articulaciones lógicas expuestas al usuario.

El motivo por el cual existen nueve motores pero solamente ocho controles lógicos es que los motores **ID 2 e ID 3** accionan conjuntamente la misma articulación, denominada `joint2`.

El repositorio incluye:

- controlador ROS 2;
- perfiles de motores;
- lectura de posiciones;
- `GroupSyncWrite`;
- GUI con Tkinter;
- escáner de IDs;
- configuración YAML;
- servicios HOME, torque y parada de software;
- modo sin hardware;
- publicación de `/joint_states`;
- publicación de posiciones RAW;
- supervisión del sincronismo entre los motores 2 y 3;
- trayectoria automática didáctica;
- visualización del manipulador sincronizada en RViz2;
- integración de una **Intel RealSense D435**;
- visualización de imagen RGB, profundidad alineada y nube de puntos `PointCloud2` en RViz2;
- conexión TF entre la cámara y el árbol cinemático del robot.

> **Ruta de trabajo utilizada durante toda la guía:** `~/ros2_lyrical/7dof_ws`.

> **Regla de seguridad:** la primera prueba debe realizarse obligatoriamente con `use_hardware:=false`.

> **Nota RealSense (ruta validada en este proyecto, 2026-09):** para evitar depender de la disponibilidad de paquetes APT de terceros, la D435 se instala con `librealsense` desde fuente y `realsense-ros` dentro del mismo workspace. Esta es la ruta que se validó con `librealsense 2.58.3` y el wrapper ROS que reportó `RealSense ROS v4.58.4`.

> **Nota sobre máquinas virtuales:** el nombre del host (por ejemplo `ubuntu-24-04@...`) no demuestra qué versión de Ubuntu está instalada. La versión real se verifica siempre con `/etc/os-release`. En Parallels, la D435 debe entregarse como USB directo al invitado; si `lsusb` muestra `203a:fff9 PARALLELS ...`, todavía está virtualizada. El objetivo es que aparezca como `8086:0b07 Intel Corp. RealSense D435`.


---

# 2. Configuración real del manipulador

La distribución de motores confirmada para este robot es:

| ID | Modelo | Protocolo | Baudrate | Función |
|---:|---|---:|---:|---|
| 1 | MX-64 | 1.0 | 1,000,000 | `joint1` |
| 2 | MX-64 | 1.0 | 1,000,000 | `joint2` |
| 3 | MX-64 | 1.0 | 1,000,000 | `joint2` |
| 4 | MX-28 | 1.0 | 1,000,000 | `joint3` |
| 5 | MX-28 | 1.0 | 1,000,000 | `joint4` |
| 6 | MX-28 | 1.0 | 1,000,000 | `joint5` |
| 7 | AX-12A | 1.0 | 1,000,000 | `joint6` |
| 8 | AX-12A | 1.0 | 1,000,000 | `joint7` |
| 9 | AX-12A | 1.0 | 1,000,000 | `gripper` |

Los motores 2 y 3 pertenecen al mismo eslabón y están instalados físicamente en sentidos opuestos.

---

# 3. Relación entre motores físicos y articulaciones lógicas

ROS 2 trabaja con las siguientes articulaciones:

```text
joint1
joint2
joint3
joint4
joint5
joint6
joint7
gripper
```

Esto significa:

```text
9 motores físicos
       ↓
8 articulaciones lógicas
```

El mapeo interno es:

```text
ID 1  MX-64  ────────────── joint1

ID 2  MX-64  ──┐
                ├────────── joint2
ID 3  MX-64  ──┘

ID 4  MX-28  ────────────── joint3
ID 5  MX-28  ────────────── joint4
ID 6  MX-28  ────────────── joint5

ID 7  AX-12A ────────────── joint6
ID 8  AX-12A ────────────── joint7
ID 9  AX-12A ────────────── gripper
```

Por tanto, `/joint_states` publica **8 posiciones**.

El tópico adicional:

```text
/arm7/motor_positions_raw
```

publica **9 posiciones RAW**, una por motor físico.

---

# 4. Funcionamiento especial de `joint2`

`joint2` está accionada por dos MX-64.

Los motores están montados en sentidos opuestos, por lo que para desplazar el eslabón hacia un mismo lado deben girar en sentidos eléctricos/matemáticos opuestos.

La regla implementada es:

```text
joint2 = +θ

ID 2 -> +θ
ID 3 -> -θ
```

y:

```text
joint2 = -θ

ID 2 -> -θ
ID 3 -> +θ
```

En la configuración:

```yaml
motor_signs:
  [1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
```

el signo correspondiente al ID 3 es `-1.0`.

## 4.1 La GUI usa un único slider

El usuario nunca controla los motores 2 y 3 por separado.

La GUI presenta:

```text
joint2
```

una sola vez.

Cuando se libera el slider, el controlador recibe un único ángulo lógico y calcula automáticamente las dos posiciones físicas.

## 4.2 Escritura simultánea

Los tres modelos del robot utilizan `Goal Position` en:

```text
Address = 30
Length  = 2 bytes
```

por ello se utiliza `GroupSyncWrite`.

El controlador calcula primero las nueve posiciones y las envía en el mismo paquete.

Conceptualmente:

```text
JointState lógico
       │
       ▼
conversión a 9 objetivos RAW
       │
       ▼
GroupSyncWrite
       │
       ├── ID 1
       ├── ID 2 = +θ
       ├── ID 3 = -θ
       ├── ID 4
       ├── ID 5
       ├── ID 6
       ├── ID 7
       ├── ID 8
       └── ID 9
```

## 4.3 Lectura de `joint2`

Cuando se leen los motores:

```text
ID2 RAW ──> ángulo lógico ──┐
                            ├── promedio ──> joint2
ID3 RAW ──> invertir signo ─┘
```

El controlador verifica además que ambos valores sean coherentes.

Por defecto:

```yaml
joint2_sync_tolerance_deg: 5.0
```

Si la diferencia supera este valor, se genera una advertencia de desacople.

---



## HOME real actual del manipulador

La configuración HOME utilizada actualmente por el controlador es:

| ID | Modelo | Articulación | HOME RAW |
|---:|---|---|---:|
| 1 | MX-64 | `joint1` | **1485** |
| 2 | MX-64 | `joint2` | **1947** |
| 3 | MX-64 | `joint2` | **2000** |
| 4 | MX-28 | `joint3` | **1060** |
| 5 | MX-28 | `joint4` | **2568** |
| 6 | MX-28 | `joint5` | **3581** |
| 7 | AX-12A | `joint6` | **151** |
| 8 | AX-12A | `joint7` | **1023** |
| 9 | AX-12A | `gripper` | **1021** |

La configuración es:

```yaml
motor_centers: [1485, 1947, 2000, 1060, 2568, 3581, 151, 1023, 1021]
home_raw:      [1485, 1947, 2000, 1060, 2568, 3581, 151, 1023, 1021]
```

Como `motor_centers` y `home_raw` son iguales:

```text
HOME físico del robot = 0° lógico en la GUI
```

Esto permite que la posición visualizada en RViz también use HOME como referencia angular cero.

> **Importante:** los AX-12A tienen un rango RAW válido de `0...1023`. El valor del ID8 es **1023**. No debe configurarse como 1200.

### Guardia de HOME actual

La configuración utilizada es:

```yaml
home_max_delta_deg: 175.0
```

Este valor es deliberadamente amplio y **no representa una garantía de trayectoria libre de colisiones**. La protección solamente impide un HOME cuando la diferencia angular respecto a la referencia supera ese umbral.

### Rangos actuales de la GUI

```yaml
gui_min_deg: [-90.0, -90.0, -90.0, -90.0, -90.0, -90.0, -90.0, -90.0]
gui_max_deg: [ 90.0,  90.0,  90.0,  90.0,  90.0,  90.0,  90.0,  90.0]
```

Estos son los rangos configurados actualmente en la interfaz. Antes de recorrer todo el rango de una articulación con hardware real, se debe validar que el recorrido sea mecánicamente seguro.

### Protecciones alrededor de HOME y Torque ON

La implementación conserva las siguientes protecciones:

1. **Un slider solo mueve su articulación física asociada.**
2. **`joint2` mueve simultáneamente los MX-64 ID2 e ID3**, aplicando signos opuestos.
3. **Antes de Torque ON se alinea `Goal Position` con `Present Position`**, reduciendo el riesgo de un salto hacia un objetivo antiguo.
4. **HOME se valida antes de enviar la postura a los nueve motores.**

### Capturar nuevamente HOME

Con el robot colocado manualmente en una nueva postura HOME y el torque deshabilitado:

```bash
ros2 run arm7_control capture_home --ros-args \
  -p port:=/dev/ttyUSB0 \
  -p baudrate:=1000000
```

Los nueve valores obtenidos deben copiarse tanto a `motor_centers` como a `home_raw` si se desea conservar la convención:

```text
HOME físico = 0° lógico
```


# 5. Arquitectura del sistema

```text
                       ┌──────────────────┐
                       │     arm7_gui     │
                       └────────┬─────────┘
                                │
                                │ /arm7/command
                                ▼
                     ┌─────────────────────┐
                     │   arm7_controller   │
                     └──────────┬──────────┘
                                │
                        conversión lógica
                                │
                    8 joints -> 9 motores
                                │
                                ▼
                     ┌─────────────────────┐
                     │   GroupSyncWrite    │
                     │   Goal Position     │
                     └──────────┬──────────┘
                                │
                ┌───────────────┼────────────────┐
                ▼               ▼                ▼
              ID 1            ID 2/3           ID 4..9
              MX64             MX64             MX/AX
                                │
                                ▼
                             joint2

Lectura:
ID 1..9 -> Present Position -> conversión -> /joint_states
```

La integración de percepción añade una segunda cadena:

```text
Intel RealSense D435
        │
        ├── RGB ------------------------> /camera/camera/color/image_raw
        ├── Depth alineado -------------> /camera/camera/aligned_depth_to_color/image_raw
        ├── PointCloud2 ----------------> /camera/camera/depth/color/points
        └── TF internos ----------------> camera_link -> frames ópticos
                                           │
                                           │ TF extrínseco medido
                                           ▼
                                      world / link del robot
                                           │
                                           ▼
                                          RViz2
```

El objetivo es que el robot, la cámara y la nube de puntos pertenezcan a **un único árbol TF**. La posición física de la D435 respecto al robot se configura mediante parámetros del launch y no se fija arbitrariamente en el URDF.

---

# 6. Tópicos y servicios

## Tópicos

### `/arm7/command`

Tipo:

```text
sensor_msgs/msg/JointState
```

Transporta objetivos articulares lógicos.

### `/joint_states`

Tipo:

```text
sensor_msgs/msg/JointState
```

Publica las 8 posiciones articulares lógicas.

### `/arm7/motor_positions_raw`

Tipo:

```text
std_msgs/msg/Int32MultiArray
```

Publica las 9 posiciones RAW en orden:

```text
[ID1, ID2, ID3, ID4, ID5, ID6, ID7, ID8, ID9]
```

### `/arm7/profile_velocity`

Tipo:

```text
std_msgs/msg/UInt32
```

Permite cambiar `Moving Speed` en los nueve motores.

### `/arm7/status`

Tipo:

```text
std_msgs/msg/String
```

Publica mensajes de estado del controlador.

## Tópicos de la Intel RealSense D435

Con `camera_namespace:=camera` y `camera_name:=camera`, la integración utiliza:

| Tópico | Tipo | Uso en RViz2 |
|---|---|---|
| `/camera/camera/color/image_raw` | `sensor_msgs/msg/Image` | Imagen RGB |
| `/camera/camera/color/camera_info` | `sensor_msgs/msg/CameraInfo` | Calibración intrínseca RGB |
| `/camera/camera/depth/image_rect_raw` | `sensor_msgs/msg/Image` | Profundidad nativa |
| `/camera/camera/aligned_depth_to_color/image_raw` | `sensor_msgs/msg/Image` | Profundidad alineada con RGB |
| `/camera/camera/depth/color/points` | `sensor_msgs/msg/PointCloud2` | Nube de puntos 3D coloreada |
| `/camera/camera/extrinsics/depth_to_color` | `realsense2_camera_msgs/msg/Extrinsics` | Extrínsecos internos depth↔RGB |
| `/tf_static` | `tf2_msgs/msg/TFMessage` | Frames internos de la cámara |

> La **D435** no incorpora IMU. No se deben activar `enable_gyro` ni `enable_accel` como si se tratara de una D435i.

## Servicios

```text
/arm7/home
/arm7/torque_enable
/arm7/software_stop
```

---

# 7. Registros DYNAMIXEL utilizados

Los tres modelos empleados en este robot trabajan con Protocol 1.0.

| Registro | Dirección | Longitud |
|---|---:|---:|
| Torque Enable | 24 | 1 byte |
| Goal Position | 30 | 2 bytes |
| Moving Speed | 32 | 2 bytes |
| Torque Limit | 34 | 2 bytes |
| Present Position | 36 | 2 bytes |

## MX-64 y MX-28

Para esta implementación:

```text
raw_min    = 0
raw_center = 2048
raw_max    = 4095
rango      ≈ 360°
```

## AX-12A

```text
raw_min    = 0
raw_center = 512
raw_max    = 1023
rango      ≈ 300°
```

> Los centros anteriores son referencias iniciales. Los centros reales del manipulador deben determinarse durante la calibración.

---

# 8. Advertencias de seguridad

> **La parada incluida en el software no sustituye un paro de emergencia físico, cableado y adecuado para el robot.**

Antes de conectar el hardware:

- fija la base del robot;
- despeja el volumen de trabajo;
- mantén disponible un corte físico de alimentación;
- comprueba la alimentación de los actuadores;
- verifica los nueve IDs;
- verifica que todos usen Protocol 1.0;
- verifica 1 Mbps;
- comprueba el sentido de cada articulación;
- calibra los centros;
- inicia con velocidades pequeñas;
- mantén `home_on_startup: false`;
- prueba primero `joint2` sin hardware;
- no ejecutes la trayectoria automática inicialmente.

### Moving Speed

En Protocol 1.0:

```text
Moving Speed = 0
```

puede representar velocidad máxima en Joint Mode.

Por seguridad, esta guía utiliza inicialmente:

```text
30
```

y evita enviar cero.

---

# 9. Requisitos

## 9.1 Software

- Ubuntu 26.04 LTS.
- ROS 2 Lyrical.
- Python 3 del sistema.
- `colcon`.
- `rosdep`.
- DynamixelSDK.
- Tkinter.
- Git.

## 9.2 Hardware

- 3 × MX-64.
- 3 × MX-28.
- 3 × AX-12A.
- interfaz DYNAMIXEL compatible;
- fuente apropiada;
- cableado del bus;
- **Intel RealSense D435**;
- cable USB 3.x de buena calidad para la D435;
- computador con puertos USB suficientes.

Para RGB + depth + nube de puntos se recomienda conectar la D435 a un puerto **USB 3.x**, evitando hubs pasivos cuando sea posible.

---

# 10. Instalación de ROS 2 Lyrical y dependencias

Esta guía supone que ROS 2 Lyrical ya se encuentra instalado.

Verifica Ubuntu:

```bash
lsb_release -a
```

Carga ROS:

```bash
source /opt/ros/lyrical/setup.bash
```

Verifica:

```bash
echo $ROS_DISTRO
```

Salida:

```text
lyrical
```

Instala primero las herramientas generales del manipulador **sin incluir todavía RealSense**. Esto evita que un problema del repositorio de la cámara bloquee la instalación completa:

```bash
sudo apt update

sudo apt install -y \
  git \
  curl \
  software-properties-common \
  python3-colcon-common-extensions \
  python3-rosdep \
  python3-serial \
  python3-tk \
  ros-lyrical-dynamixel-sdk \
  ros-lyrical-xacro \
  ros-lyrical-robot-state-publisher \
  ros-lyrical-rviz2 \
  ros-lyrical-tf2-tools \
  ros-lyrical-tf2-ros
```

Comprueba DynamixelSDK:

```bash
python3 -c "import dynamixel_sdk; print('DynamixelSDK disponible')"
```

Comprueba Tkinter:

```bash
python3 -c "import tkinter; print('Tkinter disponible')"
```

> **RealSense D435:** en este proyecto no se toma `sudo apt install ros-lyrical-realsense2-camera` como ruta principal, porque en el entorno validado APT respondió `Unable to locate package`. La instalación reproducible usada aquí está documentada en la sección 36: `librealsense 2.58.3` desde fuente + `realsense-ros` dentro de `~/ros2_lyrical/7dof_ws/src`.

Si `rosdep` nunca ha sido inicializado:

```bash
sudo rosdep init
```

Después:

```bash
rosdep update
```

Si ya fue inicializado:

```bash
rosdep update
```

---

# 11. Preparación del puerto serie

Conecta el adaptador.

Busca los dispositivos:

```bash
ls /dev/ttyUSB* 2>/dev/null
ls /dev/ttyACM* 2>/dev/null
```

Consulta el kernel:

```bash
sudo dmesg | tail -n 30
```

Añade el usuario al grupo:

```bash
sudo usermod -aG dialout $USER
```

Después cierra sesión y vuelve a ingresar.

Comprueba:

```bash
groups
```

Debe aparecer:

```text
dialout
```

Si el puerto es `/dev/ttyUSB0`:

```bash
ls -l /dev/ttyUSB0
```

> En una máquina virtual también debe asignarse el adaptador USB a Ubuntu y no al sistema anfitrión.

---

# 12. Creación del workspace y del paquete

## 12.1 Crear workspace

```bash
source /opt/ros/lyrical/setup.bash

mkdir -p ~/ros2_lyrical/7dof_ws/src
cd ~/ros2_lyrical/7dof_ws/src
```

## 12.2 Crear paquete

```bash
ros2 pkg create arm7_control \
  --build-type ament_python \
  --dependencies rclpy sensor_msgs std_msgs std_srvs dynamixel_sdk
```

## 12.3 Crear carpetas

```bash
cd ~/ros2_lyrical/7dof_ws/src/arm7_control

mkdir -p config
mkdir -p launch
```

Crea los archivos:

```bash
touch arm7_control/dynamixel_profiles.py
touch arm7_control/arm7_controller.py
touch arm7_control/arm7_gui.py
touch arm7_control/scan_dynamixel.py
touch arm7_control/trajectory_demo.py

touch config/mixed_arm.yaml
touch launch/arm7_system.launch.py
```

Para dejar la estructura igual a este repositorio puedes eliminar las pruebas generadas automáticamente:

```bash
rm -rf test
```

Si aparece `arm7_control/py.typed` y no deseas utilizarlo:

```bash
rm -f arm7_control/py.typed
```

---

# 13. Estructura completa del repositorio

```text
07_Rob_2026_II_ROS2_Lyrical_7DoF_Dynamixel/
├── README.md
├── LICENSE
├── .gitignore
└── ros2_lyrical/
    └── 7dof_ws/
        └── src/
            └── arm7_control/
                ├── package.xml
                ├── setup.py
                ├── setup.cfg
                ├── resource/
                │   └── arm7_control
                ├── config/
                │   └── mixed_arm.yaml
                ├── launch/
                │   └── arm7_system.launch.py
                └── arm7_control/
                    ├── __init__.py
                    ├── dynamixel_profiles.py
                    ├── arm7_controller.py
                    ├── arm7_gui.py
                    ├── scan_dynamixel.py
                    ├── capture_home.py
                    └── trajectory_demo.py
```

Después de añadir RViz2 y la D435, la estructura integrada queda conceptualmente:

```text
~/ros2_lyrical/7dof_ws/src/
├── arm7_control/
├── arm7_description/
├── realsense-ros/
│   ├── realsense2_camera/
│   ├── realsense2_camera_msgs/
│   └── realsense2_description/
└── diagnostics/
    └── diagnostic_updater/
```

`diagnostic_updater` se mantiene en `src` porque fue una dependencia necesaria del wrapper RealSense en la combinación utilizada. La sección 36 muestra cómo traer solamente ese paquete mediante `git sparse-checkout`, evitando compilar componentes de `diagnostics` que no necesita la cámara.

---

# 14. Código completo del repositorio


## 14.1 `.gitignore`

Ruta:

```text
.gitignore
```

```gitignore
build/
install/
log/
__pycache__/
*.pyc
.DS_Store
.vscode/
```


## 14.2 `LICENSE`

Ruta:

```text
LICENSE
```

```text
BSD 3-Clause License

Copyright (c) 2026, Curso de Robótica - Universidad Nacional de Colombia
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.
3. Neither the name of the copyright holder nor the names of its contributors
   may be used to endorse or promote products derived from this software without
   specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES ARE DISCLAIMED.
```


## 14.3 `package.xml`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_control/package.xml
```

```xml
<?xml version="1.0"?>
<package format="3">
  <name>arm7_control</name>
  <version>0.2.0</version>
  <description>Control de manipulador 7 GDL + gripper con 9 DYNAMIXEL Protocol 1.0 en ROS 2 Lyrical.</description>
  <maintainer email="pendiente@ejemplo.invalid">Curso de Robótica 2026-II</maintainer>
  <license>BSD-3-Clause</license>

  <exec_depend>rclpy</exec_depend>
  <exec_depend>sensor_msgs</exec_depend>
  <exec_depend>std_msgs</exec_depend>
  <exec_depend>std_srvs</exec_depend>
  <exec_depend>dynamixel_sdk</exec_depend>
  <exec_depend>launch</exec_depend>
  <exec_depend>launch_ros</exec_depend>
  <exec_depend>ament_index_python</exec_depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```


## 14.4 `setup.py`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_control/setup.py
```

```python
from glob import glob
import os

from setuptools import find_packages, setup

package_name = 'arm7_control'

setup(
    name=package_name,
    version='0.2.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Curso de Robótica 2026-II',
    maintainer_email='pendiente@ejemplo.invalid',
    description='Control de 7 GDL + gripper con 9 DYNAMIXEL Protocol 1.0.',
    license='BSD-3-Clause',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'arm7_controller = arm7_control.arm7_controller:main',
            'arm7_gui = arm7_control.arm7_gui:main',
            'scan_dynamixel = arm7_control.scan_dynamixel:main',
            'capture_home = arm7_control.capture_home:main',
            'trajectory_demo = arm7_control.trajectory_demo:main',
        ],
    },
)
```


## 14.5 `setup.cfg`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_control/setup.cfg
```

```ini
[develop]
script_dir=$base/lib/arm7_control

[install]
install_scripts=$base/lib/arm7_control
```


## 14.6 `resource/arm7_control`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_control/resource/arm7_control
```

```text

```


## 14.7 `__init__.py`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_control/arm7_control/__init__.py
```

```python
"""Control de manipulador de 7 GDL + gripper con 9 DYNAMIXEL Protocol 1.0."""
```


## 14.8 `dynamixel_profiles.py`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_control/arm7_control/dynamixel_profiles.py
```

```python
"""Perfiles de los tres modelos DYNAMIXEL usados por el manipulador.

Todos los motores de este proyecto usan Protocol 1.0 y comparten:
- Torque Enable: 24 (1 byte)
- Goal Position: 30 (2 bytes)
- Moving Speed: 32 (2 bytes)
- Torque Limit: 34 (2 bytes)
- Present Position: 36 (2 bytes)
"""

from dataclasses import dataclass
import math


@dataclass(frozen=True)
class MotorProfile:
    name: str
    protocol_version: float
    raw_min: int
    raw_center: int
    raw_max: int
    mechanical_range_rad: float
    torque_enable_addr: int = 24
    goal_position_addr: int = 30
    goal_position_size: int = 2
    speed_addr: int = 32
    speed_size: int = 2
    torque_limit_addr: int = 34
    torque_limit_size: int = 2
    present_position_addr: int = 36
    present_position_size: int = 2

    @property
    def units_per_rad(self) -> float:
        return (self.raw_max - self.raw_min) / self.mechanical_range_rad

    def clamp_raw(self, value: int) -> int:
        return max(self.raw_min, min(self.raw_max, int(value)))

    def raw_to_motor_radians(self, raw_value: int, center_raw: int | None = None) -> float:
        center = self.raw_center if center_raw is None else int(center_raw)
        return (self.clamp_raw(raw_value) - center) / self.units_per_rad

    def motor_radians_to_raw(self, radians: float, center_raw: int | None = None) -> int:
        center = self.raw_center if center_raw is None else int(center_raw)
        return self.clamp_raw(round(center + float(radians) * self.units_per_rad))


MOTOR_PROFILES = {
    'mx64': MotorProfile(
        name='MX-64 Protocol 1.0',
        protocol_version=1.0,
        raw_min=0,
        raw_center=2048,
        raw_max=4095,
        mechanical_range_rad=2.0 * math.pi,
    ),
    'mx28': MotorProfile(
        name='MX-28 Protocol 1.0',
        protocol_version=1.0,
        raw_min=0,
        raw_center=2048,
        raw_max=4095,
        mechanical_range_rad=2.0 * math.pi,
    ),
    'ax12a': MotorProfile(
        name='AX-12A Protocol 1.0',
        protocol_version=1.0,
        raw_min=0,
        raw_center=512,
        raw_max=1023,
        mechanical_range_rad=math.radians(300.0),
    ),
}


def get_motor_profile(model: str) -> MotorProfile:
    key = str(model).strip().lower().replace('-', '').replace('_', '')
    aliases = {
        'mx64': 'mx64',
        'mx64t': 'mx64',
        'mx64at': 'mx64',
        'mx28': 'mx28',
        'mx28t': 'mx28',
        'mx28at': 'mx28',
        'ax12': 'ax12a',
        'ax12a': 'ax12a',
    }
    canonical = aliases.get(key)
    if canonical is None:
        raise ValueError(
            f'Modelo DYNAMIXEL no soportado: {model}. '
            f'Opciones: {", ".join(sorted(MOTOR_PROFILES))}'
        )
    return MOTOR_PROFILES[canonical]
```


## 14.9 `arm7_controller.py`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_control/arm7_control/arm7_controller.py
```

```python
#!/usr/bin/env python3
"""Controlador ROS 2 para 9 DYNAMIXEL / 8 articulaciones lógicas.

Distribución física:
ID 1  MX-64  -> joint1
ID 2  MX-64  -> joint2, signo +1
ID 3  MX-64  -> joint2, signo -1 (montaje opuesto)
ID 4  MX-28  -> joint3
ID 5  MX-28  -> joint4
ID 6  MX-28  -> joint5
ID 7  AX-12A -> joint6
ID 8  AX-12A -> joint7
ID 9  AX-12A -> gripper

Los nueve motores usan Protocol 1.0 a 1 Mbps. Los comandos de Goal Position
se transmiten mediante GroupSyncWrite para que, especialmente, los motores
2 y 3 reciban simultáneamente los objetivos opuestos de joint2.
"""

from __future__ import annotations

from collections import defaultdict
import math
import os
from typing import Dict, List, Optional

import rclpy
from dynamixel_sdk import (
    COMM_SUCCESS,
    DXL_HIBYTE,
    DXL_LOBYTE,
    GroupSyncWrite,
    PacketHandler,
    PortHandler,
)
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import Int32MultiArray, String, UInt32
from std_srvs.srv import SetBool, Trigger

from arm7_control.dynamixel_profiles import MotorProfile, get_motor_profile


class Arm7Controller(Node):
    """Controlador de 7 GDL + gripper a partir de 9 motores físicos."""

    def __init__(self) -> None:
        super().__init__('arm7_controller')

        # Bus
        self.declare_parameter('use_hardware', False)
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 1000000)
        self.declare_parameter('protocol_version', 1.0)

        # Mapeo físico -> articulación lógica.
        self.declare_parameter('motor_ids', [1, 2, 3, 4, 5, 6, 7, 8, 9])
        self.declare_parameter(
            'motor_models',
            ['mx64', 'mx64', 'mx64', 'mx28', 'mx28', 'mx28', 'ax12a', 'ax12a', 'ax12a'],
        )
        self.declare_parameter(
            'motor_joints',
            ['joint1', 'joint2', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7', 'gripper'],
        )
        self.declare_parameter(
            'motor_signs',
            [1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0],
        )
        self.declare_parameter(
            'motor_centers',
            [1485, 1947, 2000, 1060, 2568, 3581, 151, 1023, 1021],
        )
        self.declare_parameter(
            'home_raw',
            [1485, 1947, 2000, 1060, 2568, 3581, 151, 1023, 1021],
        )
        self.declare_parameter(
            'moving_speeds',
            [30, 30, 30, 30, 30, 30, 30, 30, 30],
        )
        # -1 = no sobrescribir Torque Limit del motor.
        self.declare_parameter(
            'torque_limits',
            [-1, -1, -1, -1, -1, -1, -1, -1, -1],
        )

        self.declare_parameter(
            'joint_names',
            ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7', 'gripper'],
        )
        self.declare_parameter('read_rate_hz', 20.0)
        self.declare_parameter('home_on_startup', False)
        self.declare_parameter('home_max_delta_deg', 175.0)
        self.declare_parameter('disable_torque_on_shutdown', True)
        self.declare_parameter('joint2_sync_tolerance_deg', 5.0)

        self.use_hardware = bool(self.get_parameter('use_hardware').value)
        self.port_name = str(self.get_parameter('port').value)
        self.baudrate = int(self.get_parameter('baudrate').value)
        self.protocol_version = float(self.get_parameter('protocol_version').value)

        self.motor_ids = [int(v) for v in self.get_parameter('motor_ids').value]
        self.motor_models = [str(v) for v in self.get_parameter('motor_models').value]
        self.motor_joints = [str(v) for v in self.get_parameter('motor_joints').value]
        self.motor_signs = [float(v) for v in self.get_parameter('motor_signs').value]
        self.motor_centers = [int(v) for v in self.get_parameter('motor_centers').value]
        self.home_raw = [int(v) for v in self.get_parameter('home_raw').value]
        self.moving_speeds = [int(v) for v in self.get_parameter('moving_speeds').value]
        self.torque_limits = [int(v) for v in self.get_parameter('torque_limits').value]
        self.joint_names = [str(v) for v in self.get_parameter('joint_names').value]
        self.read_rate_hz = float(self.get_parameter('read_rate_hz').value)
        self.home_on_startup = bool(self.get_parameter('home_on_startup').value)
        self.home_max_delta_deg = float(
            self.get_parameter('home_max_delta_deg').value
        )
        self.disable_torque_on_shutdown = bool(
            self.get_parameter('disable_torque_on_shutdown').value
        )
        self.joint2_sync_tolerance = math.radians(
            float(self.get_parameter('joint2_sync_tolerance_deg').value)
        )

        self._validate_configuration()

        self.profiles: List[MotorProfile] = [
            get_motor_profile(model) for model in self.motor_models
        ]

        self.port_handler: Optional[PortHandler] = None
        self.packet_handler: Optional[PacketHandler] = None
        self.group_sync_write: Optional[GroupSyncWrite] = None
        self.port_open = False
        self.hardware_ready = False
        self.torque_enabled = not self.use_hardware
        self.software_stop_active = False
        self._closed = False
        self._last_read_error_ns: Dict[int, int] = {}
        self._last_joint2_warning_ns = 0

        self.commanded_joint_positions: Dict[str, float] = {
            joint: 0.0 for joint in self.joint_names
        }
        self.current_joint_positions: Dict[str, float] = {
            joint: 0.0 for joint in self.joint_names
        }
        self.current_raw = list(self.home_raw)

        self.joint_state_pub = self.create_publisher(JointState, '/joint_states', 10)
        self.raw_state_pub = self.create_publisher(
            Int32MultiArray, '/arm7/motor_positions_raw', 10
        )
        self.status_pub = self.create_publisher(String, '/arm7/status', 10)

        self.command_sub = self.create_subscription(
            JointState, '/arm7/command', self.command_callback, 10
        )
        self.speed_sub = self.create_subscription(
            UInt32, '/arm7/profile_velocity', self.speed_callback, 10
        )

        self.home_srv = self.create_service(Trigger, '/arm7/home', self.home_callback)
        self.stop_srv = self.create_service(
            Trigger, '/arm7/software_stop', self.stop_callback
        )
        self.torque_srv = self.create_service(
            SetBool, '/arm7/torque_enable', self.torque_callback
        )

        self.state_timer = self.create_timer(
            1.0 / max(self.read_rate_hz, 1.0),
            self.state_timer_callback,
        )

        # Inicializa posiciones lógicas a partir de HOME.
        self._update_logical_from_raw(self.current_raw, warn_joint2=False)

        if self.use_hardware:
            self.hardware_ready = self._connect_hardware()
            if not self.hardware_ready:
                self._publish_status(
                    'Hardware NO listo. El nodo sigue activo para diagnóstico, '
                    'pero no enviará comandos de movimiento.'
                )
            elif self.home_on_startup:
                self._move_home()
        else:
            self._publish_status(
                'Modo sin hardware activo. '
                'Configuración: 9 motores físicos / 8 articulaciones lógicas.'
            )

        self.get_logger().info(
            'Distribución: 1-3 MX-64, 4-6 MX-28, 7-9 AX-12A | '
            'Protocol 1.0 | 1 Mbps.'
        )
        self.get_logger().info(
            'joint2: ID 2 signo +1 / ID 3 signo -1 (comando simultáneo).'
        )

    def _validate_configuration(self) -> None:
        expected = 9
        fields = {
            'motor_ids': self.motor_ids,
            'motor_models': self.motor_models,
            'motor_joints': self.motor_joints,
            'motor_signs': self.motor_signs,
            'motor_centers': self.motor_centers,
            'home_raw': self.home_raw,
            'moving_speeds': self.moving_speeds,
            'torque_limits': self.torque_limits,
        }
        for name, values in fields.items():
            if len(values) != expected:
                raise ValueError(
                    f'{name} debe contener exactamente {expected} elementos; '
                    f'se recibieron {len(values)}.'
                )

        if self.motor_ids != [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            self.get_logger().warning(
                f'Los IDs no son [1..9]: {self.motor_ids}. '
                'Esto es válido solo si corresponde al robot real.'
            )

        if len(set(self.motor_ids)) != expected:
            raise ValueError('Los nueve IDs DYNAMIXEL deben ser únicos.')

        if not math.isclose(self.protocol_version, 1.0):
            raise ValueError('Este repositorio está diseñado exclusivamente para Protocol 1.0.')

        for sign in self.motor_signs:
            if not math.isclose(abs(sign), 1.0, abs_tol=1e-9):
                raise ValueError('Cada motor_sign debe ser +1.0 o -1.0.')

        logical = set(self.joint_names)
        if set(self.motor_joints) - logical:
            raise ValueError('motor_joints contiene articulaciones no declaradas en joint_names.')

        # Regla estructural obligatoria del robot.
        idx2 = self.motor_ids.index(2)
        idx3 = self.motor_ids.index(3)
        if self.motor_joints[idx2] != 'joint2' or self.motor_joints[idx3] != 'joint2':
            raise ValueError('Los motores ID 2 e ID 3 deben mapear a joint2.')
        if self.motor_signs[idx2] != 1.0 or self.motor_signs[idx3] != -1.0:
            raise ValueError(
                'Para joint2 se requiere ID 2 con signo +1 e ID 3 con signo -1.'
            )

    def _publish_status(self, text: str) -> None:
        msg = String()
        msg.data = text
        self.status_pub.publish(msg)
        self.get_logger().info(text)

    def _connect_hardware(self) -> bool:
        # Evita exactamente el fallo observado cuando /dev/ttyUSB0 no existe.
        if not os.path.exists(self.port_name):
            self.get_logger().error(
                f'No existe el puerto {self.port_name}. '
                'Revise USB/passthrough de la máquina virtual y ejecute '
                '`ls /dev/ttyUSB* /dev/ttyACM*`.'
            )
            return False

        try:
            self.port_handler = PortHandler(self.port_name)
            self.packet_handler = PacketHandler(1.0)

            if not self.port_handler.openPort():
                self.get_logger().error(f'No se pudo abrir {self.port_name}.')
                return False
            self.port_open = True

            if not self.port_handler.setBaudRate(self.baudrate):
                self.get_logger().error(
                    f'No se pudo configurar baudrate={self.baudrate}.'
                )
                self._close_port_only()
                return False

        except Exception as exc:  # pyserial puede lanzar SerialException
            self.get_logger().error(
                f'Error abriendo {self.port_name}: {type(exc).__name__}: {exc}'
            )
            self._close_port_only()
            return False

        self.get_logger().info(
            f'Puerto {self.port_name} abierto a {self.baudrate} baud, Protocol 1.0.'
        )

        # Primero ping de los 9 motores. Todavía no se habilita torque.
        missing = []
        for dxl_id in self.motor_ids:
            try:
                model_number, comm_result, dxl_error = self.packet_handler.ping(
                    self.port_handler, dxl_id
                )
            except Exception as exc:
                self.get_logger().error(f'ID {dxl_id}: excepción durante ping: {exc}')
                missing.append(dxl_id)
                continue

            if comm_result != COMM_SUCCESS or dxl_error != 0:
                self.get_logger().error(
                    f'ID {dxl_id}: no responde correctamente al ping: '
                    f'{self._communication_error_text(comm_result, dxl_error)}'
                )
                missing.append(dxl_id)
            else:
                self.get_logger().info(
                    f'ID {dxl_id}: detectado (model_number={model_number}).'
                )

        if missing:
            self.get_logger().error(
                f'Faltan motores o hay error de comunicación en IDs: {missing}. '
                'Por seguridad NO se habilitará torque.'
            )
            self._close_port_only()
            return False

        # Configuración RAM antes de Torque ON.
        for index, dxl_id in enumerate(self.motor_ids):
            if not self._write2(
                dxl_id,
                self.profiles[index].speed_addr,
                max(1, min(1023, self.moving_speeds[index])),
                'Moving Speed',
            ):
                self._safe_disable_and_close()
                return False

            limit = self.torque_limits[index]
            if limit >= 0:
                if not self._write2(
                    dxl_id,
                    self.profiles[index].torque_limit_addr,
                    max(0, min(1023, limit)),
                    'Torque Limit',
                ):
                    self._safe_disable_and_close()
                    return False

        # Preparar SyncWrite antes de Torque ON.
        self.group_sync_write = GroupSyncWrite(
            self.port_handler,
            self.packet_handler,
            30,
            2,
        )

        # Lee la postura actual, copia Present Position -> Goal Position y solo
        # entonces habilita torque. Esto evita saltos al conectar.
        if not self._set_torque_all(True):
            self._safe_disable_and_close()
            return False

        self._publish_status(
            'Hardware listo: 9/9 motores responden, Goal Position alineado '
            'con Present Position y torque habilitado.'
        )
        return True

    def _communication_error_text(self, comm_result: int, dxl_error: int) -> str:
        if self.packet_handler is None:
            return 'PacketHandler no disponible'
        parts = []
        if comm_result != COMM_SUCCESS:
            parts.append(self.packet_handler.getTxRxResult(comm_result))
        if dxl_error:
            parts.append(self.packet_handler.getRxPacketError(dxl_error))
        return ' | '.join(parts) if parts else 'sin detalle'

    def _write1(self, dxl_id: int, address: int, value: int, label: str) -> bool:
        if not self.port_open or self.port_handler is None or self.packet_handler is None:
            return False
        try:
            comm_result, dxl_error = self.packet_handler.write1ByteTxRx(
                self.port_handler, dxl_id, address, int(value)
            )
        except Exception as exc:
            self.get_logger().error(f'ID {dxl_id}: excepción escribiendo {label}: {exc}')
            return False
        if comm_result != COMM_SUCCESS or dxl_error:
            self.get_logger().error(
                f'ID {dxl_id}: error escribiendo {label}: '
                f'{self._communication_error_text(comm_result, dxl_error)}'
            )
            return False
        return True

    def _write2(self, dxl_id: int, address: int, value: int, label: str) -> bool:
        if not self.port_open or self.port_handler is None or self.packet_handler is None:
            return False
        try:
            comm_result, dxl_error = self.packet_handler.write2ByteTxRx(
                self.port_handler, dxl_id, address, int(value)
            )
        except Exception as exc:
            self.get_logger().error(f'ID {dxl_id}: excepción escribiendo {label}: {exc}')
            return False
        if comm_result != COMM_SUCCESS or dxl_error:
            self.get_logger().error(
                f'ID {dxl_id}: error escribiendo {label}: '
                f'{self._communication_error_text(comm_result, dxl_error)}'
            )
            return False
        return True

    def _read2(self, dxl_id: int, address: int, label: str) -> Optional[int]:
        if not self.port_open or self.port_handler is None or self.packet_handler is None:
            return None
        try:
            value, comm_result, dxl_error = self.packet_handler.read2ByteTxRx(
                self.port_handler, dxl_id, address
            )
        except Exception as exc:
            self._throttled_read_error(dxl_id, f'excepción leyendo {label}: {exc}')
            return None

        if comm_result != COMM_SUCCESS or dxl_error:
            self._throttled_read_error(
                dxl_id,
                f'error leyendo {label}: '
                f'{self._communication_error_text(comm_result, dxl_error)}',
            )
            return None
        return int(value)

    def _throttled_read_error(self, dxl_id: int, message: str) -> None:
        now_ns = self.get_clock().now().nanoseconds
        previous = self._last_read_error_ns.get(dxl_id, 0)
        if now_ns - previous > 2_000_000_000:
            self.get_logger().error(f'ID {dxl_id}: {message}')
            self._last_read_error_ns[dxl_id] = now_ns

    def _logical_to_raw(self, motor_index: int, joint_angle: float) -> int:
        profile = self.profiles[motor_index]
        sign = self.motor_signs[motor_index]
        center = self.motor_centers[motor_index]
        motor_angle = sign * float(joint_angle)
        return profile.motor_radians_to_raw(motor_angle, center_raw=center)

    def _raw_to_logical(self, motor_index: int, raw: int) -> float:
        profile = self.profiles[motor_index]
        sign = self.motor_signs[motor_index]
        center = self.motor_centers[motor_index]
        motor_angle = profile.raw_to_motor_radians(raw, center_raw=center)
        return motor_angle / sign

    def _goals_from_logical(self) -> List[int]:
        return [
            self._logical_to_raw(index, self.commanded_joint_positions[joint])
            for index, joint in enumerate(self.motor_joints)
        ]

    def _sync_write_goals(
        self,
        goals: List[int],
        *,
        indices: Optional[List[int]] = None,
        require_ready: bool = True,
        require_torque: bool = True,
    ) -> bool:
        """Envía Goal Position por SyncWrite.

        `indices` permite mover solamente los motores asociados al comando
        recibido. Así un slider no puede arrastrar accidentalmente otras
        articulaciones hacia HOME o hacia un objetivo anterior.

        Para joint2, `indices` contiene simultáneamente ID2 e ID3.
        """
        if not self.port_open or self.group_sync_write is None:
            self.get_logger().warning(
                'Comando rechazado: puerto/GroupSyncWrite no está listo.'
            )
            return False

        if require_ready and not self.hardware_ready:
            self.get_logger().warning('Comando rechazado: hardware no listo.')
            return False

        if require_torque and not self.torque_enabled:
            self.get_logger().warning('Comando rechazado: torque deshabilitado.')
            return False

        if indices is None:
            indices = list(range(len(self.motor_ids)))

        self.group_sync_write.clearParam()

        for index in indices:
            raw_goal = int(goals[index])
            dxl_id = self.motor_ids[index]
            data = [DXL_LOBYTE(raw_goal), DXL_HIBYTE(raw_goal)]

            if not self.group_sync_write.addParam(dxl_id, data):
                self.get_logger().error(
                    f'No se pudo agregar ID {dxl_id} al GroupSyncWrite.'
                )
                self.group_sync_write.clearParam()
                return False

        try:
            comm_result = self.group_sync_write.txPacket()
        except Exception as exc:
            self.get_logger().error(f'Excepción durante GroupSyncWrite: {exc}')
            self.group_sync_write.clearParam()
            return False
        finally:
            self.group_sync_write.clearParam()

        if comm_result != COMM_SUCCESS:
            self.get_logger().error(
                'GroupSyncWrite falló: '
                + self.packet_handler.getTxRxResult(comm_result)
            )
            return False

        return True

    def command_callback(self, msg: JointState) -> None:
        if self.software_stop_active:
            self.get_logger().warning(
                'Comando ignorado: la parada de software está activa.'
            )
            return

        updates: Dict[str, float] = {}

        if msg.name:
            for name, position in zip(msg.name, msg.position):
                if name in self.commanded_joint_positions:
                    updates[name] = float(position)
        else:
            for name, position in zip(self.joint_names, msg.position):
                updates[name] = float(position)

        if not updates:
            self.get_logger().warning('/arm7/command no contiene articulaciones válidas.')
            return

        # Actualiza solamente las articulaciones solicitadas.
        self.commanded_joint_positions.update(updates)

        # Determina qué motores físicos pertenecen a esas articulaciones.
        # joint2 selecciona automáticamente dos índices: ID2 e ID3.
        indices = [
            index
            for index, joint in enumerate(self.motor_joints)
            if joint in updates
        ]

        goals = list(self.current_raw)

        for index in indices:
            joint = self.motor_joints[index]
            goals[index] = self._logical_to_raw(
                index,
                self.commanded_joint_positions[joint],
            )

        if not self.use_hardware:
            # En simulación solo cambian los motores realmente comandados.
            for index in indices:
                self.current_raw[index] = goals[index]
            self._update_logical_from_raw(self.current_raw, warn_joint2=False)
            return

        if not self.hardware_ready:
            self.get_logger().warning(
                'Comando ignorado porque use_hardware=true pero el hardware no está listo.'
            )
            return

        self._sync_write_goals(goals, indices=indices)

    def _update_logical_from_raw(
        self,
        raw_values: List[int],
        *,
        warn_joint2: bool = True,
    ) -> None:
        grouped: Dict[str, List[float]] = defaultdict(list)

        for index, raw in enumerate(raw_values):
            grouped[self.motor_joints[index]].append(
                self._raw_to_logical(index, raw)
            )

        for joint in self.joint_names:
            values = grouped.get(joint)
            if values:
                self.current_joint_positions[joint] = sum(values) / len(values)

        # joint2 tiene dos motores físicos. Después de corregir el signo,
        # ambos deberían reportar prácticamente el mismo ángulo lógico.
        joint2_values = grouped.get('joint2', [])
        if warn_joint2 and len(joint2_values) == 2:
            mismatch = abs(joint2_values[0] - joint2_values[1])
            if mismatch > self.joint2_sync_tolerance:
                now_ns = self.get_clock().now().nanoseconds
                if now_ns - self._last_joint2_warning_ns > 2_000_000_000:
                    self.get_logger().warning(
                        'DESACOPLE joint2: '
                        f'ID2={math.degrees(joint2_values[0]):.2f}°, '
                        f'ID3 corregido={math.degrees(joint2_values[1]):.2f}°, '
                        f'diferencia={math.degrees(mismatch):.2f}°. '
                        'Detenga el robot si la diferencia persiste.'
                    )
                    self._last_joint2_warning_ns = now_ns

    def _read_all_positions(self, *, strict: bool = False) -> bool:
        updated = list(self.current_raw)
        success = True

        for index, dxl_id in enumerate(self.motor_ids):
            raw = self._read2(
                dxl_id,
                self.profiles[index].present_position_addr,
                'Present Position',
            )

            if raw is None:
                success = False
                if strict:
                    return False
            else:
                updated[index] = raw

        self.current_raw = updated
        self._update_logical_from_raw(self.current_raw)

        # Sincroniza el estado de comando con la postura realmente medida.
        # Esto evita que un comando posterior use objetivos obsoletos.
        for joint in self.joint_names:
            self.commanded_joint_positions[joint] = self.current_joint_positions[joint]

        return success

    def state_timer_callback(self) -> None:
        if self.use_hardware and self.hardware_ready:
            self._read_all_positions()

        joint_msg = JointState()
        joint_msg.header.stamp = self.get_clock().now().to_msg()
        joint_msg.name = list(self.joint_names)
        joint_msg.position = [
            self.current_joint_positions[name] for name in self.joint_names
        ]
        self.joint_state_pub.publish(joint_msg)

        raw_msg = Int32MultiArray()
        raw_msg.data = list(self.current_raw)
        self.raw_state_pub.publish(raw_msg)

    def speed_callback(self, msg: UInt32) -> None:
        speed = max(1, min(1023, int(msg.data)))
        self.moving_speeds = [speed] * 9

        if not self.use_hardware:
            self._publish_status(f'Velocidad simulada actualizada a {speed}.')
            return

        if not self.hardware_ready:
            self.get_logger().warning('No se cambia velocidad: hardware no listo.')
            return

        success = True
        for index, dxl_id in enumerate(self.motor_ids):
            success = self._write2(
                dxl_id,
                self.profiles[index].speed_addr,
                speed,
                'Moving Speed',
            ) and success

        self._publish_status(
            f'Velocidad {speed} aplicada a los 9 motores.'
            if success
            else 'Hubo errores al actualizar Moving Speed.'
        )

    def _home_guard(self) -> tuple[bool, str]:
        """Impide un salto grande hacia HOME desde una postura desconocida."""
        if not self.use_hardware:
            return True, ''

        if not self._read_all_positions(strict=True):
            return False, 'HOME bloqueado: no fue posible leer los 9 motores.'

        offenders = []

        for index, raw in enumerate(self.current_raw):
            delta_deg = abs(
                math.degrees(
                    self.profiles[index].raw_to_motor_radians(
                        raw,
                        center_raw=self.home_raw[index],
                    )
                )
            )

            if delta_deg > self.home_max_delta_deg:
                offenders.append(
                    f'ID{self.motor_ids[index]}={delta_deg:.1f}°'
                )

        if offenders:
            return (
                False,
                'HOME bloqueado por seguridad: uno o más motores están a más de '
                f'{self.home_max_delta_deg:.1f}° de HOME: '
                + ', '.join(offenders)
                + '. Acerque el robot de forma controlada antes de reintentar.',
            )

        return True, ''

    def _move_home(self) -> bool:
        # En esta versión motor_centers == home_raw, por lo que HOME es 0°
        # lógico para todas las articulaciones.
        for joint in self.joint_names:
            self.commanded_joint_positions[joint] = 0.0

        if not self.use_hardware:
            self.current_raw = list(self.home_raw)
            self._update_logical_from_raw(self.current_raw, warn_joint2=False)
            return True

        # Los 9 motores reciben la postura HOME real en un único SyncWrite.
        return self._sync_write_goals(list(self.home_raw))

    def home_callback(
        self,
        request: Trigger.Request,
        response: Trigger.Response,
    ) -> Trigger.Response:
        del request

        if self.software_stop_active:
            response.success = False
            response.message = 'HOME bloqueado: parada de software activa.'
            return response

        if self.use_hardware and not self.hardware_ready:
            response.success = False
            response.message = 'HOME bloqueado: hardware no listo.'
            return response

        if not self.torque_enabled:
            response.success = False
            response.message = 'HOME bloqueado: torque deshabilitado.'
            return response

        guard_ok, guard_message = self._home_guard()
        if not guard_ok:
            response.success = False
            response.message = guard_message
            self._publish_status(response.message)
            return response

        response.success = self._move_home()
        response.message = (
            'HOME enviado a los 9 motores.'
            if response.success
            else 'No se pudo ejecutar HOME.'
        )
        self._publish_status(response.message)
        return response

    def _set_torque_all(self, enabled: bool) -> bool:
        if not self.use_hardware:
            self.torque_enabled = enabled
            return True

        if not self.port_open:
            return False

        # Antes de Torque ON, captura la postura actual y la copia a Goal Position.
        # Así el robot no "salta" hacia un objetivo viejo almacenado en RAM.
        if enabled:
            if not self._read_all_positions(strict=True):
                self.get_logger().error(
                    'No se habilita torque: no fue posible leer los 9 motores.'
                )
                return False

            if not self._sync_write_goals(
                list(self.current_raw),
                require_ready=False,
                require_torque=False,
            ):
                self.get_logger().error(
                    'No se habilita torque: no fue posible alinear Goal Position '
                    'con Present Position.'
                )
                return False

        success = True

        for dxl_id in self.motor_ids:
            success = self._write1(
                dxl_id,
                24,
                1 if enabled else 0,
                'Torque Enable',
            ) and success

        if success:
            self.torque_enabled = enabled

        return success

    def torque_callback(
        self,
        request: SetBool.Request,
        response: SetBool.Response,
    ) -> SetBool.Response:
        requested = bool(request.data)

        if requested and self.use_hardware and not self.hardware_ready:
            response.success = False
            response.message = 'No se puede habilitar torque: hardware no listo.'
            return response

        response.success = self._set_torque_all(requested)

        if response.success:
            if requested:
                self.software_stop_active = False
                response.message = 'Torque habilitado en los 9 motores.'
            else:
                response.message = 'Torque deshabilitado en los 9 motores.'
        else:
            response.message = 'No se pudo cambiar torque en todos los motores.'

        self._publish_status(response.message)
        return response

    def stop_callback(
        self,
        request: Trigger.Request,
        response: Trigger.Response,
    ) -> Trigger.Response:
        del request
        self.software_stop_active = True

        if not self.use_hardware:
            self.torque_enabled = False
            response.success = True
        elif self.port_open:
            response.success = self._set_torque_all(False)
        else:
            # No hay puerto: no existe nada que escribir. El stop lógico sigue activo.
            response.success = True
            self.torque_enabled = False

        response.message = (
            'Parada de software activa. Nuevos comandos quedan bloqueados y '
            'el torque se deshabilitó cuando había hardware disponible.'
        )
        self._publish_status(response.message)
        return response

    def _safe_disable_and_close(self) -> None:
        if self.port_open:
            for dxl_id in self.motor_ids:
                self._write1(dxl_id, 24, 0, 'Torque Disable Recovery')
        self.torque_enabled = False
        self.hardware_ready = False
        self._close_port_only()

    def _close_port_only(self) -> None:
        if self.port_open and self.port_handler is not None:
            try:
                self.port_handler.closePort()
            except Exception as exc:
                self.get_logger().warning(f'Error cerrando puerto: {exc}')
        self.port_open = False

    def close(self) -> None:
        if self._closed:
            return
        self._closed = True

        # Nunca intenta escribir si el puerto jamás abrió.
        if (
            self.use_hardware
            and self.port_open
            and self.disable_torque_on_shutdown
        ):
            for dxl_id in self.motor_ids:
                self._write1(dxl_id, 24, 0, 'Torque Disable Shutdown')

        self.torque_enabled = False
        self.hardware_ready = False
        self._close_port_only()

    def destroy_node(self) -> bool:
        self.close()
        return super().destroy_node()


def main(args=None) -> None:
    rclpy.init(args=args)
    node: Optional[Arm7Controller] = None
    try:
        node = Arm7Controller()
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
```


## 14.10 `arm7_gui.py`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_control/arm7_control/arm7_gui.py
```

```python
#!/usr/bin/env python3
"""GUI Tkinter: 8 sliders lógicos para 9 motores físicos.

Solo existe un slider para joint2. El controlador ROS convierte ese único
valor en objetivos simultáneos opuestos para los MX-64 ID 2 e ID 3.
"""

from __future__ import annotations

import math
import tkinter as tk
from tkinter import messagebox, ttk
from typing import Dict, List

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState
from std_msgs.msg import String, UInt32
from std_srvs.srv import SetBool, Trigger


class Arm7GuiNode(Node):
    def __init__(self) -> None:
        super().__init__('arm7_gui')

        self.declare_parameter(
            'gui_joint_names',
            ['joint1', 'joint2', 'joint3', 'joint4', 'joint5', 'joint6', 'joint7', 'gripper'],
        )
        self.declare_parameter(
            'gui_min_deg',
            [-90.0, -90.0, -90.0, -90.0, -90.0, -90.0, -90.0, -90.0],
        )
        self.declare_parameter(
            'gui_max_deg',
            [90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0, 90.0],
        )

        self.joint_names = [str(v) for v in self.get_parameter('gui_joint_names').value]
        self.min_deg = [float(v) for v in self.get_parameter('gui_min_deg').value]
        self.max_deg = [float(v) for v in self.get_parameter('gui_max_deg').value]

        if not (
            len(self.joint_names) == len(self.min_deg) == len(self.max_deg) == 8
        ):
            raise ValueError('La GUI requiere 8 articulaciones y 8 pares de límites.')

        self.command_pub = self.create_publisher(JointState, '/arm7/command', 10)
        self.speed_pub = self.create_publisher(UInt32, '/arm7/profile_velocity', 10)

        self.home_client = self.create_client(Trigger, '/arm7/home')
        self.stop_client = self.create_client(Trigger, '/arm7/software_stop')
        self.torque_client = self.create_client(SetBool, '/arm7/torque_enable')

        self.latest_status = 'Esperando controlador...'
        self.latest_positions: Dict[str, float] = {}

        self.create_subscription(String, '/arm7/status', self.status_cb, 10)
        self.create_subscription(JointState, '/joint_states', self.joint_state_cb, 10)

    def status_cb(self, msg: String) -> None:
        self.latest_status = msg.data

    def joint_state_cb(self, msg: JointState) -> None:
        self.latest_positions = {
            name: math.degrees(pos) for name, pos in zip(msg.name, msg.position)
        }

    def publish_single_joint(self, joint: str, degrees: float) -> None:
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = [joint]
        msg.position = [math.radians(float(degrees))]
        self.command_pub.publish(msg)

    def publish_all(self, degrees_by_joint: Dict[str, float]) -> None:
        msg = JointState()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.name = list(self.joint_names)
        msg.position = [
            math.radians(float(degrees_by_joint[name]))
            for name in self.joint_names
        ]
        self.command_pub.publish(msg)

    def publish_speed(self, speed: int) -> None:
        msg = UInt32()
        msg.data = max(1, min(1023, int(speed)))
        self.speed_pub.publish(msg)


class Arm7Gui:
    def __init__(self, node: Arm7GuiNode) -> None:
        self.node = node
        self.root = tk.Tk()
        self.root.title('7DoF + Gripper | 9 DYNAMIXEL | ROS 2 Lyrical')
        self.root.minsize(880, 650)
        self.root.protocol('WM_DELETE_WINDOW', self.close)

        self.variables: Dict[str, tk.DoubleVar] = {
            name: tk.DoubleVar(value=0.0) for name in self.node.joint_names
        }
        self.entries: Dict[str, ttk.Entry] = {}
        self.actual_labels: Dict[str, tk.StringVar] = {
            name: tk.StringVar(value='--') for name in self.node.joint_names
        }
        self.status_var = tk.StringVar(value=self.node.latest_status)
        self.speed_var = tk.IntVar(value=30)

        self._build()
        self.root.after(20, self._spin_ros)
        self.root.after(200, self._refresh)

    def _build(self) -> None:
        header = ttk.Frame(self.root, padding=12)
        header.pack(fill='x')

        ttk.Label(
            header,
            text='Manipulador 7 GDL + Gripper',
            font=('TkDefaultFont', 16, 'bold'),
        ).pack(anchor='w')

        ttk.Label(
            header,
            text=(
                '9 motores físicos: 3×MX-64 + 3×MX-28 + 3×AX-12A | '
                'Protocol 1.0 | 1 Mbps'
            ),
        ).pack(anchor='w')

        ttk.Label(
            header,
            text=(
                'joint2 usa UN solo slider: el controlador mueve ID 2 (+θ) '
                'e ID 3 (-θ) simultáneamente.'
            ),
            foreground='darkred',
        ).pack(anchor='w', pady=(4, 0))

        frame = ttk.LabelFrame(self.root, text='Articulaciones lógicas', padding=12)
        frame.pack(fill='both', expand=True, padx=12, pady=8)
        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text='Articulación').grid(row=0, column=0, sticky='w')
        ttk.Label(frame, text='Comando').grid(row=0, column=1)
        ttk.Label(frame, text='°').grid(row=0, column=2)
        ttk.Label(frame, text='Actual [°]').grid(row=0, column=3)

        for row, (name, lower, upper) in enumerate(
            zip(self.node.joint_names, self.node.min_deg, self.node.max_deg),
            start=1,
        ):
            label = name
            if name == 'joint2':
                label = 'joint2  [MX64 ID2 + ID3 espejo]'

            ttk.Label(frame, text=label).grid(
                row=row, column=0, sticky='w', padx=(0, 8), pady=5
            )

            scale = ttk.Scale(
                frame,
                from_=lower,
                to=upper,
                variable=self.variables[name],
                orient='horizontal',
                command=lambda value, j=name: self._scale_changed(j, value),
            )
            scale.grid(row=row, column=1, sticky='ew', pady=5)
            # Por seguridad se envía al soltar el slider, no en cada pixel.
            scale.bind(
                '<ButtonRelease-1>',
                lambda event, j=name: self.send_single(j),
            )

            entry = ttk.Entry(frame, width=9)
            entry.insert(0, '0.0')
            entry.grid(row=row, column=2, padx=6)
            entry.bind('<Return>', lambda event, j=name: self._entry_send(j))
            self.entries[name] = entry

            ttk.Label(
                frame,
                textvariable=self.actual_labels[name],
                width=12,
            ).grid(row=row, column=3, padx=(8, 0))

        controls = ttk.LabelFrame(self.root, text='Control general', padding=12)
        controls.pack(fill='x', padx=12, pady=8)

        ttk.Label(controls, text='Moving Speed [1..1023]:').grid(row=0, column=0)
        ttk.Spinbox(
            controls,
            from_=1,
            to=1023,
            textvariable=self.speed_var,
            width=8,
        ).grid(row=0, column=1, padx=5)

        ttk.Button(
            controls, text='Aplicar velocidad', command=self.apply_speed
        ).grid(row=0, column=2, padx=5)

        ttk.Button(
            controls, text='Enviar todos', command=self.send_all
        ).grid(row=0, column=3, padx=5)

        ttk.Button(
            controls, text='HOME', command=self.call_home
        ).grid(row=0, column=4, padx=5)

        ttk.Button(
            controls, text='Torque ON', command=lambda: self.call_torque(True)
        ).grid(row=1, column=0, pady=(10, 0), padx=4)

        ttk.Button(
            controls, text='Torque OFF', command=lambda: self.call_torque(False)
        ).grid(row=1, column=1, pady=(10, 0), padx=4)

        ttk.Button(
            controls,
            text='PARADA DE SOFTWARE',
            command=self.call_stop,
        ).grid(row=1, column=2, columnspan=3, sticky='ew', pady=(10, 0), padx=4)

        status = ttk.LabelFrame(self.root, text='Estado', padding=10)
        status.pack(fill='x', padx=12, pady=(0, 12))
        ttk.Label(
            status, textvariable=self.status_var, wraplength=830
        ).pack(anchor='w')

        ttk.Label(
            status,
            text='La parada de software NO sustituye un paro de emergencia físico.',
        ).pack(anchor='w', pady=(5, 0))

    def _scale_changed(self, joint: str, value: str) -> None:
        entry = self.entries[joint]
        entry.delete(0, tk.END)
        entry.insert(0, f'{float(value):.2f}')

    def _entry_value(self, joint: str) -> float:
        idx = self.node.joint_names.index(joint)
        lower = self.node.min_deg[idx]
        upper = self.node.max_deg[idx]

        try:
            value = float(self.entries[joint].get())
        except ValueError:
            value = float(self.variables[joint].get())
            messagebox.showwarning('Valor inválido', f'{joint}: use un número.')

        value = max(lower, min(upper, value))
        self.variables[joint].set(value)
        self._scale_changed(joint, str(value))
        return value

    def _entry_send(self, joint: str) -> None:
        self.send_single(joint)

    def send_single(self, joint: str) -> None:
        value = self._entry_value(joint)
        self.node.publish_single_joint(joint, value)
        if joint == 'joint2':
            self.status_var.set(
                f'joint2={value:.2f}° enviado: ID2=+θ e ID3=-θ.'
            )
        else:
            self.status_var.set(f'{joint}={value:.2f}° enviado.')

    def send_all(self) -> None:
        values = {
            joint: self._entry_value(joint)
            for joint in self.node.joint_names
        }
        self.node.publish_all(values)
        self.status_var.set('Comando de las 8 articulaciones publicado.')

    def apply_speed(self) -> None:
        try:
            speed = int(self.speed_var.get())
        except (ValueError, tk.TclError):
            messagebox.showwarning('Valor inválido', 'La velocidad debe ser entera.')
            return
        speed = max(1, min(1023, speed))
        self.speed_var.set(speed)
        self.node.publish_speed(speed)

    def _service_ready(self, client, name: str) -> bool:
        if client.service_is_ready():
            return True
        self.status_var.set(f'Servicio {name} todavía no disponible.')
        return False

    def call_home(self) -> None:
        if not self._service_ready(self.node.home_client, '/arm7/home'):
            return

        confirmed = messagebox.askyesno(
            'Confirmar HOME',
            'Se enviará la postura HOME REAL a los 9 motores.\n\n'
            'HOME lógico = 0° para todos los sliders.\n'
            'El controlador rechazará HOME si algún motor está demasiado '
            'lejos de la postura registrada.\n\n'
            '¿Desea continuar?',
        )

        if not confirmed:
            return

        future = self.node.home_client.call_async(Trigger.Request())
        future.add_done_callback(self._home_done)

    def _home_done(self, future) -> None:
        try:
            response = future.result()
            self.status_var.set(response.message)

            if response.success:
                # HOME es el cero lógico del sistema.
                for joint in self.node.joint_names:
                    self.variables[joint].set(0.0)
                    self._scale_changed(joint, '0.0')

        except Exception as exc:
            self.status_var.set(f'Error ejecutando HOME: {exc}')

    def call_stop(self) -> None:
        if not self._service_ready(self.node.stop_client, '/arm7/software_stop'):
            return
        future = self.node.stop_client.call_async(Trigger.Request())
        future.add_done_callback(self._service_done)

    def call_torque(self, enabled: bool) -> None:
        if not self._service_ready(self.node.torque_client, '/arm7/torque_enable'):
            return
        req = SetBool.Request()
        req.data = enabled
        future = self.node.torque_client.call_async(req)
        future.add_done_callback(self._service_done)

    def _service_done(self, future) -> None:
        try:
            response = future.result()
            self.status_var.set(response.message)
        except Exception as exc:
            self.status_var.set(f'Error de servicio: {exc}')

    def _spin_ros(self) -> None:
        if rclpy.ok():
            rclpy.spin_once(self.node, timeout_sec=0.0)
            self.root.after(20, self._spin_ros)

    def _refresh(self) -> None:
        if self.node.latest_status:
            self.status_var.set(self.node.latest_status)

        for joint, value in self.node.latest_positions.items():
            if joint in self.actual_labels:
                self.actual_labels[joint].set(f'{value:.2f}')

        if rclpy.ok():
            self.root.after(200, self._refresh)

    def run(self) -> None:
        self.root.mainloop()

    def close(self) -> None:
        self.root.destroy()


def main(args=None) -> None:
    rclpy.init(args=args)
    node = Arm7GuiNode()
    gui = Arm7Gui(node)
    try:
        gui.run()
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
```


## 14.11 `scan_dynamixel.py`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_control/arm7_control/scan_dynamixel.py
```

```python
#!/usr/bin/env python3
"""Escáner DYNAMIXEL Protocol 1.0 para el bus del manipulador."""

from __future__ import annotations

import os
from typing import Optional

import rclpy
from dynamixel_sdk import COMM_SUCCESS, PacketHandler, PortHandler
from rclpy.node import Node


class DynamixelScanner(Node):
    def __init__(self) -> None:
        super().__init__('dynamixel_scanner')
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 1000000)
        self.declare_parameter('min_id', 1)
        self.declare_parameter('max_id', 20)

        self.port_name = str(self.get_parameter('port').value)
        self.baudrate = int(self.get_parameter('baudrate').value)
        self.min_id = max(0, int(self.get_parameter('min_id').value))
        self.max_id = min(253, int(self.get_parameter('max_id').value))

    def scan(self) -> list[int]:
        if not os.path.exists(self.port_name):
            raise RuntimeError(
                f'No existe {self.port_name}. Revise USB/passthrough y permisos.'
            )

        port = PortHandler(self.port_name)
        packet = PacketHandler(1.0)
        opened = False

        try:
            if not port.openPort():
                raise RuntimeError(f'No se pudo abrir {self.port_name}.')
            opened = True

            if not port.setBaudRate(self.baudrate):
                raise RuntimeError(f'No se pudo configurar {self.baudrate} baud.')

            detected = []
            for dxl_id in range(self.min_id, self.max_id + 1):
                model_number, comm_result, dxl_error = packet.ping(port, dxl_id)
                if comm_result == COMM_SUCCESS and dxl_error == 0:
                    detected.append(dxl_id)
                    self.get_logger().info(
                        f'ID {dxl_id}: model_number={model_number}'
                    )

            self.get_logger().info(f'IDs detectados: {detected}')

            expected = list(range(1, 10))
            if detected == expected:
                self.get_logger().info('OK: se detectaron exactamente los IDs 1..9.')
            else:
                missing = sorted(set(expected) - set(detected))
                extra = sorted(set(detected) - set(expected))
                if missing:
                    self.get_logger().warning(f'IDs esperados ausentes: {missing}')
                if extra:
                    self.get_logger().warning(f'IDs adicionales: {extra}')

            return detected
        finally:
            if opened:
                try:
                    port.closePort()
                except Exception:
                    pass


def main(args=None) -> None:
    rclpy.init(args=args)
    node: Optional[DynamixelScanner] = None
    try:
        node = DynamixelScanner()
        node.scan()
    except Exception as exc:
        if node is not None:
            node.get_logger().error(str(exc))
        else:
            print(exc)
    finally:
        if node is not None:
            node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
```



### `capture_home.py`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_control/arm7_control/capture_home.py
```

```python
#!/usr/bin/env python3
"""Lee Present Position de los 9 motores sin habilitar torque.

Úselo con el robot colocado manualmente en la postura HOME para obtener
los RAW exactos que deben copiarse a motor_centers y home_raw.
"""

from __future__ import annotations

import os

import rclpy
from dynamixel_sdk import COMM_SUCCESS, PacketHandler, PortHandler
from rclpy.node import Node


class HomeCapture(Node):
    def __init__(self) -> None:
        super().__init__('arm7_capture_home')
        self.declare_parameter('port', '/dev/ttyUSB0')
        self.declare_parameter('baudrate', 1000000)

        self.port_name = str(self.get_parameter('port').value)
        self.baudrate = int(self.get_parameter('baudrate').value)

    def capture(self) -> list[int]:
        if not os.path.exists(self.port_name):
            raise RuntimeError(f'No existe {self.port_name}.')

        port = PortHandler(self.port_name)
        packet = PacketHandler(1.0)
        opened = False

        try:
            if not port.openPort():
                raise RuntimeError(f'No se pudo abrir {self.port_name}.')
            opened = True

            if not port.setBaudRate(self.baudrate):
                raise RuntimeError(f'No se pudo configurar {self.baudrate} baud.')

            values = []

            for dxl_id in range(1, 10):
                raw, comm_result, dxl_error = packet.read2ByteTxRx(
                    port, dxl_id, 36
                )

                if comm_result != COMM_SUCCESS or dxl_error != 0:
                    raise RuntimeError(
                        f'No se pudo leer Present Position del ID {dxl_id}.'
                    )

                values.append(int(raw))
                self.get_logger().info(f'ID {dxl_id}: Present Position RAW={raw}')

            self.get_logger().info(f'HOME RAW = {values}')
            print()
            print('Copiar en mixed_arm.yaml:')
            print(f'motor_centers: {values}')
            print(f'home_raw:      {values}')
            return values

        finally:
            if opened:
                try:
                    port.closePort()
                except Exception:
                    pass


def main(args=None) -> None:
    rclpy.init(args=args)
    node = HomeCapture()
    try:
        node.capture()
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
```

## 14.12 `trajectory_demo.py`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_control/arm7_control/trajectory_demo.py
```

```python
#!/usr/bin/env python3
"""Trayectoria didáctica pequeña para probar primero SIN hardware."""

import math

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import JointState


class TrajectoryDemo(Node):
    def __init__(self) -> None:
        super().__init__('arm7_trajectory_demo')
        self.declare_parameter('amplitude_deg', 5.0)
        self.declare_parameter('frequency_hz', 0.03)
        self.declare_parameter('publish_rate_hz', 20.0)

        self.amplitude = math.radians(
            float(self.get_parameter('amplitude_deg').value)
        )
        self.frequency = float(self.get_parameter('frequency_hz').value)
        rate = float(self.get_parameter('publish_rate_hz').value)

        self.joint_names = [
            'joint1', 'joint2', 'joint3', 'joint4',
            'joint5', 'joint6', 'joint7', 'gripper'
        ]
        self.publisher = self.create_publisher(JointState, '/arm7/command', 10)
        self.start = self.get_clock().now()
        self.timer = self.create_timer(1.0 / max(rate, 1.0), self.tick)

        self.get_logger().warning(
            'Trayectoria automática: úsela primero con use_hardware:=false.'
        )

    def tick(self) -> None:
        now = self.get_clock().now()
        t = (now - self.start).nanoseconds * 1e-9

        msg = JointState()
        msg.header.stamp = now.to_msg()
        msg.name = list(self.joint_names)

        positions = []
        for index in range(7):
            phase = index * math.pi / 7.0
            positions.append(
                self.amplitude
                * math.sin(2.0 * math.pi * self.frequency * t + phase)
            )
        positions.append(0.0)  # gripper quieto durante esta demostración
        msg.position = positions
        self.publisher.publish(msg)


def main(args=None) -> None:
    rclpy.init(args=args)
    node = TrajectoryDemo()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        if rclpy.ok():
            rclpy.shutdown()


if __name__ == '__main__':
    main()
```


## 14.13 `mixed_arm.yaml`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_control/config/mixed_arm.yaml
```

```yaml
arm7_controller:
  ros__parameters:
    use_hardware: false
    port: /dev/ttyUSB0
    baudrate: 1000000
    protocol_version: 1.0

    # 9 motores físicos.
    motor_ids: [1, 2, 3, 4, 5, 6, 7, 8, 9]
    motor_models: [mx64, mx64, mx64, mx28, mx28, mx28, ax12a, ax12a, ax12a]

    # 8 articulaciones lógicas: joint2 usa dos motores.
    motor_joints: [joint1, joint2, joint2, joint3, joint4, joint5, joint6, joint7, gripper]

    # ID2 e ID3 están montados en sentidos opuestos.
    motor_signs: [1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

    # HOME REAL ACTUAL del robot.
    # Como motor_centers == home_raw, HOME corresponde a 0° lógico en la GUI.
    motor_centers: [1485, 1947, 2000, 1060, 2568, 3581, 151, 1023, 1021]
    home_raw:      [1485, 1947, 2000, 1060, 2568, 3581, 151, 1023, 1021]

    # Valor 0 en Protocol 1.0 significa velocidad máxima; por eso se evita 0.
    moving_speeds: [30, 30, 30, 30, 30, 30, 30, 30, 30]

    # -1 = no sobrescribir Torque Limit del actuador.
    torque_limits: [-1, -1, -1, -1, -1, -1, -1, -1, -1]

    joint_names: [joint1, joint2, joint3, joint4, joint5, joint6, joint7, gripper]

    read_rate_hz: 20.0
    home_on_startup: false

    # HOME se rechaza si algún motor está demasiado lejos de la postura HOME.
    # Este valor fue definido para la configuración actual del robot.
    home_max_delta_deg: 175.0

    disable_torque_on_shutdown: true

    # Advierte si ID2 e ID3, una vez corregido el signo, difieren demasiado.
    joint2_sync_tolerance_deg: 5.0

arm7_gui:
  ros__parameters:
    gui_joint_names: [joint1, joint2, joint3, joint4, joint5, joint6, joint7, gripper]

    # Rangos actuales de la GUI.
    # Validar mecánicamente cada articulación antes de recorrer todo el rango con hardware.
    gui_min_deg: [-90.0, -90.0, -90.0, -90.0, -90.0, -90.0, -90.0, -90.0]
    gui_max_deg: [ 90.0,  90.0,  90.0,  90.0,  90.0,  90.0,  90.0,  90.0]
```


## 14.14 `arm7_system.launch.py`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_control/launch/arm7_system.launch.py
```

```python
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    share = get_package_share_directory('arm7_control')
    default_config = os.path.join(share, 'config', 'mixed_arm.yaml')

    return LaunchDescription([
        DeclareLaunchArgument('config_file', default_value=default_config),
        DeclareLaunchArgument('use_hardware', default_value='false'),
        DeclareLaunchArgument('port', default_value='/dev/ttyUSB0'),
        DeclareLaunchArgument('baudrate', default_value='1000000'),
        DeclareLaunchArgument('start_gui', default_value='true'),

        Node(
            package='arm7_control',
            executable='arm7_controller',
            name='arm7_controller',
            output='screen',
            parameters=[
                LaunchConfiguration('config_file'),
                {
                    'use_hardware': ParameterValue(
                        LaunchConfiguration('use_hardware'),
                        value_type=bool,
                    ),
                    'port': LaunchConfiguration('port'),
                    'baudrate': ParameterValue(
                        LaunchConfiguration('baudrate'),
                        value_type=int,
                    ),
                },
            ],
        ),

        Node(
            package='arm7_control',
            executable='arm7_gui',
            name='arm7_gui',
            output='screen',
            parameters=[LaunchConfiguration('config_file')],
            condition=IfCondition(LaunchConfiguration('start_gui')),
        ),
    ])
```


---

# 15. Compilación del workspace

Ve al workspace:

```bash
cd ~/ros2_lyrical/7dof_ws
```

Carga primero ROS 2:

```bash
source /opt/ros/lyrical/setup.bash
```

## 15.1 Regla importante de `rosdep`

Mientras el workspace contenga solamente `arm7_control`, puedes ejecutar:

```bash
rosdep install \
  --from-paths src \
  --ignore-src \
  --rosdistro lyrical \
  -r -y
```

Cuando ya hayas añadido `arm7_description` con dependencias de RealSense, **completa primero la sección 36** para que `realsense2_camera`, `realsense2_camera_msgs` y `diagnostic_updater` existan dentro de `src`. Así `--ignore-src` evita que `rosdep` intente buscarlos por APT.

Si todavía no has instalado RealSense y solo quieres compilar el robot, usa temporalmente:

```bash
rosdep install \
  --from-paths src \
  --ignore-src \
  --rosdistro lyrical \
  --skip-keys="realsense2_camera realsense2_camera_msgs librealsense2" \
  -r -y
```

> Si APT muestra `Could not get lock /var/lib/dpkg/lock-frontend` porque `unattended-upgr` está trabajando, **no borres el lock**. Espera a que termine. Puedes comprobarlo con `ps aux | grep -E 'apt|dpkg|unattended' | grep -v grep`. Cuando ya no haya un proceso activo, ejecuta `sudo dpkg --configure -a` y continúa.

## 15.2 Compilar

```bash
colcon build --symlink-install
```

Después de **cada** compilación, vuelve a cargar el overlay:

```bash
source ~/ros2_lyrical/7dof_ws/install/setup.bash
```

No omitas este paso. Si no haces `source`, ROS puede encontrar solamente los paquetes instalados en `/opt/ros/lyrical` o una versión anterior del workspace.

Verifica:

```bash
ros2 pkg prefix arm7_control
ros2 pkg executables arm7_control
```

Debes encontrar, entre otros:

```text
arm7_control arm7_controller
arm7_control arm7_gui
arm7_control scan_dynamixel
arm7_control capture_home
arm7_control trajectory_demo
```

> El archivo correcto es `install/setup.bash`. Un error tipográfico como `source install/setup.baa` producirá `No such file or directory`.

> Después de modificar `setup.py`, archivos launch, YAML, Xacro o Python, recompila y vuelve a ejecutar `source install/setup.bash`.

# 16. Práctica 1: validación completa sin hardware

Esta prueba no abre ningún puerto.

Terminal 1:

```bash
source /opt/ros/lyrical/setup.bash
source ~/ros2_lyrical/7dof_ws/install/setup.bash

ros2 launch arm7_control arm7_system.launch.py \
  use_hardware:=false
```

Debe abrirse la GUI.

En terminal debe aparecer información similar a:

```text
Modo sin hardware activo.
Configuración: 9 motores físicos / 8 articulaciones lógicas.
Distribución: 1-3 MX-64, 4-6 MX-28, 7-9 AX-12A.
joint2: ID 2 signo +1 / ID 3 signo -1.
```

En otra terminal:

```bash
source /opt/ros/lyrical/setup.bash
source ~/ros2_lyrical/7dof_ws/install/setup.bash

ros2 node list
```

Debes ver:

```text
/arm7_controller
/arm7_gui
```

---

# 17. Práctica 2: uso de la interfaz gráfica

La GUI muestra 8 controles:

```text
joint1
joint2
joint3
joint4
joint5
joint6
joint7
gripper
```

Cada slider trabaja inicialmente en un rango conservador.

Al soltar el slider se publica el comando.

## `joint2`

Solo existe un slider.

Moverlo a:

```text
+10°
```

equivale internamente a:

```text
ID2 -> +10°
ID3 -> -10°
```

La GUI también incluye:

- posición actual;
- HOME;
- Torque ON;
- Torque OFF;
- PARADA DE SOFTWARE;
- Moving Speed;
- envío de todas las articulaciones.

---

# 18. Práctica 3: verificar el comportamiento de `joint2`

Mantén:

```text
use_hardware:=false
```

Abre otra terminal:

```bash
source /opt/ros/lyrical/setup.bash
source ~/ros2_lyrical/7dof_ws/install/setup.bash

ros2 topic echo /arm7/motor_positions_raw
```

El array corresponde a:

```text
[ID1, ID2, ID3, ID4, ID5, ID6, ID7, ID8, ID9]
```

Con `joint2 = 0°` los valores de referencia son:

```text
ID2 = 1947
ID3 = 2000
```

Mueve `joint2` positivamente.

La condición esperada es:

```text
ID2 > 1947
ID3 < 2000
```

Ejemplo conceptual:

```text
joint2 = +θ

ID2 = center_2 + Δ
ID3 = center_3 - Δ
```

Mueve `joint2` negativamente.

Ahora:

```text
ID2 < 1947
ID3 > 2000
```

Esta prueba debe realizarse antes del robot real.

---

# 19. Práctica 4: inspección de ROS 2

## Nodos

```bash
ros2 node list
```

## Tópicos

```bash
ros2 topic list -t
```

## Estado articular lógico

```bash
ros2 topic echo /joint_states
```

Debe contener 8 nombres.

## Estado físico RAW

```bash
ros2 topic echo /arm7/motor_positions_raw
```

Debe contener 9 enteros.

## Servicios

```bash
ros2 service list | grep arm7
```

## Información del comando

```bash
ros2 topic info /arm7/command -v
```

---

# 20. Práctica 5: detectar el puerto e IDs DYNAMIXEL

Detén primero cualquier controlador que esté usando el bus.

Comprueba el dispositivo:

```bash
ls /dev/ttyUSB* 2>/dev/null
ls /dev/ttyACM* 2>/dev/null
```

Si el adaptador es `/dev/ttyUSB0`:

```bash
source /opt/ros/lyrical/setup.bash
source ~/ros2_lyrical/7dof_ws/install/setup.bash

ros2 run arm7_control scan_dynamixel --ros-args \
  -p port:=/dev/ttyUSB0 \
  -p baudrate:=1000000 \
  -p min_id:=1 \
  -p max_id:=20
```

La condición ideal es:

```text
IDs detectados: [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

No continúes si falta un motor.

El escáner también imprime el `model_number`.

---

# 21. Práctica 6: primera conexión con el robot real

## 21.1 Antes de ejecutar

Confirma:

```bash
ls -l /dev/ttyUSB0
```

Verifica permisos:

```bash
groups
```

Verifica que los nueve IDs respondan.

Mantén:

```yaml
home_on_startup: false
```

## 21.2 Lanzar

```bash
source /opt/ros/lyrical/setup.bash
source ~/ros2_lyrical/7dof_ws/install/setup.bash

ros2 launch arm7_control arm7_system.launch.py \
  use_hardware:=true \
  port:=/dev/ttyUSB0 \
  baudrate:=1000000
```

El controlador realiza:

```text
1. comprobar que el puerto existe
2. abrir el puerto
3. configurar 1 Mbps
4. hacer ping a ID 1..9
5. abortar habilitación de torque si falta alguno
6. configurar Moving Speed
7. aplicar Torque Limit solo si se configuró
8. habilitar torque
9. preparar GroupSyncWrite
10. aceptar comandos
```

No debería moverse automáticamente al iniciar porque:

```yaml
home_on_startup: false
```

---

# 22. Práctica 7: movimiento individual de articulaciones

La primera prueba real debe hacerse con movimientos pequeños.

## `joint1`

```bash
ros2 topic pub --once \
  /arm7/command \
  sensor_msgs/msg/JointState \
  "{name: ['joint1'], position: [0.05236]}"
```

`0.05236 rad` son aproximadamente `3°`.

## `joint2`

```bash
ros2 topic pub --once \
  /arm7/command \
  sensor_msgs/msg/JointState \
  "{name: ['joint2'], position: [0.05236]}"
```

El controlador enviará automáticamente:

```text
ID2 = +3°
ID3 = -3°
```

No envíes manualmente dos nombres para los motores 2 y 3. ROS solo conoce `joint2`.

## Gripper

```bash
ros2 topic pub --once \
  /arm7/command \
  sensor_msgs/msg/JointState \
  "{name: ['gripper'], position: [0.0349]}"
```

Empieza siempre con desplazamientos mínimos.

---

# 23. Práctica 8: HOME, velocidad, torque y parada

## Cambiar Moving Speed

```bash
ros2 topic pub --once \
  /arm7/profile_velocity \
  std_msgs/msg/UInt32 \
  "{data: 20}"
```

## HOME

Esta versión incorpora el HOME actual del robot. Además, HOME se rechaza si cualquier motor está a más de `175°` de la postura registrada.

Ejecutar:

```bash
ros2 service call \
  /arm7/home \
  std_srvs/srv/Trigger \
  "{}"
```

## Torque OFF

```bash
ros2 service call \
  /arm7/torque_enable \
  std_srvs/srv/SetBool \
  "{data: false}"
```

## Torque ON

```bash
ros2 service call \
  /arm7/torque_enable \
  std_srvs/srv/SetBool \
  "{data: true}"
```

## Parada de software

```bash
ros2 service call \
  /arm7/software_stop \
  std_srvs/srv/Trigger \
  "{}"
```

Mientras la parada esté activa, los comandos nuevos se ignoran.

Para liberar la parada lógica:

```bash
ros2 service call \
  /arm7/torque_enable \
  std_srvs/srv/SetBool \
  "{data: true}"
```

---

# 24. Práctica 9: trayectoria automática

Primero sin hardware:

```bash
ros2 launch arm7_control arm7_system.launch.py \
  use_hardware:=false
```

En otra terminal:

```bash
ros2 run arm7_control trajectory_demo
```

La configuración predeterminada es deliberadamente lenta:

```text
amplitud  = 5°
frecuencia = 0.03 Hz
```

Puedes disminuirla:

```bash
ros2 run arm7_control trajectory_demo --ros-args \
  -p amplitude_deg:=3.0 \
  -p frequency_hz:=0.02
```

El gripper permanece quieto en esta demostración.

> No ejecutes esta trayectoria con hardware real hasta terminar la calibración mecánica y verificar todas las articulaciones individualmente.

---


> **Importante sobre colisiones:** estos cambios corrigen el HOME objetivo, evitan
> movimientos colaterales de articulaciones no comandadas y bloquean saltos grandes.
> Aun así, una trayectoria desde una postura arbitraria hasta HOME no puede declararse
> matemáticamente libre de colisiones sin un modelo cinemático/geométrico del robot o
> una secuencia de homing físicamente validada.

# 25. Calibración del manipulador

Los centros iniciales son:

```yaml
motor_centers:
  [1485, 1947, 2000, 1060, 2568, 3581, 151, 1023, 1021]
```

y HOME inicialmente:

```yaml
home_raw:
  [1485, 1947, 2000, 1060, 2568, 3581, 151, 1023, 1021]
```

Estos valores son referencias matemáticas, no necesariamente ceros mecánicos.

## 25.1 Qué calibrar

Para cada motor determina:

- posición RAW correspondiente a cero;
- dirección positiva;
- límites mecánicos;
- HOME seguro;
- velocidad inicial.

## 25.2 Calibración especial de `joint2`

Los motores ID 2 e ID 3 pueden tener centros físicos diferentes.

Por ejemplo:

```yaml
motor_centers:
  [2048, 2062, 2027, 2048, 2048, 2048, 512, 512, 512]
```

Con esta calibración:

```text
joint2 = +θ
```

produce:

```text
ID2 = 2062 + Δ
ID3 = 2027 - Δ
```

Por tanto no es necesario que ambos motores tengan el mismo RAW central.

---

# 26. Diagnóstico y verificación

## Ver distribución

```bash
echo $ROS_DISTRO
```

## Ver paquete

```bash
ros2 pkg prefix arm7_control
```

## Ver controlador

```bash
ros2 node info /arm7_controller
```

## Ver parámetros

```bash
ros2 param list /arm7_controller
```

## Ver IDs configurados

```bash
ros2 param get /arm7_controller motor_ids
```

## Ver modelos

```bash
ros2 param get /arm7_controller motor_models
```

## Ver signos

```bash
ros2 param get /arm7_controller motor_signs
```

Debe verse el signo negativo para el tercer motor.

## Ver estados

```bash
ros2 topic echo /joint_states
```

## Ver RAW

```bash
ros2 topic echo /arm7/motor_positions_raw
```

## Ver frecuencia

```bash
ros2 topic hz /joint_states
```

## Ver estado textual

```bash
ros2 topic echo /arm7/status
```

---

# 27. Solución de problemas

## 27.1 `Package 'arm7_control' not found`

```bash
source /opt/ros/lyrical/setup.bash
source ~/ros2_lyrical/7dof_ws/install/setup.bash
```

Si continúa:

```bash
cd ~/ros2_lyrical/7dof_ws
colcon build --symlink-install
source install/setup.bash
```

---

## 27.2 `No module named dynamixel_sdk`

```bash
sudo apt update
sudo apt install -y ros-lyrical-dynamixel-sdk
```

Después:

```bash
source /opt/ros/lyrical/setup.bash
```

Comprueba:

```bash
python3 -c "import dynamixel_sdk"
```

---

## 27.3 `/dev/ttyUSB0` no existe

Comprueba:

```bash
ls /dev/ttyUSB* 2>/dev/null
ls /dev/ttyACM* 2>/dev/null
```

En máquinas virtuales verifica que el dispositivo USB esté conectado al sistema Ubuntu invitado.

### Protección incluida en el controlador

El controlador comprueba:

```python
os.path.exists(self.port_name)
```

antes de crear comunicación real.

También mantiene:

```text
port_open = False
```

hasta que la apertura termina correctamente.

Por tanto, si el puerto no existe, **no intenta posteriormente escribir `Torque Disable` sobre un puerto inválido**.

Esto evita un error secundario del tipo:

```text
AttributeError: 'NoneType' object has no attribute 'flush'
```

---

## 27.4 `Permission denied` en `/dev/ttyUSB0`

```bash
sudo usermod -aG dialout $USER
```

Cierra sesión y vuelve a entrar.

---

## 27.5 Falta uno de los nueve motores

Ejecuta:

```bash
ros2 run arm7_control scan_dynamixel --ros-args \
  -p port:=/dev/ttyUSB0 \
  -p baudrate:=1000000 \
  -p min_id:=1 \
  -p max_id:=20
```

Si falta un ID:

- no habilites el brazo;
- revisa alimentación;
- revisa cableado;
- revisa ID;
- revisa baudrate.

El controlador real tampoco habilita torque si alguno falla durante el ping inicial.

---

## 27.6 `joint2` se mueve en sentidos incorrectos

Primero detén el robot.

La configuración esperada es:

```yaml
motor_signs:
  [1.0, 1.0, -1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]
```

Comprueba:

```bash
ros2 param get /arm7_controller motor_signs
```

No cambies ambos signos a la vez sin verificar físicamente la instalación.

---

## 27.7 Advertencia `DESACOPLE joint2`

La advertencia significa que después de invertir matemáticamente el ID 3, los dos motores no reportan el mismo ángulo lógico.

Posibles causas:

- centros mal calibrados;
- holgura;
- un motor no sigue la consigna;
- carga excesiva;
- desalineación mecánica;
- problema de alimentación;
- montaje incorrecto.

Detén el movimiento si la diferencia es grande o aumenta.

---

## 27.8 Un AX-12A se mueve demasiado

Recuerda que el AX-12A utiliza un rango RAW diferente al MX.

No intercambies perfiles.

La configuración debe ser:

```yaml
motor_models:
  [mx64, mx64, mx64, mx28, mx28, mx28, ax12a, ax12a, ax12a]
```

---

## 27.9 El brazo se mueve al arrancar

En esta guía debe permanecer:

```yaml
home_on_startup: false
```

No habilites HOME automático hasta terminar la calibración.

---

## 27.10 La GUI no abre

Comprueba:

```bash
python3 -c "import tkinter"
```

Instala:

```bash
sudo apt install -y python3-tk
```

Además necesitas una sesión gráfica válida.

---

## 27.11 Los cambios de código no aparecen

Recompila:

```bash
cd ~/ros2_lyrical/7dof_ws

source /opt/ros/lyrical/setup.bash

colcon build --symlink-install

source install/setup.bash
```

---

# 28. Actividad propuesta para estudiantes

## Parte A — Identificación

1. Conectar el adaptador.
2. Identificar el puerto.
3. Ejecutar `scan_dynamixel`.
4. Confirmar IDs 1 a 9.
5. Registrar `model_number`.

## Parte B — Validación sin hardware

1. Ejecutar `use_hardware:=false`.
2. Mover `joint1`.
3. Observar RAW.
4. Mover `joint2`.
5. demostrar que ID2 e ID3 cambian en sentidos contrarios.

## Parte C — Robot real

1. Calibrar centros.
2. Calibrar signos.
3. Probar movimientos de aproximadamente 3°.
4. Verificar `joint2`.
5. verificar gripper.
6. definir HOME.

## Parte D — ROS 2

Registrar:

- nodos;
- tópicos;
- servicios;
- `/joint_states`;
- `/arm7/motor_positions_raw`.

## Entregables

- tabla ID/modelo/articulación;
- captura del escaneo;
- archivo `mixed_arm.yaml`;
- evidencia de `joint2`;
- captura de la GUI;
- video corto del robot;
- explicación de medidas de seguridad.

---

# 29. Publicación en GitHub

Nombre recomendado:

```text
07_Rob_2026_II_ROS2_Lyrical_7DoF_Dynamixel
```

Desde la raíz del repositorio:

```bash
git status
git add .
git commit -m "Actualizar manipulador 7DoF a ROS 2 Lyrical y 9 DYNAMIXEL"
git push origin main
```

Si el repositorio fue renombrado:

```bash
git remote set-url origin \
  https://github.com/labsir-un/07_Rob_2026_II_ROS2_Lyrical_7DoF_Dynamixel.git
```

Comprueba:

```bash
git remote -v
```

---

# 30. Cambios respecto a la versión Jazzy

| Elemento | Versión anterior | Esta versión |
|---|---|---|
| Ubuntu | 24.04 | 26.04 |
| ROS 2 | Jazzy | Lyrical |
| Workspace | `ros2_jazzy/...` | `ros2_lyrical/7dof_ws` |
| Motores asumidos | no completamente definidos | 9 motores reales |
| MX-64 | no definido correctamente | IDs 1, 2 y 3 |
| MX-28 | no definido correctamente | IDs 4, 5 y 6 |
| AX-12A | no definido correctamente | IDs 7, 8 y 9 |
| Protocol | genérico | 1.0 para los 9 |
| Baudrate | genérico | 1 Mbps para los 9 |
| `joint2` | no modelada correctamente | ID2 +θ e ID3 -θ |
| GUI | no correspondía al robot | 8 sliders lógicos |
| Escritura | individual/genérica | GroupSyncWrite |
| Lectura `joint2` | no definida | promedio lógico ID2/ID3 |
| Seguridad USB | podía fallar al cerrar | cierre protegido |
| Inicio | genérico | ping 9/9 antes de torque |
| Diagnóstico | básico | RAW + sincronismo + scanner |

---


# 31. Visualización sincronizada en RViz2

El objetivo de esta integración es que **RViz represente el estado que realmente publica el controlador del robot**, no una simulación independiente.

La cadena de información queda:

```text
DYNAMIXEL físicos
      │
      │ Present Position
      ▼
arm7_controller
      │
      │ /joint_states
      ▼
robot_state_publisher
      │
      ├── /tf
      └── /tf_static
             │
             ▼
           RViz2
```

Cuando `use_hardware:=true`, `/joint_states` se construye a partir de las posiciones leídas de los DYNAMIXEL. Por tanto, si un eslabón cambia físicamente de posición, su equivalente debe cambiar también en RViz.

> **No se debe ejecutar `joint_state_publisher` ni `joint_state_publisher_gui` al mismo tiempo que `arm7_controller`**, porque el controlador ya publica `/joint_states`.

## 31.1 Mapeo de las diez mallas STL

Las mallas entregadas se utilizan así:

| STL | Link de ROS | Función |
|---|---|---|
| `01.stl` | `base_link` | Base fija |
| `02.stl` | `link1` | Eslabón posterior a `joint1` |
| `03.stl` | `link2` | Eslabón posterior a `joint2` |
| `04.stl` | `link3` | Eslabón posterior a `joint3` |
| `05.stl` | `link4` | Eslabón posterior a `joint4` |
| `06.stl` | `link5` | Eslabón posterior a `joint5` |
| `07.stl` | `link6` | Eslabón posterior a `joint6` |
| `08.stl` | `link7` | Tool y soporte final |
| `09.stl` | `finger_09` | Primer dedo |
| `10.stl` | `finger_10` | Segundo dedo |

Las mallas fueron exportadas en **milímetros** y conservan el mismo sistema de coordenadas global del ensamblaje de Inventor. El URDF utiliza:

```xml
scale="0.001 0.001 0.001"
```

para convertir milímetros a metros.

## 31.2 Centros y ejes medidos en Autodesk Inventor

Las posiciones se midieron respecto al origen global del ensamblaje:

| Joint | X [mm] | Y [mm] | Z [mm] | Eje |
|---|---:|---:|---:|---|
| `joint1` | 2.164 | 1.611 | 48.499 | Z |
| `joint2` | 2.467 | 62.611 | 148.489 | Y |
| `joint3` | 2.120 | 1.112 | 266.489 | Z |
| `joint4` | 2.251 | 32.111 | 348.579 | Y |
| `joint5` | 0.339 | 1.121 | 466.566 | Z |
| `joint6` | 0.570 | 22.850 | 521.574 | Y |
| `joint7` | -0.171 | 3.068 | 591.061 | Z |
| Driver gripper | -0.039 | 3.034 | 634.811 | Z |

Para el URDF se convierten a posiciones relativas:

| Joint | `origin xyz` relativo [m] |
|---|---|
| `joint1` | `0.002164 0.001611 0.048499` |
| `joint2` | `0.000303 0.061000 0.099990` |
| `joint3` | `-0.000347 -0.061499 0.118000` |
| `joint4` | `0.000131 0.030999 0.082090` |
| `joint5` | `-0.001912 -0.030990 0.117987` |
| `joint6` | `0.000231 0.021729 0.055008` |
| `joint7` | `-0.000741 -0.019782 0.069487` |
| `gripper` | `0.000132 -0.000034 0.043750` |

## 31.3 `joint2` en RViz

Físicamente:

```text
MX-64 ID2 ─┐
           ├── joint2
MX-64 ID3 ─┘
```

pero cinemáticamente existe un único grado de libertad:

```text
joint2
```

El controlador se encarga de:

```text
ID2 = +θ
ID3 = -θ
```

mientras RViz recibe únicamente:

```text
joint2 = θ
```

Por eso el URDF contiene **un solo `joint2`**.

## 31.4 Gripper: motor rotacional y dedos prismáticos

El AX-12A ID9 gira alrededor de Z, pero el mecanismo transforma esa rotación en movimiento lineal de los dos dedos sobre Y.

La representación en RViz es:

```text
                    gripper
                motor angular ID9
                       │
             ┌─────────┴─────────┐
             │                   │
        finger_09            finger_10
        prismatic            prismatic
            -Y                   +Y
```

Como el mecanismo es equivalente al del Pincher X100, se utiliza inicialmente:

```text
desplazamiento por dedo = 0.008 m/rad × ángulo del gripper
```

La referencia de HOME es cero, de forma que:

```text
gripper = 0 rad
```

mantiene los STL `09.stl` y `10.stl` exactamente en la posición en la que fueron exportados.

El Xacro utiliza articulaciones `mimic`, por lo que `/joint_states` solo necesita contener:

```text
gripper
```

y `robot_state_publisher` calcula el movimiento de ambos dedos.

---

# 32. Paquete `arm7_description`

Se añade un segundo paquete al workspace:

```text
~/ros2_lyrical/7dof_ws/src/
├── arm7_control/
└── arm7_description/
```

`arm7_control` continúa controlando el hardware. `arm7_description` contiene exclusivamente geometría, URDF/Xacro, TF, launch y RViz.

## 32.1 Crear el paquete

```bash
source /opt/ros/lyrical/setup.bash

cd ~/ros2_lyrical/7dof_ws/src

ros2 pkg create arm7_description   --build-type ament_python

cd arm7_description

mkdir -p meshes urdf rviz launch

rm -rf arm7_description
rm -rf test
```

La estructura final es:

```text
arm7_description/
├── package.xml
├── setup.py
├── setup.cfg
├── resource/
│   └── arm7_description
├── meshes/
│   ├── README.md
│   ├── 01.stl
│   ├── 02.stl
│   ├── 03.stl
│   ├── 04.stl
│   ├── 05.stl
│   ├── 06.stl
│   ├── 07.stl
│   ├── 08.stl
│   ├── 09.stl
│   └── 10.stl
├── urdf/
│   └── arm7.urdf.xacro
├── rviz/
│   └── arm7.rviz
└── launch/
    ├── display.launch.py
    ├── realsense.launch.py
    └── full_system.launch.py
```

## 32.2 `package.xml`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_description/package.xml
```

```xml
<?xml version="1.0"?>
<package format="3">
  <name>arm7_description</name>
  <version>0.1.0</version>
  <description>Modelo URDF/Xacro y visualización RViz2 del manipulador 7 GDL.</description>

  <maintainer email="pendiente@ejemplo.invalid">Curso de Robótica 2026-II</maintainer>
  <license>BSD-3-Clause</license>

  <exec_depend>ament_index_python</exec_depend>
  <exec_depend>arm7_control</exec_depend>
  <exec_depend>launch</exec_depend>
  <exec_depend>launch_ros</exec_depend>
  <exec_depend>robot_state_publisher</exec_depend>
  <exec_depend>rviz2</exec_depend>
  <exec_depend>tf2_ros</exec_depend>
  <exec_depend>xacro</exec_depend>
  <exec_depend>realsense2_camera</exec_depend>
  <exec_depend>realsense2_camera_msgs</exec_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>
```

## 32.3 `setup.py`

Ruta:

```text
ros2_lyrical/7dof_ws/src/arm7_description/setup.py
```

```python
from glob import glob
import os

from setuptools import setup

package_name = 'arm7_description'

setup(
    name=package_name,
    version='0.1.0',
    packages=[],
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*')),
        (os.path.join('share', package_name, 'rviz'), glob('rviz/*')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*.stl')),
        (os.path.join('share', package_name, 'meshes'), glob('meshes/*.md')),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Curso de Robótica 2026-II',
    maintainer_email='pendiente@ejemplo.invalid',
    description='Descripción RViz2 del manipulador 7 GDL.',
    license='BSD-3-Clause',
)
```

## 32.4 `setup.cfg`

```ini
[develop]
script_dir=$base/lib/arm7_description

[install]
install_scripts=$base/lib/arm7_description
```

## 32.5 `resource/arm7_description`

Crear el archivo vacío:

```bash
mkdir -p resource
touch resource/arm7_description
```

## 32.6 `meshes/README.md`

```markdown
# Mallas del manipulador 7 GDL

Copiar en esta carpeta exactamente:

- `01.stl`: base fija (`base_link`)
- `02.stl`: `link1`
- `03.stl`: `link2`
- `04.stl`: `link3`
- `05.stl`: `link4`
- `06.stl`: `link5`
- `07.stl`: `link6`
- `08.stl`: `link7` / conjunto tool
- `09.stl`: dedo del gripper
- `10.stl`: segundo dedo del gripper

Las diez mallas fueron exportadas en milímetros y conservando el mismo sistema
de coordenadas global del ensamblaje de Inventor. El Xacro aplica
`scale="0.001 0.001 0.001"`.

```

## 32.7 `urdf/arm7.urdf.xacro`

```xml
<?xml version="1.0"?>
<robot xmlns:xacro="http://www.ros.org/wiki/xacro" name="arm7">

  <!--
    Todas las mallas STL fueron exportadas en milímetros y conservando
    el mismo sistema global del ensamblaje de Inventor.
    Por eso se usa scale=0.001 y cada visual aplica el negativo de la
    posición global del frame de su articulación.
  -->

  <xacro:property name="mesh_scale" value="0.001"/>

  <!--
    Relación angular -> desplazamiento lineal de cada dedo.
    El mecanismo del gripper es equivalente al Pincher X100.
    0.008 m/rad es la relación usada para el mecanismo Pincher.
    Cambiar el signo si la apertura visual queda invertida.
  -->
  <xacro:property name="gripper_scale" value="0.008"/>

  <link name="world"/>

  <joint name="world_to_base" type="fixed">
    <parent link="world"/>
    <child link="base_link"/>
    <origin xyz="0 0 0" rpy="0 0 0"/>
  </joint>

  <!-- ========================================================== -->
  <!-- BASE FIJA - STL 01                                        -->
  <!-- ========================================================== -->
  <link name="base_link">
    <visual>
      <origin xyz="0 0 0" rpy="0 0 0"/>
      <geometry>
        <mesh filename="package://arm7_description/meshes/01.stl"
              scale="${mesh_scale} ${mesh_scale} ${mesh_scale}"/>
      </geometry>
    </visual>
  </link>

  <!-- ========================================================== -->
  <!-- JOINT 1: P=(2.164, 1.611, 48.499) mm, eje Z               -->
  <!-- ========================================================== -->
  <joint name="joint1" type="revolute">
    <parent link="base_link"/>
    <child link="link1"/>
    <origin xyz="0.002164 0.001611 0.048499" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-pi/2}" upper="${pi/2}" effort="1.0" velocity="1.0"/>
  </joint>

  <link name="link1">
    <visual>
      <origin xyz="-0.002164 -0.001611 -0.048499" rpy="0 0 0"/>
      <geometry>
        <mesh filename="package://arm7_description/meshes/02.stl"
              scale="${mesh_scale} ${mesh_scale} ${mesh_scale}"/>
      </geometry>
    </visual>
  </link>

  <!-- ========================================================== -->
  <!-- JOINT 2: P=(2.467, 62.611, 148.489) mm, eje Y             -->
  <!-- MX-64 ID2 + ID3 representan UN solo joint cinemático.      -->
  <!-- ========================================================== -->
  <joint name="joint2" type="revolute">
    <parent link="link1"/>
    <child link="link2"/>
    <origin xyz="0.000303 0.061000 0.099990" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-pi/2}" upper="${pi/2}" effort="1.0" velocity="1.0"/>
  </joint>

  <link name="link2">
    <visual>
      <origin xyz="-0.002467 -0.062611 -0.148489" rpy="0 0 0"/>
      <geometry>
        <mesh filename="package://arm7_description/meshes/03.stl"
              scale="${mesh_scale} ${mesh_scale} ${mesh_scale}"/>
      </geometry>
    </visual>
  </link>

  <!-- ========================================================== -->
  <!-- JOINT 3: P=(2.120, 1.112, 266.489) mm, eje Z              -->
  <!-- ========================================================== -->
  <joint name="joint3" type="revolute">
    <parent link="link2"/>
    <child link="link3"/>
    <origin xyz="-0.000347 -0.061499 0.118000" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-pi/2}" upper="${pi/2}" effort="1.0" velocity="1.0"/>
  </joint>

  <link name="link3">
    <visual>
      <origin xyz="-0.002120 -0.001112 -0.266489" rpy="0 0 0"/>
      <geometry>
        <mesh filename="package://arm7_description/meshes/04.stl"
              scale="${mesh_scale} ${mesh_scale} ${mesh_scale}"/>
      </geometry>
    </visual>
  </link>

  <!-- ========================================================== -->
  <!-- JOINT 4: P=(2.251, 32.111, 348.579) mm, eje Y             -->
  <!-- ========================================================== -->
  <joint name="joint4" type="revolute">
    <parent link="link3"/>
    <child link="link4"/>
    <origin xyz="0.000131 0.030999 0.082090" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-pi/2}" upper="${pi/2}" effort="1.0" velocity="1.0"/>
  </joint>

  <link name="link4">
    <visual>
      <origin xyz="-0.002251 -0.032111 -0.348579" rpy="0 0 0"/>
      <geometry>
        <mesh filename="package://arm7_description/meshes/05.stl"
              scale="${mesh_scale} ${mesh_scale} ${mesh_scale}"/>
      </geometry>
    </visual>
  </link>

  <!-- ========================================================== -->
  <!-- JOINT 5: P=(0.339, 1.121, 466.566) mm, eje Z              -->
  <!-- ========================================================== -->
  <joint name="joint5" type="revolute">
    <parent link="link4"/>
    <child link="link5"/>
    <origin xyz="-0.001912 -0.030990 0.117987" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-pi/2}" upper="${pi/2}" effort="1.0" velocity="1.0"/>
  </joint>

  <link name="link5">
    <visual>
      <origin xyz="-0.000339 -0.001121 -0.466566" rpy="0 0 0"/>
      <geometry>
        <mesh filename="package://arm7_description/meshes/06.stl"
              scale="${mesh_scale} ${mesh_scale} ${mesh_scale}"/>
      </geometry>
    </visual>
  </link>

  <!-- ========================================================== -->
  <!-- JOINT 6: P=(0.570, 22.850, 521.574) mm, eje Y             -->
  <!-- ========================================================== -->
  <joint name="joint6" type="revolute">
    <parent link="link5"/>
    <child link="link6"/>
    <origin xyz="0.000231 0.021729 0.055008" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="${-pi/2}" upper="${pi/2}" effort="1.0" velocity="1.0"/>
  </joint>

  <link name="link6">
    <visual>
      <origin xyz="-0.000570 -0.022850 -0.521574" rpy="0 0 0"/>
      <geometry>
        <mesh filename="package://arm7_description/meshes/07.stl"
              scale="${mesh_scale} ${mesh_scale} ${mesh_scale}"/>
      </geometry>
    </visual>
  </link>

  <!-- ========================================================== -->
  <!-- JOINT 7: P=(-0.171, 3.068, 591.061) mm, eje Z             -->
  <!-- ========================================================== -->
  <joint name="joint7" type="revolute">
    <parent link="link6"/>
    <child link="link7"/>
    <origin xyz="-0.000741 -0.019782 0.069487" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-pi/2}" upper="${pi/2}" effort="1.0" velocity="1.0"/>
  </joint>

  <link name="link7">
    <visual>
      <origin xyz="0.000171 -0.003068 -0.591061" rpy="0 0 0"/>
      <geometry>
        <mesh filename="package://arm7_description/meshes/08.stl"
              scale="${mesh_scale} ${mesh_scale} ${mesh_scale}"/>
      </geometry>
    </visual>
  </link>

  <!-- ========================================================== -->
  <!-- DRIVER DEL GRIPPER                                        -->
  <!-- P=(-0.039, 3.034, 634.811) mm, eje Z                     -->
  <!-- ID9 es angular, pero el mecanismo mueve los dedos en ±Y.  -->
  <!-- ========================================================== -->
  <joint name="gripper" type="revolute">
    <parent link="link7"/>
    <child link="gripper_drive_link"/>
    <origin xyz="0.000132 -0.000034 0.043750" rpy="0 0 0"/>
    <axis xyz="0 0 1"/>
    <limit lower="${-pi/2}" upper="${pi/2}" effort="1.0" velocity="1.0"/>
  </joint>

  <!-- El link es virtual: la rotación del motor no representa una pieza
       visible que deba girar completa en RViz. -->
  <link name="gripper_drive_link"/>

  <!-- ========================================================== -->
  <!-- DEDO STL 09 - desplazamiento hacia -Y para gripper positivo -->
  <!-- ========================================================== -->
  <joint name="finger_09_joint" type="prismatic">
    <parent link="link7"/>
    <child link="finger_09"/>
    <origin xyz="0.000132 -0.000034 0.043750" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.020" upper="0.020" effort="1.0" velocity="0.05"/>
    <mimic joint="gripper" multiplier="${-gripper_scale}" offset="0.0"/>
  </joint>

  <link name="finger_09">
    <visual>
      <origin xyz="0.000039 -0.003034 -0.634811" rpy="0 0 0"/>
      <geometry>
        <mesh filename="package://arm7_description/meshes/09.stl"
              scale="${mesh_scale} ${mesh_scale} ${mesh_scale}"/>
      </geometry>
    </visual>
  </link>

  <!-- ========================================================== -->
  <!-- DEDO STL 10 - desplazamiento hacia +Y para gripper positivo -->
  <!-- ========================================================== -->
  <joint name="finger_10_joint" type="prismatic">
    <parent link="link7"/>
    <child link="finger_10"/>
    <origin xyz="0.000132 -0.000034 0.043750" rpy="0 0 0"/>
    <axis xyz="0 1 0"/>
    <limit lower="-0.020" upper="0.020" effort="1.0" velocity="0.05"/>
    <mimic joint="gripper" multiplier="${gripper_scale}" offset="0.0"/>
  </joint>

  <link name="finger_10">
    <visual>
      <origin xyz="0.000039 -0.003034 -0.634811" rpy="0 0 0"/>
      <geometry>
        <mesh filename="package://arm7_description/meshes/10.stl"
              scale="${mesh_scale} ${mesh_scale} ${mesh_scale}"/>
      </geometry>
    </visual>
  </link>

</robot>
```

## 32.8 `launch/display.launch.py`

Este launch **no publica `/joint_states`**. Solamente escucha los que ya existen, genera TF y abre RViz.

```python
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import OpaqueFunction
from launch_ros.actions import Node
import xacro


def _launch_setup(context):
    del context

    share = get_package_share_directory('arm7_description')
    xacro_file = os.path.join(share, 'urdf', 'arm7.urdf.xacro')
    rviz_file = os.path.join(share, 'rviz', 'arm7.rviz')

    robot_description = xacro.process_file(xacro_file).toxml()

    return [
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='arm7_robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description,
                'publish_frequency': 30.0,
                'ignore_timestamp': False,
            }],
        ),
        Node(
            package='rviz2',
            executable='rviz2',
            name='arm7_rviz2',
            output='screen',
            arguments=['-d', rviz_file],
        ),
    ]


def generate_launch_description():
    return LaunchDescription([
        OpaqueFunction(function=_launch_setup),
    ])
```

## 32.9 `launch/realsense.launch.py`

Este launch inicia exclusivamente la Intel RealSense D435 y crea la transformación entre el frame del robot elegido por el usuario y `camera_link`.

La posición de la cámara **no puede determinarse a partir del README**. Por eso `camera_x`, `camera_y`, `camera_z`, `camera_roll`, `camera_pitch` y `camera_yaw` son parámetros externos. Los valores `0` solo verifican conectividad TF; **no representan una calibración extrínseca**.

Además, los perfiles por defecto se fijan en `640x480x6` porque esta configuración fue la más prudente para una D435 entregada a Ubuntu mediante Parallels cuando `rs-enumerate-devices` reporta `Usb Type Descriptor: 2.0`. Si se confirma USB 3.x, puede aumentarse a `640x480x30`.

```python
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    realsense_share = get_package_share_directory('realsense2_camera')
    rs_launch = os.path.join(realsense_share, 'launch', 'rs_launch.py')

    camera_driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(rs_launch),
        launch_arguments={
            'camera_namespace': 'camera',
            'camera_name': 'camera',
            'enable_color': 'true',
            'enable_depth': 'true',
            'enable_infra1': 'false',
            'enable_infra2': 'false',
            'enable_sync': LaunchConfiguration('enable_sync'),
            'align_depth.enable': LaunchConfiguration('align_depth'),
            'pointcloud.enable': LaunchConfiguration('enable_pointcloud'),
            'publish_tf': 'true',
            'initial_reset': LaunchConfiguration('initial_reset'),
            'depth_module.depth_profile': LaunchConfiguration('depth_profile'),
            'rgb_camera.color_profile': LaunchConfiguration('color_profile'),
        }.items(),
        condition=IfCondition(LaunchConfiguration('start_realsense')),
    )

    camera_to_robot_tf = Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        name='arm7_to_realsense_tf',
        output='screen',
        arguments=[
            '--x', LaunchConfiguration('camera_x'),
            '--y', LaunchConfiguration('camera_y'),
            '--z', LaunchConfiguration('camera_z'),
            '--roll', LaunchConfiguration('camera_roll'),
            '--pitch', LaunchConfiguration('camera_pitch'),
            '--yaw', LaunchConfiguration('camera_yaw'),
            '--frame-id', LaunchConfiguration('camera_parent_frame'),
            '--child-frame-id', 'camera_link',
        ],
        condition=IfCondition(LaunchConfiguration('start_realsense')),
    )

    return LaunchDescription([
        DeclareLaunchArgument('start_realsense', default_value='true'),

        # Frame rígido al que está montada la cámara.
        # world: cámara fija en el entorno.
        # link7 u otro link: cámara fijada físicamente al robot.
        DeclareLaunchArgument('camera_parent_frame', default_value='world'),

        # Extrínsecos parent -> camera_link [m, rad].
        DeclareLaunchArgument('camera_x', default_value='0.0'),
        DeclareLaunchArgument('camera_y', default_value='0.0'),
        DeclareLaunchArgument('camera_z', default_value='0.0'),
        DeclareLaunchArgument('camera_roll', default_value='0.0'),
        DeclareLaunchArgument('camera_pitch', default_value='0.0'),
        DeclareLaunchArgument('camera_yaw', default_value='0.0'),

        # Perfil seguro para Parallels/USB 2.0.
        DeclareLaunchArgument('depth_profile', default_value='640x480x6'),
        DeclareLaunchArgument('color_profile', default_value='640x480x6'),

        # Procesamiento.
        DeclareLaunchArgument('enable_sync', default_value='true'),
        DeclareLaunchArgument('align_depth', default_value='true'),
        DeclareLaunchArgument('enable_pointcloud', default_value='true'),

        # Déjalo false normalmente. Úsalo solo si la cámara quedó en un estado
        # incorrecto después de una desconexión o cierre anormal.
        DeclareLaunchArgument('initial_reset', default_value='false'),

        camera_driver,
        camera_to_robot_tf,
    ])
```

### Perfiles recomendados

**Parallels / USB 2.0 detectado:**

```text
depth_profile = 640x480x6
color_profile = 640x480x6
```

**USB 3.x confirmado y estable:**

```text
depth_profile = 640x480x30
color_profile = 640x480x30
```

No aumentes FPS solamente porque el nodo inicia. Comprueba primero la frecuencia real con `ros2 topic hz` y que no aparezcan `USB2 Limit`, `Resource temporarily unavailable` ni `uvc streamer watchdog triggered`.

## 32.10 `launch/full_system.launch.py`

Este launch inicia conjuntamente:

- `arm7_controller`;
- GUI;
- `robot_state_publisher`;
- Intel RealSense D435;
- TF extrínseco robot ↔ cámara;
- RViz2.

La inclusión de RealSense tiene una condición en el **launch padre**. Esto es importante: con `start_realsense:=false`, el sistema puede abrir robot + GUI + RViz aunque `realsense2_camera` no esté disponible en esa terminal.

```python
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    OpaqueFunction,
)
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue
import xacro


def _launch_setup(context):
    del context

    description_share = get_package_share_directory('arm7_description')
    control_share = get_package_share_directory('arm7_control')

    xacro_file = os.path.join(description_share, 'urdf', 'arm7.urdf.xacro')
    rviz_file = os.path.join(description_share, 'rviz', 'arm7.rviz')
    config_file = os.path.join(control_share, 'config', 'mixed_arm.yaml')
    realsense_launch = os.path.join(
        description_share, 'launch', 'realsense.launch.py'
    )

    robot_description = xacro.process_file(xacro_file).toxml()

    return [
        Node(
            package='arm7_control',
            executable='arm7_controller',
            name='arm7_controller',
            output='screen',
            parameters=[
                config_file,
                {
                    'use_hardware': ParameterValue(
                        LaunchConfiguration('use_hardware'),
                        value_type=bool,
                    ),
                    'port': LaunchConfiguration('port'),
                    'baudrate': ParameterValue(
                        LaunchConfiguration('baudrate'),
                        value_type=int,
                    ),
                },
            ],
        ),

        Node(
            package='arm7_control',
            executable='arm7_gui',
            name='arm7_gui',
            output='screen',
            parameters=[config_file],
            condition=IfCondition(LaunchConfiguration('start_gui')),
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='arm7_robot_state_publisher',
            output='screen',
            parameters=[{
                'robot_description': robot_description,
                'publish_frequency': 30.0,
                'ignore_timestamp': False,
            }],
        ),

        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(realsense_launch),
            launch_arguments={
                'start_realsense': 'true',
                'camera_parent_frame': LaunchConfiguration('camera_parent_frame'),
                'camera_x': LaunchConfiguration('camera_x'),
                'camera_y': LaunchConfiguration('camera_y'),
                'camera_z': LaunchConfiguration('camera_z'),
                'camera_roll': LaunchConfiguration('camera_roll'),
                'camera_pitch': LaunchConfiguration('camera_pitch'),
                'camera_yaw': LaunchConfiguration('camera_yaw'),
                'depth_profile': LaunchConfiguration('depth_profile'),
                'color_profile': LaunchConfiguration('color_profile'),
                'enable_sync': LaunchConfiguration('enable_sync'),
                'align_depth': LaunchConfiguration('align_depth'),
                'enable_pointcloud': LaunchConfiguration('enable_pointcloud'),
                'initial_reset': LaunchConfiguration('initial_reset'),
            }.items(),
            condition=IfCondition(LaunchConfiguration('start_realsense')),
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='arm7_rviz2',
            output='screen',
            arguments=['-d', rviz_file],
        ),
    ]


def generate_launch_description():
    return LaunchDescription([
        DeclareLaunchArgument('use_hardware', default_value='false'),
        DeclareLaunchArgument('port', default_value='/dev/ttyUSB0'),
        DeclareLaunchArgument('baudrate', default_value='1000000'),
        DeclareLaunchArgument('start_gui', default_value='true'),
        DeclareLaunchArgument('start_realsense', default_value='true'),

        DeclareLaunchArgument('camera_parent_frame', default_value='world'),
        DeclareLaunchArgument('camera_x', default_value='0.0'),
        DeclareLaunchArgument('camera_y', default_value='0.0'),
        DeclareLaunchArgument('camera_z', default_value='0.0'),
        DeclareLaunchArgument('camera_roll', default_value='0.0'),
        DeclareLaunchArgument('camera_pitch', default_value='0.0'),
        DeclareLaunchArgument('camera_yaw', default_value='0.0'),

        # Valores seguros para el caso Parallels/USB 2.0.
        DeclareLaunchArgument('depth_profile', default_value='640x480x6'),
        DeclareLaunchArgument('color_profile', default_value='640x480x6'),

        DeclareLaunchArgument('enable_sync', default_value='true'),
        DeclareLaunchArgument('align_depth', default_value='true'),
        DeclareLaunchArgument('enable_pointcloud', default_value='true'),
        DeclareLaunchArgument('initial_reset', default_value='false'),

        OpaqueFunction(function=_launch_setup),
    ])
```

## 32.11 `rviz/arm7.rviz`

La configuración añade tres displays de percepción: RGB, profundidad alineada y `PointCloud2`. El robot permanece en el mismo RViz y el `Fixed Frame` continúa siendo `world`.

```yaml
Panels:
  - Class: rviz_common/Displays
    Name: Displays
    Property Tree Widget:
      Expanded:
        - /Global Options1
        - /RobotModel1
        - /RealSense PointCloud1
      Splitter Ratio: 0.5
    Tree Height: 650
  - Class: rviz_common/Views
    Name: Views

Visualization Manager:
  Class: ""
  Displays:
    - Alpha: 0.5
      Cell Size: 0.05
      Class: rviz_default_plugins/Grid
      Color: 160; 160; 164
      Enabled: true
      Line Style:
        Line Width: 0.03
        Value: Lines
      Name: Grid
      Plane: XY
      Plane Cell Count: 20
      Reference Frame: world
      Value: true

    - Class: rviz_default_plugins/RobotModel
      Collision Enabled: false
      Description Source: Topic
      Description Topic:
        Depth: 5
        Durability Policy: Transient Local
        History Policy: Keep Last
        Reliability Policy: Reliable
        Value: /robot_description
      Enabled: true
      Links:
        All Links Enabled: true
        Expand Joint Details: false
        Expand Link Details: false
        Expand Tree: false
        Link Tree Style: Links in Alphabetic Order
      Name: RobotModel
      TF Prefix: ""
      Update Interval: 0
      Value: true
      Visual Enabled: true

    - Class: rviz_default_plugins/TF
      Enabled: true
      Frame Timeout: 15
      Frames:
        All Enabled: true
      Marker Scale: 0.05
      Name: TF
      Show Arrows: true
      Show Axes: true
      Show Names: false
      Update Interval: 0
      Value: true

    - Class: rviz_default_plugins/Image
      Enabled: true
      Name: RealSense RGB
      Normalize Range: true
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Best Effort
        Value: /camera/camera/color/image_raw
      Value: true

    - Class: rviz_default_plugins/Image
      Enabled: false
      Name: RealSense Depth Aligned
      Normalize Range: true
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Best Effort
        Value: /camera/camera/aligned_depth_to_color/image_raw
      Value: false

    - Alpha: 1
      Autocompute Intensity Bounds: true
      Autocompute Value Bounds:
        Max Value: 10
        Min Value: -10
        Value: true
      Axis: Z
      Channel Name: intensity
      Class: rviz_default_plugins/PointCloud2
      Color Transformer: RGB8
      Decay Time: 0
      Enabled: true
      Invert Rainbow: false
      Max Color: 255; 255; 255
      Min Color: 0; 0; 0
      Name: RealSense PointCloud
      Position Transformer: XYZ
      Queue Size: 5
      Selectable: true
      Size (Pixels): 2
      Size (m): 0.01
      Style: Points
      Topic:
        Depth: 5
        Durability Policy: Volatile
        History Policy: Keep Last
        Reliability Policy: Best Effort
        Value: /camera/camera/depth/color/points
      Use Fixed Frame: true
      Value: true

  Enabled: true

  Global Options:
    Background Color: 48; 48; 48
    Fixed Frame: world
    Frame Rate: 30

  Name: root

  Tools:
    - Class: rviz_default_plugins/Interact
      Hide Inactive Objects: true
    - Class: rviz_default_plugins/MoveCamera
    - Class: rviz_default_plugins/Select
    - Class: rviz_default_plugins/FocusCamera
    - Class: rviz_default_plugins/Measure
      Line color: 128; 128; 0

  Transformation:
    Current:
      Class: rviz_default_plugins/TF

  Views:
    Current:
      Class: rviz_default_plugins/Orbit
      Distance: 1.0
      Focal Point:
        X: 0.0
        Y: 0.0
        Z: 0.35
      Name: Current View
      Near Clip Distance: 0.01
      Pitch: 0.45
      Target Frame: world
      Yaw: 0.75
    Saved: ~
```

Si tu versión de RViz ignora alguna propiedad de QoS del archivo, agrega manualmente un display `Image` o `PointCloud2` y selecciona **Reliability = Best Effort**, que es la opción habitual para tópicos de sensores.

---

# 33. Ejecución: GUI + robot físico + RViz2

La validación debe hacerse en dos etapas: **primero el robot sin cámara** y después la integración completa de la sección 38. Esto permite separar errores de cinemática/URDF de errores USB/RealSense.

## 33.1 Copiar las mallas

```bash
cd ~/ros2_lyrical/7dof_ws/src/arm7_description/meshes
```

Copia allí:

```text
01.stl
02.stl
03.stl
04.stl
05.stl
06.stl
07.stl
08.stl
09.stl
10.stl
```

Verifica:

```bash
find . -maxdepth 1 -type f -name '*.stl' -printf '%f\n' | sort
```

## 33.2 Compilar el robot

Si todavía no completaste la instalación RealSense de la sección 36, evita que `rosdep` intente resolverla por APT:

```bash
cd ~/ros2_lyrical/7dof_ws
source /opt/ros/lyrical/setup.bash

rosdep install \
  --from-paths src \
  --ignore-src \
  --rosdistro lyrical \
  --skip-keys="realsense2_camera realsense2_camera_msgs librealsense2" \
  -r -y

colcon build --symlink-install

source install/setup.bash
```

Si ya completaste la sección 36 y `realsense-ros` está dentro de `src`, usa simplemente:

```bash
rosdep install \
  --from-paths src \
  --ignore-src \
  --rosdistro lyrical \
  --skip-keys=librealsense2 \
  -r -y

colcon build --symlink-install
source install/setup.bash
```

Valida el Xacro:

```bash
xacro \
  ~/ros2_lyrical/7dof_ws/src/arm7_description/urdf/arm7.urdf.xacro \
  > /tmp/arm7.urdf

check_urdf /tmp/arm7.urdf
```

No debe aparecer el warning `redefining global symbol: pi`; esta versión del Xacro ya no redefine `pi`.

## 33.3 Primera prueba: controlador simulado + RViz, sin D435

```bash
ros2 launch arm7_description full_system.launch.py \
  use_hardware:=false \
  start_realsense:=false
```

Debe abrir:

```text
GUI
+
RViz2
```

Mueve `joint1`: debe rotar alrededor de Z.

Mueve `joint2`: RViz debe mostrar un único `joint2`, mientras el controlador maneja internamente ID2 e ID3.

Mueve `gripper`: los STL `09.stl` y `10.stl` deben deslizarse en sentidos opuestos sobre Y.

## 33.4 Robot físico + RViz, todavía sin D435

Solo después de validar la simulación:

```bash
ros2 launch arm7_description full_system.launch.py \
  use_hardware:=true \
  port:=/dev/ttyUSB0 \
  baudrate:=1000000 \
  start_realsense:=false
```

RViz debe representar la **posición medida** publicada en `/joint_states`, no únicamente la posición solicitada desde la GUI.

## 33.5 Comprobar `/joint_states`

```bash
ros2 topic echo /joint_states
```

Deben aparecer:

```text
joint1
joint2
joint3
joint4
joint5
joint6
joint7
gripper
```

Los dedos se calculan mediante `mimic`.

## 33.6 Comprobar TF

```bash
ros2 topic hz /tf
ros2 run tf2_tools view_frames
```

El árbol del robot debe ser conceptualmente:

```text
world
  └── base_link
      └── link1
          └── link2
              └── link3
                  └── link4
                      └── link5
                          └── link6
                              └── link7
                                  ├── gripper_drive_link
                                  ├── finger_09
                                  └── finger_10
```

Cuando esta etapa esté correcta, continúa con la instalación y prueba de la D435 en la sección 36.

# 34. Ajuste y validación del modelo en RViz

Las posiciones y ejes del URDF provienen de las mediciones del ensamblaje, pero el **signo del eje** debe comprobarse comparando movimiento físico y movimiento visual.

## 34.1 Si una articulación gira al revés en RViz

Ejemplo: si `joint4` se mueve físicamente hacia un lado pero RViz hacia el contrario, cambia únicamente:

```xml
<axis xyz="0 1 0"/>
```

por:

```xml
<axis xyz="0 -1 0"/>
```

No cambies `motor_signs` para corregir un problema exclusivamente visual. `motor_signs` define la relación controlador-motor; `<axis>` define la relación cinemática del URDF.

Verifica una articulación a la vez:

```text
joint1 -> Z
joint2 -> Y
joint3 -> Z
joint4 -> Y
joint5 -> Z
joint6 -> Y
joint7 -> Z
```

## 34.2 Si el gripper abre al revés en RViz

En:

```text
arm7_description/urdf/arm7.urdf.xacro
```

busca:

```xml
<xacro:property name="gripper_scale" value="0.008"/>
```

Si la dirección visual resulta opuesta a la física, cambia únicamente a:

```xml
<xacro:property name="gripper_scale" value="-0.008"/>
```

## 34.3 Si el recorrido visual del gripper es diferente

El valor `0.008 m/rad` reproduce la relación utilizada por el mecanismo tipo Pincher X100.

Si después de comparar el robot real con RViz se observa que, por ejemplo, el robot desplaza cada dedo 10 mm mientras RViz desplaza 8 mm, ajusta únicamente:

```xml
<xacro:property name="gripper_scale" value="..."/>
```

La forma experimental es:

```text
gripper_scale =
desplazamiento lineal de UN dedo [m]
-----------------------------------
variación angular del ID9 [rad]
```

## 34.4 Si el robot aparece correctamente en HOME pero se separa al moverse

Eso normalmente indica una de estas causas:

- signo de eje incorrecto;
- centro de articulación incorrecto;
- STL asignado al link equivocado;
- malla exportada con un sistema de coordenadas diferente;
- un eslabón contiene piezas que realmente pertenecen a otro conjunto rígido.

En ese caso no se debe “corregir a ojo” con offsets arbitrarios. Se vuelve a medir el centro de la articulación correspondiente en Inventor.

## 34.5 Colores del modelo

STL conserva principalmente geometría y no reproduce de forma fiable las apariencias de Inventor. Por tanto, RViz puede mostrar la forma correcta pero no los colores rojo/negro/gris del ensamblaje original.

Si posteriormente se desea conservar materiales y colores, conviene exportar mallas visuales a Collada (`.dae`) o definir materiales separados en URDF.

## 34.6 Prueba recomendada de correspondencia físico-RViz

Realiza movimientos pequeños, uno por uno:

```text
HOME
↓
joint1 +5°
↓
joint1 HOME
↓
joint2 +5°
↓
joint2 HOME
...
↓
joint7 +5°
↓
gripper ±5°
```

En cada paso compara:

1. dirección física;
2. dirección en RViz;
3. centro de rotación;
4. ausencia de separación artificial entre eslabones;
5. movimiento de ambos dedos.

Solo después de verificar esta correspondencia conviene utilizar rangos grandes de la GUI.

---

---

# 35. Integración de la Intel RealSense D435

La D435 añade percepción RGB-D al manipulador. En esta guía se integran tres productos de datos:

```text
RGB                         sensor_msgs/Image
Profundidad alineada        sensor_msgs/Image
Nube de puntos 3D           sensor_msgs/PointCloud2
```

La cámara utiliza el wrapper oficial `realsense2_camera`. Con los nombres por defecto del wrapper:

```text
camera_namespace = camera
camera_name      = camera
```

el nodo se identifica como:

```text
/camera/camera
```

y los tópicos principales usados por esta guía son:

```text
/camera/camera/color/image_raw
/camera/camera/aligned_depth_to_color/image_raw
/camera/camera/depth/color/points
```

La nube de puntos solo puede dibujarse correctamente junto con el robot cuando RViz conoce una transformación completa desde el `Fixed Frame` (`world`) hasta el frame de la cámara.

## 35.1 Frames de la D435

El wrapper de RealSense publica `camera_link` como frame base de la cámara y publica las transformaciones internas hacia los sensores y sus frames ópticos.

Conceptualmente:

```text
camera_link
  ├── camera_depth_frame
  │    └── camera_depth_optical_frame
  └── camera_color_frame
       └── camera_color_optical_frame
```

Los datos de imagen utilizan la convención óptica de cámara, mientras ROS utiliza la convención de robot. El wrapper proporciona los TF internos necesarios para pasar entre ambas.

## 35.2 D435 frente a D435i

Esta guía está preparada para la **Intel RealSense D435**.

La D435 proporciona:

- profundidad estereoscópica;
- imagen RGB;
- cámaras infrarrojas;
- nube de puntos derivada de profundidad.

No se configura IMU. Si en el futuro se cambia físicamente a una **D435i**, entonces se puede ampliar el launch con acelerómetro y giroscopio.

## 35.3 Qué debe verse en RViz2

Con el sistema correctamente configurado deben coexistir:

1. modelo del manipulador;
2. árbol TF del robot;
3. árbol TF interno de RealSense;
4. imagen RGB;
5. profundidad alineada;
6. nube de puntos 3D coloreada.

La nube debe moverse junto con el frame padre si la D435 está montada sobre un eslabón móvil del robot.

---

# 36. Instalación y prueba independiente de la D435

Esta sección recoge la **ruta que realmente funcionó** en el entorno del proyecto. No depende de que exista `ros-lyrical-realsense2-camera` en APT.

La cadena validada es:

```text
D435 física
   ↓ USB passthrough directo
Ubuntu invitado
   ↓
librealsense 2.58.3
   ↓
realsense-ros (el nodo validado reportó v4.58.4)
   ↓
ROS 2 Lyrical
```

## 36.1 Verificar el sistema real

No deduzcas la versión de Ubuntu a partir del hostname.

```bash
cat /etc/os-release | grep -E 'PRETTY_NAME|VERSION_CODENAME|UBUNTU_CODENAME'
echo "ROS_DISTRO=$ROS_DISTRO"
```

Para el entorno principal de esta guía se espera ROS 2 Lyrical sobre Ubuntu Resolute 26.04.

> Un prompt como `ubuntu-24-04@...` puede ser simplemente un hostname heredado. La fuente de verdad es `/etc/os-release`.

## 36.2 Parallels: entregar la D435 como USB real

Antes de probar ROS, Ubuntu debe ver el VID/PID real de la cámara.

### Estado incorrecto: cámara virtualizada por Parallels

Si:

```bash
lsusb
```

muestra algo similar a:

```text
203a:fff9 PARALLELS Intel(R) RealSense(TM) Depth Camera 435 ...
```

`librealsense` puede no reconocerla como una D435 real.

En Parallels:

1. abre **Parallels Desktop Preferences → Devices**;
2. desbloquea los cambios;
3. elimina una asignación permanente de la D435 a **Your Mac**, si existe;
4. deja **Ask me what to do**;
5. con Ubuntu encendido, desconecta y vuelve a conectar físicamente la D435;
6. asígnala a la máquina virtual Ubuntu, no al Mac;
7. también puedes comprobarlo desde **Devices → USB & Bluetooth**.

### Estado correcto

Después:

```bash
lsusb
```

debe mostrar la cámara física. Para una D435 como la usada en este proyecto:

```text
8086:0b07 Intel Corp. RealSense D435
```

Comprueba también la velocidad:

```bash
lsusb -t
```

- `5000M` o superior: USB 3.x, recomendado.
- `480M`: USB 2.0; la cámara puede detectarse, pero hay que reducir resolución/FPS.

> En la validación realizada, el passthrough directo corrigió la detección (`8086:0b07`), pero `rs-enumerate-devices` siguió reportando `Usb Type Descriptor: 2.0`. Por eso esta guía incluye un perfil conservador de 6 Hz.

## 36.3 Compilar e instalar `librealsense 2.58.3`

Instala dependencias:

```bash
sudo apt update

sudo apt install -y \
  git \
  cmake \
  build-essential \
  pkg-config \
  libusb-1.0-0-dev \
  libudev-dev \
  libssl-dev \
  libgtk-3-dev \
  libglfw3-dev \
  libgl1-mesa-dev \
  libglu1-mesa-dev \
  v4l-utils
```

`v4l-utils` es necesario porque `setup_udev_rules.sh` comprueba `v4l2-ctl`.

Clona el SDK y fija la versión:

```bash
cd ~

git clone https://github.com/realsenseai/librealsense.git
cd ~/librealsense

git fetch --tags
git checkout v2.58.3
```

El mensaje de Git:

```text
You are in 'detached HEAD' state
```

es normal al hacer checkout de una etiqueta y **no es un error**.

Instala las reglas udev:

```bash
cd ~/librealsense
sudo ./scripts/setup_udev_rules.sh
```

Si el script pide retirar las cámaras RealSense, desconéctala, continúa y vuelve a conectarla cuando termine.

Compila con backend RSUSB. Esta ruta evita depender de parches específicos de `uvcvideo` y resultó apropiada para la VM:

```bash
cd ~/librealsense

rm -rf build
mkdir build
cd build

cmake .. \
  -DCMAKE_BUILD_TYPE=Release \
  -DFORCE_RSUSB_BACKEND=ON \
  -DBUILD_EXAMPLES=OFF \
  -DBUILD_GRAPHICAL_EXAMPLES=OFF \
  -DBUILD_WITH_DDS=OFF
```

En una VM usa paralelismo moderado:

```bash
make -j2
```

Instala:

```bash
sudo make install
sudo ldconfig
```

Verifica:

```bash
pkg-config --modversion realsense2
find /usr/local -name 'realsense2Config.cmake' 2>/dev/null
```

La configuración validada debe mostrar:

```text
2.58.3
```

y una ruta como:

```text
/usr/local/lib/cmake/realsense2/realsense2Config.cmake
```

## 36.4 Verificar la D435 fuera de ROS

Con la cámara asignada directamente a Ubuntu:

```bash
lsusb | grep -i -E '8086|RealSense'
rs-enumerate-devices
```

Debes obtener información de la D435, incluido:

```text
Name            : RealSense D435
Product Id      : 0B07
Product Line    : D400
```

Fíjate especialmente en:

```text
Usb Type Descriptor
```

Si indica `2.0`, usa los perfiles conservadores de esta guía.

> `Camera Locked: YES` no impidió el uso normal de la D435 en esta integración.

## 36.5 Añadir `diagnostic_updater` al workspace

Durante la compilación del wrapper se verificó que `realsense2_camera` necesita `diagnostic_updater`.

Para no traer y compilar innecesariamente todos los paquetes del repositorio `diagnostics`, usa sparse checkout:

```bash
cd ~/ros2_lyrical/7dof_ws/src

git clone \
  --filter=blob:none \
  --no-checkout \
  -b ros2 \
  https://github.com/ros/diagnostics.git \
  diagnostics

cd diagnostics
git sparse-checkout init --cone
git sparse-checkout set diagnostic_updater
git checkout ros2
```

Comprueba:

```bash
ls ~/ros2_lyrical/7dof_ws/src/diagnostics/diagnostic_updater
```

Si ya habías clonado el repositorio `diagnostics` completo y compila correctamente, no es necesario repetir este paso.

## 36.6 Añadir `realsense-ros`

```bash
cd ~/ros2_lyrical/7dof_ws/src

git clone \
  -b ros2-master \
  https://github.com/realsenseai/realsense-ros.git
```

En el entorno validado, el nodo resultante reportó:

```text
RealSense ROS v4.58.4
Built with LibRealSense v2.58.3
Running with LibRealSense v2.58.3
```

Para un repositorio de curso/proyecto conviene registrar el commit utilizado:

```bash
cd ~/ros2_lyrical/7dof_ws/src/realsense-ros
git rev-parse HEAD
```

Así una actualización futura de `ros2-master` no vuelve irreproducible la guía.

## 36.7 Resolver dependencias

```bash
cd ~/ros2_lyrical/7dof_ws

source /opt/ros/lyrical/setup.bash

rosdep update

rosdep install \
  --from-paths src \
  --ignore-src \
  --rosdistro lyrical \
  --skip-keys=librealsense2 \
  -r -y
```

`--ignore-src` es importante porque `diagnostic_updater` y `realsense2_camera` ya están dentro del workspace.

Si APT está ocupado por `unattended-upgr`, no elimines manualmente `/var/lib/dpkg/lock-frontend`. Espera a que termine y comprueba:

```bash
ps aux | grep -E 'apt|dpkg|unattended' | grep -v grep
```

Cuando no haya un proceso activo:

```bash
sudo dpkg --configure -a
```

y repite `rosdep`.

## 36.8 Compilar el workspace completo

Asegura que CMake pueda encontrar `/usr/local`:

```bash
export CMAKE_PREFIX_PATH=/usr/local:$CMAKE_PREFIX_PATH
```

Compila:

```bash
cd ~/ros2_lyrical/7dof_ws
source /opt/ros/lyrical/setup.bash

colcon build --symlink-install
```

Una compilación correcta puede mostrar warnings C++20 o de headers TF2 deprecados en `realsense2_camera`. Si el resumen termina con:

```text
Summary: ... packages finished
```

y **no** aparece `Failed <<< realsense2_camera`, esos warnings no bloquean el uso.

Después, obligatorio:

```bash
source ~/ros2_lyrical/7dof_ws/install/setup.bash
```

Verifica:

```bash
ros2 pkg prefix realsense2_camera
ros2 pkg prefix realsense2_camera_msgs
ros2 pkg prefix realsense2_description
```

## 36.9 Prueba ROS mínima: primero sin point cloud

Si `Usb Type Descriptor` es `2.0`, no empieces con 15 o 30 Hz.

Primera prueba:

```bash
source /opt/ros/lyrical/setup.bash
source ~/ros2_lyrical/7dof_ws/install/setup.bash

ros2 launch realsense2_camera rs_launch.py \
  pointcloud.enable:=false \
  align_depth.enable:=false \
  depth_module.depth_profile:=640x480x6 \
  rgb_camera.color_profile:=640x480x6
```

En otra terminal:

```bash
source /opt/ros/lyrical/setup.bash
source ~/ros2_lyrical/7dof_ws/install/setup.bash

ros2 topic hz /camera/camera/color/image_raw
ros2 topic hz /camera/camera/depth/image_rect_raw
```

Si ambos streams son estables, prueba profundidad alineada:

```bash
ros2 launch realsense2_camera rs_launch.py \
  pointcloud.enable:=false \
  align_depth.enable:=true \
  depth_module.depth_profile:=640x480x6 \
  rgb_camera.color_profile:=640x480x6
```

Finalmente prueba la nube:

```bash
ros2 launch realsense2_camera rs_launch.py \
  pointcloud.enable:=true \
  align_depth.enable:=true \
  depth_module.depth_profile:=640x480x6 \
  rgb_camera.color_profile:=640x480x6
```

Comprueba:

```bash
ros2 topic hz /camera/camera/depth/color/points
```

## 36.10 Perfil USB 3.x

Solo si:

```bash
lsusb -t
```

muestra USB 3.x y `rs-enumerate-devices` no reporta `Usb Type Descriptor: 2.0`, sube gradualmente:

```bash
ros2 launch realsense2_camera rs_launch.py \
  pointcloud.enable:=true \
  align_depth.enable:=true \
  depth_module.depth_profile:=640x480x30 \
  rgb_camera.color_profile:=640x480x30
```

No uses 30 Hz como prueba inicial dentro de Parallels.

## 36.11 Interpretación de mensajes observados

### Mensaje normal

```text
No valid configuration file found at ~/.realsense-config.json loading defaults
```

Solo indica que no proporcionaste un JSON personalizado.

### Mensajes que sí requieren atención

```text
Device USB type: 2.0
Device ... is connected using a 2.0 port
Hardware Notification: USB2 Limit
control_transfer returned error ... Resource temporarily unavailable
uvc streamer watchdog triggered
```

En conjunto indican un problema de transporte/ancho de banda USB, especialmente dentro de una VM. Reduce FPS/resolución y desactiva temporalmente `pointcloud`/`align_depth` para aislar el problema.

### Nodo correcto

La línea:

```text
RealSense Node Is Up!
```

confirma que el nodo arrancó, pero no garantiza por sí sola que los streams sean estables. Siempre confirma con `ros2 topic hz`.

## 36.12 D435, no D435i

La D435 usada aquí no requiere configuración de IMU. No actives `enable_gyro` ni `enable_accel` salvo que cambies físicamente a una variante con IMU.

# 37. TF entre la D435 y el robot

Esta es la parte más importante para combinar la cámara con el manipulador.

El wrapper conoce la geometría **interna** de la D435, pero no puede saber dónde la instalaste respecto al robot.

Por ello debes aportar:

```text
parent_frame -> camera_link
```

## 37.1 Cámara fija fuera del robot

Si la D435 está sobre un trípode, mesa o estructura fija, usa:

```text
camera_parent_frame = world
```

Ejemplo de ejecución, una vez medidas las distancias y orientación:

```bash
ros2 launch arm7_description full_system.launch.py \
  use_hardware:=false \
  camera_parent_frame:=world \
  camera_x:=0.40 \
  camera_y:=0.10 \
  camera_z:=0.65 \
  camera_roll:=0.0 \
  camera_pitch:=0.0 \
  camera_yaw:=0.0
```

Los números anteriores son **solo un ejemplo de sintaxis**. No deben copiarse como calibración real.

## 37.2 Cámara montada sobre el manipulador

Si la D435 se desplaza con el extremo del brazo, usa como padre el link rígido al que esté atornillada.

Por ejemplo, si realmente está fijada a `link7`:

```bash
ros2 launch arm7_description full_system.launch.py \
  use_hardware:=false \
  camera_parent_frame:=link7 \
  camera_x:=0.0 \
  camera_y:=0.0 \
  camera_z:=0.0 \
  camera_roll:=0.0 \
  camera_pitch:=0.0 \
  camera_yaw:=0.0
```

Los ceros permiten validar conectividad TF, pero después deben sustituirse por la pose física medida.

## 37.3 Qué significan los seis parámetros

```text
camera_x      [m]
camera_y      [m]
camera_z      [m]
camera_roll   [rad]
camera_pitch  [rad]
camera_yaw    [rad]
```

Representan la transformación rígida:

```text
camera_parent_frame -> camera_link
```

## 37.4 Cómo validar el TF

Con el sistema activo:

```bash
ros2 run tf2_ros tf2_echo world camera_link
```

Si la cámara está montada en `link7`, también puedes comprobar:

```bash
ros2 run tf2_ros tf2_echo link7 camera_link
```

Debe existir una transformación continua y sin errores.

Para generar el árbol:

```bash
ros2 run tf2_tools view_frames
```

Conceptualmente debe quedar:

```text
world
  └── base_link
      └── ...
          └── link7
               └── camera_link        <- si la cámara está montada en link7
                    ├── camera_depth_frame
                    │    └── camera_depth_optical_frame
                    └── camera_color_frame
                         └── camera_color_optical_frame
```

Si la cámara es externa, `camera_link` será otro hijo de `world` y no de `link7`.

---

# 38. Ejecución del sistema completo con cámara

Antes de esta sección deben cumplirse las siguientes condiciones:

```text
ros2 pkg prefix arm7_control          ✓
ros2 pkg prefix arm7_description      ✓
ros2 pkg prefix realsense2_camera     ✓
rs-enumerate-devices                  ✓ detecta D435
```

Y en Parallels:

```text
lsusb -> 8086:0b07 Intel Corp. RealSense D435
```

no:

```text
203a:fff9 PARALLELS ...
```

## 38.1 Robot simulado + D435 + RViz2

Para el entorno Parallels/USB 2.0 validado:

```bash
cd ~/ros2_lyrical/7dof_ws

source /opt/ros/lyrical/setup.bash
source install/setup.bash

ros2 launch arm7_description full_system.launch.py \
  use_hardware:=false \
  start_realsense:=true \
  camera_parent_frame:=world \
  depth_profile:=640x480x6 \
  color_profile:=640x480x6 \
  enable_pointcloud:=true \
  align_depth:=true
```

Debe abrir:

```text
GUI del brazo
+
RealSense D435
+
RViz2
```

En RViz comprueba:

- `RobotModel`: visible;
- `RealSense RGB`: recibe imagen;
- `RealSense PointCloud`: recibe nube;
- `TF`: no tiene frames huérfanos relacionados con la cámara.

Si la nube no es estable, vuelve temporalmente a:

```bash
ros2 launch arm7_description full_system.launch.py \
  use_hardware:=false \
  start_realsense:=true \
  enable_pointcloud:=false \
  align_depth:=false \
  depth_profile:=640x480x6 \
  color_profile:=640x480x6
```

y vuelve a activar cada procesamiento por separado.

## 38.2 USB 3.x confirmado

Si la cámara trabaja realmente como USB 3.x:

```bash
ros2 launch arm7_description full_system.launch.py \
  use_hardware:=false \
  start_realsense:=true \
  depth_profile:=640x480x30 \
  color_profile:=640x480x30 \
  enable_pointcloud:=true \
  align_depth:=true
```

Confirma la frecuencia real antes de pasar al robot físico.

## 38.3 Robot real + cámara real + RViz2

Solo después de validar por separado:

1. DYNAMIXEL;
2. RViz del robot;
3. D435;
4. TF cámara↔robot.

Ejemplo conservador:

```bash
ros2 launch arm7_description full_system.launch.py \
  use_hardware:=true \
  port:=/dev/ttyUSB0 \
  baudrate:=1000000 \
  start_realsense:=true \
  camera_parent_frame:=world \
  depth_profile:=640x480x6 \
  color_profile:=640x480x6
```

Sustituye `camera_parent_frame` y los seis extrínsecos por la geometría real del montaje.

## 38.4 Ejecutar el robot sin cámara

```bash
ros2 launch arm7_description full_system.launch.py \
  use_hardware:=false \
  start_realsense:=false
```

Gracias a la condición del launch padre, RealSense no se intenta cargar en este modo.

## 38.5 Ejecutar únicamente la D435 con el launch del proyecto

```bash
source /opt/ros/lyrical/setup.bash
source ~/ros2_lyrical/7dof_ws/install/setup.bash

ros2 launch arm7_description realsense.launch.py \
  start_realsense:=true \
  camera_parent_frame:=world \
  depth_profile:=640x480x6 \
  color_profile:=640x480x6
```

En otra terminal puedes abrir RViz:

```bash
source /opt/ros/lyrical/setup.bash
source ~/ros2_lyrical/7dof_ws/install/setup.bash

rviz2 -d $(ros2 pkg prefix arm7_description)/share/arm7_description/rviz/arm7.rviz
```

El `RobotModel` puede aparecer en error si no está activo `robot_state_publisher`; los displays de cámara siguen siendo válidos para diagnóstico.

# 39. Diagnóstico de la RealSense en ROS 2 y RViz2

Sigue el diagnóstico en este orden. No recompiles ROS si el problema es USB.

## 39.1 `No RealSense devices were found`

Primero:

```bash
lsusb
rs-enumerate-devices
```

### Caso A — no aparece la D435

Es un problema de conexión física/Parallels.

### Caso B — aparece como `203a:fff9 PARALLELS ...`

La cámara está virtualizada. Reasígnala como USB directo a Ubuntu.

### Caso C — aparece como `8086:0b07` pero `rs-enumerate-devices` falla

Prueba permisos:

```bash
sudo rs-enumerate-devices
```

Si con `sudo` funciona:

```bash
cd ~/librealsense
sudo ./scripts/setup_udev_rules.sh
sudo udevadm control --reload-rules
sudo udevadm trigger
```

Desconecta y reconecta la cámara.

## 39.2 `USB2 Limit`, `Resource temporarily unavailable` o watchdog UVC

Comprueba:

```bash
rs-enumerate-devices | grep -i -A2 'Usb Type'
lsusb -t
```

Si el descriptor es 2.0 o el árbol USB muestra `480M`, usa:

```bash
ros2 launch realsense2_camera rs_launch.py \
  pointcloud.enable:=false \
  align_depth.enable:=false \
  depth_module.depth_profile:=640x480x6 \
  rgb_camera.color_profile:=640x480x6
```

Después activa primero alineación y finalmente point cloud.

No interpretes `RealSense Node Is Up!` como prueba de estabilidad: verifica los tópicos con `ros2 topic hz`.

## 39.3 El nodo no se encuentra

```bash
source /opt/ros/lyrical/setup.bash
source ~/ros2_lyrical/7dof_ws/install/setup.bash

ros2 pkg prefix realsense2_camera
```

Si el paquete compiló pero no aparece, normalmente faltó `source install/setup.bash`.

## 39.4 `realsense2Config.cmake` no encontrado al compilar

Comprueba:

```bash
pkg-config --modversion realsense2
find /usr/local -name 'realsense2Config.cmake' 2>/dev/null
```

Para la instalación validada:

```text
2.58.3
/usr/local/lib/cmake/realsense2/realsense2Config.cmake
```

Si existe pero CMake no lo encuentra:

```bash
export CMAKE_PREFIX_PATH=/usr/local:$CMAKE_PREFIX_PATH
```

y recompila solamente después de verificar que la instalación del SDK está completa.

## 39.5 Falta `diagnostic_updater`

Error típico:

```text
Could not find diagnostic_updaterConfig.cmake
```

Comprueba:

```bash
ls ~/ros2_lyrical/7dof_ws/src/diagnostics/diagnostic_updater
```

Luego:

```bash
cd ~/ros2_lyrical/7dof_ws
source /opt/ros/lyrical/setup.bash
colcon build --symlink-install
source install/setup.bash
```

## 39.6 Hay RGB pero no hay nube de puntos

Comprueba:

```bash
ros2 param get /camera/camera pointcloud.enable
ros2 topic list | grep points
ros2 topic hz /camera/camera/depth/color/points
```

Si no está habilitado, inicia con:

```text
pointcloud.enable:=true
```

## 39.7 La nube existe pero RViz no la muestra

Comprueba el header:

```bash
ros2 topic echo \
  /camera/camera/depth/color/points \
  --once \
  --field header
```

Luego:

```bash
ros2 run tf2_ros tf2_echo world camera_link
```

En RViz:

```text
Fixed Frame = world
Reliability = Best Effort
Topic = /camera/camera/depth/color/points
```

## 39.8 La nube está desplazada o girada

El problema normalmente está en los extrínsecos:

```text
camera_parent_frame -> camera_link
```

Corrige solamente los valores medidos:

```text
camera_x
camera_y
camera_z
camera_roll
camera_pitch
camera_yaw
```

No “acomodes” la nube visualmente en RViz.

## 39.9 La cámara se mueve con el brazo pero la nube queda fija

Si la D435 está físicamente atornillada a un eslabón móvil, `camera_parent_frame` debe ser ese link real. Por ejemplo:

```text
camera_parent_frame = link7
```

solo si la cámara está rígidamente montada en `link7`.

## 39.10 Profundidad alineada

```bash
ros2 param get /camera/camera align_depth.enable
ros2 topic hz /camera/camera/aligned_depth_to_color/image_raw
```

## 39.11 Ver parámetros y diagnóstico

```bash
ros2 param list /camera/camera
ros2 param dump /camera/camera > realsense_d435_params.yaml
```

También puedes inspeccionar todos los tópicos:

```bash
ros2 topic list | grep /camera/camera
```

## 39.12 Warnings de compilación C++20/TF2

Warnings como:

```text
TRANSFORM_BROADCASTER_HEADER_DEPRECATION
STATIC_TRANSFORM_BROADCASTER_HEADER_DEPRECATION
implicit capture of 'this' ... deprecated in C++20
```

no impiden usar el wrapper si el resumen de `colcon` finaliza correctamente y `realsense2_camera` aparece como `Finished`.

No modifiques el código del wrapper solamente para eliminar estos warnings durante esta práctica.

# 40. Actividad de percepción propuesta

Una vez que el robot y la D435 estén correctamente sincronizados en RViz2, se propone una práctica adicional.

## Parte E — Intel RealSense D435

1. Verificar la cámara con `lsusb`.
2. Ejecutar `realsense2_camera`.
3. Registrar los tópicos RGB y depth.
4. Activar `align_depth.enable`.
5. Activar `pointcloud.enable`.
6. Visualizar RGB en RViz2.
7. Visualizar la nube de puntos.
8. Identificar `camera_link` y los frames ópticos.
9. Conectar la cámara al árbol TF del robot.
10. Medir y documentar los extrínsecos de montaje.

## Parte F — Correspondencia robot/cámara

Si la cámara está montada en el robot:

1. llevar el brazo a HOME;
2. observar la nube de puntos;
3. mover una articulación aproximadamente `+5°`;
4. comprobar que el frame de cámara se desplaza coherentemente;
5. comprobar que la nube permanece rígida respecto a la cámara y cambia respecto a `world`;
6. volver a HOME.

Si la cámara es externa, la nube debe permanecer fija respecto a `world` mientras el robot se mueve dentro de ella.

## Entregables adicionales

- captura de la imagen RGB en RViz2;
- captura de la nube de puntos;
- árbol TF generado con `view_frames`;
- tabla con `camera_parent_frame` y los seis extrínsecos medidos;
- explicación de la diferencia entre el frame ROS de la cámara y el frame óptico;
- video corto mostrando robot + nube de puntos en RViz2.

---

# 41. Bibliografía

1. ROS 2 Lyrical Documentation  
   https://docs.ros.org/en/lyrical/

2. ROS 2 Lyrical - Ubuntu Installation  
   https://docs.ros.org/en/lyrical/Installation/Ubuntu-Install-Debs.html

3. ROBOTIS - DYNAMIXEL SDK  
   https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/overview/

4. ROBOTIS - DYNAMIXEL Protocol 1.0  
   https://emanual.robotis.com/docs/en/dxl/protocol1/

5. ROBOTIS - MX-64  
   https://emanual.robotis.com/docs/en/dxl/mx/mx-64/

6. ROBOTIS - MX-28  
   https://emanual.robotis.com/docs/en/dxl/mx/mx-28/

7. ROBOTIS - AX-12A  
   https://emanual.robotis.com/docs/en/dxl/ax/ax-12a/

8. ROBOTIS - DynamixelSDK Python GroupSyncWrite  
   https://emanual.robotis.com/docs/en/software/dynamixel/dynamixel_sdk/api_reference/python/python_groupsyncwrite/

9. ROS 2 - `sensor_msgs/msg/JointState`  
   https://docs.ros.org/en/lyrical/p/sensor_msgs/msg/JointState.html

10. ROS - `robot_state_publisher`  
    https://github.com/ros/robot_state_publisher

11. Interbotix X-Series Arms - Arm Descriptions  
    https://docs.trossenrobotics.com/interbotix_xsarms_docs/ros2_packages/arm_descriptions.html

12. Referencia de gripper tipo Pincher X100 usada en la Guía 06 del curso: dos dedos prismáticos acoplados al joint angular `gripper`.

13. RealSense ROS Wrapper - repositorio oficial  
    https://github.com/realsenseai/realsense-ros

14. RealSense ROS Wrapper - parámetros, tópicos, TF y filtros  
    https://github.com/realsenseai/realsense-ros#usage

15. ROS Index - `realsense2_camera_msgs` para ROS 2 Lyrical  
    https://index.ros.org/p/realsense2_camera_msgs/

16. ROS 2 TF2 - `static_transform_publisher`  
    https://docs.ros.org/en/lyrical/Concepts/Intermediate/About-Tf2.html

17. RealSense D400 Series - documentación del producto  
    https://dev.realsenseai.com/docs

18. RealSense SDK `librealsense` - instalación y código fuente  
    https://github.com/realsenseai/librealsense

19. RealSense SDK 2.58.3 - release  
    https://github.com/realsenseai/librealsense/releases/tag/v2.58.3

20. Parallels - conexión directa de dispositivos USB a una máquina virtual  
    https://kb.parallels.com/122993

21. Parallels - preferencias y asignaciones permanentes de dispositivos USB  
    https://kb.parallels.com/120389

---

<div align="center">

### Universidad Nacional de Colombia
### Curso de Robótica 2026-II

**7 GDL + Gripper · 9 DYNAMIXEL · Intel RealSense D435 · RGB-D + PointCloud2 · ROS 2 Lyrical**

</div>

</div>
