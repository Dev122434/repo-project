from tkinter import *
  
from tkinter import messagebox
root = Tk()
root.title("Menu")

root.geometry("1100x800")
root.resizable(0,0)

miFrame1 = Frame(root, width=650, height=400)

def SalirAplicacion():
    valor = messagebox.askquestion("Salir", "Deseas Salir?")
    if valor == "yes":
        root.destroy()


def Registrar():
	pass
def Consultar():
	pass 
def Actualizar():
	pass
def Eliminar():
	pass
#-------------------
barraMenu=Menu(root)
root.config(menu=barraMenu)

bbddMenu=Menu(barraMenu, tearoff=0)
LimpiarMenu=Menu(barraMenu, tearoff=0)
crudMenu=Menu(barraMenu, tearoff=0)
ayudaMenu=Menu(barraMenu, tearoff=0)

bbddMenu.add_command(label="Salir", command=SalirAplicacion)

crudMenu.add_command(label="Registro", command=Registrar)
crudMenu.add_command(label="Consulta", command=Consultar)
crudMenu.add_command(label="Actualizar", command=Actualizar)
crudMenu.add_command(label="Eliminar", command=Eliminar)

barraMenu.add_cascade(label="BBDD", menu=bbddMenu)
barraMenu.add_cascade(label="Limpiar", menu=LimpiarMenu)
barraMenu.add_cascade(label="CRUD", menu=crudMenu)
barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)

root.mainloop()

