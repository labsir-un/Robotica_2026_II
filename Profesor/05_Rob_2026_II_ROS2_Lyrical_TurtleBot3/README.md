<div align="center">
<picture>
    <source srcset="https://imgur.com/5bYAzsb.png" media="(prefers-color-scheme: dark)">
    <source srcset="https://imgur.com/Os03JoE.png" media="(prefers-color-scheme: light)">
    <img src="https://imgur.com/Os03JoE.png" alt="Escudo UNAL" width="350px">
</picture>

<h3>Curso de Robótica 2026-II</h3>

<h1>TurtleBot3 con RViz2, SLAM y Construcción de Mapas</h1>

<h2>Guía 05 - TurtleBot3 con RViz2 para ROS 2 Lyrical</h2>


<h4>Pedro Fabián Cárdenas Herrera<br>
    Manuel Felipe Carranza Montenegro</h4>

<p>
  <img alt="Ubuntu 26.04 LTS" src="https://img.shields.io/badge/Ubuntu-26.04%20LTS-E95420?logo=ubuntu&logoColor=white">
  <img alt="ROS 2 Lyrical" src="https://img.shields.io/badge/ROS%202-Lyrical-22314E?logo=ros&logoColor=white">
  <img alt="TurtleBot3" src="https://img.shields.io/badge/TurtleBot3-RViz2-2ea44f">
  <img alt="Nivel" src="https://img.shields.io/badge/Nivel-Intermedio-0969da">
</p>



</div>

<div align="justify"> 

## Tabla de contenidos

