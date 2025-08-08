import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
class BaseListWindow(tk.Toplevel):
    def __init__(self, master, title: str, columns: list[tuple[str,str]]):
        super().__init__(master)
        self.title(title)
        self.geometry("800x420")
        self.columns = columns  # list of (attr_name, column label)
        self.setup_ui()

    def setup_ui(self):
        frm_top = ttk.Frame(self)
        frm_top.pack(fill="x", padx=6, pady=6)

        btn_add = ttk.Button(frm_top, text="Agregar", command=self.on_add)
        btn_edit = ttk.Button(frm_top, text="Editar", command=self.on_edit)
        btn_delete = ttk.Button(frm_top, text="Eliminar", command=self.on_delete)
        btn_refresh = ttk.Button(frm_top, text="Refrescar", command=self.load_data)
        btn_add.pack(side="left", padx=4)
        btn_edit.pack(side="left", padx=4)
        btn_delete.pack(side="left", padx=4)
        btn_refresh.pack(side="left", padx=4)

        self.tree = ttk.Treeview(self, columns=[c[0] for c in self.columns], show="headings")
        for attr, label in self.columns:
            self.tree.heading(attr, text=label)
            self.tree.column(attr, width=130, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=6, pady=6)

    def load_data(self):
        raise NotImplementedError

    def on_add(self):
        raise NotImplementedError

    def on_edit(self):
        raise NotImplementedError

    def on_delete(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atención", "Seleccione un registro.", parent=self)
            return
        item = self.tree.item(sel[0])["values"]
        pk = item[0]
        if not messagebox.askyesno("Confirmar", "¿Eliminar registro?", parent=self):
            return
        raise NotImplementedError