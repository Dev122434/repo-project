from sqlite3 import *
from tkinter import *
from matplotlib.pyplot import *
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import tkinter as tk
from total_ventas import datos
from genero import total

def cuadro1():
    pass

def cuadro2():
    pass

def abrir_subventana():

    
    def grafica_total_ventas():
        ventana_ventas = Toplevel(sub)
        ventana_ventas.title('Grafica De Ventas')
        ventana_ventas.geometry('800x550')
        tk.Button(ventana_ventas, text='Cerrar', width=50, height=5, command=ventana_ventas.destroy).pack()


        inicio = '2024-04-16'
        final = '2025-04-26'


        fechas = [fila[0] for fila in datos]
        totales = [fila[1] for fila in datos]


        grafica, area =plt.subplots(figsize=(8, 4))
        area.bar(fechas, totales, color='dodgerblue')
        area.set_title('Ventas Por Rango De Fecha')
        area.set_xlabel('Fecha')
        area.set_ylabel('Total ($)')
        area.tick_params(axis='x', rotation=45)

        for i, total in enumerate(totales):
            area.text(i, total + max(totales)*0.01, f'${total:.2f}', ha='center', fontsize=8)

        
        canvas = FigureCanvasTkAgg(grafica, master=ventana_ventas)
        canvas.draw()
        canvas.get_tk_widget().pack(padx=10, pady=10)

    def grafica_genero():
        ventana_genero = Toplevel(sub)
        ventana_genero.title('Grafica De Ventas')
        ventana_genero.geometry('800x550')
        tk.Button(ventana_genero, text='Cerrar', width=50, height=5, command=ventana_genero.destroy).pack()

        f, m = total
        valores = [f, m]
        area, grafica =plt.subplots(figsize=(8, 4))
        colores = ['plum', 'royalblue']
        etiquetas = ['Femenino', 'Masculino']

        grafica.pie(valores, colors=colores, labels=etiquetas, startangle=90, shadow=True, explode=(0.1,0), autopct='%1.1f%%')
        grafica.set_title('Distribucion Por Genero')

        canvas = FigureCanvasTkAgg(area, master=ventana_genero)
        canvas.draw()
        canvas.get_tk_widget().pack()

    sub = tk.Toplevel(raiz)
    sub.title('Ventana Secundaria')
    tk.Label(sub, text='Esto es una subventana', font=('Comic Sans MS', 18)).pack()
    sub.geometry('800x500')
    opciones = [
        ('Grafica: Total Ventas', grafica_total_ventas),
        ('Grafica: Por Genero', grafica_genero),
        ('Cerrar', sub.destroy)
    ]

    for texto, funcion in opciones:
        tk.Button(sub, text=texto, width=25, height=5, command=funcion).pack(padx=20, pady=20)
# Programa Principal
raiz = Tk()
raiz.title('Ventana Principal')
raiz.config(bg='bisque3')
raiz.geometry('1000x800')
tk.Button(raiz, text='Abrir Ventana', width=25, height=5, command=abrir_subventana).pack()
raiz.mainloop()