# HotelPro - Sistema de gestión hotelera

Aplicación de escritorio para gestionar clientes, habitaciones, reservas y el registro de entrada y salida (check-in y check-out) de un hotel. Está desarrollada en Python con Tkinter, usa MySQL como base de datos y sigue el patrón de arquitectura MVC (Modelo - Vista - Controlador).

Proyecto académico de la asignatura Profundización de la programación orientada a objetos, CEFIT.

## Funcionalidades

La aplicación tiene cuatro módulos. Todos muestran sus registros en una tabla y se manejan desde botones y formularios emergentes.

| Módulo | Qué permite hacer | Datos que maneja |
|---|---|---|
| Clientes | Crear, editar, eliminar y listar clientes | Nombre, apellido, documento, teléfono y correo |
| Habitaciones | Crear, editar, eliminar y listar habitaciones | Número, tipo, estado y tarifa |
| Reservas | Crear, editar y cancelar reservas; el listado muestra el cliente y la habitación de cada una | Cliente, habitación, fecha de llegada, fecha de salida y estado |
| Check-in / Check-out | Registrar la entrada de un huésped a partir de una reserva y registrar su salida | Reserva, fecha de entrada y fecha de salida |

Otras características:

- Validación de campos obligatorios en cada módulo antes de guardar.
- Confirmación antes de eliminar un cliente o una habitación, o de cancelar una reserva.
- Selección de fechas con un calendario (`tkcalendar`) en reservas y check-in.
- Exportación a Excel (`.xlsx`) de los datos de cada módulo.
- Favicon propio en la ventana principal y en cada formulario.
- Íconos en los botones de acción de cada módulo.

## Tecnologías utilizadas

| Tecnología | Uso |
|---|---|
| Python 3 | Lenguaje principal, con programación orientada a objetos |
| Tkinter (ttk) | Interfaz gráfica de escritorio |
| tkcalendar | Selector de fechas |
| MySQL | Base de datos `hotelpro` y stored procedures |
| mysql-connector-python | Conexión de Python con MySQL y llamada a los procedimientos |
| Pillow | Generación del favicon de la aplicación |
| openpyxl | Exportación de los datos de cada módulo a Excel |

## Arquitectura

El proyecto separa la interfaz, la lógica y el acceso a los datos en tres capas:

```
Vista (Tkinter)  ->  Controlador  ->  Modelo  ->  MySQL (stored procedures)
```

- **Vista (`view/`):** formularios y tablas de cada módulo. No conoce la base de datos; solo habla con el controlador.
- **Controlador (`controller/`):** valida los datos recibidos y devuelve a la vista un mensaje de éxito o de error.
- **Modelo (`model/`):** se conecta a MySQL y ejecuta los stored procedures con `callproc`.

Los cuatro módulos repiten la misma estructura.

## Estructura del proyecto

```
MiApp/
├── main.py
├── generar_favicon.py
├── favicon.ico
├── hotelpro.sql
├── controller/
│   ├── __init__.py
│   ├── cliente_controller.py
│   ├── habitacion_controller.py
│   ├── reserva_controller.py
│   └── checkin_controller.py
├── model/
│   ├── __init__.py
│   ├── cliente_model.py
│   ├── habitacion_model.py
│   ├── reserva_model.py
│   └── checkin_model.py
└── view/
    ├── __init__.py
    ├── cliente_view.py
    ├── habitacion_view.py
    ├── reserva_view.py
    └── checkin_view.py
```

## Stored procedures

Todas las operaciones sobre la base de datos se hacen mediante stored procedures.

| Módulo | Procedimientos |
|---|---|
| Clientes | `sp_obtener_clientes`, `sp_crear_cliente`, `sp_actualizar_cliente`, `sp_eliminar_cliente` |
| Habitaciones | `sp_obtener_habitaciones`, `sp_crear_habitacion`, `sp_actualizar_habitacion`, `sp_eliminar_habitacion` |
| Reservas | `sp_obtener_reservas`, `sp_crear_reserva`, `sp_actualizar_reserva`, `sp_eliminar_reserva` |
| Check-in / Check-out | `sp_obtener_checkins`, `sp_crear_checkin`, `sp_checkout`, `sp_eliminar_checkin` |

## Requisitos

- Python 3 (Tkinter viene incluido con la instalación estándar de Python).
- MySQL Server en `localhost`.
- Las librerías `mysql-connector-python` y `tkcalendar`.

## Instalación y ejecución

1. Clonar el repositorio y entrar a la carpeta del proyecto.

2. Instalar las dependencias:

   ```
   pip install mysql-connector-python tkcalendar Pillow openpyxl
   ```

3. Crear la base de datos importando el script `hotelpro.sql`, que contiene las tablas y los stored procedures. Se puede hacer desde HeidiSQL, MySQL Workbench o la consola de MySQL.

4. Revisar los datos de conexión. Cada archivo de la carpeta `model/` los define en su método `__init__`; por defecto son:

   ```python
   host="localhost"
   user="root"
   password=""
   database="hotelpro"
   ```

   Si tu servidor MySQL usa otro usuario o contraseña, cámbialos en los cuatro archivos del modelo.

5. Generar el favicon (solo la primera vez):

   ```
   python generar_favicon.py
   ```

6. Ejecutar la aplicación:

   ```
   python main.py
   ```

## Autor

Isaac - CEFIT
