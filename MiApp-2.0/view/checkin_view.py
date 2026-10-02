import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from tkcalendar import DateEntry
from controller.checkin_controller import CheckinController
from openpyxl import Workbook

class CheckinView:

    def __init__(self, parent):
        self.controller = CheckinController()
        self.frame = ttk.Frame(parent)

        # titulo del modulo
        tk.Label(self.frame, text="Gestión de Check-in y Check-out",
                 font=("Arial", 12, "bold"), fg="#1F4E79").pack(pady=10)

        # tabla para mostrar los registros
        cols = ("ID", "Reserva", "Cliente", "Apellido", "Habitación", "Entrada", "Salida", "Estado")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings", height=8)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90)
        self.tree.pack(padx=10, fill="both", expand=True)

        # botones de accion
        frame_btn = tk.Frame(self.frame)
        frame_btn.pack(pady=8)
        tk.Button(frame_btn, text="Check-in",  width=10, bg="#1F4E79", fg="white",
                  relief="flat", command=self.abrir_formulario_checkin).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="Check-out", width=10, bg="#C0392B", fg="white",
                  relief="flat", command=self.hacer_checkout).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="Exportar Excel", width=14, bg="#217346", fg="white",
                  relief="flat", command=self.exportar_excel).pack(side=tk.LEFT, padx=5)

        self.cargar_datos()

    def cargar_datos(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for registro in self.controller.obtener_checkins():
            self.tree.insert("", tk.END, values=registro)

    def abrir_formulario_checkin(self):
        ventana = tk.Toplevel()
        ventana.iconbitmap("favicon.ico")
        ventana.title("Check-in")
        ventana.geometry("300x180")
        ventana.resizable(False, False)

        tk.Label(ventana, text="ID Reserva").pack(pady=2)
        entrada_reserva = tk.Entry(ventana, width=30)
        entrada_reserva.pack()

        # fecha de entrada con tkcalendar
        tk.Label(ventana, text="Fecha entrada").pack(pady=2)
        fecha_entrada = DateEntry(ventana, width=27, date_pattern="yyyy-mm-dd")
        fecha_entrada.pack()

        def guardar():
            id_reserva = entrada_reserva.get()
            entrada    = fecha_entrada.get()
            msg = self.controller.crear_checkin(id_reserva, entrada)
            messagebox.showinfo("Info", msg)
            ventana.destroy()
            self.cargar_datos()

        tk.Button(ventana, text="Registrar", bg="#1F4E79", fg="white",
                  relief="flat", command=guardar).pack(pady=10)

    def hacer_checkout(self):
        # verifica que haya un registro seleccionado y registra la salida
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona un registro para hacer check-out")
            return

        ventana = tk.Toplevel()
        ventana.iconbitmap("favicon.ico")
        ventana.title("Check-out")
        ventana.geometry("300x150")
        ventana.resizable(False, False)

        tk.Label(ventana, text="Fecha salida").pack(pady=2)
        fecha_salida = DateEntry(ventana, width=27, date_pattern="yyyy-mm-dd")
        fecha_salida.pack()

        def guardar():
            datos  = self.tree.item(seleccion[0])["values"]
            salida = fecha_salida.get()
            msg = self.controller.checkout(datos[0], salida)
            messagebox.showinfo("Info", msg)
            ventana.destroy()
            self.cargar_datos()

        tk.Button(ventana, text="Registrar salida", bg="#C0392B", fg="white",
                  relief="flat", command=guardar).pack(pady=10)

    def exportar_excel(self):
        # exporta los datos de la tabla a un archivo Excel
        ruta = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                             filetypes=[("Excel", "*.xlsx")])
        if not ruta:
            return

        wb = Workbook()
        hoja = wb.active
        hoja.title = "Checkins"

        encabezados = ("ID", "Reserva", "Cliente", "Apellido", "Habitación", "Entrada", "Salida", "Estado")
        hoja.append(encabezados)

        for fila in self.tree.get_children():
            hoja.append(self.tree.item(fila)["values"])

        wb.save(ruta)
        messagebox.showinfo("Info", "Datos exportados correctamente")