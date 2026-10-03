class Usuario:
    def __init__(self, id, nombre, contrasena="", rol="Empleado"):
        self.id = id
        self.nombre = nombre
        self.contrasena = contrasena
        self.rol = rol  # Administrador / Empleado / Cliente

    def to_dict(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "contrasena": self.contrasena,
            "rol": self.rol
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos.get("contrasena", ""),
            datos.get("rol", "Empleado")
        )