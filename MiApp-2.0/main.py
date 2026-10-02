
# main.py
import tkinter as tk
from tkinter import ttk
from view.cliente_view import ClienteView
from view.habitacion_view import HabitacionView
from view.reserva_view import ReservaView
from view.checkin_view import CheckinView

# ventana principal
root = tk.Tk()
root.title("HotelPro — Estancias de Lujo")
root.geometry("800x500")
root.resizable(False, False)

# estilos
style = ttk.Style()
style.configure("TNotebook.Tab", font=("Arial", 10), padding=[10, 5])

# contenedor de pestañas
notebook = ttk.Notebook(root)

# instanciamos cada modulo y lo agregamos al notebook
clientes    = ClienteView(notebook)
habitaciones = HabitacionView(notebook)
reservas    = ReservaView(notebook)
checkin     = CheckinView(notebook)

notebook.add(clientes.frame,     text="  Clientes       ")
notebook.add(habitaciones.frame, text="  Habitaciones   ")
notebook.add(reservas.frame,     text="  Reservas       ")
notebook.add(checkin.frame,      text="  Check-in/out   ")
notebook.pack(expand=True, fill="both", padx=10, pady=10)

# iniciamos la ventana
root.mainloop()