from importaciones import *
from main import map_products
from interfaz.formulario import BaseListWindow
from models.entities import DetalleVenta, Producto, Venta
from database.conexion import engine
from typing import Optional

class DetalleVentaWindow(BaseListWindow):
    def __init__(self, master, venta_id: Optional[int]=None):
        self.venta_id = venta_id
        cols = [
            ("id_detalle_venta", "ID"),
            ("id_venta", "ID Venta"),
            ("id_producto", "ID Producto"),
            ("cantidad", "Cantidad"),
            ("precio_unitario", "Precio Unitario"),
            ("subtotal", "Subtotal"),
        ]
        title = f"DetalleVenta - Venta {venta_id}" if venta_id else "DetalleVenta (general)"
        super().__init__(master, title, cols)
        self.load_data()

    def load_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        with Session(engine) as session:
            q = select(DetalleVenta)
            if self.venta_id:
                q = q.where(DetalleVenta.id_venta == self.venta_id)
            rows = session.exec(q).all()
            for d in rows:
                self.tree.insert("", "end", values=(d.id_detalle_venta, d.id_venta, d.id_producto, d.cantidad, d.precio_unitario, d.subtotal))

    def on_add(self):
        DetalleVentaForm(self, venta_id=self.venta_id, on_done=self.load_data)

    def on_edit(self):
        messagebox.showinfo("Info", "Editar detalle no implementado para evitar inconsistencias.", parent=self)

    def on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un detalle.", parent=self)
            return
        vals = self.tree.item(sel[0])["values"]
        dk = vals[0]
        if not messagebox.askyesno("Confirmar", "¿Eliminar detalle y revertir stock?", parent=self):
            return
        with Session(engine) as session:
            d = session.get(DetalleVenta, dk)
            if d:
                prod = session.get(Producto, d.id_producto)
                if prod:
                    prod.stock_actual += d.cantidad
                    session.add(prod)
                session.delete(d)
                venta = session.get(Venta, d.id_venta)
                if venta:
                    detalles = session.exec(select(DetalleVenta).where(DetalleVenta.id_venta==venta.id_venta)).all()
                    venta.total_venta = sum(x.subtotal for x in detalles)
                    session.add(venta)
                session.commit()
        self.load_data()

class DetalleVentaForm(tk.Toplevel):
    def __init__(self, master, venta_id: Optional[int]=None, on_done=None):
        super().__init__(master)
        self.venta_id = venta_id
        self.on_done = on_done
        self.title("Agregar DetalleVenta")
        self.geometry("520x260")
        self.build()

    def build(self):
        frm = ttk.Frame(self, padding=8)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Venta ID:").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_venta = ttk.Entry(frm)
        self.ent_venta.grid(row=0, column=1, pady=4)
        if self.venta_id:
            self.ent_venta.insert(0, str(self.venta_id))
            self.ent_venta.config(state="disabled")

        ttk.Label(frm, text="Producto:").grid(row=1, column=0, sticky="w", pady=4)
        with Session(engine) as s:
            items, mapping = map_products(s)
        self.prod_items, self.prod_mapping = items, mapping
        self.cmb_prod = ttk.Combobox(frm, values=items, state="readonly", width=50)
        self.cmb_prod.grid(row=1, column=1, pady=4)

        ttk.Label(frm, text="Cantidad:").grid(row=2, column=0, sticky="w", pady=4)
        self.ent_cant = ttk.Entry(frm)
        self.ent_cant.grid(row=2, column=1, pady=4)
        ttk.Label(frm, text="Precio unitario (si vacío usa precio producto):").grid(row=3, column=0, sticky="w", pady=4)
        self.ent_precio = ttk.Entry(frm)
        self.ent_precio.grid(row=3, column=1, pady=4)

        btn_save = ttk.Button(frm, text="Agregar", command=self.save)
        btn_cancel = ttk.Button(frm, text="Cancelar", command=self.destroy)
        btn_save.grid(row=4, column=0, pady=8)
        btn_cancel.grid(row=4, column=1, pady=8)

    def save(self):
        venta_in = self.ent_venta.get().strip()
        if not venta_in:
            messagebox.showwarning("Validación", "Ingrese ID Venta (o cree la cabecera primero).", parent=self)
            return
        try:
            venta_id = int(venta_in)
        except:
            messagebox.showwarning("Validación", "ID Venta inválido.", parent=self)
            return
        prod_display = self.cmb_prod.get()
        if not prod_display:
            messagebox.showwarning("Validación", "Seleccione producto.", parent=self)
            return
        pid = self.prod_mapping.get(prod_display)
        try:
            cantidad = int(self.ent_cant.get().strip())
            precio_in = self.ent_precio.get().strip()
            if precio_in:
                precio = float(precio_in)
            else:
                with Session(engine) as s:
                    prod = s.get(Producto, pid)
                    precio = prod.precio if prod else 0.0
        except Exception:
            messagebox.showwarning("Validación", "Cantidad o precio inválido.", parent=self)
            return
        if cantidad <= 0:
            messagebox.showwarning("Validación", "Cantidad debe ser > 0", parent=self)
            return
        with Session(engine) as session:
            prod = session.get(Producto, pid)
            if not prod:
                messagebox.showerror("Error", "Producto no encontrado.", parent=self)
                return
            if prod.stock_actual < cantidad:
                messagebox.showerror("Error", "Stock insuficiente.", parent=self)
                return
            subtotal = cantidad * precio
            prod.stock_actual = prod.stock_actual - cantidad
            detalle = DetalleVenta(id_venta=venta_id, id_producto=pid, cantidad=cantidad, precio_unitario=precio, subtotal=subtotal)
            session.add(prod)
            session.add(detalle)
            session.commit()
            venta = session.get(Venta, venta_id)
            if venta:
                detalles = session.exec(select(DetalleVenta).where(DetalleVenta.id_venta==venta.id_venta)).all()
                venta.total_venta = sum(d.subtotal for d in detalles)
                session.add(venta)
                session.commit()
        messagebox.showinfo("OK", "DetalleVenta agregado y stock actualizado.", parent=self)
        if self.on_done:
            self.on_done()
        self.destroy()