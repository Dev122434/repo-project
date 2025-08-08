from interfaz.formulario import BaseListWindow
from main import Session, select, tk, ttk, messagebox, map_proveedores
from models.entities import Compra, DetalleCompra
from interfaz.detalle_compra import DetalleCompraWindow
from database.conexion import engine
from typing import Optional
from datetime import date

class CompraWindow(BaseListWindow):
    def __init__(self, master):
        cols = [
            ("id_compra", "ID"),
            ("fecha_compra", "Fecha"),
            ("id_proveedor", "ID Proveedor"),
            ("total_compra", "Total"),
        ]
        super().__init__(master, "Compras (cabecera)", cols)
        self.load_data()

    def load_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        with Session(engine) as session:
            rows = session.exec(select(Compra)).all()
            for c in rows:
                self.tree.insert("", "end", values=(c.id_compra, str(c.fecha_compra), c.id_proveedor, c.total_compra))

    def on_add(self):
        CompraForm(self, mode="add", on_done=self.load_data)

    def on_edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una compra.", parent=self)
            return
        vals = self.tree.item(sel[0])["values"]
        CompraForm(self, mode="edit", compra_id=vals[0], on_done=self.load_data)

    def on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una compra.", parent=self)
            return
        vals = self.tree.item(sel[0])["values"]
        pk = vals[0]
        if not messagebox.askyesno("Confirmar", "¿Eliminar compra? Esto eliminará detalles también.", parent=self):
            return
        with Session(engine) as session:
            detalles = session.exec(select(DetalleCompra).where(DetalleCompra.id_compra==pk)).all()
            for d in detalles:
                session.delete(d)
            c = session.get(Compra, pk)
            if c:
                session.delete(c)
            session.commit()
        self.load_data()

class CompraForm(tk.Toplevel):
    def __init__(self, master, mode="add", compra_id: Optional[int]=None, on_done=None):
        super().__init__(master)
        self.mode = mode
        self.compra_id = compra_id
        self.on_done = on_done
        self.title("Compra - " + ("Nueva" if mode=="add" else "Editar"))
        self.geometry("480x200")
        self.build()
        if mode == "edit":
            self.load_compra()

    def build(self):
        frm = ttk.Frame(self, padding=8)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Proveedor:").grid(row=0, column=0, sticky="w", pady=4)
        with Session(engine) as s:
            items, _ = map_proveedores(s)
        self.cmb_prov = ttk.Combobox(frm, values=items, state="readonly", width=40)
        self.cmb_prov.grid(row=0, column=1, pady=4)
        ttk.Label(frm, text="Fecha (YYYY-MM-DD o vacío = hoy):").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_fecha = ttk.Entry(frm)
        self.ent_fecha.grid(row=1, column=1, pady=4)
        btn_detalle = ttk.Button(frm, text="Abrir Detalles de Compra", command=self.open_detalles)
        btn_detalle.grid(row=2, column=0, columnspan=2, pady=8)
        btn_save = ttk.Button(frm, text="Guardar", command=self.save)
        btn_cancel = ttk.Button(frm, text="Cancelar", command=self.destroy)
        btn_save.grid(row=3, column=0, pady=6)
        btn_cancel.grid(row=3, column=1, pady=6)

    def load_compra(self):
        with Session(engine) as session:
            c = session.get(Compra, self.compra_id)
            if c:
                provs, mapping = map_proveedores(session)
                selected = None
                for k,v in mapping.items():
                    if v == c.id_proveedor:
                        selected = k
                        break
                if selected:
                    self.cmb_prov.set(selected)
                self.ent_fecha.insert(0, str(c.fecha_compra))

    def open_detalles(self):
        if self.mode == "add":
            if not messagebox.askyesno("Atención", "La compra será creada ahora para poder agregar detalles. Continuar?", parent=self):
                return
            prov_display = self.cmb_prov.get()
            if not prov_display:
                messagebox.showwarning("Validación", "Seleccione proveedor.", parent=self)
                return
            with Session(engine) as session:
                _, mapping = map_proveedores(session)
                pid = mapping.get(prov_display)
                if not pid:
                    messagebox.showerror("Error", "Proveedor inválido.", parent=self)
                    return
                fecha_in = self.ent_fecha.get().strip()
                try:
                    if fecha_in:
                        fecha_val = date.fromisoformat(fecha_in)
                    else:
                        fecha_val = date.today()
                except Exception:
                    messagebox.showwarning("Validación", "Fecha inválida.", parent=self)
                    return
                comp = Compra(fecha_compra=fecha_val, id_proveedor=pid, total_compra=0.0)
                session.add(comp)
                session.commit()
                session.refresh(comp)
                self.compra_id = comp.id_compra
                messagebox.showinfo("OK", f"Compra creada con ID {self.compra_id}. Ahora abra DetalleCompra.", parent=self)
        DetalleCompraWindow(self, compra_id=self.compra_id)

    def save(self):
        prov_display = self.cmb_prov.get()
        if not prov_display:
            messagebox.showwarning("Validación", "Seleccione proveedor.", parent=self)
            return
        fecha_in = self.ent_fecha.get().strip()
        try:
            fecha_val = date.fromisoformat(fecha_in) if fecha_in else date.today()
        except Exception:
            messagebox.showwarning("Validación", "Fecha inválida.", parent=self)
            return
        with Session(engine) as session:
            _, mapping = map_proveedores(session)
            pid = mapping.get(prov_display)
            if not pid:
                messagebox.showerror("Error", "Proveedor inválido.", parent=self)
                return
            try:
                if self.mode == "add":
                    comp = Compra(fecha_compra=fecha_val, id_proveedor=pid, total_compra=0.0)
                    session.add(comp)
                else:
                    comp = session.get(Compra, self.compra_id)
                    comp.fecha_compra = fecha_val
                    comp.id_proveedor = pid
                    # recompute total from detalles
                    detalles = session.exec(select(DetalleCompra).where(DetalleCompra.id_compra==comp.id_compra)).all()
                    comp.total_compra = sum(d.subtotal for d in detalles)
                    session.add(comp)
                session.commit()
                if self.on_done:
                    self.on_done()
                self.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)