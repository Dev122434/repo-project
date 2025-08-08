from tkinter import ttk
from interfaz.cliente import ClienteWindow
from interfaz.producto import ProductoWindow
from interfaz.proveedor import ProveedorWindow
from interfaz.compra import CompraWindow, DetalleCompraWindow
from interfaz.venta import VentaWindow, DetalleVentaWindow
import tkinter as tk

def main_window():
    root = tk.Tk()
    root.title("TIENDA - Consultas (CRUD) - Mejorado")
    root.geometry("420x520")
    frm = ttk.Frame(root, padding=16)
    frm.pack(fill="both", expand=True)
    title = ttk.Label(frm, text="Consultas", font=("Helvetica", 16))
    title.pack(pady=6)

    btns = [
        ("Clientes", lambda: ClienteWindow(root)),
        ("Proveedores", lambda: ProveedorWindow(root)),
        ("Productos", lambda: ProductoWindow(root)),
        ("Compras (cabecera)", lambda: CompraWindow(root)),
        ("Detalle Compras", lambda: DetalleCompraWindow(root)),
        ("Ventas (cabecera)", lambda: VentaWindow(root)),
        ("Detalle Ventas", lambda: DetalleVentaWindow(root)),
    ]

    for (txt, cmd) in btns:
        b = ttk.Button(frm, text=txt, command=cmd)
        b.pack(fill="x", pady=6, ipadx=4, ipady=8)

    btn_close = ttk.Button(frm, text="Cerrar", command=root.destroy)
    btn_close.pack(side="bottom", pady=10)
    root.mainloop()