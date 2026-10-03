import os
import json
from modelos.usuario import Usuario
from modelos.producto import Producto
from modelos.venta import Venta

class RestauranteServicio:
    def __init__(self):
        self.usuarios = []
        self.productos = []
        self.ventas = []
        self._cargar_datos()

    def _cargar_datos(self):
        ruta_usu = os.path.join("datos", "usuarios.json")
        if os.path.exists(ruta_usu):
            with open(ruta_usu, "r", encoding="utf-8") as f:
                datos = json.load(f)
                self.usuarios = [Usuario.from_dict(d) for d in datos]
        
        ruta_prod = os.path.join("datos", "productos.json")
        if os.path.exists(ruta_prod):
            with open(ruta_prod, "r", encoding="utf-8") as f:
                datos = json.load(f)
                self.productos = [Producto.from_dict(d) for d in datos]
        
        ruta_vent = os.path.join("datos", "ventas.json")
        if os.path.exists(ruta_vent):
            with open(ruta_vent, "r", encoding="utf-8") as f:
                datos = json.load(f)
                self.ventas = [Venta.from_dict(d) for d in datos]

    def iniciar_sesion(self, nombre, contrasena):
        for u in self.usuarios:
            if u.nombre == nombre and u.contrasena == contrasena:
                return True, u
        return False, None

    def obtener_productos(self):
        return self.productos

    def obtener_usuarios(self):
        return self.usuarios

    def registrar_venta(self, usuario_id, producto_id, cantidad):
        nuevo_id = max([v.id for v in self.ventas] + [0]) + 1
        venta = Venta(nuevo_id, usuario_id, producto_id, cantidad)
        self.ventas.append(venta)
        self._guardar_ventas()
        return True, "Venta registrada"

    def obtener_ventas(self):
        return self.ventas

    def _guardar_ventas(self):
        ruta = os.path.join("datos", "ventas.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump([v.to_dict() for v in self.ventas], f, ensure_ascii=False, indent=2)

    # === Gestión de Usuarios - Semana 16 ===
    def obtener_usuario_por_id(self, usuario_id):
        for u in self.usuarios:
            if u.id == usuario_id:
                return u
        return None

    def registrar_usuario(self, nombre, contrasena, rol):
        if not nombre:
            return False, "El nombre es obligatorio"
        for u in self.usuarios:
            if u.nombre == nombre:
                return False, "El usuario ya existe"
        nuevo_id = max([u.id for u in self.usuarios] + [0]) + 1
        usuario = Usuario(nuevo_id, nombre, contrasena, rol)
        self.usuarios.append(usuario)
        self._guardar_usuarios()
        return True, f"Usuario {nombre} registrado"

    def actualizar_usuario(self, usuario_id, nombre, contrasena, rol):
        usuario = self.obtener_usuario_por_id(usuario_id)
        if not usuario:
            return False, "Usuario no encontrado"
        if not nombre:
            return False, "El nombre es obligatorio"
        for u in self.usuarios:
            if u.nombre == nombre and u.id != usuario_id:
                return False, "El nombre ya está en uso"
        usuario.nombre = nombre
        if contrasena:
            usuario.contrasena = contrasena
        usuario.rol = rol
        self._guardar_usuarios()
        return True, f"Usuario {nombre} actualizado"

    def eliminar_usuario(self, usuario_id, usuario_actual_id):
        if usuario_id == usuario_actual_id:
            return False, "No puedes eliminarte a ti mismo"
        usuario = self.obtener_usuario_por_id(usuario_id)
        if not usuario:
            return False, "Usuario no encontrado"
        self.usuarios = [u for u in self.usuarios if u.id != usuario_id]
        self._guardar_usuarios()
        return True, f"Usuario {usuario.nombre} eliminado"

    def _guardar_usuarios(self):
        ruta = os.path.join("datos", "usuarios.json")
        with open(ruta, "w", encoding="utf-8") as f:
            json.dump([u.to_dict() for u in self.usuarios], f, ensure_ascii=False, indent=2)