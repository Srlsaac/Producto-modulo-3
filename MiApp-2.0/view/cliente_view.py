import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controller.cliente_controller import ClienteController
from openpyxl import Workbook

class ClienteView:

    def __init__(self, parent):

        self.controller = ClienteController()
        self.frame = ttk.Frame(parent)

        # titulo del modulo
        tk.Label(self.frame, text="Gestión de Clientes",
                 font=("Arial", 12, "bold"), fg="#1F4E79").pack(pady=10)

        # tabla para mostrar los clientes
        cols = ("ID", "Nombre", "Apellido", "Documento", "Teléfono", "Correo")
        # Treeview = la tabla donde se listan los clientes
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings", height=8)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(padx=10, fill="both", expand=True)

        # botones de accion
        frame_btn = tk.Frame(self.frame)
        frame_btn.pack(pady=8)
        #cada boton llama a una funcion de esta clase con command=
        tk.Button(frame_btn, text="➕ Nuevo", width=10, bg="#1F4E79", fg="white",
                  relief="flat", command=self.abrir_formulario_nuevo).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="✏ Editar", width=10, bg="#1F4E79", fg="white",
                  relief="flat", command=self.abrir_formulario_editar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="🗑 Eliminar", width=10, bg="#C0392B", fg="white",
                  relief="flat", command=self.eliminar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="Exportar Excel", width=14, bg="#217346", fg="white",
                  relief="flat", command=self.exportar_excel).pack(side=tk.LEFT, padx=5)

        # cargamos los datos al iniciar
        self.cargar_datos()

    def cargar_datos(self):
        # limpia la tabla y vuelve a cargar los datos
        for row in self.tree.get_children():
            self.tree.delete(row)
        # pide los datos al controller que se los pide al model y llena la tabla
        for cliente in self.controller.obtener_clientes():
            self.tree.insert("", tk.END, values=cliente)

    def abrir_formulario_nuevo(self):
        # abre el formulario para crear un cliente
        self.formulario()

    def abrir_formulario_editar(self):
        # verifica que haya un cliente seleccionado y abre el formulario
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un cliente para editar")
            return
        datos = self.tree.item(seleccion[0])["values"]
        self.formulario(datos)

    # un solo formulario sirve para crear y para editar:
    # si llegan datos se rellenan los campos, si no queda vacio
    def formulario(self, datos=None):
        # ventana emergente para crear o editar un cliente
        ventana = tk.Toplevel()
        ventana.iconbitmap("favicon.ico")
        ventana.title("Cliente")
        ventana.geometry("300x280")
        ventana.resizable(False, False)

        campos = ["Nombre", "Apellido", "Documento", "Teléfono", "Correo"]
        entradas = {}

        for campo in campos:
            tk.Label(ventana, text=campo).pack(pady=2)
            entrada = tk.Entry(ventana, width=30)
            entrada.pack()
            entradas[campo] = entrada

        # si es edicion, pre-llenamos los campos
        if datos:
            entradas["Nombre"].insert(0, datos[1])
            entradas["Apellido"].insert(0, datos[2])
            entradas["Documento"].insert(0, datos[3])
            entradas["Teléfono"].insert(0, datos[4])
            entradas["Correo"].insert(0, datos[5])

        #al dar clic en Guardar la vista recoge los datos y se los pasa al controller
        def guardar():
            nombre    = entradas["Nombre"].get()
            apellido  = entradas["Apellido"].get()
            documento = entradas["Documento"].get()
            telefono  = entradas["Teléfono"].get()
            correo    = entradas["Correo"].get()

            if datos:
                # actualiza el cliente existente
                msg = self.controller.actualizar_cliente(datos[0], nombre, apellido, documento, telefono, correo)
            else:
                # crea un nuevo cliente
                msg = self.controller.crear_cliente(nombre, apellido, documento, telefono, correo)

            # el controller devuelve un mensaje exito o error y la vista solo lo muestra
            messagebox.showinfo("Info", msg)
            ventana.destroy()
            self.cargar_datos()

        tk.Button(ventana, text="Guardar", bg="#1F4E79", fg="white",
                  relief="flat", command=guardar).pack(pady=10)

    def eliminar(self):
        # confirma y elimina el cliente seleccionado
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un cliente para eliminar")
            return
        #confirmacion antes de eliminar requisito del enunciado
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este cliente?"):
            datos = self.tree.item(seleccion[0])["values"]
            msg = self.controller.eliminar_cliente(datos[0])
            messagebox.showinfo("Info", msg)
            self.cargar_datos()
    def eliminar(self):
        # confirma y elimina el cliente seleccionado
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un cliente para eliminar")
            return
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar este cliente?"):
            datos = self.tree.item(seleccion[0])["values"]
            msg = self.controller.eliminar_cliente(datos[0])
            messagebox.showinfo("Info", msg)
            self.cargar_datos()

    def exportar_excel(self):
        # exporta los datos de la tabla a un archivo Excel
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel", "*.xlsx")])
        if not ruta:
            return

        wb = Workbook()
        hoja = wb.active
        hoja.title = "Clientes"

        encabezados = ("ID", "Nombre", "Apellido", "Documento", "Teléfono", "Correo")
        hoja.append(encabezados)

        for fila in self.tree.get_children():
            hoja.append(self.tree.item(fila)["values"])

        wb.save(ruta)
        messagebox.showinfo("Info", "Datos exportados correctamente")