from datetime import datetime

class Venta:
    def __init__(self, id, usuario_id, producto_id, cantidad):
        self.id = id
        self.usuario_id = usuario_id
        self.producto_id = producto_id
        self.cantidad = cantidad
        self.fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def to_dict(self):
        return {
            "id": self.id,
            "usuario_id": self.usuario_id,
            "producto_id": self.producto_id,
            "cantidad": self.cantidad,
            "fecha": self.fecha
        }

    @classmethod
    def from_dict(cls, datos):
        return cls(
            id=datos["id"],
            usuario_id=datos["usuario_id"],
            producto_id=datos["producto_id"],
            cantidad=datos["cantidad"]
        )