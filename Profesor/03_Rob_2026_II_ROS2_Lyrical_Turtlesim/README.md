<div align="center">
<picture>
    <source srcset="https://imgur.com/5bYAzsb.png" media="(prefers-color-scheme: dark)">
    <source srcset="https://imgur.com/Os03JoE.png" media="(prefers-color-scheme: light)">
    <img src="https://imgur.com/Os03JoE.png" alt="Escudo UNAL" width="350px">
</picture>

<h3>Curso de Robótica 2026-II</h3>

<h1>Introducción a Turtlesim</h1>

<h2>Uso de Turtlesim en ROS 2 Lyrical (Ubuntu 26.04)</h2>

<h4>Pedro Fabián Cárdenas Herrera<br>
    Manuel Felipe Carranza Montenegro</h4>

<p>
  <img alt="Ubuntu 26.04 LTS" src="https://img.shields.io/badge/Ubuntu-26.04%20LTS-E95420?logo=ubuntu&logoColor=white">
  <img alt="ROS 2 Lyrical" src="https://img.shields.io/badge/ROS%202-Lyrical-22314E?logo=ros&logoColor=white">
  <img alt="Package" src="https://img.shields.io/badge/Package-turtlesim-2ea44f">
</p>

</div>

<div align="justify"> 

## Tabla de contenidos
- [Introducción](#introducción)
- [Objetivos](#objetivos)
- [Prerrequisitos](#prerrequisitos)
- [1. Instalar turtlesim](#1-instalar-turtlesim)
- [2. Iniciar turtlesim](#2-iniciar-turtlesim)
- [3. Controlar la tortuga (teleop)](#3-controlar-la-tortuga-teleop)
- [4. Explorar nodos, tópicos, servicios y acciones](#4-explorar-nodos-tópicos-servicios-y-acciones)
- [5. Instalar y usar rqt](#5-instalar-y-usar-rqt)
- [6. Servicios clave en turtlesim](#6-servicios-clave-en-turtlesim)
- [7. Controlar múltiples tortugas (remapeo)](#7-controlar-múltiples-tortugas-remapeo)
- [8. Workspace + VS Code (mínimo recomendado)](#8-workspace--vs-code-mínimo-recomendado)
- [9. Crear un nodo en Python para controlar la tortuga](#9-crear-un-nodo-en-python-para-controlar-la-tortuga)
- [Checklist de verificación](#checklist-de-verificación)
- [Errores comunes y solución rápida](#errores-comunes-y-solución-rápida)
- [Recursos útiles](#recursos-útiles)
- [Bibliografía](#bibliografía)

---

## Introducción

El paquete `turtlesim` es un simulador ligero incluido en ROS 2 que permite comprender de forma **visual y práctica** conceptos fundamentales como **nodos**, **tópicos**, **servicios**, **acciones**, **parámetros** y **remapeo**. A través de una tortuga animada, es posible interactuar con estos elementos usando comandos de terminal o interfaces gráficas como `rqt`.

Este entorno es ideal para comenzar en ROS 2 porque ofrece un “laboratorio” rápido: todo ocurre en tu computador, sin hardware físico, y con retroalimentación inmediata.

> **Nota del curso:** esta guía asume **Ubuntu 26.04 LTS (Resolute Raccoon)** y **ROS 2 Lyrical Luth**, que es la combinación utilizada en el curso.
>
> En ROS 2 Lyrical, las interfaces propias de Turtlesim —por ejemplo `Pose`, `Spawn` y `SetPen`— se encuentran en el paquete `turtlesim_msgs`.

---

## Objetivos

- Instalar y ejecutar el simulador `turtlesim`.
- Controlar una tortuga mediante el teclado usando ROS 2.
- Visualizar y manipular nodos, tópicos, servicios y acciones mediante comandos y la herramienta gráfica `rqt`.
- Utilizar servicios para crear nuevas tortugas y cambiar propiedades como el color del trazo.
- Aplicar remapeo para controlar múltiples tortugas simultáneamente.
- Crear un primer nodo en Python que publique comandos de velocidad (`Twist`) para controlar a la tortuga.

---

## Prerrequisitos

- Tener **Ubuntu 26.04 LTS** instalado.
- Tener **ROS 2 Lyrical Luth** correctamente instalado y configurado.
- Haber ejecutado `source /opt/ros/lyrical/setup.bash` o tenerlo configurado en `~/.bashrc`.
- Conocer comandos básicos de terminal.

Verifica rápidamente la distribución activa de ROS 2:

```bash
printenv | grep ROS_DISTRO
# Debe mostrar: ROS_DISTRO=lyrical
```

También puedes verificar la versión de Ubuntu:

```bash
lsb_release -a
```

---

## 1. Instalar turtlesim

Actualiza el índice de paquetes e instala Turtlesim para ROS 2 Lyrical:

```bash
sudo apt update
sudo apt install -y ros-lyrical-turtlesim
```

Verifica que existan los ejecutables del paquete:

```bash
ros2 pkg executables turtlesim
```

Entre los ejecutables deberían aparecer:

```text
turtlesim draw_square
turtlesim mimic
turtlesim turtle_teleop_key
turtlesim turtlesim_node
```

---

## 2. Iniciar turtlesim

Abre una terminal y carga ROS 2:

```bash
source /opt/ros/lyrical/setup.bash
```

Luego inicia el simulador:

```bash
ros2 run turtlesim turtlesim_node
```

Deberías ver una ventana con una tortuga sobre el fondo del simulador.

> Si estás trabajando en una máquina virtual o en un entorno sin interfaz gráfica, la ventana puede no abrir correctamente. Para el curso se recomienda una instalación nativa de Ubuntu 26.04 o una máquina virtual con aceleración gráfica y visualización correctamente configuradas.

---

## 3. Controlar la tortuga (teleop)

En una segunda terminal:

```bash
source /opt/ros/lyrical/setup.bash
ros2 run turtlesim turtle_teleop_key
```

Mantén activa esta terminal y utiliza las flechas del teclado para mover la tortuga.

> Cada pulsación genera un comando de movimiento corto. Este comportamiento evita que un robot continúe moviéndose indefinidamente si se pierde la comunicación con el operador.

---

## 4. Explorar nodos, tópicos, servicios y acciones

Con `turtlesim_node` y `turtle_teleop_key` ejecutándose, abre una tercera terminal y prueba:

```bash
ros2 node list
ros2 topic list
ros2 service list
ros2 action list
```

### Inspección rápida

Consulta información sobre el tópico de velocidad:

```bash
ros2 topic info /turtle1/cmd_vel
```

Observa en tiempo real la posición de la tortuga:

```bash
ros2 topic echo /turtle1/pose
```

Inspecciona la estructura del mensaje de velocidad:

```bash
ros2 interface show geometry_msgs/msg/Twist
```

En ROS 2 Lyrical, la pose de Turtlesim pertenece a `turtlesim_msgs`:

```bash
ros2 interface show turtlesim_msgs/msg/Pose
```

También puedes listar los tópicos junto con sus tipos:

```bash
ros2 topic list -t
```

Deberías encontrar, entre otros:

```text
/turtle1/cmd_vel [geometry_msgs/msg/Twist]
/turtle1/color_sensor [turtlesim_msgs/msg/Color]
/turtle1/pose [turtlesim_msgs/msg/Pose]
```

---

## 5. Instalar y usar rqt

`rqt` proporciona herramientas gráficas para inspeccionar e interactuar con ROS 2.

### 5.1 Instalar rqt

En Ubuntu 26.04 con ROS 2 Lyrical:

```bash
sudo apt update
sudo apt install -y ros-lyrical-rqt ros-lyrical-rqt-common-plugins
```

### 5.2 Ejecutar rqt

```bash
rqt
```

Si al abrir `rqt` no aparecen los plugins:

```bash
rqt --force-discover
```

Para trabajar con los servicios de Turtlesim selecciona:

**Plugins > Services > Service Caller**

---

## 6. Servicios clave en turtlesim

Antes de utilizar los servicios, asegúrate de tener `turtlesim_node` ejecutándose.

### 6.1 Usar `/spawn` para crear otra tortuga

En `rqt`, selecciona el servicio:

```text
/spawn
```

Ingresa, por ejemplo:

- `x = 1.0`
- `y = 1.0`
- `theta = 0.0`
- `name = turtle2`

Luego presiona **Call**.

✅ Aparecerá una nueva tortuga llamada `turtle2`.

También puedes comprobar el tipo del servicio desde la terminal:

```bash
ros2 service type /spawn
```

En ROS 2 Lyrical debe reportar:

```text
turtlesim_msgs/srv/Spawn
```

Para ver su estructura:

```bash
ros2 interface show turtlesim_msgs/srv/Spawn
```

### 6.2 Usar `/turtle1/set_pen`

Selecciona:

```text
/turtle1/set_pen
```

Ejemplo de configuración:

- `r = 255`
- `g = 0`
- `b = 0`
- `width = 5`
- `off = 0`

Luego presiona **Call**.

✅ La tortuga dibujará una línea roja y gruesa.

Puedes consultar su interfaz mediante:

```bash
ros2 interface show turtlesim_msgs/srv/SetPen
```

### 6.3 Otros servicios útiles

Lista los servicios y sus tipos:

```bash
ros2 service list -t
```

Consulta el tipo de un servicio:

```bash
ros2 service type /spawn
```

También puedes inspeccionarlo automáticamente:

```bash
ros2 interface show $(ros2 service type /spawn)
```

Borra el dibujo realizado por las tortugas:

```bash
ros2 service call /clear std_srvs/srv/Empty {}
```

### 6.4 Cambiar el color del fondo mediante parámetros

Lista los parámetros del nodo:

```bash
ros2 param list /turtlesim
```

Cambia los componentes RGB:

```bash
ros2 param set /turtlesim background_r 200
ros2 param set /turtlesim background_g 200
ros2 param set /turtlesim background_b 255
```

Para aplicar inmediatamente el cambio de fondo puedes llamar el servicio `/clear`:

```bash
ros2 service call /clear std_srvs/srv/Empty {}
```

---

## 7. Controlar múltiples tortugas (remapeo)

La teleoperación de Turtlesim utiliza por defecto los elementos asociados a `turtle1`, entre ellos:

- `turtle1/cmd_vel`
- `turtle1/rotate_absolute`

Si ya creaste `turtle2`, abre una nueva terminal y carga ROS 2:

```bash
source /opt/ros/lyrical/setup.bash
```

Luego ejecuta una segunda instancia de teleoperación remapeando tanto el tópico de velocidad como la acción de rotación:

```bash
ros2 run turtlesim turtle_teleop_key --ros-args \
  --remap turtle1/cmd_vel:=turtle2/cmd_vel \
  --remap turtle1/rotate_absolute:=turtle2/rotate_absolute
```

✅ Esta terminal controlará `turtle2`, mientras la primera instancia de `turtle_teleop_key` seguirá controlando `turtle1`.

> El remapeo permite reutilizar el mismo nodo sin modificar su código fuente, cambiando los nombres de los elementos de ROS 2 con los que se comunica.

---

## 8. Workspace + VS Code (mínimo recomendado)

### 8.1 Instalar herramientas de compilación

```bash
sudo apt update
sudo apt install -y python3-colcon-common-extensions
```

### 8.2 Crear un workspace

```bash
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws
colcon build
```

Carga primero ROS 2 y después el workspace:

```bash
source /opt/ros/lyrical/setup.bash
source ~/ros2_ws/install/setup.bash
```

### 8.3 Configuración automática

Opcionalmente, puedes agregar ambos comandos a `~/.bashrc`:

```bash
echo "source /opt/ros/lyrical/setup.bash" >> ~/.bashrc
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

> Si acabas de crear el workspace y todavía no contiene paquetes, `colcon build` puede generar únicamente la estructura básica de `build`, `install` y `log`.

---

## 9. Crear un nodo en Python para controlar la tortuga

En esta sección se creará un nodo que publicará mensajes `geometry_msgs/msg/Twist` en `/turtle1/cmd_vel`.

### 9.1 Crear el paquete

```bash
ros2 pkg create my_turtle_controller \
  --build-type ament_python \
  --dependencies rclpy geometry_msgs
```

Esto crea un paquete Python e incluye las dependencias necesarias en `package.xml`.

### 9.2 Configurar `setup.py`

Edita:

```text
~/ros2_ws/src/my_turtle_controller/setup.py
```

Asegúrate de que `entry_points` contenga:

```python
entry_points={
    'console_scripts': [
        'move_turtle = my_turtle_controller.move_turtle:main',
    ],
},
```

### 9.3 Crear el nodo `move_turtle.py`

Crea el archivo:

```text
~/ros2_ws/src/my_turtle_controller/my_turtle_controller/move_turtle.py
```

Con el siguiente contenido:

```python
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist


class TurtleController(Node):
    def __init__(self):
        super().__init__('turtle_controller')
        self.publisher_ = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )
        self.timer = self.create_timer(0.5, self.move_turtle)

    def move_turtle(self):
        msg = Twist()
        msg.linear.x = 2.0
        msg.angular.z = 1.0

        self.publisher_.publish(msg)
        self.get_logger().info('Moviendo la tortuga')


def main(args=None):
    rclpy.init(args=args)

    node = TurtleController()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
```

> Si quieres controlar `turtle2`, puedes cambiar `/turtle1/cmd_vel` por `/turtle2/cmd_vel` o utilizar remapeo al ejecutar el nodo.

---

## Compilar y ejecutar el nodo

Primero asegúrate de tener `turtlesim_node` ejecutándose:

```bash
ros2 run turtlesim turtlesim_node
```

En otra terminal, compila el workspace:

```bash
cd ~/ros2_ws
source /opt/ros/lyrical/setup.bash
colcon build --symlink-install
```

Carga el workspace:

```bash
source install/setup.bash
```

Ejecuta el nodo:

```bash
ros2 run my_turtle_controller move_turtle
```

✅ La tortuga debería comenzar a desplazarse automáticamente describiendo una trayectoria curva.

---

## Checklist de verificación

```bash
# 1) ¿Estoy usando ROS 2 Lyrical?
printenv | grep ROS_DISTRO

# 2) ¿Turtlesim está instalado?
ros2 pkg list | grep turtlesim

# 3) ¿Se encuentran los ejecutables?
ros2 pkg executables turtlesim

# 4) ¿Están disponibles sus interfaces?
ros2 interface list | grep turtlesim_msgs

# 5) ¿Se ven los nodos con Turtlesim ejecutándose?
ros2 node list

# 6) ¿Se ven los tópicos?
ros2 topic list -t

# 7) ¿Se ven los servicios?
ros2 service list -t

# 8) ¿Se ven las acciones?
ros2 action list -t
```

---

## Errores comunes y solución rápida

### 1) `ros2: command not found`

ROS 2 no está instalado o el entorno no ha sido cargado.

Ejecuta:

```bash
source /opt/ros/lyrical/setup.bash
```

Si funciona, puedes agregarlo permanentemente:

```bash
echo "source /opt/ros/lyrical/setup.bash" >> ~/.bashrc
source ~/.bashrc
```

### 2) `Package 'turtlesim' not found`

Instala el paquete correspondiente a ROS 2 Lyrical:

```bash
sudo apt update
sudo apt install -y ros-lyrical-turtlesim
```

Comprueba la distribución activa:

```bash
printenv | grep ROS_DISTRO
```

Debe mostrar:

```text
ROS_DISTRO=lyrical
```

### 3) `rqt` abre pero no aparecen plugins

Instala los plugins comunes:

```bash
sudo apt install -y ros-lyrical-rqt ros-lyrical-rqt-common-plugins
```

Luego fuerza el descubrimiento:

```bash
rqt --force-discover
```

### 4) `turtlesim/msg/Pose` no existe

En versiones recientes de ROS 2 las interfaces de Turtlesim se encuentran en `turtlesim_msgs`.

Utiliza:

```bash
ros2 interface show turtlesim_msgs/msg/Pose
```

En lugar de:

```text
turtlesim/msg/Pose
```

### 5) La ventana de Turtlesim no aparece

Posibles causas:

- Sesión sin entorno gráfico.
- Máquina virtual sin GUI correctamente configurada.
- Problemas con la variable `DISPLAY`.

Para comprobarla:

```bash
echo $DISPLAY
```

Para el curso se recomienda ejecutar Ubuntu 26.04 con escritorio gráfico y ROS 2 Lyrical de forma nativa o en una máquina virtual correctamente configurada.

### 6) `turtle2` no responde completamente al teclado

Asegúrate de remapear tanto `cmd_vel` como `rotate_absolute`:

```bash
ros2 run turtlesim turtle_teleop_key --ros-args \
  --remap turtle1/cmd_vel:=turtle2/cmd_vel \
  --remap turtle1/rotate_absolute:=turtle2/rotate_absolute
```

---

## Recursos útiles

- Documentación oficial ROS 2 Lyrical — **Using turtlesim, ros2, and rqt**:  
  https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html

- Documentación ROS 2 Lyrical — **Understanding topics**:  
  https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html

- Documentación ROS 2 Lyrical — **Understanding services**:  
  https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html

- RQt — conceptos y uso:  
  https://docs.ros.org/en/lyrical/Concepts/Intermediate/About-RQt.html

- ROS Index — paquete `turtlesim`:  
  https://index.ros.org/p/turtlesim/

- Código fuente de Turtlesim (`ros_tutorials`):  
  https://github.com/ros/ros_tutorials

- Extensión ROS para Visual Studio Code:  
  https://marketplace.visualstudio.com/items?itemName=ms-iot.vscode-ros

### Videos recomendados (opcionales)

- Búsqueda: **ROS 2 Lyrical turtlesim rqt**  
  https://www.youtube.com/results?search_query=ROS2+Lyrical+turtlesim+rqt

- Búsqueda: **ROS 2 turtlesim topics services**  
  https://www.youtube.com/results?search_query=ros2+turtlesim+topics+services

---

## Bibliografía

[1] Open Robotics, “Using turtlesim, ros2, and rqt,” *ROS 2 Lyrical Documentation*, 2026. Disponible en: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html

[2] Open Robotics, “Understanding topics,” *ROS 2 Lyrical Documentation*, 2026. Disponible en: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html

[3] Open Robotics, “Understanding services,” *ROS 2 Lyrical Documentation*, 2026. Disponible en: https://docs.ros.org/en/lyrical/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html

[4] Open Robotics, “About RQt,” *ROS 2 Lyrical Documentation*, 2026. Disponible en: https://docs.ros.org/en/lyrical/Concepts/Intermediate/About-RQt.html

[5] Open Robotics, “turtlesim — ROS Index,” 2026. Disponible en: https://index.ros.org/p/turtlesim/

[6] Open Robotics, “Lyrical Luth,” *ROS 2 Documentation*, 2026. Disponible en: https://docs.ros.org/en/lyrical/Releases/Release-Lyrical-Luth.html

</div>
