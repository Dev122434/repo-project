from interfaz.formulario import BaseListWindow
from models.entities import Producto
from typing import Optional
from tkinter import messagebox, ttk
import tkinter as tk
from database.conexion import engine
from sqlmodel import select, Session

class ProductoWindow(BaseListWindow):
    def __init__(self, master):
        cols = [
            ("id_producto", "ID"),
            ("modelo", "Modelo"),
            ("talla", "Talla"),
            ("color", "Color"),
            ("precio", "Precio"),
            ("stock_actual", "Stock"),
        ]
        super().__init__(master, "Productos", cols)
        self.load_data()

    def load_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        with Session(engine) as session:
            rows = session.exec(select(Producto)).all()
            for p in rows:
                self.tree.insert("", "end", values=(p.id_producto, p.modelo, p.talla, p.color, p.precio, p.stock_actual))

    def on_add(self):
        ProductoForm(self, mode="add", on_done=self.load_data)

    def on_edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un producto.", parent=self)
            return
        vals = self.tree.item(sel[0])["values"]
        ProductoForm(self, mode="edit", producto_id=vals[0], on_done=self.load_data)

    def on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un producto.", parent=self)
            return
        vals = self.tree.item(sel[0])["values"]
        pk = vals[0]
        if not messagebox.askyesno("Confirmar", "¿Eliminar producto?", parent=self):
            return
        with Session(engine) as session:
            obj = session.get(Producto, pk)
            if obj:
                session.delete(obj)
                session.commit()
        self.load_data()

class ProductoForm(tk.Toplevel):
    def __init__(self, master, mode="add", producto_id: Optional[int]=None, on_done=None):
        super().__init__(master)
        self.mode = mode
        self.producto_id = producto_id
        self.on_done = on_done
        self.title("Producto - " + ("Nuevo" if mode=="add" else "Editar"))
        self.geometry("420x320")
        self.build()
        if mode == "edit":
            self.load_producto()

    def build(self):
        frm = ttk.Frame(self, padding=8)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Modelo:").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_modelo = ttk.Entry(frm, width=30)
        self.ent_modelo.grid(row=0, column=1, pady=4)
        ttk.Label(frm, text="Talla:").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_talla = ttk.Entry(frm)
        self.ent_talla.grid(row=1, column=1, pady=4)
        ttk.Label(frm, text="Color:").grid(row=2, column=0, sticky="w", pady=4)
        self.ent_color = ttk.Entry(frm)
        self.ent_color.grid(row=2, column=1, pady=4)
        ttk.Label(frm, text="Precio:").grid(row=3, column=0, sticky="w", pady=4)
        self.ent_precio = ttk.Entry(frm)
        self.ent_precio.grid(row=3, column=1, pady=4)
        ttk.Label(frm, text="Stock Inicial:").grid(row=4, column=0, sticky="w", pady=4)
        self.ent_stock = ttk.Entry(frm)
        self.ent_stock.grid(row=4, column=1, pady=4)

        btn_save = ttk.Button(frm, text="Guardar", command=self.save)
        btn_cancel = ttk.Button(frm, text="Cancelar", command=self.destroy)
        btn_save.grid(row=5, column=0, pady=12)
        btn_cancel.grid(row=5, column=1, pady=12)

    def load_producto(self):
        with Session(engine) as session:
            p = session.get(Producto, self.producto_id)
            if p:
                self.ent_modelo.insert(0, p.modelo)
                self.ent_talla.insert(0, str(p.talla))
                self.ent_color.insert(0, p.color)
                self.ent_precio.insert(0, str(p.precio))
                self.ent_stock.insert(0, str(p.stock_actual))

    def save(self):
        modelo = self.ent_modelo.get().strip()
        try:
            talla = float(self.ent_talla.get().strip())
            precio = float(self.ent_precio.get().strip())
            stock = int(self.ent_stock.get().strip())
        except Exception:
            messagebox.showwarning("Validación", "Talla / Precio / Stock no válidos.", parent=self)
            return
        color = self.ent_color.get().strip()
        if not (modelo and color):
            messagebox.showwarning("Validación", "Complete todos los campos.", parent=self)
            return
        with Session(engine) as session:
            try:
                if self.mode == "add":
                    p = Producto(modelo=modelo, talla=talla, color=color, precio=precio, stock_actual=stock)
                    session.add(p)
                else:
                    p = session.get(Producto, self.producto_id)
                    if not p:
                        messagebox.showerror("Error", "Producto no encontrado.", parent=self)
                        return
                    p.modelo = modelo
                    p.talla = talla
                    p.color = color
                    p.precio = precio
                    p.stock_actual = stock
                    session.add(p)
                session.commit()
                if self.on_done:
                    self.on_done()
                self.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)