import tkinter as tk
from servicios.restaurante_servicio import RestauranteServicio
from ui.login_view import LoginView

class App:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Restaurante App")
        self.servicio = RestauranteServicio()
        self._mostrar_login()

    def _mostrar_login(self):
        self.login_view = LoginView(self.ventana, self.servicio)

    def ejecutar(self):
        self.ventana.mainloop()

if __name__ == "__main__":
    app = App()
    app.ejecutar()