- [1. Propósito de la guía](#1-propósito-de-la-guía)
- [2. Conceptos que se van a trabajar](#2-conceptos-que-se-van-a-trabajar)
- [3. Requisitos del entorno](#3-requisitos-del-entorno)
- [4. Instalación de paquetes](#4-instalación-de-paquetes)
- [5. Estructura del repositorio](#5-estructura-del-repositorio)
- [6. Creación del workspace y paquete](#6-creación-del-workspace-y-paquete)
- [7. Código fuente completo](#7-código-fuente-completo)
  - [7.1 `package.xml`](#71-packagexml)
  - [7.2 `setup.py`](#72-setuppy)
  - [7.3 `setup.cfg`](#73-setupcfg)
  - [7.4 `resource/turtlebot3_rviz_course`](#74-resourceturtlebot3_rviz_course)
  - [7.5 `turtlebot3_rviz_course/__init__.py`](#75-turtlebot3_rviz_course__init__py)
  - [7.6 `cmd_vel_bridge.py`](#76-cmd_vel_bridgepy)
  - [7.7 `fake_laser_scan.py`](#77-fake_laser_scanpy)
  - [7.8 `square_motion.py`](#78-square_motionpy)
  - [7.9 `simple_avoidance.py`](#79-simple_avoidancepy)
  - [7.10 `map_monitor.py`](#710-map_monitorpy)
  - [7.11 `turtlebot3_rviz_tools.launch.py`](#711-tb3_rviz_toolslaunchpy)
  - [7.12 `turtlebot3_burger_lyrical.urdf`](#712-turtlebot3_burger_lyricalurdf)
  - [7.13 `turtlebot3_fake_lyrical.launch.py`](#713-turtlebot3_fake_lyricallaunchpy)
- [8. Compilación del workspace](#8-compilación-del-workspace)
- [9. Práctica 1: iniciar TurtleBot3 en RViz2](#9-práctica-1-iniciar-turtlebot3-en-rviz2)
- [10. Práctica 2: teleoperación por teclado](#10-práctica-2-teleoperación-por-teclado)
- [11. Práctica 3: inspección de nodos, tópicos y TF](#11-práctica-3-inspección-de-nodos-tópicos-y-tf)
- [12. Práctica 4: escaneo láser sintético en RViz2](#12-práctica-4-escaneo-láser-sintético-en-rviz2)
- [13. Práctica 5: SLAM y construcción del mapa](#13-práctica-5-slam-y-construcción-del-mapa)
- [14. Práctica 6: guardar el mapa](#14-práctica-6-guardar-el-mapa)
- [15. Práctica 7: cargar un mapa guardado](#15-práctica-7-cargar-un-mapa-guardado)
- [16. Práctica 8: movimiento automático](#16-práctica-8-movimiento-automático)
- [17. Práctica 9: evitación autónoma simple](#17-práctica-9-evitación-autónoma-simple)
- [18. Problemas comunes y solución](#18-problemas-comunes-y-solución)
- [19. Actividad propuesta para estudiantes](#19-actividad-propuesta-para-estudiantes)
- [20. Bibliografía](#20-bibliografía)

---

## 1. Propósito de la guía

> **Ruta utilizada en toda la guía:** `~/turtlebot3_lyrical_ws`. Esta guía usa un workspace nuevo para evitar que overlays o archivos instalados de prácticas anteriores interfieran con TurtleBot3.

Esta guía permite realizar una práctica completa con **TurtleBot3 en ROS 2 Lyrical**, usando **RViz2** como herramienta principal de visualización. El objetivo es pasar de los conceptos vistos con `turtlesim` a una plataforma móvil más cercana a la robótica real, trabajando teleoperación, odometría, transformaciones, escaneo láser, SLAM y persistencia del mapa mediante serialización del pose graph.

La guía está pensada para ejecutarse en una máquina virtual o computador con recursos limitados, por lo que se evita cargar entornos gráficos pesados y se trabaja con una arquitectura liviana basada en nodos ROS 2.

> **Regla importante:** después de cualquier `colcon build` es obligatorio cargar `~/turtlebot3_lyrical_ws/install/setup.bash` antes de ejecutar `ros2 pkg prefix`, `ros2 run` o `ros2 launch` sobre paquetes compilados en este workspace.


---

## 2. Conceptos que se van a trabajar

| Concepto | Aplicación en la práctica |
|---|---|
| **Nodo** | Programas como `turtlebot3_fake_node`, `fake_laser_scan`, `cmd_vel_bridge` y `slam_toolbox`. |
| **Tópico** | Comunicación mediante `/cmd_vel`, `/odom`, `/scan`, `/tf`, `/map`. |
| **Mensaje** | Uso de `Twist`, `Odometry`, `LaserScan` y `OccupancyGrid`. |
| **TF** | Relación entre marcos como `odom`, `base_footprint`, `base_link` y `base_scan`. |
| **Odometría** | Estimación del desplazamiento del robot a partir de su movimiento. |
| **Escaneo láser** | Lectura sintética tipo LiDAR publicada en `/scan`. |
| **SLAM** | Construcción simultánea de mapa y estimación de posición. |
| **Mapa** | Representación tipo `OccupancyGrid` publicada en `/map`; la sesión se conserva mediante serialización del pose graph de `slam_toolbox`. |

---

## 3. Requisitos del entorno

- Ubuntu 26.04 LTS.
- ROS 2 Lyrical instalado.
- Terminal con `bash`.
- RViz2 funcionando.
- Conexión a internet para instalar paquetes.

> **Compatibilidad de esta guía:** ROS 2 Lyrical utiliza Ubuntu 26.04 (`Resolute`). Los paquetes `turtlebot3_fake_node`, `turtlebot3_gazebo`, `turtlebot3_simulations` y `turtlebot3_msgs` se instalan mediante APT. `slam_toolbox` se compila desde su rama `lyrical`.

> **Modelo del robot:** `turtlebot3_description` se utiliza únicamente como fuente de las mallas 3D (`burger_base.stl`, ruedas y LiDAR). La descripción cinemática activa **no utiliza** el URDF con variables `${namespace}` de la rama Jazzy. El paquete del curso incluye un URDF explícito, sin Xacro ni placeholders, cuyos frames coinciden directamente con los que publica `turtlebot3_fake_node`.

Antes de iniciar, verifica que el entorno corresponda a Lyrical:

```bash
source /opt/ros/lyrical/setup.bash
echo $ROS_DISTRO
```

La salida esperada es:

```text
lyrical
```

---

## 4. Instalación de paquetes

### 4.1 Paquetes disponibles mediante APT

Actualiza el índice de paquetes e instala las herramientas utilizadas en la práctica:

```bash
sudo apt update
sudo apt install -y \
  git \
  libg2o-dev \
  python3-colcon-common-extensions \
  python3-rosdep \
  ros-lyrical-turtlebot3-fake-node \
  ros-lyrical-turtlebot3-msgs \
  ros-lyrical-turtlebot3-simulations \
  ros-lyrical-teleop-twist-keyboard \
  ros-lyrical-rviz2 \
  ros-lyrical-rqt-graph \
  ros-lyrical-rqt-tf-tree
```

> **No agregues `ros-lyrical-slam-toolbox` a este comando.** En ROS 2 Lyrical el código fuente de `slam_toolbox` ya dispone de rama `lyrical`, pero actualmente el paquete binario no está publicado en el repositorio APT. Si se incluye en el mismo `apt install`, APT cancela toda la operación con `Unable to locate package ros-lyrical-slam-toolbox`.

### 4.2 Instalar las mallas 3D de `turtlebot3_description`

En esta guía `turtlebot3_description` se necesita **solo para obtener las mallas 3D** del TurtleBot3 Burger. La descripción URDF que moverá RViz2 se define posteriormente dentro del paquete `turtlebot3_rviz_course` y no contiene `${namespace}`.

No es necesario descargar todo el repositorio de TurtleBot3. Se usa `git sparse-checkout` para obtener únicamente `turtlebot3_description`.

Ejecuta:

```bash
source /opt/ros/lyrical/setup.bash

mkdir -p ~/turtlebot3_lyrical_ws/src
cd ~/turtlebot3_lyrical_ws/src

git clone --depth 1 --branch jazzy --filter=blob:none --sparse \
  https://github.com/ROBOTIS-GIT/turtlebot3.git turtlebot3

cd turtlebot3
git sparse-checkout set turtlebot3_description
```

Si ya existe `~/turtlebot3_lyrical_ws/src/turtlebot3`, no vuelvas a clonarlo. Comprueba primero:

```bash
cd ~/turtlebot3_lyrical_ws/src/turtlebot3
git branch --show-current
ls
```

Instala las dependencias del paquete:

```bash
cd ~/turtlebot3_lyrical_ws

rosdep install \
  --from-paths src/turtlebot3/turtlebot3_description \
  --ignore-src \
  -r -y
```

Compila únicamente la descripción:

```bash
cd ~/turtlebot3_lyrical_ws
source /opt/ros/lyrical/setup.bash

colcon build --symlink-install --packages-select turtlebot3_description
```

> **Muy importante:** terminar `colcon build` no hace que ROS 2 detecte automáticamente el paquete en la terminal actual. Después de compilar debes cargar el **overlay** del workspace.

Carga el workspace inmediatamente después de compilar:

```bash
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash
```

Ahora sí verifica que ROS 2 encuentre el paquete:

```bash
ros2 pkg prefix turtlebot3_description
```

La salida debe ser similar a:

```text
/home/usuario/turtlebot3_lyrical_ws/install/turtlebot3_description
```

También puedes hacer una segunda comprobación:

```bash
ros2 pkg list | grep '^turtlebot3_description$'
```

Comprueba además que las mallas estén instaladas:

```bash
find "$(ros2 pkg prefix turtlebot3_description)/share/turtlebot3_description/meshes" \
  -type f | head -20
```

Deben aparecer archivos de geometría del TurtleBot3.

> El mensaje `CMake Deprecation Warning` que puede aparecer al compilar la rama `jazzy` de `turtlebot3_description` es una **advertencia**, no un error. Si `colcon` termina con `Finished <<< turtlebot3_description` y `Summary: 1 package finished`, la compilación fue correcta.

Si después de compilar aparece `Package not found`, **no repitas `rosdep install`**. Primero ejecuta exactamente:

```bash
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash
ros2 pkg prefix turtlebot3_description
```

Si aun así no aparece, comprueba que exista el resultado de compilación:

```bash
ls ~/turtlebot3_lyrical_ws/install/turtlebot3_description
```

Si esa carpeta existe, el problema es únicamente que el overlay no se había cargado en la terminal. Si no existe, vuelve a ejecutar `colcon build --symlink-install --packages-select turtlebot3_description`.

### 4.3 Instalar `slam_toolbox` desde código fuente

Crea el workspace si todavía no existe y clona específicamente la rama de ROS 2 Lyrical:

```bash
source /opt/ros/lyrical/setup.bash

mkdir -p ~/turtlebot3_lyrical_ws/src
cd ~/turtlebot3_lyrical_ws/src

git clone --branch lyrical --depth 1 \
  https://github.com/SteveMacenski/slam_toolbox.git
```

Si ya existe la carpeta `slam_toolbox`, no vuelvas a clonarla. Puedes verificar la rama con:

```bash
cd ~/turtlebot3_lyrical_ws/src/slam_toolbox
git branch --show-current
```

La salida esperada es:

```text
lyrical
```

Inicializa `rosdep` si es la primera vez que lo utilizas:

```bash
sudo rosdep init 2>/dev/null || true
rosdep update
```

Instala las dependencias de compilación:

```bash
cd ~/turtlebot3_lyrical_ws

rosdep install \
  --from-paths src/slam_toolbox \
  --ignore-src \
  -r -y \
  --skip-keys nav2_map_server
```

> **¿Por qué se omite `nav2_map_server`?** La rama Lyrical de `slam_toolbox` lo declara como dependencia de ejecución para el guardado tradicional de mapas mediante Navigation2. El nodo SLAM y los servicios de serialización del pose graph no necesitan `nav2_map_server` para compilar ni para las actividades de esta guía.

Compila `slam_toolbox`:

```bash
cd ~/turtlebot3_lyrical_ws
source /opt/ros/lyrical/setup.bash

colcon build --symlink-install --packages-select slam_toolbox
source ~/turtlebot3_lyrical_ws/install/setup.bash
```

Comprueba que ROS 2 pueda localizarlo:

```bash
ros2 pkg prefix slam_toolbox
```

Debe mostrar una ruta similar a:

```text
/home/usuario/turtlebot3_lyrical_ws/install/slam_toolbox
```

También puedes comprobar sus ejecutables:

```bash
ros2 pkg executables slam_toolbox
```

### 4.4 Configurar TurtleBot3

Configura el modelo del robot:

```bash
grep -qxF 'export TURTLEBOT3_MODEL=burger' ~/.bashrc || \
  echo 'export TURTLEBOT3_MODEL=burger' >> ~/.bashrc
source ~/.bashrc
```

> Para esta guía se recomienda `burger`, porque es el modelo más simple para clase.

Comprueba los paquetes principales:

```bash
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash

ros2 pkg prefix turtlebot3_fake_node
ros2 pkg prefix turtlebot3_description
ros2 pkg prefix slam_toolbox
ros2 pkg prefix teleop_twist_keyboard
```

---

## 5. Estructura del repositorio

La estructura del repositorio queda así:

```text
TurtleBot3_RViz2_SLAM_Lyrical/
  README.md
  turtlebot3_ws/
    src/
      turtlebot3/
        turtlebot3_description/
          # URDF/Xacro y mallas 3D del robot
      slam_toolbox/
        # Código fuente, rama lyrical
      turtlebot3_rviz_course/
        package.xml
        setup.py
        setup.cfg
        resource/
          turtlebot3_rviz_course
        launch/
          turtlebot3_rviz_tools.launch.py
          turtlebot3_fake_lyrical.launch.py
        urdf/
          turtlebot3_burger_lyrical.urdf
        maps/
          .gitkeep
        turtlebot3_rviz_course/
          __init__.py
          cmd_vel_bridge.py
          fake_laser_scan.py
          square_motion.py
          simple_avoidance.py
          map_monitor.py
```

Todo el código fuente necesario está incluido directamente en este README para que el material sea auditable, editable y fácil de reconstruir.

---

## 6. Creación del workspace y paquete

Si quieres recrear el proyecto desde cero, ejecuta:

```bash
source /opt/ros/lyrical/setup.bash

mkdir -p ~/turtlebot3_lyrical_ws/src
cd ~/turtlebot3_lyrical_ws/src

ros2 pkg create turtlebot3_rviz_course \
  --build-type ament_python \
  --dependencies rclpy geometry_msgs nav_msgs sensor_msgs std_msgs visualization_msgs

mkdir -p turtlebot3_rviz_course/launch
mkdir -p turtlebot3_rviz_course/urdf
mkdir -p turtlebot3_rviz_course/maps
mkdir -p turtlebot3_rviz_course/resource
mkdir -p turtlebot3_rviz_course/turtlebot3_rviz_course

touch turtlebot3_rviz_course/resource/turtlebot3_rviz_course
touch turtlebot3_rviz_course/turtlebot3_rviz_course/__init__.py
```

Luego reemplaza los archivos con el contenido de la sección siguiente.

---

## 7. Código fuente completo

### 7.1 `package.xml`

#### `package.xml`

```xml
<?xml version="1.0"?>
<package format="3">
  <name>turtlebot3_rviz_course</name>
  <version>0.1.0</version>
  <description>Material didáctico para TurtleBot3 con RViz2, teleoperación, escaneo sintético, SLAM y guardado de mapa en ROS 2 Lyrical.</description>
  <maintainer email="manuel@example.com">Curso de Robótica 2026-II</maintainer>
  <license>MIT</license>

  <exec_depend>rclpy</exec_depend>
  <exec_depend>geometry_msgs</exec_depend>
  <exec_depend>nav_msgs</exec_depend>
  <exec_depend>sensor_msgs</exec_depend>
  <exec_depend>std_msgs</exec_depend>
  <exec_depend>visualization_msgs</exec_depend>
  <exec_depend>launch</exec_depend>
  <exec_depend>launch_ros</exec_depend>
  <exec_depend>ament_index_python</exec_depend>
  <exec_depend>robot_state_publisher</exec_depend>
  <exec_depend>rviz2</exec_depend>
  <exec_depend>turtlebot3_fake_node</exec_depend>
  <exec_depend>turtlebot3_description</exec_depend>
  <exec_depend>turtlebot3_gazebo</exec_depend>

  <test_depend>ament_copyright</test_depend>
  <test_depend>ament_flake8</test_depend>
  <test_depend>ament_pep257</test_depend>
  <test_depend>python3-pytest</test_depend>

  <export>
    <build_type>ament_python</build_type>
  </export>
</package>

```


### 7.2 `setup.py`

#### `setup.py`

```python
import os
from glob import glob
from setuptools import find_packages, setup

package_name = 'turtlebot3_rviz_course'

setup(
    name=package_name,
    version='0.1.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'urdf'), glob('urdf/*.urdf')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Curso de Robótica 2026-II',
    maintainer_email='manuel@example.com',
    description='Material didáctico para TurtleBot3 con RViz2, teleoperación, escaneo sintético, SLAM y mapas.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'cmd_vel_bridge = turtlebot3_rviz_course.cmd_vel_bridge:main',
            'fake_laser_scan = turtlebot3_rviz_course.fake_laser_scan:main',
            'square_motion = turtlebot3_rviz_course.square_motion:main',
            'simple_avoidance = turtlebot3_rviz_course.simple_avoidance:main',
            'map_monitor = turtlebot3_rviz_course.map_monitor:main',
        ],
    },
)

```


### 7.3 `setup.cfg`

#### `setup.cfg`

```ini
[develop]
script_dir=$base/lib/turtlebot3_rviz_course
[install]
install_scripts=$base/lib/turtlebot3_rviz_course

```


### 7.4 `resource/turtlebot3_rviz_course`

Este archivo debe existir aunque esté vacío:

#### `resource/turtlebot3_rviz_course`

```text

```


### 7.5 `turtlebot3_rviz_course/__init__.py`

Este archivo debe existir aunque esté vacío:

#### `turtlebot3_rviz_course/__init__.py`

```python

```


### 7.6 `cmd_vel_bridge.py`

Recibe comandos `Twist` en `/cmd_vel_raw`, limita velocidades y los republica como `Twist` en `/cmd_vel`. Esto permite centralizar la entrada de teleoperación y aplicar límites antes de enviar el comando al Fake Node.

#### `turtlebot3_rviz_course/cmd_vel_bridge.py`

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class CmdVelBridge(Node):
    def __init__(self):
        super().__init__('cmd_vel_bridge')

        self.declare_parameter('input_topic', '/cmd_vel_raw')
        self.declare_parameter('output_topic', '/cmd_vel')
        self.declare_parameter('linear_limit', 0.25)
        self.declare_parameter('angular_limit', 1.20)

        input_topic = self.get_parameter('input_topic').value
        output_topic = self.get_parameter('output_topic').value
        self.linear_limit = float(self.get_parameter('linear_limit').value)
        self.angular_limit = float(self.get_parameter('angular_limit').value)

        self.publisher = self.create_publisher(Twist, output_topic, 10)
        self.subscription = self.create_subscription(Twist, input_topic, self.callback, 10)

        self.get_logger().info(f'Escuchando {input_topic} [Twist]')
        self.get_logger().info(f'Publicando {output_topic} [Twist]')

    def clamp(self, value: float, limit: float) -> float:
        return max(-limit, min(limit, value))

    def callback(self, msg: Twist):
        safe_msg = Twist()

        safe_msg.linear.x = self.clamp(msg.linear.x, self.linear_limit)
        safe_msg.linear.y = self.clamp(msg.linear.y, self.linear_limit)
        safe_msg.linear.z = self.clamp(msg.linear.z, self.linear_limit)

        safe_msg.angular.x = self.clamp(msg.angular.x, self.angular_limit)
        safe_msg.angular.y = self.clamp(msg.angular.y, self.angular_limit)
        safe_msg.angular.z = self.clamp(msg.angular.z, self.angular_limit)

        self.publisher.publish(safe_msg)


def main(args=None):
    rclpy.init(args=args)
    node = CmdVelBridge()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        stop_msg = Twist()
        node.publisher.publish(stop_msg)
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```


### 7.7 `fake_laser_scan.py`

Publica un escaneo sintético `/scan` a partir de la odometría del robot. Esto permite explicar SLAM y construcción de mapas usando RViz2.

#### `turtlebot3_rviz_course/fake_laser_scan.py`

```python
#!/usr/bin/env python3
"""Publicador de LaserScan sintético para prácticas de SLAM con RViz2.

El nodo usa la odometría del robot para calcular intersecciones de rayos
contra un mundo 2D simple formado por paredes y obstáculos circulares.
"""

import math
from typing import List, Optional, Tuple

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point
from nav_msgs.msg import Odometry
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker, MarkerArray

Point2D = Tuple[float, float]
Segment = Tuple[Point2D, Point2D]
Circle = Tuple[float, float, float]


def yaw_from_quaternion(x: float, y: float, z: float, w: float) -> float:
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = 1.0 - 2.0 * (y * y + z * z)
    return math.atan2(siny_cosp, cosy_cosp)


def cross(a: Point2D, b: Point2D) -> float:
    return a[0] * b[1] - a[1] * b[0]


def ray_segment_distance(origin: Point2D, direction: Point2D, segment: Segment) -> Optional[float]:
    px, py = origin
    rx, ry = direction
    (ax, ay), (bx, by) = segment
    sx, sy = bx - ax, by - ay

    denominator = cross((rx, ry), (sx, sy))
    if abs(denominator) < 1e-9:
        return None

    ap = (ax - px, ay - py)
    t = cross(ap, (sx, sy)) / denominator
    u = cross(ap, (rx, ry)) / denominator

    if t >= 0.0 and 0.0 <= u <= 1.0:
        return t
    return None


def ray_circle_distance(origin: Point2D, direction: Point2D, circle: Circle) -> Optional[float]:
    ox, oy = origin
    dx, dy = direction
    cx, cy, radius = circle

    fx = ox - cx
    fy = oy - cy

    b = 2.0 * (fx * dx + fy * dy)
    c = fx * fx + fy * fy - radius * radius
    discriminant = b * b - 4.0 * c

    if discriminant < 0.0:
        return None

    sqrt_disc = math.sqrt(discriminant)
    t1 = (-b - sqrt_disc) / 2.0
    t2 = (-b + sqrt_disc) / 2.0

    candidates = [t for t in (t1, t2) if t >= 0.0]
    return min(candidates) if candidates else None


class FakeLaserScan(Node):
    def __init__(self):
        super().__init__('fake_laser_scan')

        self.declare_parameter('scan_topic', '/scan')
        self.declare_parameter('odom_topic', '/odom')
        self.declare_parameter('scan_frame', 'base_scan')
        self.declare_parameter('odom_frame', 'odom')
        self.declare_parameter('rate_hz', 10.0)
        self.declare_parameter('range_min', 0.08)
        self.declare_parameter('range_max', 6.0)
        self.declare_parameter('angle_min', -3.14159)
        self.declare_parameter('angle_max', 3.14159)
        self.declare_parameter('samples', 360)

        self.scan_topic = self.get_parameter('scan_topic').value
        self.odom_topic = self.get_parameter('odom_topic').value
        self.scan_frame = self.get_parameter('scan_frame').value
        self.odom_frame = self.get_parameter('odom_frame').value
        self.rate_hz = float(self.get_parameter('rate_hz').value)
        self.range_min = float(self.get_parameter('range_min').value)
        self.range_max = float(self.get_parameter('range_max').value)
        self.angle_min = float(self.get_parameter('angle_min').value)
        self.angle_max = float(self.get_parameter('angle_max').value)
        self.samples = int(self.get_parameter('samples').value)

        self.pose_x = 0.0
        self.pose_y = 0.0
        self.pose_yaw = 0.0
        self.has_odom = False

        # Mundo virtual 2D: paredes externas, entrantes y obstáculos circulares.
        self.walls: List[Segment] = [
            ((-3.0, -2.4), (3.0, -2.4)),
            ((3.0, -2.4), (3.0, -0.7)),
            ((3.0, -0.7), (2.45, -0.7)),
            ((2.45, -0.7), (2.45, 1.5)),
            ((2.45, 1.5), (1.2, 2.3)),
            ((1.2, 2.3), (0.0, 1.75)),
            ((0.0, 1.75), (-1.2, 2.3)),
            ((-1.2, 2.3), (-2.45, 1.5)),
            ((-2.45, 1.5), (-2.45, -0.7)),
            ((-2.45, -0.7), (-3.0, -0.7)),
            ((-3.0, -0.7), (-3.0, -2.4)),
        ]
        self.circles: List[Circle] = [
            (-1.15, 0.85, 0.18),
            (0.00, 0.85, 0.18),
            (1.15, 0.85, 0.18),
            (-1.15, -0.25, 0.18),
            (0.00, -0.25, 0.18),
            (1.15, -0.25, 0.18),
            (-1.15, -1.35, 0.18),
            (0.00, -1.35, 0.18),
            (1.15, -1.35, 0.18),
        ]

        self.scan_pub = self.create_publisher(LaserScan, self.scan_topic, 10)
        self.marker_pub = self.create_publisher(MarkerArray, '/turtlebot3_virtual_world_markers', 1)
        self.odom_sub = self.create_subscription(Odometry, self.odom_topic, self.odom_cb, 10)
        self.timer = self.create_timer(1.0 / max(self.rate_hz, 1.0), self.publish_scan)
        self.marker_timer = self.create_timer(1.0, self.publish_markers)

        self.get_logger().info(f'Publicando LaserScan sintético en {self.scan_topic}')
        self.get_logger().info(f'Leyendo odometría desde {self.odom_topic}')

    def odom_cb(self, msg: Odometry):
        self.pose_x = msg.pose.pose.position.x
        self.pose_y = msg.pose.pose.position.y
        q = msg.pose.pose.orientation
        self.pose_yaw = yaw_from_quaternion(q.x, q.y, q.z, q.w)
        self.has_odom = True

    def ray_distance(self, angle: float) -> float:
        origin = (self.pose_x, self.pose_y)
        direction = (math.cos(angle), math.sin(angle))
        best = self.range_max

        for wall in self.walls:
            distance = ray_segment_distance(origin, direction, wall)
            if distance is not None:
                best = min(best, distance)

        for circle in self.circles:
            distance = ray_circle_distance(origin, direction, circle)
            if distance is not None:
                best = min(best, distance)

        return max(self.range_min, min(self.range_max, best))

    def publish_scan(self):
        if not self.has_odom:
            return

        msg = LaserScan()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = self.scan_frame
        msg.angle_min = self.angle_min
        msg.angle_max = self.angle_max
        msg.angle_increment = (self.angle_max - self.angle_min) / max(self.samples - 1, 1)
        msg.time_increment = 0.0
        msg.scan_time = 1.0 / max(self.rate_hz, 1.0)
        msg.range_min = self.range_min
        msg.range_max = self.range_max

        ranges = []
        for i in range(self.samples):
            local_angle = self.angle_min + i * msg.angle_increment
            world_angle = self.pose_yaw + local_angle
            ranges.append(self.ray_distance(world_angle))
        msg.ranges = ranges
        self.scan_pub.publish(msg)

    def publish_markers(self):
        array = MarkerArray()
        now = self.get_clock().now().to_msg()

        walls_marker = Marker()
        walls_marker.header.stamp = now
        walls_marker.header.frame_id = self.odom_frame
        walls_marker.ns = 'virtual_world_walls'
        walls_marker.id = 0
        walls_marker.type = Marker.LINE_LIST
        walls_marker.action = Marker.ADD
        walls_marker.scale.x = 0.04
        walls_marker.color.r = 0.0
        walls_marker.color.g = 0.0
        walls_marker.color.b = 0.0
        walls_marker.color.a = 1.0

        for (x1, y1), (x2, y2) in self.walls:
            p1 = Point(x=x1, y=y1, z=0.02)
            p2 = Point(x=x2, y=y2, z=0.02)
            walls_marker.points.append(p1)
            walls_marker.points.append(p2)
        array.markers.append(walls_marker)

        for idx, (x, y, radius) in enumerate(self.circles, start=1):
            marker = Marker()
            marker.header.stamp = now
            marker.header.frame_id = self.odom_frame
            marker.ns = 'virtual_world_obstacles'
            marker.id = idx
            marker.type = Marker.CYLINDER
            marker.action = Marker.ADD
            marker.pose.position.x = x
            marker.pose.position.y = y
            marker.pose.position.z = 0.15
            marker.pose.orientation.w = 1.0
            marker.scale.x = 2.0 * radius
            marker.scale.y = 2.0 * radius
            marker.scale.z = 0.30
            marker.color.r = 1.0
            marker.color.g = 1.0
            marker.color.b = 1.0
            marker.color.a = 1.0
            array.markers.append(marker)

        self.marker_pub.publish(array)


def main(args=None):
    rclpy.init(args=args)
    node = FakeLaserScan()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

```


### 7.8 `square_motion.py`

Publica comandos de velocidad para que el robot ejecute un patrón cuadrado.

#### `turtlebot3_rviz_course/square_motion.py`

```python
#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class SquareMotion(Node):
    def __init__(self):
        super().__init__('square_motion')

        self.declare_parameter('cmd_topic', '/cmd_vel')
        self.declare_parameter('forward_speed', 0.15)
        self.declare_parameter('turn_speed', 0.75)
        self.declare_parameter('forward_duration', 3.0)
        self.declare_parameter('turn_duration', 2.1)
        self.declare_parameter('rate_hz', 10.0)

        self.cmd_topic = self.get_parameter('cmd_topic').value
        self.forward_speed = float(self.get_parameter('forward_speed').value)
        self.turn_speed = float(self.get_parameter('turn_speed').value)
        self.forward_duration = float(self.get_parameter('forward_duration').value)
        self.turn_duration = float(self.get_parameter('turn_duration').value)
        self.rate_hz = float(self.get_parameter('rate_hz').value)

        self.publisher = self.create_publisher(Twist, self.cmd_topic, 10)

        self.state = 'forward'
        self.state_start = self.get_clock().now()

        self.timer = self.create_timer(
            1.0 / max(self.rate_hz, 1.0),
            self.loop
        )

        self.get_logger().info(f'Publicando comandos Twist en {self.cmd_topic}')
        self.get_logger().info('Movimiento cuadrado iniciado.')

    def elapsed(self) -> float:
        now = self.get_clock().now()
        return (now - self.state_start).nanoseconds * 1e-9

    def switch_state(self, new_state: str):
        self.state = new_state
        self.state_start = self.get_clock().now()
        self.get_logger().info(f'Cambio de estado: {self.state}')

    def publish_cmd(self, linear_x: float, angular_z: float):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.publisher.publish(msg)

    def stop_robot(self):
        self.publish_cmd(0.0, 0.0)

    def loop(self):
        if self.state == 'forward':
            self.publish_cmd(self.forward_speed, 0.0)

            if self.elapsed() >= self.forward_duration:
                self.switch_state('turn')

        elif self.state == 'turn':
            self.publish_cmd(0.0, self.turn_speed)

            if self.elapsed() >= self.turn_duration:
                self.switch_state('forward')


def main(args=None):
    rclpy.init(args=args)
    node = SquareMotion()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_robot()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```


### 7.9 `simple_avoidance.py`

Usa `/scan` para avanzar y girar cuando detecta obstáculos al frente.

#### `turtlebot3_rviz_course/simple_avoidance.py`

```python
#!/usr/bin/env python3

import math
from typing import Iterable, List

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan


class SimpleAvoidance(Node):
    def __init__(self):
        super().__init__('simple_avoidance')

        self.declare_parameter('scan_topic', '/scan')
        self.declare_parameter('cmd_topic', '/cmd_vel')
        self.declare_parameter('safe_distance', 0.55)
        self.declare_parameter('forward_speed', 0.12)
        self.declare_parameter('turn_speed', 0.70)
        self.declare_parameter('front_angle_deg', 35.0)

        self.scan_topic = self.get_parameter('scan_topic').value
        self.cmd_topic = self.get_parameter('cmd_topic').value
        self.safe_distance = float(self.get_parameter('safe_distance').value)
        self.forward_speed = float(self.get_parameter('forward_speed').value)
        self.turn_speed = float(self.get_parameter('turn_speed').value)
        self.front_angle = math.radians(
            float(self.get_parameter('front_angle_deg').value)
        )

        self.publisher = self.create_publisher(Twist, self.cmd_topic, 10)

        self.subscription = self.create_subscription(
            LaserScan,
            self.scan_topic,
            self.scan_callback,
            10
        )

        self.get_logger().info(f'Leyendo LaserScan desde {self.scan_topic}')
        self.get_logger().info(f'Publicando comandos Twist en {self.cmd_topic}')
        self.get_logger().info('Evitación autónoma simple iniciada.')

    def clean_ranges(self, ranges: Iterable[float], max_range: float) -> List[float]:
        cleaned = []

        for value in ranges:
            if math.isfinite(value):
                cleaned.append(value)
            else:
                cleaned.append(max_range)

        return cleaned

    def publish_cmd(self, linear_x: float, angular_z: float):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.publisher.publish(msg)

    def stop_robot(self):
        self.publish_cmd(0.0, 0.0)

    def scan_callback(self, msg: LaserScan):
        ranges = self.clean_ranges(msg.ranges, msg.range_max)

        front_ranges = []
        left_ranges = []
        right_ranges = []

        for i, distance in enumerate(ranges):
            angle = msg.angle_min + i * msg.angle_increment

            if abs(angle) <= self.front_angle:
                front_ranges.append(distance)

            elif self.front_angle < angle < math.pi / 2.0:
                left_ranges.append(distance)

            elif -math.pi / 2.0 < angle < -self.front_angle:
                right_ranges.append(distance)

        front_min = min(front_ranges) if front_ranges else msg.range_max
        left_min = min(left_ranges) if left_ranges else msg.range_max
        right_min = min(right_ranges) if right_ranges else msg.range_max

        if front_min < self.safe_distance:
            if left_min > right_min:
                self.publish_cmd(0.0, self.turn_speed)
                self.get_logger().info('Obstáculo al frente: girando a la izquierda')
            else:
                self.publish_cmd(0.0, -self.turn_speed)
                self.get_logger().info('Obstáculo al frente: girando a la derecha')
        else:
            self.publish_cmd(self.forward_speed, 0.0)


def main(args=None):
    rclpy.init(args=args)
    node = SimpleAvoidance()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.stop_robot()
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
```


### 7.10 `map_monitor.py`

Escucha `/map` y muestra en terminal información básica del mapa construido.

#### `turtlebot3_rviz_course/map_monitor.py`

```python
#!/usr/bin/env python3
"""Monitor didáctico para observar el crecimiento del mapa /map."""

import rclpy
from rclpy.node import Node
from nav_msgs.msg import OccupancyGrid


class MapMonitor(Node):
    def __init__(self):
        super().__init__('map_monitor')
        self.declare_parameter('map_topic', '/map')
        self.declare_parameter('print_every_n', 10)

        self.map_topic = self.get_parameter('map_topic').value
        self.print_every_n = int(self.get_parameter('print_every_n').value)
        self.counter = 0

        self.subscription = self.create_subscription(OccupancyGrid, self.map_topic, self.map_cb, 10)
        self.get_logger().info(f'Monitor escuchando {self.map_topic}')

    def map_cb(self, msg: OccupancyGrid):
        self.counter += 1
        if self.counter % max(self.print_every_n, 1) != 0:
            return

        total = len(msg.data)
        unknown = sum(1 for value in msg.data if value < 0)
        free = sum(1 for value in msg.data if value == 0)
        occupied = sum(1 for value in msg.data if value > 50)

        known = total - unknown
        known_percent = 100.0 * known / max(total, 1)

        self.get_logger().info(
            f'map: {msg.info.width}x{msg.info.height} | '
            f'resolution={msg.info.resolution:.3f} m/cell | '
            f'known={known_percent:.1f}% | free={free} | occupied={occupied}'
        )


def main(args=None):
    rclpy.init(args=args)
    node = MapMonitor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()

```


### 7.11 `turtlebot3_rviz_tools.launch.py`

Lanza las herramientas auxiliares de la guía: escaneo sintético y puente de velocidades.

#### `launch/turtlebot3_rviz_tools.launch.py`

```python
from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='turtlebot3_rviz_course',
            executable='fake_laser_scan',
            name='fake_laser_scan',
            output='screen',
            parameters=[{
                'scan_topic': '/scan',
                'odom_topic': '/odom',
                'scan_frame': 'base_scan',
                'rate_hz': 10.0,
                'range_max': 6.0,
                'samples': 360,
            }],
        ),
        Node(
            package='turtlebot3_rviz_course',
            executable='cmd_vel_bridge',
            name='cmd_vel_bridge',
            output='screen',
            parameters=[{
                'input_topic': '/cmd_vel_raw',
                'output_topic': '/cmd_vel',
                'linear_limit': 0.35,
                'angular_limit': 1.50,
            }],
        ),
    ])

```



### 7.12 `turtlebot3_burger_lyrical.urdf`

Este archivo define el árbol cinemático utilizado por RViz2. No contiene
Xacro, `namespace`, sustituciones `$(...)` ni expresiones `${...}`.

Los nombres de frames y joints coinciden con los utilizados por
`turtlebot3_fake_node`:

```text
odom
└── base_footprint
    └── base_link
        ├── wheel_left_link
        ├── wheel_right_link
        ├── caster_back_link
        ├── imu_link
        └── base_scan
```

El Fake Node publica `odom -> base_footprint` y los estados de
`wheel_left_joint` y `wheel_right_joint`. `robot_state_publisher` completa el
resto del árbol utilizando este URDF.

#### `urdf/turtlebot3_burger_lyrical.urdf`

```xml
<?xml version="1.0"?>
<robot name="turtlebot3_burger_lyrical">

  <material name="tb3_dark">
    <color rgba="0.18 0.18 0.18 1.0"/>
  </material>

  <material name="tb3_black">
    <color rgba="0.05 0.05 0.05 1.0"/>
  </material>

  <material name="tb3_sensor">
    <color rgba="0.12 0.12 0.12 1.0"/>
  </material>

  <!-- Frame de referencia móvil publicado desde odom por turtlebot3_fake_node -->
  <link name="base_footprint"/>

  <!-- Cuerpo principal -->
  <joint name="base_joint" type="fixed">
    <parent link="base_footprint"/>
    <child link="base_link"/>
    <origin xyz="0 0 0.010" rpy="0 0 0"/>
  </joint>

  <link name="base_link">
    <visual>
      <origin xyz="-0.032 0 0" rpy="0 0 0"/>
      <geometry>
        <mesh
          filename="package://turtlebot3_description/meshes/bases/burger_base.stl"
          scale="0.001 0.001 0.001"/>
      </geometry>
      <material name="tb3_dark"/>
    </visual>

    <collision>
      <origin xyz="-0.032 0 0.070" rpy="0 0 0"/>
      <geometry>
        <box size="0.140 0.140 0.143"/>
      </geometry>
    </collision>
  </link>

  <!-- Rueda izquierda -->
  <joint name="wheel_left_joint" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_left_link"/>
    <origin xyz="0 0.080 0.023" rpy="-1.5708 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

  <link name="wheel_left_link">
    <visual>
      <origin xyz="0 0 0" rpy="1.5708 0 0"/>
      <geometry>
        <mesh
          filename="package://turtlebot3_description/meshes/wheels/left_tire.stl"
          scale="0.001 0.001 0.001"/>
      </geometry>
      <material name="tb3_black"/>
    </visual>
  </link>

  <!-- Rueda derecha -->
  <joint name="wheel_right_joint" type="continuous">
    <parent link="base_link"/>
    <child link="wheel_right_link"/>
    <origin xyz="0 -0.080 0.023" rpy="-1.5708 0 0"/>
    <axis xyz="0 0 1"/>
  </joint>

  <link name="wheel_right_link">
    <visual>
      <origin xyz="0 0 0" rpy="1.5708 0 0"/>
      <geometry>
        <mesh
          filename="package://turtlebot3_description/meshes/wheels/right_tire.stl"
          scale="0.001 0.001 0.001"/>
      </geometry>
      <material name="tb3_black"/>
    </visual>
  </link>

  <!-- Apoyo trasero -->
  <joint name="caster_back_joint" type="fixed">
    <parent link="base_link"/>
    <child link="caster_back_link"/>
    <origin xyz="-0.081 0 -0.004" rpy="0 0 0"/>
  </joint>

  <link name="caster_back_link">
    <visual>
      <geometry>
        <sphere radius="0.012"/>
      </geometry>
      <material name="tb3_black"/>
    </visual>
  </link>

  <!-- IMU -->
  <joint name="imu_joint" type="fixed">
    <parent link="base_link"/>
    <child link="imu_link"/>
    <origin xyz="-0.032 0 0.068" rpy="0 0 0"/>
  </joint>

  <link name="imu_link"/>

  <!-- LiDAR -->
  <joint name="scan_joint" type="fixed">
    <parent link="base_link"/>
    <child link="base_scan"/>
    <origin xyz="-0.032 0 0.172" rpy="0 0 0"/>
  </joint>

  <link name="base_scan">
    <visual>
      <geometry>
        <mesh
          filename="package://turtlebot3_description/meshes/sensors/lds.stl"
          scale="0.001 0.001 0.001"/>
      </geometry>
      <material name="tb3_sensor"/>
    </visual>
  </link>

</robot>
```

Antes de compilar puedes comprobar que esta descripción no contiene ningún
placeholder:

```bash
grep -nE '\$\{namespace\}|\$\(arg|xacro:' \
  ~/turtlebot3_lyrical_ws/src/turtlebot3_rviz_course/urdf/turtlebot3_burger_lyrical.urdf \
  || echo "OK: URDF limpio"
```

La salida esperada es:

```text
OK: URDF limpio
```

---

### 7.13 `turtlebot3_fake_lyrical.launch.py`

Este launch utiliza exclusivamente el URDF limpio de la sección anterior.
No lee el URDF de `turtlebot3_description` ni el URDF incluido dentro de
`turtlebot3_gazebo`.

#### `launch/turtlebot3_fake_lyrical.launch.py`

```python
#!/usr/bin/env python3

import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, LogInfo
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    model = os.environ.get('TURTLEBOT3_MODEL', 'burger')

    if model != 'burger':
        raise RuntimeError(
            'Esta guía utiliza TURTLEBOT3_MODEL=burger. '
            f'Valor recibido: {model!r}'
        )

    use_sim_time = LaunchConfiguration('use_sim_time')

    course_share = get_package_share_directory(
        'turtlebot3_rviz_course'
    )
    fake_share = get_package_share_directory(
        'turtlebot3_fake_node'
    )
    gazebo_share = get_package_share_directory(
        'turtlebot3_gazebo'
    )

    urdf_file = os.path.join(
        course_share,
        'urdf',
        'turtlebot3_burger_lyrical.urdf'
    )

    param_file = os.path.join(
        fake_share,
        'param',
        'burger.yaml'
    )

    rviz_config = os.path.join(
        gazebo_share,
        'rviz',
        'tb3_gazebo.rviz'
    )

    if not os.path.isfile(urdf_file):
        raise RuntimeError(
            f'No se encontró el URDF del curso: {urdf_file}'
        )

    with open(urdf_file, 'r', encoding='utf-8') as stream:
        robot_description = stream.read()

    forbidden_tokens = (
        '${namespace}',
        '$(arg',
        '<xacro:',
    )

    for token in forbidden_tokens:
        if token in robot_description:
            raise RuntimeError(
                f'URDF inválido: quedó el marcador {token!r}'
            )

    required_frames = (
        'base_footprint',
        'base_link',
        'wheel_left_link',
        'wheel_right_link',
        'base_scan',
    )

    for frame in required_frames:
        if frame not in robot_description:
            raise RuntimeError(
                f'URDF inválido: falta el frame {frame!r}'
            )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='false',
            description='Usar reloj de simulación'
        ),

        LogInfo(
            msg=['TurtleBot3 Burger - ROS 2 Lyrical']
        ),
        LogInfo(
            msg=[f'URDF limpio: {urdf_file}']
        ),

        Node(
            package='turtlebot3_fake_node',
            executable='turtlebot3_fake_node',
            name='turtlebot3_fake_node',
            parameters=[param_file],
            output='screen'
        ),

        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            name='robot_state_publisher',
            parameters=[{
                'use_sim_time': use_sim_time,
                'robot_description': robot_description,
            }],
            output='screen'
        ),

        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config],
            output='screen'
        ),
    ])
```

Con este launch hay una sola cadena coherente de transformaciones:

```text
turtlebot3_fake_node
    │
    └── odom -> base_footprint
                     │
                     ▼
           robot_state_publisher
                     │
                     ├── base_link
                     ├── wheel_left_link
                     ├── wheel_right_link
                     ├── caster_back_link
                     ├── imu_link
                     └── base_scan
```

Por lo tanto, cuando cambia `odom -> base_footprint`, **todo el RobotModel se
desplaza con el sistema coordenado**.

---

## 8. Compilación del workspace

Compila siempre desde la raíz del workspace nuevo:

```bash
cd ~/turtlebot3_lyrical_ws

source /opt/ros/lyrical/setup.bash

rosdep update
rosdep install \
  --from-paths src \
  --ignore-src \
  -r -y \
  --skip-keys nav2_map_server

colcon build --symlink-install
```

Cuando termine:

```bash
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash
```

Comprueba los tres paquetes principales:

```bash
ros2 pkg prefix turtlebot3_description
ros2 pkg prefix slam_toolbox
ros2 pkg prefix turtlebot3_rviz_course
```

Comprueba que el URDF instalado sea el del curso:

```bash
URDF_COURSE="$(
  ros2 pkg prefix turtlebot3_rviz_course
)/share/turtlebot3_rviz_course/urdf/turtlebot3_burger_lyrical.urdf"

echo "$URDF_COURSE"

test -f "$URDF_COURSE" && echo "OK: URDF instalado"
```

Comprueba que **no exista `${namespace}`**:

```bash
grep -n '\${namespace}' "$URDF_COURSE" \
  || echo "OK: no existen placeholders de namespace"
```

Comprueba los nombres de los links:

```bash
grep -o 'link name="[^"]*"' "$URDF_COURSE"
```

Debes encontrar:

```text
link name="base_footprint"
link name="base_link"
link name="wheel_left_link"
link name="wheel_right_link"
link name="caster_back_link"
link name="imu_link"
link name="base_scan"
```

Finalmente verifica el launch:

```bash
find "$(
  ros2 pkg prefix turtlebot3_rviz_course
)/share/turtlebot3_rviz_course/launch" \
  -maxdepth 1 -type f -name '*.launch.py' -print
```

Deben aparecer:

```text
turtlebot3_rviz_tools.launch.py
turtlebot3_fake_lyrical.launch.py
```

> No agregues todavía el overlay del workspace a `~/.bashrc`. Durante la práctica
> es preferible cargarlo explícitamente en cada terminal para evitar mezclar este
> entorno con workspaces antiguos.

---

## 9. Práctica 1: iniciar TurtleBot3 en RViz2

La práctica se inicia **únicamente** con el launch del paquete del curso.

Terminal 1:

```bash
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash

export TURTLEBOT3_MODEL=burger

ros2 launch \
  turtlebot3_rviz_course \
  turtlebot3_fake_lyrical.launch.py
```

Deja esta terminal abierta.

RViz2 debe mostrar el TurtleBot3 y el display **RobotModel** debe quedar en
estado `OK`.

### 9.1 Verificación del `robot_description`

En una segunda terminal:

```bash
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash
```

Comprueba el tópico:

```bash
ros2 topic info /robot_description -v
```

Debe existir un publisher correspondiente a `robot_state_publisher`.

Ahora verifica que la descripción publicada no contenga `${namespace}`:

```bash
ros2 topic echo /robot_description --once | \
  grep '\${namespace}' \
  || echo "OK: robot_description sin namespace literal"
```

La salida correcta es:

```text
OK: robot_description sin namespace literal
```

Comprueba además los frames:

```bash
ros2 run tf2_ros tf2_echo odom base_footprint
```

y en otra terminal:

```bash
ros2 run tf2_ros tf2_echo base_footprint base_link
```

Ambas transformaciones deben existir.

### 9.2 Verificación de las ruedas

```bash
ros2 topic echo /joint_states --once
```

Debes encontrar:

```text
wheel_left_joint
wheel_right_joint
```

Estos nombres coinciden exactamente con los joints definidos en el URDF del
curso.

### 9.3 Verificación de RViz2

Dentro de RViz2:

1. Abre **Global Options**.
2. Confirma:
   ```text
   Fixed Frame: odom
   ```
3. Abre **RobotModel**.
4. Debe mostrar:
   ```text
   Status: Ok
   URDF parsed OK
   ```
5. Dentro de `Links` deben aparecer nombres normales:
   ```text
   base_link
   wheel_left_link
   wheel_right_link
   base_scan
   ```
6. **No debe aparecer ningún link cuyo nombre comience con `${namespace}`.**

---

## 10. Práctica 2: teleoperación por teclado

En esta guía se usa un puente/limitador para recibir `Twist` en `/cmd_vel_raw` y entregar `Twist` limitado en `/cmd_vel`.

Terminal 2: lanza las herramientas auxiliares:

```bash
cd ~/turtlebot3_lyrical_ws
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash
ros2 launch turtlebot3_rviz_course turtlebot3_rviz_tools.launch.py
```

Terminal 3: lanza el teclado enviando los comandos a `/cmd_vel_raw`:

```bash
source /opt/ros/lyrical/setup.bash
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/cmd_vel_raw
```

Teclas principales:

```text
i : avanzar
, : retroceder
j : girar izquierda
l : girar derecha
k : detener
q/z : aumentar/disminuir velocidad máxima
```

Verifica el comando final enviado al robot:

```bash
ros2 topic echo /cmd_vel geometry_msgs/msg/Twist
```

Verifica odometría:

```bash
ros2 topic echo /odom
```

---

## 11. Práctica 3: inspección de nodos, tópicos y TF

### 11.1 Nodos

```bash
ros2 node list
```

### 11.2 Tópicos

```bash
ros2 topic list
```

Tópicos importantes:

```text
/cmd_vel
/cmd_vel_raw
/odom
/scan
/tf
/tf_static
/map
/turtlebot3_virtual_world_markers
```

### 11.3 Tipos de mensajes

```bash
ros2 topic info /cmd_vel -v
ros2 topic info /odom -v
ros2 topic info /scan -v
```

### 11.4 Grafo ROS 2

```bash
ros2 run rqt_graph rqt_graph
```

Relación esperada:

```text
teleop_twist_keyboard -> /cmd_vel_raw -> cmd_vel_bridge -> /cmd_vel -> turtlebot3_fake_node
```

### 11.5 Árbol de transformaciones

```bash
ros2 run rqt_tf_tree rqt_tf_tree
```

Marcos importantes:

```text
odom
base_footprint
base_link
base_scan
```

---

## 12. Práctica 4: escaneo láser sintético en RViz2

El nodo `fake_laser_scan` publica el tópico `/scan` y también marcadores del mundo virtual en `/turtlebot3_virtual_world_markers`.

En RViz2 agrega manualmente:

1. **LaserScan**
   - Topic: `/scan`
   - Size: `0.03`
   - Style: `Points`
2. **MarkerArray**
   - Topic: `/turtlebot3_virtual_world_markers`
3. **Odometry**
   - Topic: `/odom`
4. **TF**
5. **RobotModel**

Comandos útiles:

```bash
ros2 topic echo /scan --once
ros2 topic hz /scan
```

Si no aparece el escaneo, revisa que el nodo auxiliar esté activo:

```bash
ros2 node list | grep fake_laser_scan
```

---

## 13. Práctica 5: SLAM y construcción del mapa

Con el robot activo, el puente de velocidad activo y `/scan` funcionando, lanza SLAM.

Terminal 4:

```bash
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=false
```

En RViz2 agrega:

1. **Map**
   - Topic: `/map`
   - Alpha: `0.7`
2. **LaserScan**
   - Topic: `/scan`
3. **TF**
4. **RobotModel**
5. **MarkerArray**
   - Topic: `/turtlebot3_virtual_world_markers`

Ahora mueve el robot con el teclado. El mapa se irá construyendo a medida que el robot recorra el entorno.

Para monitorear el mapa desde terminal:

```bash
cd ~/turtlebot3_lyrical_ws
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash
ros2 run turtlebot3_rviz_course map_monitor
```

Comandos de diagnóstico:

```bash
ros2 topic list | grep map
ros2 topic echo /map --once
ros2 topic hz /map
```

---

## 14. Práctica 6: guardar el mapa

En ROS 2 Lyrical, esta guía guarda el **pose graph** de `slam_toolbox` en lugar de depender de `nav2_map_server`.

Primero verifica que el servicio de serialización esté disponible:

```bash
ros2 service list | grep /slam_toolbox/serialize_map
```

Crea la carpeta de mapas y define el prefijo de salida:

```bash
mkdir -p ~/turtlebot3_lyrical_ws/src/turtlebot3_rviz_course/maps

MAP_PREFIX="$HOME/turtlebot3_ws/src/turtlebot3_rviz_course/maps/turtlebot3_rviz_map"
```

Serializa el mapa y el pose graph:

```bash
ros2 service call /slam_toolbox/serialize_map \
  slam_toolbox/srv/SerializePoseGraph \
  "{filename: '$MAP_PREFIX'}"
```

La respuesta debe indicar un código de resultado exitoso. Luego verifica los archivos generados:

```bash
ls -lh "${MAP_PREFIX}"*
```

`slam_toolbox` guarda la información necesaria para recuperar la sesión de mapeo y continuar trabajando sobre ella posteriormente.

> **Nota:** el flujo tradicional `map_saver_cli` que genera directamente `.yaml` + `.pgm` pertenece a `nav2_map_server`. No se usa en esta versión mientras Navigation2 no tenga una release oficial para Lyrical.

---

## 15. Práctica 7: cargar un mapa guardado

Esta práctica recupera el pose graph serializado y permite **continuar el mapeo** desde la sesión guardada.

Primero detén el nodo de SLAM anterior con `Ctrl + C` y vuelve a iniciarlo:

```bash
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=false
```

En otra terminal:

```bash
source /opt/ros/lyrical/setup.bash

MAP_PREFIX="$HOME/turtlebot3_ws/src/turtlebot3_rviz_course/maps/turtlebot3_rviz_map"

ros2 service call /slam_toolbox/deserialize_map \
  slam_toolbox/srv/DeserializePoseGraph \
  "{filename: '$MAP_PREFIX', match_type: 1, initial_pose: {position: {x: 0.0, y: 0.0, z: 0.0}, orientation: {x: 0.0, y: 0.0, z: 0.0, w: 1.0}}}"
```

En este servicio, `match_type: 1` corresponde a **START_AT_FIRST_NODE**. Para esta práctica se asume que el robot vuelve a iniciar cerca del punto donde comenzó el mapa original.

Comprueba:

```bash
ros2 topic echo /map --once
```

En RViz2 conserva o agrega el display **Map**:

```text
Topic: /map
```

Si reaparece el mapa anterior, la serialización y recuperación fueron correctas.

---

## 16. Práctica 8: movimiento automático

Detén la teleoperación por teclado y ejecuta:

```bash
cd ~/turtlebot3_lyrical_ws
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash
ros2 run turtlebot3_rviz_course square_motion
```

Puedes cambiar parámetros:

```bash
ros2 run turtlebot3_rviz_course square_motion --ros-args   -p forward_speed:=0.18   -p turn_speed:=0.70   -p forward_duration:=2.5   -p turn_duration:=2.0
```

Para detener:

```bash
Ctrl + C
```

---

## 17. Práctica 9: evitación autónoma simple

Detén la teleoperación y cualquier nodo que publique comandos de velocidad. Luego ejecuta:

```bash
cd ~/turtlebot3_lyrical_ws
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash
ros2 run turtlebot3_rviz_course simple_avoidance
```

El robot avanzará si no hay obstáculos al frente y girará cuando el escaneo detecte una distancia menor al umbral de seguridad.

Parámetros útiles:

```bash
ros2 run turtlebot3_rviz_course simple_avoidance --ros-args   -p safe_distance:=0.65   -p forward_speed:=0.10   -p turn_speed:=0.60
```

---

## 18. Problemas comunes y solución

### 18.1 El robot no se mueve

Revisa quién publica y quién se suscribe a `/cmd_vel`:

```bash
ros2 topic info /cmd_vel -v
```

Con `turtlebot3_fake_node`, el comando esperado es `geometry_msgs/msg/Twist`.

Si usas teleoperación con el puente de esta guía:

```bash
ros2 launch turtlebot3_rviz_course turtlebot3_rviz_tools.launch.py
ros2 run teleop_twist_keyboard teleop_twist_keyboard --ros-args -r /cmd_vel:=/cmd_vel_raw
```

Comprueba ambos tópicos:

```bash
ros2 topic echo /cmd_vel_raw geometry_msgs/msg/Twist
ros2 topic echo /cmd_vel geometry_msgs/msg/Twist
```

### 18.2 `/cmd_vel` presenta un tipo inesperado

Verifica:

```bash
ros2 topic type /cmd_vel
```

Para **TurtleBot3 Fake Node** en esta guía debe aparecer:

```text
geometry_msgs/msg/Twist
```

No uses `TwistStamped` en este flujo. Ese tipo puede aparecer en otras integraciones de TurtleBot3, por ejemplo en ciertos bridges de Gazebo, pero no es el tipo de entrada del Fake Node utilizado aquí.

### 18.3 No aparece `/scan`

Verifica:

```bash
ros2 node list | grep fake_laser_scan
ros2 topic list | grep scan
ros2 topic hz /scan
```

Si el nodo está activo pero no publica, revisa que `/odom` exista:

```bash
ros2 topic echo /odom --once
```

### 18.4 El mapa no aparece en RViz2

Revisa que SLAM esté publicando `/map`:

```bash
ros2 topic list | grep map
ros2 topic echo /map --once
```

En RViz2 agrega un display **Map** con:

```text
Topic: /map
```

### 18.5 El mapa se guarda vacío

Antes de guardar, mueve el robot durante algunos minutos para cubrir más área. También revisa:

```bash
ros2 topic hz /scan
ros2 topic hz /map
```

### 18.6 RobotModel muestra `${namespace}` o el modelo no sigue al TF

En esta versión de la guía esto indica que se está ejecutando una descripción
antigua o un launch distinto al del curso.

Primero identifica todos los publishers:

```bash
ros2 topic info /robot_description -v
```

Debe existir únicamente el `robot_state_publisher` iniciado por:

```text
turtlebot3_rviz_course/turtlebot3_fake_lyrical.launch.py
```

Comprueba el contenido publicado:

```bash
ros2 topic echo /robot_description --once | grep '\${namespace}'
```

La salida correcta es **ninguna**.

Comprueba el archivo instalado:

```bash
URDF_COURSE="$(
  ros2 pkg prefix turtlebot3_rviz_course
)/share/turtlebot3_rviz_course/urdf/turtlebot3_burger_lyrical.urdf"

grep -n '\${namespace}' "$URDF_COURSE" \
  || echo "OK: URDF instalado limpio"
```

Si el archivo instalado está limpio pero el tópico contiene `${namespace}`,
hay otro `robot_state_publisher` ejecutándose. Cierra todas las sesiones ROS 2
de TurtleBot3 y vuelve a iniciar únicamente:

```bash
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash
export TURTLEBOT3_MODEL=burger

ros2 launch \
  turtlebot3_rviz_course \
  turtlebot3_fake_lyrical.launch.py
```

Después verifica:

```bash
ros2 run tf2_ros tf2_echo odom base_link
```

Cuando el robot se mueva, esta transformación debe cambiar y el RobotModel debe
moverse junto con ella.

### 18.7 `colcon build` termina correctamente, pero `ros2 pkg prefix turtlebot3_description` no muestra el paquete

Este caso ocurre cuando `turtlebot3_description` **sí fue compilado**, pero todavía no se ha cargado el overlay del workspace en la terminal actual.

Si viste una salida como:

```text
Finished <<< turtlebot3_description
Summary: 1 package finished
```

la compilación fue correcta. No necesitas volver a ejecutar `rosdep install`.

Ejecuta:

```bash
source /opt/ros/lyrical/setup.bash
source ~/turtlebot3_lyrical_ws/install/setup.bash

ros2 pkg prefix turtlebot3_description
```

Luego verifica:

```bash
ros2 pkg list | grep '^turtlebot3_description$'
```

y las mallas:

```bash
find "$(ros2 pkg prefix turtlebot3_description)/share/turtlebot3_description/meshes" \
  -type f | head -20
```

Si sigue sin localizarlo, comprueba directamente la instalación:

```bash
ls ~/turtlebot3_lyrical_ws/install/turtlebot3_description
```

- Si la carpeta existe: vuelve a cargar `install/setup.bash`.
- Si la carpeta no existe: recompila el paquete.

```bash
cd ~/turtlebot3_lyrical_ws
source /opt/ros/lyrical/setup.bash
colcon build --symlink-install --packages-select turtlebot3_description
source ~/turtlebot3_lyrical_ws/install/setup.bash
```

> No confundas `cd ..` con `cd..`. En Bash debe existir un espacio entre `cd` y `..`.

### 18.8 `Unable to locate package ros-lyrical-slam-toolbox`

Este error es esperado con el estado actual de ROS 2 Lyrical. No intentes instalar `slam_toolbox` mediante APT. Comprueba primero que el resto de paquetes se instalen con el comando de la sección 4.1 y luego instala `slam_toolbox` desde su rama `lyrical` siguiendo la sección 4.3.

Si ya clonaste el repositorio, verifica:

```bash
cd ~/turtlebot3_lyrical_ws/src/slam_toolbox
git branch --show-current
```

Debe indicar:

```text
lyrical
```

Después recompila:

```bash
cd ~/turtlebot3_lyrical_ws
source /opt/ros/lyrical/setup.bash

rosdep install \
  --from-paths src/slam_toolbox \
  --ignore-src \
  -r -y \
  --skip-keys nav2_map_server

colcon build --symlink-install --packages-select slam_toolbox
source ~/turtlebot3_lyrical_ws/install/setup.bash
ros2 pkg prefix slam_toolbox
```

### 18.9 `nav2_map_server` o `navigation2` no se encuentran

No son necesarios para esta guía. El `package.xml` de `slam_toolbox` incluye `nav2_map_server` como dependencia de ejecución para el guardado tradicional del mapa, por eso se omite deliberadamente durante `rosdep`. Para guardar y recuperar la sesión de SLAM se utilizan los servicios nativos de serialización:

```bash
ros2 service list | grep slam_toolbox
```

Debes encontrar, entre otros:

```text
/slam_toolbox/serialize_map
/slam_toolbox/deserialize_map
```

### 18.10 RViz2 se ve lento

Reduce la cantidad de puntos del escaneo:

```bash
ros2 launch turtlebot3_rviz_course turtlebot3_rviz_tools.launch.py fake_laser_scan.samples:=180
```

Si usas el archivo de lanzamiento incluido, también puedes editar el parámetro `samples` dentro de `turtlebot3_rviz_tools.launch.py`.

---

## 19. Actividad propuesta para estudiantes

### Objetivo

Construir un mapa del entorno virtual, serializar el pose graph, recuperarlo y explicar la relación entre `/cmd_vel`, `/odom`, `/scan`, `/tf` y `/map`.

### Entregables

1. Captura de RViz2 mostrando:
   - TurtleBot3.
   - LaserScan.
   - Mapa.
   - TF.
2. Archivos del pose graph serializado cuyo prefijo sea:
   - `turtlebot3_rviz_map`.
3. Captura de `rqt_graph`.
4. Respuesta corta:
   - ¿Qué nodo publica `/scan`?
   - ¿Qué nodo publica `/map`?
   - ¿Qué diferencia hay entre `/cmd_vel` y `/odom`?
   - ¿Por qué TF es necesario para construir el mapa?

### Reto adicional

Modificar el nodo `fake_laser_scan.py` para cambiar la forma del entorno o agregar más obstáculos circulares.

Ejemplo: agregar un obstáculo nuevo en la lista `self.circles`:

```python
self.circles.append((1.8, 0.2, 0.20))
```

Luego recompilar:

```bash
cd ~/turtlebot3_lyrical_ws
colcon build --symlink-install
source ~/turtlebot3_lyrical_ws/install/setup.bash
```

---

## 20. Bibliografía

[1] ROBOTIS, “TurtleBot3 Fake Node Simulation,” TurtleBot3 e-Manual, consultado en 2026. Disponible: https://emanual.robotis.com/docs/en/platform/turtlebot3/fakenode_simulation/

[2] ROBOTIS, “TurtleBot3 SLAM,” TurtleBot3 e-Manual, consultado en 2026. Disponible: https://emanual.robotis.com/docs/en/platform/turtlebot3/slam/

[3] Open Robotics, “ROS 2 Lyrical Documentation,” consultado en 2026. Disponible: https://docs.ros.org/en/lyrical/

[4] ROBOTIS, “TurtleBot3 Burger URDF,” repositorio oficial `turtlebot3`, rama `jazzy`, consultado en 2026. Disponible: https://github.com/ROBOTIS-GIT/turtlebot3/blob/jazzy/turtlebot3_description/urdf/turtlebot3_burger.urdf

[5] ROBOTIS, “TurtleBot3 Fake Node,” repositorio `turtlebot3_simulations`, consultado en 2026. Disponible: https://github.com/ROBOTIS-GIT/turtlebot3_simulations/tree/main/turtlebot3_fake_node

[6] ROS, “robot_state_publisher,” repositorio oficial, consultado en 2026. Disponible: https://github.com/ros/robot_state_publisher

[7] Steve Macenski et al., “SLAM Toolbox,” rama `lyrical`, consultado en 2026. Disponible: https://github.com/SteveMacenski/slam_toolbox/tree/lyrical

</div>
