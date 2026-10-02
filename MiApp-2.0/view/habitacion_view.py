import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controller.habitacion_controller import HabitacionController
from openpyxl import Workbook

class HabitacionView:

    def __init__(self, parent):
        self.controller = HabitacionController()
        self.frame = ttk.Frame(parent)

        # titulo del modulo
        tk.Label(self.frame, text="Gestión de Habitaciones",
                 font=("Arial", 12, "bold"), fg="#1F4E79").pack(pady=10)

        # tabla para mostrar las habitaciones
        cols = ("ID", "Número", "Tipo", "Estado", "Tarifa")
        self.tree = ttk.Treeview(self.frame, columns=cols, show="headings", height=8)
        for col in cols:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=110)
        self.tree.pack(padx=10, fill="both", expand=True)

        # botones de accion
        frame_btn = tk.Frame(self.frame)
        frame_btn.pack(pady=8)
        tk.Button(frame_btn, text="➕ Nuevo", width=10, bg="#1F4E79", fg="white",
                  relief="flat", command=self.abrir_formulario_nuevo).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="✏ Editar", width=10, bg="#1F4E79", fg="white",
                  relief="flat", command=self.abrir_formulario_editar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="🗑 Eliminar", width=10, bg="#C0392B", fg="white",
                  relief="flat", command=self.eliminar).pack(side=tk.LEFT, padx=5)
        tk.Button(frame_btn, text="Exportar Excel", width=14, bg="#217346", fg="white",
                  relief="flat", command=self.exportar_excel).pack(side=tk.LEFT, padx=5)

        self.cargar_datos()

    def cargar_datos(self):
        # limpia y recarga la tabla
        for row in self.tree.get_children():
            self.tree.delete(row)
        for hab in self.controller.obtener_habitaciones():
            self.tree.insert("", tk.END, values=hab)

    def abrir_formulario_nuevo(self):
        self.formulario()

    def abrir_formulario_editar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una habitación para editar")
            return
        datos = self.tree.item(seleccion[0])["values"]
        self.formulario(datos)

    def formulario(self, datos=None):
        ventana = tk.Toplevel()
        ventana.iconbitmap("favicon.ico")
        ventana.title("Habitación")
        ventana.geometry("300x250")
        ventana.resizable(False, False)

        campos = ["Número", "Tipo", "Estado", "Tarifa"]
        entradas = {}

        for campo in campos:
            tk.Label(ventana, text=campo).pack(pady=2)
            entrada = tk.Entry(ventana, width=30)
            entrada.pack()
            entradas[campo] = entrada

        if datos:
            entradas["Número"].insert(0, datos[1])
            entradas["Tipo"].insert(0, datos[2])
            entradas["Estado"].insert(0, datos[3])
            entradas["Tarifa"].insert(0, datos[4])

        def guardar():
            numero = entradas["Número"].get()
            tipo   = entradas["Tipo"].get()
            estado = entradas["Estado"].get()
            tarifa = entradas["Tarifa"].get()

            if datos:
                msg = self.controller.actualizar_habitacion(datos[0], numero, tipo, estado, tarifa)
            else:
                msg = self.controller.crear_habitacion(numero, tipo, estado, tarifa)

            messagebox.showinfo("Info", msg)
            ventana.destroy()
            self.cargar_datos()

        tk.Button(ventana, text="Guardar", bg="#1F4E79", fg="white",
                  relief="flat", command=guardar).pack(pady=10)

    def eliminar(self):
        seleccion = self.tree.selection()
        if not seleccion:
            messagebox.showwarning("Aviso", "Selecciona una habitación para eliminar")
            return
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta habitación?"):
            datos = self.tree.item(seleccion[0])["values"]
            msg = self.controller.eliminar_habitacion(datos[0])
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
        hoja.title = "Habitaciones"

        encabezados = ("ID", "Número", "Tipo", "Estado", "Tarifa")
        hoja.append(encabezados)

        for fila in self.tree.get_children():
            hoja.append(self.tree.item(fila)["values"])

        wb.save(ruta)
        messagebox.showinfo("Info", "Datos exportados correctamente")