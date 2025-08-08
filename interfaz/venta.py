from main import map_clientes
from models.entities import Venta, DetalleVenta, Producto
from interfaz.formulario import BaseListWindow
from interfaz.detalle_venta import DetalleVenta, DetalleVentaWindow
from typing import Optional
from tkinter import messagebox, ttk
from datetime import date
from sqlmodel import Session, select
from database.conexion import engine
import tkinter as tk

class VentaWindow(BaseListWindow):
    def __init__(self, master):
        cols = [
            ("id_venta", "ID"),
            ("fecha_venta", "Fecha"),
            ("id_cliente", "ID Cliente"),
            ("total_venta", "Total"),
        ]
        super().__init__(master, "Ventas (cabecera)", cols)
        self.load_data()

    def load_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        with Session(engine) as session:
            rows = session.exec(select(Venta)).all()
            for v in rows:
                self.tree.insert("", "end", values=(v.id_venta, str(v.fecha_venta), v.id_cliente, v.total_venta))

    def on_add(self):
        VentaForm(self, mode="add", on_done=self.load_data)

    def on_edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una venta.", parent=self)
            return
        vals = self.tree.item(sel[0])["values"]
        VentaForm(self, mode="edit", venta_id=vals[0], on_done=self.load_data)

    def on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione una venta.", parent=self)
            return
        vals = self.tree.item(sel[0])["values"]
        pk = vals[0]
        if not messagebox.askyesno("Confirmar", "¿Eliminar venta y sus detalles? Esto revertirá stock.", parent=self):
            return
        with Session(engine) as session:
            detalles = session.exec(select(DetalleVenta).where(DetalleVenta.id_venta==pk)).all()
            for d in detalles:
                prod = session.get(Producto, d.id_producto)
                if prod:
                    prod.stock_actual += d.cantidad  # revert sale
                    session.add(prod)
                session.delete(d)
            v = session.get(Venta, pk)
            if v:
                session.delete(v)
            session.commit()
        self.load_data()

class VentaForm(tk.Toplevel):
    def __init__(self, master, mode="add", venta_id: Optional[int]=None, on_done=None):
        super().__init__(master)
        self.mode = mode
        self.venta_id = venta_id
        self.on_done = on_done
        self.title("Venta - " + ("Nueva" if mode=="add" else "Editar"))
        self.geometry("480x200")
        self.build()
        if mode == "edit":
            self.load_venta()

    def build(self):
        frm = ttk.Frame(self, padding=8)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Cliente:").grid(row=0, column=0, sticky="w", pady=4)
        with Session(engine) as s:
            items, _ = map_clientes(s)
        self.cmb_cli = ttk.Combobox(frm, values=items, state="readonly", width=40)
        self.cmb_cli.grid(row=0, column=1, pady=4)
        ttk.Label(frm, text="Fecha (YYYY-MM-DD o vacío = hoy):").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_fecha = ttk.Entry(frm)
        self.ent_fecha.grid(row=1, column=1, pady=4)
        btn_detalle = ttk.Button(frm, text="Abrir Detalles de Venta", command=self.open_detalles)
        btn_detalle.grid(row=2, column=0, columnspan=2, pady=8)
        btn_save = ttk.Button(frm, text="Guardar", command=self.save)
        btn_cancel = ttk.Button(frm, text="Cancelar", command=self.destroy)
        btn_save.grid(row=3, column=0, pady=6)
        btn_cancel.grid(row=3, column=1, pady=6)

    def load_venta(self):
        with Session(engine) as session:
            v = session.get(Venta, self.venta_id)
            if v:
                clientes, mapping = map_clientes(session)
                sel = None
                for k,val in mapping.items():
                    if val == v.id_cliente:
                        sel = k
                        break
                if sel:
                    self.cmb_cli.set(sel)
                self.ent_fecha.insert(0, str(v.fecha_venta))

    def open_detalles(self):
        if self.mode == "add":
            if not messagebox.askyesno("Atención", "La venta será creada ahora para poder agregar detalles. Continuar?", parent=self):
                return
            cli_display = self.cmb_cli.get()
            if not cli_display:
                messagebox.showwarning("Validación", "Seleccione cliente.", parent=self)
                return
            with Session(engine) as session:
                _, mapping = map_clientes(session)
                cid = mapping.get(cli_display)
                if not cid:
                    messagebox.showerror("Error", "Cliente inválido.", parent=self)
                    return
                fecha_in = self.ent_fecha.get().strip()
                try:
                    fecha_val = date.fromisoformat(fecha_in) if fecha_in else date.today()
                except Exception:
                    messagebox.showwarning("Validación", "Fecha inválida.", parent=self)
                    return
                venta = Venta(fecha_venta=fecha_val, id_cliente=cid, total_venta=0.0)
                session.add(venta)
                session.commit()
                session.refresh(venta)
                self.venta_id = venta.id_venta
                messagebox.showinfo("OK", f"Venta creada con ID {self.venta_id}. Ahora abra DetalleVenta.", parent=self)
        DetalleVentaWindow(self, venta_id=self.venta_id)

    def save(self):
        cli_display = self.cmb_cli.get()
        if not cli_display:
            messagebox.showwarning("Validación", "Seleccione cliente.", parent=self)
            return
        fecha_in = self.ent_fecha.get().strip()
        try:
            fecha_val = date.fromisoformat(fecha_in) if fecha_in else date.today()
        except Exception:
            messagebox.showwarning("Validación", "Fecha inválida.", parent=self)
            return
        with Session(engine) as session:
            _, mapping = map_clientes(session)
            cid = mapping.get(cli_display)
            if not cid:
                messagebox.showerror("Error", "Cliente inválido.", parent=self)
                return
            try:
                if self.mode == "add":
                    venta = Venta(fecha_venta=fecha_val, id_cliente=cid, total_venta=0.0)
                    session.add(venta)
                else:
                    venta = session.get(Venta, self.venta_id)
                    venta.fecha_venta = fecha_val
                    venta.id_cliente = cid
                    detalles = session.exec(select(DetalleVenta).where(DetalleVenta.id_venta==venta.id_venta)).all()
                    venta.total_venta = sum(d.subtotal for d in detalles)
                    session.add(venta)
                session.commit()
                if self.on_done:
                    self.on_done()
                self.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)