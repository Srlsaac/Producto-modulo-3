import mysql.connector

class ReservaModel:

    def __init__(self):
        # conexion a la base de datos
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hotelpro"
        )
        self.cursor = self.conn.cursor()

    def obtener_reservas(self):
        # retorna todas las reservas con datos de cliente y habitacion
        self.cursor.callproc("sp_obtener_reservas")
        for result in self.cursor.stored_results():
            return result.fetchall()

    def crear_reserva(self, id_cliente, id_habitacion, fecha_llegada, fecha_salida, estado):
        # inserta una nueva reserva
        self.cursor.callproc("sp_crear_reserva", (id_cliente, id_habitacion, fecha_llegada, fecha_salida, estado))
        self.conn.commit()

    def actualizar_reserva(self, id, fecha_llegada, fecha_salida, estado):
        # actualiza los datos de una reserva
        self.cursor.callproc("sp_actualizar_reserva", (id, fecha_llegada, fecha_salida, estado))
        self.conn.commit()

    def eliminar_reserva(self, id):
        # elimina una reserva por id
        self.cursor.callproc("sp_eliminar_reserva", (id,))
        self.conn.commit()