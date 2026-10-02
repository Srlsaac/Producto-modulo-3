import mysql.connector

class HabitacionModel:

    def __init__(self):
        # conexion a la base de datos
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hotelpro"
        )
        self.cursor = self.conn.cursor()

    def obtener_habitaciones(self):
        # retorna todas las habitaciones
        self.cursor.callproc("sp_obtener_habitaciones")
        for result in self.cursor.stored_results():
            return result.fetchall()

    def crear_habitacion(self, numero, tipo, estado, tarifa):
        # inserta una nueva habitacion
        self.cursor.callproc("sp_crear_habitacion", (numero, tipo, estado, tarifa))
        self.conn.commit()

    def actualizar_habitacion(self, id, numero, tipo, estado, tarifa):
        # actualiza los datos de una habitacion
        self.cursor.callproc("sp_actualizar_habitacion", (id, numero, tipo, estado, tarifa))
        self.conn.commit()

    def eliminar_habitacion(self, id):
        # elimina una habitacion por id
        self.cursor.callproc("sp_eliminar_habitacion", (id,))
        self.conn.commit()