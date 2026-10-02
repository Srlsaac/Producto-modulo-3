from model.reserva_model import ReservaModel

class ReservaController:

    def __init__(self):
        # conectamos con el model
        self.model = ReservaModel()

    def obtener_reservas(self):
        # retorna todas las reservas
        return self.model.obtener_reservas()

    def crear_reserva(self, id_cliente, id_habitacion, fecha_llegada, fecha_salida, estado):
        # valida campos obligatorios
        if not id_cliente or not id_habitacion or not fecha_llegada or not fecha_salida:
            return "Todos los campos son obligatorios"
        self.model.crear_reserva(id_cliente, id_habitacion, fecha_llegada, fecha_salida, estado)
        return "Reserva creada correctamente"

    def actualizar_reserva(self, id, fecha_llegada, fecha_salida, estado):
        # valida y actualiza la reserva
        if not fecha_llegada or not fecha_salida:
            return "Las fechas son obligatorias"
        self.model.actualizar_reserva(id, fecha_llegada, fecha_salida, estado)
        return "Reserva actualizada correctamente"

    def eliminar_reserva(self, id):
        # elimina la reserva por id
        self.model.eliminar_reserva(id)
        return "Reserva eliminada correctamente"