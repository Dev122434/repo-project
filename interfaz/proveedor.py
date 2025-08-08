from interfaz.formulario import BaseListWindow
from models.entities import Proveedor
from sqlmodel import Session, select
from database.conexion import engine
from tkinter import ttk, messagebox
import tkinter as tk
from typing import Optional


class ProveedorWindow(BaseListWindow):
    def __init__(self, master):
        cols = [
            ("id_proveedor", "ID"),
            ("nombre_proveedor", "Nombre Proveedor"),
            ("telefono", "Teléfono"),
            ("email_proveedor", "Email"),
            ("fecha_alta", "Fecha Alta"),
        ]
        super().__init__(master, "Proveedores", cols)
        self.load_data()

    def load_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        with Session(engine) as session:
            rows = session.exec(select(Proveedor)).all()
            for p in rows:
                self.tree.insert("", "end", values=(p.id_proveedor, p.nombre_proveedor, p.telefono, p.email_proveedor, str(p.fecha_alta)))

    def on_add(self):
        ProveedorForm(self, mode="add", on_done=self.load_data)

    def on_edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un proveedor.", parent=self)
            return
        vals = self.tree.item(sel[0])["values"]
        ProveedorForm(self, mode="edit", proveedor_id=vals[0], on_done=self.load_data)

    def on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un proveedor.", parent=self)
            return
        vals = self.tree.item(sel[0])["values"]
        pk = vals[0]
        if not messagebox.askyesno("Confirmar", "¿Eliminar proveedor?", parent=self):
            return
        with Session(engine) as session:
            obj = session.get(Proveedor, pk)
            if obj:
                session.delete(obj)
                session.commit()
        self.load_data()

class ProveedorForm(tk.Toplevel):
    def __init__(self, master, mode="add", proveedor_id: Optional[int]=None, on_done=None):
        super().__init__(master)
        self.mode = mode
        self.proveedor_id = proveedor_id
        self.on_done = on_done
        self.title("Proveedor - " + ("Nuevo" if mode=="add" else "Editar"))
        self.geometry("420x260")
        self.build()
        if mode == "edit":
            self.load_proveedor()

    def build(self):
        frm = ttk.Frame(self, padding=8)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Nombre Proveedor:").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_nombre = ttk.Entry(frm, width=40)
        self.ent_nombre.grid(row=0, column=1, pady=4)
        ttk.Label(frm, text="Teléfono:").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_tel = ttk.Entry(frm)
        self.ent_tel.grid(row=1, column=1, pady=4)
        ttk.Label(frm, text="Email:").grid(row=2, column=0, sticky="w", pady=4)
        self.ent_email = ttk.Entry(frm)
        self.ent_email.grid(row=2, column=1, pady=4)

        btn_save = ttk.Button(frm, text="Guardar", command=self.save)
        btn_cancel = ttk.Button(frm, text="Cancelar", command=self.destroy)
        btn_save.grid(row=3, column=0, pady=12)
        btn_cancel.grid(row=3, column=1, pady=12)

    def load_proveedor(self):
        with Session(engine) as session:
            p = session.get(Proveedor, self.proveedor_id)
            if p:
                self.ent_nombre.insert(0, p.nombre_proveedor)
                self.ent_tel.insert(0, p.telefono)
                self.ent_email.insert(0, p.email_proveedor)

    def save(self):
        nombre = self.ent_nombre.get().strip()
        tel = self.ent_tel.get().strip()
        email = self.ent_email.get().strip()
        if not (nombre and tel and email):
            messagebox.showwarning("Validación", "Complete todos los campos.", parent=self)
            return
        with Session(engine) as session:
            try:
                if self.mode == "add":
                    p = Proveedor(nombre_proveedor=nombre, telefono=tel, email_proveedor=email)
                    session.add(p)
                else:
                    p = session.get(Proveedor, self.proveedor_id)
                    if not p:
                        messagebox.showerror("Error", "Proveedor no encontrado.", parent=self)
                        return
                    p.nombre_proveedor = nombre
                    p.telefono = tel
                    p.email_proveedor = email
                    session.add(p)
                session.commit()
                if self.on_done:
                    self.on_done()
                self.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)