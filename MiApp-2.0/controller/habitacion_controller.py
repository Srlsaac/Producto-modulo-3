from model.habitacion_model import HabitacionModel

class HabitacionController:

    def __init__(self):
        # conectamos con el model
        self.model = HabitacionModel()

    def obtener_habitaciones(self):
        # retorna todas las habitaciones
        return self.model.obtener_habitaciones()

    def crear_habitacion(self, numero, tipo, estado, tarifa):
        # valida campos obligatorios
        if not numero or not tipo or not tarifa:
            return "Los campos numero, tipo y tarifa son obligatorios"
        self.model.crear_habitacion(numero, tipo, estado, tarifa)
        return "Habitacion creada correctamente"

    def actualizar_habitacion(self, id, numero, tipo, estado, tarifa):
        # valida y actualiza la habitacion
        if not numero or not tipo or not tarifa:
            return "Los campos numero, tipo y tarifa son obligatorios"
        self.model.actualizar_habitacion(id, numero, tipo, estado, tarifa)
        return "Habitacion actualizada correctamente"

    def eliminar_habitacion(self, id):
        # elimina la habitacion por id
        self.model.eliminar_habitacion(id)
        return "Habitacion eliminada correctamente"