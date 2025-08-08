from interfaz.cliente import ClienteWindow
from interfaz.proveedor import ProveedorWindow
from interfaz.producto import ProductoWindow
from interfaz.compra import CompraWindow
from interfaz.detalle_compra import DetalleCompraWindow
from interfaz.venta import VentaWindow
from interfaz.detalle_venta import DetalleVentaWindow
import tkinter as tk
from tkinter import ttk, messagebox
from sqlmodel import Session, select