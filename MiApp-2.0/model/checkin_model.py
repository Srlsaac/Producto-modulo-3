import mysql.connector

class CheckinModel:

    def __init__(self):
        # conexion a la base de datos
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hotelpro"
        )
        self.cursor = self.conn.cursor()

    def obtener_checkins(self):
        # retorna todos los checkins con datos relacionados
        self.cursor.callproc("sp_obtener_checkins")
        for result in self.cursor.stored_results():
            return result.fetchall()

    def crear_checkin(self, id_reserva, fecha_entrada):
        # registra el check-in de un huesped
        self.cursor.callproc("sp_crear_checkin", (id_reserva, fecha_entrada))
        self.conn.commit()

    def checkout(self, id, fecha_salida):
        # registra la salida del huesped
        self.cursor.callproc("sp_checkout", (id, fecha_salida))
        self.conn.commit()

    def eliminar_checkin(self, id):
        # elimina un registro de checkin por id
        self.cursor.callproc("sp_eliminar_checkin", (id,))
        self.conn.commit()