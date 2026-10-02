from model.cliente_model import ClienteModel

#el controller es el intermediario: valida los datos y decide si se llama al model
class ClienteController:

    def __init__(self):
        # conectamos con el model
        self.model = ClienteModel()

    def obtener_clientes(self):
        # pide los clientes al model y los retorna a la view
        return self.model.obtener_clientes()

    def crear_cliente(self, nombre, apellido, documento, telefono, correo):
        # valida que los campos obligatorios no esten vacios
        if not nombre or not apellido or not documento:
            # el controller no muestra nada en pantalla: devuelve un texto y la vista lo muestra
            return "Los campos nombre, apellido y documento son obligatorios"
        # si la validacion pasa, le pide al model que guarde el cliente
        self.model.crear_cliente(nombre, apellido, documento, telefono, correo)
        return "Cliente creado correctamente"

    def actualizar_cliente(self, id, nombre, apellido, documento, telefono, correo):
        # valida y actualiza el cliente
        if not nombre or not apellido or not documento:
            return "Los campos nombre, apellido y documento son obligatorios"
        self.model.actualizar_cliente(id, nombre, apellido, documento, telefono, correo)
        return "Cliente actualizado correctamente"

    def eliminar_cliente(self, id):
        # elimina el cliente por id
        self.model.eliminar_cliente(id)
        return "Cliente eliminado correctamente"