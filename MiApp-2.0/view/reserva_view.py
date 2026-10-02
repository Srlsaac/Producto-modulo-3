import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from controller.reserva_controller import ReservaController
from openpyxl import Workbook

class ReservaView:

    def __init__(self, parent):
        self.controller = ReservaController()
        self.frame = ttk.Frame(parent)

        # titulo del modulo
        tk.Label(self.frame, text="Gestión de Reservas",
                 font=("Arial", 12, "bold"), fg="#1F4E79").pack(pady=10)

        # tabla para mostrar las reservas
        cols = ("ID", "Cliente", "Apellido", "Habitación", "Llegada", "Salida", "Estado")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings", height=8)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90)
        self.tree.pack(padx=10, fill="both", expand=True)

        # botones de accion
        frame_btn = tk.Frame(self.frame)
        frame_btn.pack(pady=8)
        tk.Button(frame_btn, text="Nueva",    width=10, bg="#1F4E79", fg="white",
                  relief="flat", command=self.abrir_formulario_nuevo).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="Editar",   width=10, bg="#1F4E79", fg="white",
                  relief="flat", command=self.abrir_formulario_editar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="Cancelar", width=10, bg="#C0392B", fg="white",
                  relief="flat", command=self.eliminar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="Exportar Excel", width=14, bg="#217346", fg="white",
                  relief="flat", command=self.exportar_excel).pack(side=tk.LEFT, padx=5)

        self.cargar_datos()

    def cargar_datos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for reserva in self.controller.obtener_reservas():
            self.tree.insert("", tk.END, values=reserva)

    def abrir_formulario_nuevo(self):
        self.formulario()

    def abrir_formulario_editar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una reserva para editar")
            return
        datos = self.tree.item(seleccion[0])["values"]
        self.formulario(datos)

    def formulario(self, datos=None):
        ventana = tk.Toplevel()
        ventana.iconbitmap("favicon.ico")
        ventana.title("Reserva")
        ventana.geometry("300x300")
        ventana.resizable(False, False)

        # campos de texto
        tk.Label(ventana, text="ID Cliente").pack(pady=2)
        entrada_cliente = tk.Entry(ventana, width=30)
        entrada_cliente.pack()

        tk.Label(ventana, text="ID Habitación").pack(pady=2)
        entrada_hab = tk.Entry(ventana, width=30)
        entrada_hab.pack()

        # campos de fecha con tkcalendar
        tk.Label(ventana, text="Fecha llegada").pack(pady=2)
        fecha_llegada = DateEntry(ventana, width=27, date_pattern="yyyy-mm-dd")
        fecha_llegada.pack()

        tk.Label(ventana, text="Fecha salida").pack(pady=2)
        fecha_salida = DateEntry(ventana, width=27, date_pattern="yyyy-mm-dd")
        fecha_salida.pack()

        tk.Label(ventana, text="Estado").pack(pady=2)
        entrada_estado = tk.Entry(ventana, width=30)
        entrada_estado.pack()

        if datos:
            entrada_cliente.insert(0, datos[0])
            entrada_hab.insert(0, datos[3])
            entrada_estado.insert(0, datos[6])

        def guardar():
            id_cliente    = entrada_cliente.get()
            id_habitacion = entrada_hab.get()
            llegada       = fecha_llegada.get()
            salida        = fecha_salida.get()
            estado        = entrada_estado.get()

            if datos:
                msg = self.controller.actualizar_reserva(datos[0], llegada, salida, estado)
            else:
                msg = self.controller.crear_reserva(id_cliente, id_habitacion, llegada, salida, estado)

            messagebox.showinfo("Info", msg)
            ventana.destroy()
            self.cargar_datos()

        tk.Button(ventana, text="Guardar", bg="#1F4E79", fg="white",
                  relief="flat", command=guardar).pack(pady=10)

    def eliminar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una reserva para cancelar")
            return
        if messagebox.askyesno("Confirmar", "¿Estás seguro de cancelar esta reserva?"):
            datos = self.tree.item(seleccion[0])["values"]
            msg = self.controller.eliminar_reserva(datos[0])
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
        hoja.title = "Reservas"

        encabezados = ("ID", "Cliente", "Apellido", "Habitación", "Llegada", "Salida", "Estado")
        hoja.append(encabezados)

        for fila in self.tree.get_children():
            hoja.append(self.tree.item(fila)["values"])

        wb.save(ruta)
        messagebox.showinfo("Info", "Datos exportados correctamente")