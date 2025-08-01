from tkinter import *
from tkinter import ttk
from sqlmodel import Session, select
from main import Cliente, Proveedor, Producto, Compra, DetalleCompra, Venta, DetalleVenta, engine
from typing import Annotated

global tabla

def mostrar_clientes():
    for renglon in tabla.get_children():
        tabla.delete(renglon)

    with Session(engine) as session:
        statement = select(Cliente)
        clientes = session.exec(statement).all()

        for cliente in clientes:
            tabla.insert('', END, values=(
                cliente.id_cliente,
                cliente.nombre,
                cliente.apellidos,
                cliente.email,
                cliente.fecha_registro.strftime("%Y-%m-%d")
            ))

# Función para mostrar proveedores
def mostrar_proveedores():
    for renglon in tabla.get_children():
        tabla.delete(renglon)

    with Session(engine) as session:
        statement = select(Proveedor)
        proveedores = session.exec(statement).all()

        for proveedor in proveedores:
            tabla.insert('', END, values=(
                proveedor.id_proveedor,
                proveedor.nombre_proveedor,
                proveedor.telefono,
                proveedor.email_proveedor,
                proveedor.fecha_alta.strftime("%Y-%m-%d")
            ))

# Función para mostrar productos
def mostrar_productos():
    for renglon in tabla.get_children():
        tabla.delete(renglon)

    with Session(engine) as session:
        statement = select(Producto)
        productos = session.exec(statement).all()

        for producto in productos:
            tabla.insert('', END, values=(
                producto.id_producto,
                producto.modelo,
                producto.talla,
                producto.color,
                producto.precio,
                producto.stock_actual
            ))

# Función para mostrar compras
def mostrar_compras():
    for renglon in tabla.get_children():
        tabla.delete(renglon)

    with Session(engine) as session:
        statement = select(Compra)
        compras = session.exec(statement).all()

        for compra in compras:
            tabla.insert('', END, values=(
                compra.id_compra,
                compra.fecha_compra.strftime("%Y-%m-%d"),
                compra.id_proveedor,
                compra.total_compra
            ))

# Función para mostrar detalles de compras
def mostrar_detalle_compras():
    for renglon in tabla.get_children():
        tabla.delete(renglon)

    with Session(engine) as session:
        statement = select(DetalleCompra)
        detalles = session.exec(statement).all()

        for detalle in detalles:
            tabla.insert('', END, values=(
                detalle.id_detalle_compra,
                detalle.id_compra,
                detalle.id_producto,
                detalle.cantidad,
                detalle.costo_unitario,
                detalle.subtotal
            ))

# Función para mostrar ventas
def mostrar_ventas():
    for renglon in tabla.get_children():
        tabla.delete(renglon)

    with Session(engine) as session:
        statement = select(Venta)
        ventas = session.exec(statement).all()

        for venta in ventas:
            tabla.insert('', END, values=(
                venta.id_venta,
                venta.fecha_venta.strftime("%Y-%m-%d"),
                venta.id_cliente,
                venta.total_venta
            ))

# Función para mostrar detalles de ventas
def mostrar_detalle_ventas():
    for renglon in tabla.get_children():
        tabla.delete(renglon)

    with Session(engine) as session:
        statement = select(DetalleVenta)
        detalles = session.exec(statement).all()

        for detalle in detalles:
            tabla.insert('', END, values=(
                detalle.id_detalle_venta,
                detalle.id_venta,
                detalle.id_producto,
                detalle.cantidad,
                detalle.precio_unitario,
                detalle.subtotal
            ))

# Función genérica para abrir subventanas de cada modelo
def mostrar_modelo(modelo, titulo, columnas, mostrar_func):
    vtn_modelo = Toplevel()
    vtn_modelo.title(titulo)
    vtn_modelo.geometry('900x500')

    ibl_titulo = Label(vtn_modelo, text=titulo, font=('Comic Sans MS', 18))
    ibl_titulo.grid(row=0, column=0, padx=10, pady=10, columnspan=10)

    btn_cerrar = Button(vtn_modelo, text='Cerrar', command=vtn_modelo.destroy)
    btn_cerrar.grid(row=6, column=4, sticky='e', padx=10, pady=10)

    tabla = ttk.Treeview(vtn_modelo, columns=columnas, show='headings')
    for col in columnas:
        tabla.heading(col, text=col)
        tabla.column(col, anchor='center')
    tabla.grid(row=8, column=0, padx=5, pady=5, columnspan=10)

    mostrar_func()  # Llamamos a la función de mostrar los datos para ese modelo

# Ventana principal
raiz = Tk()
raiz.title('Sistema de Gestión')
raiz.config(bg='gray')
raiz.geometry('1000x800')

mi_frame = Frame(raiz, bg='red', width=650, height=500, pady=20, padx=20)
mi_frame.pack()

# Botones para abrir cada subventana de modelo
btn_clientes = Button(mi_frame, text='Mostrar Clientes', width=50, height=5, 
                      command=lambda: mostrar_modelo(Cliente, 'Clientes', ('ID', 'Nombre', 'Apellidos', 'Email', 'Fecha de Registro'), mostrar_clientes))
btn_clientes.grid(row=1, column=0, sticky='e', padx=5, pady=5)

btn_proveedores = Button(mi_frame, text='Mostrar Proveedores', width=50, height=5, 
                         command=lambda: mostrar_modelo(Proveedor, 'Proveedores', ('ID', 'Nombre', 'Teléfono', 'Email', 'Fecha de Alta'), mostrar_proveedores))
btn_proveedores.grid(row=2, column=0, sticky='e', padx=5, pady=5)

btn_productos = Button(mi_frame, text='Mostrar Productos', width=50, height=5, 
                       command=lambda: mostrar_modelo(Producto, 'Productos', ('ID', 'Modelo', 'Talla', 'Color', 'Precio', 'Stock'), mostrar_productos))
btn_productos.grid(row=3, column=0, sticky='e', padx=5, pady=5)

btn_compras = Button(mi_frame, text='Mostrar Compras', width=50, height=5, 
                     command=lambda: mostrar_modelo(Compra, 'Compras', ('ID', 'Fecha', 'Proveedor', 'Total Compra'), mostrar_compras))
btn_compras.grid(row=4, column=0, sticky='e', padx=5, pady=5)

btn_detalle_compras = Button(mi_frame, text='Mostrar Detalle Compras', width=50, height=5, 
                             command=lambda: mostrar_modelo(DetalleCompra, 'Detalle Compras', ('ID', 'Compra', 'Producto', 'Cantidad', 'Costo Unitario', 'Subtotal'), mostrar_detalle_compras))
btn_detalle_compras.grid(row=5, column=0, sticky='e', padx=5, pady=5)

btn_ventas = Button(mi_frame, text='Mostrar Ventas', width=50, height=5, 
                    command=lambda: mostrar_modelo(Venta, 'Ventas', ('ID', 'Fecha', 'Cliente', 'Total Venta'), mostrar_ventas))
btn_ventas.grid(row=6, column=0, sticky='e', padx=5, pady=5)

btn_detalle_ventas = Button(mi_frame, text='Mostrar Detalle Ventas', width=50, height=5, 
                            command=lambda: mostrar_modelo(DetalleVenta, 'Detalle Ventas', ('ID', 'Venta', 'Producto', 'Cantidad', 'Precio Unitario', 'Subtotal'), mostrar_detalle_ventas))
btn_detalle_ventas.grid(row=7, column=0, sticky='e', padx=5, pady=5)

raiz.mainloop()
