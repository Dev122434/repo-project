from models.entities import Cliente
from typing import Optional
from interfaz.formulario import BaseListWindow
from tkinter import ttk, messagebox
import tkinter as tk
from sqlmodel import Session, select
from database.conexion import engine
class ClienteWindow(BaseListWindow):
    def __init__(self, master):
        cols = [
            ("id_cliente", "ID"),
            ("nombre", "Nombre"),
            ("apellidos", "Apellidos"),
            ("email", "Email"),
            ("fecha_registro", "Fecha Registro"),
        ]
        super().__init__(master, "Clientes", cols)
        self.load_data()

    def load_data(self):
        for r in self.tree.get_children():
            self.tree.delete(r)
        with Session(engine) as session:
            rows = session.exec(select(Cliente)).all()
            for c in rows:
                self.tree.insert("", "end", values=(c.id_cliente, c.nombre, c.apellidos, c.email, str(c.fecha_registro)))

    def on_add(self):
        ClienteForm(self, mode="add", on_done=self.load_data)

    def on_edit(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un cliente.", parent=self)
            return
        vals = self.tree.item(sel[0])["values"]
        ClienteForm(self, mode="edit", cliente_id=vals[0], on_done=self.load_data)

    def on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un cliente.", parent=self)
            return
        vals = self.tree.item(sel[0])["values"]
        pk = vals[0]
        if not messagebox.askyesno("Confirmar", "¿Eliminar cliente?", parent=self):
            return
        with Session(engine) as session:
            obj = session.get(Cliente, pk)
            if obj:
                session.delete(obj)
                session.commit()
        self.load_data()

class ClienteForm(tk.Toplevel):
    def __init__(self, master, mode="add", cliente_id: Optional[int]=None, on_done=None):
        super().__init__(master)
        self.mode = mode
        self.cliente_id = cliente_id
        self.on_done = on_done
        self.title("Cliente - " + ("Nuevo" if mode=="add" else "Editar"))
        self.geometry("380x260")
        self.build()
        if mode == "edit":
            self.load_cliente()

    def build(self):
        frm = ttk.Frame(self, padding=8)
        frm.pack(fill="both", expand=True)
        ttk.Label(frm, text="Nombre:").grid(row=0, column=0, sticky="w", pady=4)
        self.ent_nombre = ttk.Entry(frm)
        self.ent_nombre.grid(row=0, column=1, pady=4)
        ttk.Label(frm, text="Apellidos:").grid(row=1, column=0, sticky="w", pady=4)
        self.ent_ap = ttk.Entry(frm)
        self.ent_ap.grid(row=1, column=1, pady=4)
        ttk.Label(frm, text="Email:").grid(row=2, column=0, sticky="w", pady=4)
        self.ent_email = ttk.Entry(frm)
        self.ent_email.grid(row=2, column=1, pady=4)

        btn_save = ttk.Button(frm, text="Guardar", command=self.save)
        btn_cancel = ttk.Button(frm, text="Cancelar", command=self.destroy)
        btn_save.grid(row=3, column=0, pady=12)
        btn_cancel.grid(row=3, column=1, pady=12)

    def load_cliente(self):
        with Session(engine) as session:
            c = session.get(Cliente, self.cliente_id)
            if c:
                self.ent_nombre.insert(0, c.nombre)
                self.ent_ap.insert(0, c.apellidos)
                self.ent_email.insert(0, c.email)

    def save(self):
        nombre = self.ent_nombre.get().strip()
        ap = self.ent_ap.get().strip()
        email = self.ent_email.get().strip()
        if not (nombre and ap and email):
            messagebox.showwarning("Validación", "Complete todos los campos.", parent=self)
            return
        with Session(engine) as session:
            try:
                if self.mode == "add":
                    c = Cliente(nombre=nombre, apellidos=ap, email=email)
                    session.add(c)
                else:
                    c = session.get(Cliente, self.cliente_id)
                    if not c:
                        messagebox.showerror("Error", "Cliente no encontrado.", parent=self)
                        return
                    c.nombre = nombre
                    c.apellidos = ap
                    c.email = email
                    session.add(c)
                session.commit()
                if self.on_done:
                    self.on_done()
                self.destroy()
            except Exception as e:
                messagebox.showerror("Error", str(e), parent=self)