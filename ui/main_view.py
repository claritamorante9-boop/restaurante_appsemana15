import tkinter as tk
from tkinter import ttk, messagebox

class MainView:
    def __init__(self, ventana, servicio, usuario_actual):
        self.ventana = ventana
        self.servicio = servicio
        self.usuario_actual = usuario_actual
        self.ventana.title(f"Restaurante App — {usuario_actual.nombre}")
        self.ventana.geometry("900x600")
        
        self._construir_pestanas()
        self._cargar_combos()
        self._cargar_historial_ventas()
        if hasattr(self, 'tree_usuarios'):
            self._cargar_usuarios()

    def _construir_pestanas(self):
        self.notebook = ttk.Notebook(self.ventana)
        self.notebook.pack(fill="both", expand=True, padx=10, pady=10)

        # === Pestaña Registrar Venta ===
        self.frame_venta = ttk.Frame(self.notebook, padding=15)
        self.notebook.add(self.frame_venta, text="Registrar Venta")
        self._construir_pestaña_venta()

        # === Pestaña Gestión de Usuarios ===
        if self.usuario_actual.rol == "Administrador":
            self.frame_usuarios = ttk.Frame(self.notebook, padding=15)
            self.notebook.add(self.frame_usuarios, text="Gestión de Usuarios")
            self._construir_pestaña_usuarios()

    # === PESTAÑA: REGISTRAR VENTA ===
    def _construir_pestaña_venta(self):
        marco = ttk.Frame(self.frame_venta)
        marco.pack(fill="x", pady=5)

        ttk.Label(marco, text="Usuario:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.cmb_usuario = ttk.Combobox(marco, state="readonly", width=45)
        self.cmb_usuario.grid(row=0, column=1, padx=5, pady=5)
        self.cmb_usuario.bind("<<ComboboxSelected>>", self._actualizar_productos)

        ttk.Label(marco, text="Producto:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.cmb_producto = ttk.Combobox(marco, state="readonly", width=45)
        self.cmb_producto.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(marco, text="Cantidad:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.ent_cantidad = ttk.Entry(marco, width=48)
        self.ent_cantidad.grid(row=2, column=1, padx=5, pady=5)
        self.ent_cantidad.insert(0, "1")

        ttk.Button(marco, text="Registrar Venta", 
                   command=self._registrar_venta).grid(row=3, column=0, columnspan=2, pady=15)

        # Tabla historial
        ttk.Label(self.frame_venta, text="Historial de Ventas:").pack(anchor="w", pady=(15,5))
        columnas = ("id", "usuario", "producto", "cantidad", "fecha")
        self.tree_ventas = ttk.Treeview(self.frame_venta, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tree_ventas.heading(col, text=col.title())
            self.tree_ventas.column(col, width=160)
        self.tree_ventas.pack(fill="both", expand=True)

    def _cargar_combos(self, evento=None):
        usuarios = self.servicio.obtener_usuarios()
        self.cmb_usuario["values"] = [f"{u.id} - {u.nombre}" for u in usuarios]
        if usuarios:
            self.cmb_usuario.current(0)
            self._actualizar_productos()

    def _actualizar_productos(self, evento=None):
        productos = self.servicio.obtener_productos()
        self.cmb_producto["values"] = [f"{p.id} - {p.nombre} - ${p.precio:.2f}" for p in productos]
        if productos:
            self.cmb_producto.current(0)

    def _registrar_venta(self):
        sel_usuario = self.cmb_usuario.get()
        sel_producto = self.cmb_producto.get()
        cantidad = self.ent_cantidad.get().strip()

        if not sel_usuario or not sel_producto or not cantidad:
            messagebox.showwarning("Aviso", "Completa todos los campos")
            return

        try:
            usuario_id = int(sel_usuario.split(" - ")[0])
            producto_id = int(sel_producto.split(" - ")[0])
            cant = int(cantidad)
            if cant <= 0:
                raise ValueError
        except:
            messagebox.showerror("Error", "Datos inválidos")
            return

        ok, msg = self.servicio.registrar_venta(usuario_id, producto_id, cant)
        if ok:
            messagebox.showinfo("Éxito", msg)
            self._cargar_historial_ventas()
            self.ent_cantidad.delete(0, tk.END)
            self.ent_cantidad.insert(0, "1")
        else:
            messagebox.showerror("Error", msg)

    def _cargar_historial_ventas(self):
        if not hasattr(self, 'tree_ventas'):
            return
        for fila in self.tree_ventas.get_children():
            self.tree_ventas.delete(fila)
        for v in self.servicio.obtener_ventas():
            usuario = self.servicio.obtener_usuario_por_id(v.usuario_id)
            nombre_usuario = usuario.nombre if usuario else "Desconocido"
            producto = next((p for p in self.servicio.obtener_productos() if p.id == v.producto_id), None)
            nombre_producto = producto.nombre if producto else "Desconocido"
            self.tree_ventas.insert("", "end", values=(
                v.id, nombre_usuario, nombre_producto, v.cantidad, v.fecha
            ))

    # === PESTAÑA: GESTIÓN DE USUARIOS ===
    def _construir_pestaña_usuarios(self):
        marco_form = ttk.Frame(self.frame_usuarios)
        marco_form.pack(fill="x", pady=10)

        ttk.Label(marco_form, text="Nombre:").grid(row=0, column=0, sticky="w", padx=5, pady=3)
        self.ent_nombre = ttk.Entry(marco_form, width=30)
        self.ent_nombre.grid(row=0, column=1, padx=5, pady=3)

        ttk.Label(marco_form, text="Contraseña:").grid(row=0, column=2, sticky="w", padx=5, pady=3)
        self.ent_clave = ttk.Entry(marco_form, width=30, show="*")
        self.ent_clave.grid(row=0, column=3, padx=5, pady=3)

        ttk.Label(marco_form, text="Rol:").grid(row=1, column=0, sticky="w", padx=5, pady=3)
        self.cmb_rol = ttk.Combobox(marco_form, values=["Administrador", "Empleado"], state="readonly", width=28)
        self.cmb_rol.grid(row=1, column=1, padx=5, pady=3)
        self.cmb_rol.current(1)

        self.usuario_seleccionado_id = None

        marco_botones = ttk.Frame(self.frame_usuarios)
        marco_botones.pack(fill="x", pady=5)
        self.btn_guardar = ttk.Button(marco_botones, text="Guardar", command=self._guardar_usuario)
        self.btn_guardar.pack(side="left", padx=5)
        self.btn_limpiar = ttk.Button(marco_botones, text="Limpiar", command=self._limpiar_formulario)
        self.btn_limpiar.pack(side="left", padx=5)
        self.btn_eliminar = ttk.Button(marco_botones, text="Eliminar", command=self._eliminar_usuario)
        self.btn_eliminar.pack(side="left", padx=5)

        # Tabla
        columnas = ("id", "nombre", "rol")
        self.tree_usuarios = ttk.Treeview(self.frame_usuarios, columns=columnas, show="headings", height=10)
        for col in columnas:
            self.tree_usuarios.heading(col, text=col.title())
            self.tree_usuarios.column(col, width=250)
        self.tree_usuarios.pack(fill="both", expand=True, pady=10)
        self.tree_usuarios.bind("<<TreeviewSelect>>", self._al_cambiar_seleccion)

    def _cargar_usuarios(self):
        for fila in self.tree_usuarios.get_children():
            self.tree_usuarios.delete(fila)
        for u in self.servicio.obtener_usuarios():
            self.tree_usuarios.insert("", "end", values=(u.id, u.nombre, u.rol))

    def _al_cambiar_seleccion(self, evento):
        seleccion = self.tree_usuarios.selection()
        if seleccion:
            fila = self.tree_usuarios.item(seleccion[0])["values"]
            self.usuario_seleccionado_id = fila[0]
            self.ent_nombre.delete(0, tk.END)
            self.ent_nombre.insert(0, fila[1])
            self.cmb_rol.set(fila[2])
            self.ent_clave.delete(0, tk.END)

    def _guardar_usuario(self):
        nombre = self.ent_nombre.get().strip()
        clave = self.ent_clave.get().strip()
        rol = self.cmb_rol.get()

        if self.usuario_seleccionado_id:
            ok, msg = self.servicio.actualizar_usuario(
                int(self.usuario_seleccionado_id), nombre, clave, rol
            )
        else:
            ok, msg = self.servicio.registrar_usuario(nombre, clave, rol)

        if ok:
            messagebox.showinfo("Éxito", msg)
            self._limpiar_formulario()
            self._cargar_usuarios()
            self._cargar_combos()
        else:
            messagebox.showerror("Error", msg)

    def _eliminar_usuario(self):
        if not self.usuario_seleccionado_id:
            messagebox.showwarning("Aviso", "Selecciona un usuario")
            return
        if not messagebox.askyesno("Confirmar", "¿Eliminar este usuario?"):
            return
        ok, msg = self.servicio.eliminar_usuario(
            int(self.usuario_seleccionado_id), self.usuario_actual.id
        )
        if ok:
            messagebox.showinfo("Éxito", msg)
            self._limpiar_formulario()
            self._cargar_usuarios()
            self._cargar_combos()
        else:
            messagebox.showerror("Error", msg)

    def _limpiar_formulario(self):
        self.usuario_seleccionado_id = None
        self.ent_nombre.delete(0, tk.END)
        self.ent_clave.delete(0, tk.END)
        self.cmb_rol.current(1)
        self.tree_usuarios.selection_remove(self.tree_usuarios.selection())