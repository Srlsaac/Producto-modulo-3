import mysql.connector


# el model es el unico que habla con MySQL: aqui no hay validaciones ni interfaz
class ClienteModel:

    def __init__(self):
        # conexion a la base de datos
        self.conn = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="hotelpro"
        )
        # el cursor es el objeto que ejecuta los stored procedures
        self.cursor = self.conn.cursor()

    def obtener_clientes(self):
        # retorna todos los clientes
        #  callproc ejecuta un stored procedure de MySQL usando su nombre
        self.cursor.callproc("sp_obtener_clientes")
        # stored_results trae lo que devolvio el procedure (el SELECT con los clientes)
        for result in self.cursor.stored_results():
            return result.fetchall()

    def crear_cliente(self, nombre, apellido, documento, telefono, correo):
        # inserta un nuevo cliente
        # llama a sp_crear_cliente pasandole los datos como parametros
        self.cursor.callproc("sp_crear_cliente", (nombre, apellido, documento, telefono, correo))
        # commit confirma el cambio en la base de datos; sin esto no se guarda
        self.conn.commit()

    def actualizar_cliente(self, id, nombre, apellido, documento, telefono, correo):
        # actualiza los datos de un cliente
        self.cursor.callproc("sp_actualizar_cliente", (id, nombre, apellido, documento, telefono, correo))
        self.conn.commit()

    def eliminar_cliente(self, id):
        # elimina un cliente por id
        self.cursor.callproc("sp_eliminar_cliente", (id,))
        self.conn.commit()