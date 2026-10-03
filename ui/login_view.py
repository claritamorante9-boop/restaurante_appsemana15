import tkinter as tk
from tkinter import ttk, messagebox

class LoginView:
    def __init__(self, ventana, servicio):
        self.ventana = ventana
        self.servicio = servicio
        self.ventana.title("Restaurante App — Iniciar Sesión")
        self.ventana.geometry("350x220")
        self.ventana.resizable(False, False)
        
        self._construir()

    def _construir(self):
        marco = ttk.Frame(self.ventana, padding=25)
        marco.pack(fill="both", expand=True)

        ttk.Label(marco, text="Restaurante App", font=("Arial", 14, "bold")).pack(pady=(0, 20))

        ttk.Label(marco, text="Usuario:").pack(anchor="w")
        self.ent_usuario = ttk.Entry(marco, width=35)
        self.ent_usuario.pack(pady=(0, 10))
        self.ent_usuario.insert(0, "admin")

        ttk.Label(marco, text="Contraseña:").pack(anchor="w")
        self.ent_clave = ttk.Entry(marco, width=35, show="*")
        self.ent_clave.pack(pady=(0, 15))
        self.ent_clave.insert(0, "1234")

        ttk.Button(marco, text="Ingresar", command=self._ingresar).pack(fill="x", pady=5)

    def _ingresar(self):
        usuario = self.ent_usuario.get().strip()
        clave = self.ent_clave.get().strip()
        
        ok, u = self.servicio.iniciar_sesion(usuario, clave)
        
        if ok:
            self.ventana.destroy()
            from ui.main_view import MainView
            ventana_principal = tk.Tk()
            ventana_principal.geometry("850x550")
            MainView(ventana_principal, self.servicio, u)
            ventana_principal.mainloop()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")