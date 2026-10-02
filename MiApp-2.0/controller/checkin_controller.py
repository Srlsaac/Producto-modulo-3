from model.checkin_model import CheckinModel

class CheckinController:

    def __init__(self):
        # conectamos con el model
        self.model = CheckinModel()

    def obtener_checkins(self):
        # retorna todos los checkins
        return self.model.obtener_checkins()

    def crear_checkin(self, id_reserva, fecha_entrada):
        # valida campos obligatorios
        if not id_reserva or not fecha_entrada:
            return "La reserva y la fecha de entrada son obligatorias"
        self.model.crear_checkin(id_reserva, fecha_entrada)
        return "Check-in registrado correctamente"

    def checkout(self, id, fecha_salida):
        # registra la salida del huesped
        if not fecha_salida:
            return "La fecha de salida es obligatoria"
        self.model.checkout(id, fecha_salida)
        return "Check-out registrado correctamente"

    def eliminar_checkin(self, id):
        # elimina el registro de checkin por id
        self.model.eliminar_checkin(id)
        return "Registro eliminado correctamente"