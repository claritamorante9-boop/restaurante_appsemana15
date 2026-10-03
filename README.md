#Restaurante App — Sistema de Ventas
**Semana 16** — Gestión de Usuarios y Manejo de Eventos

#Descripción
Aplicación de escritorio en Python con Tkinter para gestión de ventas de restaurante. Evolutiva: conserva funciones anteriores y agrega administración de usuarios con roles y manejo de eventos.

#Funcionalidades

#Generales
-  Inicio de sesión con validación
- Registro de ventas con historial
- Persistencia en archivos JSON
- Logo personalizado

#Semana 16 — Gestión de Usuarios
- **Roles:** Administrador / Empleado / Cliente
-  Solo **Administrador** ve y gestiona la sección de Usuarios
-  Registrar, Consultar, Actualizar y Eliminar usuarios
-  Tabla `Treeview` con ID, Nombre y Rol
-**Eventos implementados:**
  - `<<TreeviewSelect>>` → carga datos al formulario
  - `<Return>` → Registrar con tecla Enter
  - `<Escape>` → Limpiar formulario
  - `<<ComboboxSelected>>` → detecta cambio de rol
-  No permite eliminarse a sí mismo
-  Confirmación antes de eliminar

#Estructura
restaurante_appsemana15/
├── assets/logo.png
├── datos/
│ ├── usuarios.json
│ ├── productos.json
│ └── ventas.json
├── modelos/
│ ├── usuario.py ← atributo rol
│ ├── producto.py
│ └── venta.py
├── servicios/
│ └── restaurante_servicio.py ← lógica y persistencia
├── ui/
│ ├── login_view.py
│ └── main_view.py ← eventos y pestañas
├── main.py
└── README.md

##Ejecución
```bash
pip install pillow
python main.py
Credenciales:
Usuario: admin
Contraseña: 1234
Rol: Administrador 
Flujo
Inicio → Login → MainView
Administrador ve pestaña Gestión de Usuarios
Seleccionar fila → datos cargados → Actualizar/Eliminar
Enter = Registrar | Escape = Limpiar
Cambios guardados en usuarios.json
