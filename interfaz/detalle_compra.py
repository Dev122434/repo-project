from interfaz.formulario import BaseListWindow
from models.entities import Producto, Compra, DetalleCompra
from sqlmodel import Session, select
from main import map_products
from typing import Optional
from tkinter import ttk, messagebox
from database.conexion import engine
import tkinter as tk

class DetalleCompraWindow(BaseListWindow):
    def __init__(self, master, compra_id: Optional[int]=None):
        self.compra_id = compra_id
        cols = [
            ("id_detalle_compra", "ID"),
            ("id_compra", "ID Compra"),
            ("id_producto", "ID Producto"),
            ("cantidad", "Cantidad"),
            ("costo_unitario", "Costo Unitario"),
            ("subtotal", "Subtotal"),
        ]
        title = f"DetalleCompra - Compra {compra_id}" if compra_id else "DetalleCompra (general)"
        super().__init__(master, title, cols)
        self.load_data()

    def load_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        with Session(engine) as session:
            q = select(DetalleCompra)
            if self.compra_id:
                q = q.where(DetalleCompra.id_compra == self.compra_id)
            rows = session.exec(q).all()
            for d in rows:
                self.tree.insert("", "end", values=(d.id_detalle_compra, d.id_compra, d.id_producto, d.cantidad, d.costo_unitario, d.subtotal))

    def on_add(self):
        DetalleCompraForm(self, compra_id=self.compra_id, on_done=self.load_data)

    def on_edit(self):
        messagebox.showinfo("Info", "Editar detalles no implementado (evita inconsistencias).", parent=self)

    def on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un detalle.", parent=self)
            return
        vals = self.tree.item(sel[0])["values"]
        dk = vals[0]
        if not messagebox.askyesno("Confirmar", "¿Eliminar detalle y ajustar stock?", parent=self):
            return
        with Session(engine) as session:
            d = session.get(DetalleCompra, dk)
            if d:
                prod = session.get(Producto, d.id_producto)
                if prod:
                    prod.stock_actual = max(0, prod.stock_actual - d.cantidad)  # revert the increase
                    session.add(prod)
                session.delete(d)
                # update compra total
                compra = session.get(Compra, d.id_compra)
                if compra:
                    detalles = session.exec(select(DetalleCompra).where(DetalleCompra.id_compra==compra.id_compra)).all()
                    compra.total_compra = sum(x.subtotal for x in detalles)
                    session.add(compra)
                session.commit()
        self.load_data()

class DetalleCompraForm(tk.Toplevel):
    def __init__(self, master, compra_id: Optional[int]=None, on_done=None):
        super().__init__(master)
        self.compra_id = compra_id
        self.on_done = on_done
        self.title("Agregar DetalleCompra")
        self.geometry("520x260")
        self.build()

    def build(self):
        frm = ttk.Frame(self, padding=8)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Compra ID:").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_compra = ttk.Entry(frm)
        self.ent_compra.grid(row=0, column=1, pady=4)
        if self.compra_id:
            self.ent_compra.insert(0, str(self.compra_id))
            self.ent_compra.config(state="disabled")

        ttk.Label(frm, text="Producto:").grid(row=1, column=0, sticky="w", pady=4)
        with Session(engine) as s:
            items, mapping = map_products(s)
        self.prod_items, self.prod_mapping = items, mapping
        self.cmb_prod = ttk.Combobox(frm, values=items, state="readonly", width=50)
        self.cmb_prod.grid(row=1, column=1, pady=4)

        ttk.Label(frm, text="Cantidad:").grid(row=2, column=0, sticky="w", pady=4)
        self.ent_cant = ttk.Entry(frm)
        self.ent_cant.grid(row=2, column=1, pady=4)
        ttk.Label(frm, text="Costo unitario:").grid(row=3, column=0, sticky="w", pady=4)
        self.ent_costo = ttk.Entry(frm)
        self.ent_costo.grid(row=3, column=1, pady=4)

        btn_save = ttk.Button(frm, text="Agregar", command=self.save)
        btn_cancel = ttk.Button(frm, text="Cancelar", command=self.destroy)
        btn_save.grid(row=4, column=0, pady=8)
        btn_cancel.grid(row=4, column=1, pady=8)

    def save(self):
        compra_in = self.ent_compra.get().strip()
        if not compra_in:
            messagebox.showwarning("Validación", "Ingrese ID Compra (o cree la cabecera primero).", parent=self)
            return
        try:
            compra_id = int(compra_in)
        except:
            messagebox.showwarning("Validación", "ID Compra inválido.", parent=self)
            return
        prod_display = self.cmb_prod.get()
        if not prod_display:
            messagebox.showwarning("Validación", "Seleccione producto.", parent=self)
            return
        pid = self.prod_mapping.get(prod_display)
        try:
            cantidad = int(self.ent_cant.get().strip())
            costo = float(self.ent_costo.get().strip())
        except Exception:
            messagebox.showwarning("Validación", "Cantidad o costo inválido.", parent=self)
            return
        subtotal = cantidad * costo
        with Session(engine) as session:
            prod = session.get(Producto, pid)
            if not prod:
                messagebox.showerror("Error", "Producto no encontrado.", parent=self)
                return
            # increase stock by purchase cantidad
            prod.stock_actual = prod.stock_actual + cantidad
            detalle = DetalleCompra(id_compra=compra_id, id_producto=pid, cantidad=cantidad, costo_unitario=costo, subtotal=subtotal)
            session.add(prod)
            session.add(detalle)
            session.commit()
            session.refresh(detalle)
            # update compra total
            compra = session.get(Compra, compra_id)
            if compra:
                detalles = session.exec(select(DetalleCompra).where(DetalleCompra.id_compra==compra.id_compra)).all()
                compra.total_compra = sum(d.subtotal for d in detalles)
                session.add(compra)
                session.commit()
        messagebox.showinfo("OK", "Detalle agregado y stock actualizado.", parent=self)
        if self.on_done:
            self.on_done()
        self.destroy()