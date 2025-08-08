from datetime import date
from typing import Optional
from database.conexion import SQLModel
from typing import Annotated
from sqlmodel import Field

class Cliente(SQLModel, table=True):
    id_cliente: Annotated[Optional[int], Field(default=None, primary_key=True)]
    nombre: Annotated[str, Field(nullable=False, min_length=3, max_length=50)]
    apellidos: Annotated[str, Field(nullable=False, min_length=3, max_length=50)]
    email: Annotated[str, Field(nullable=False, unique=True)]
    fecha_registro: Annotated[date, Field(default_factory=date.today, nullable=False)]

class Proveedor(SQLModel, table=True):
    id_proveedor: Annotated[Optional[int], Field(default=None, primary_key=True)]
    nombre_proveedor: Annotated[str, Field(nullable=False, min_length=3, max_length=100)]
    telefono: Annotated[str, Field(nullable=False, max_length=15)]
    email_proveedor: Annotated[str, Field(nullable=False, unique=True)]
    fecha_alta: Annotated[date, Field(default_factory=date.today, nullable=False)]

class Compra(SQLModel, table=True):
    id_compra: Annotated[Optional[int], Field(default=None, primary_key=True)]
    fecha_compra: Annotated[date, Field(default_factory=date.today, nullable=False)]
    id_proveedor: Annotated[int, Field(foreign_key="proveedor.id_proveedor")]
    total_compra: Annotated[float, Field(default=0.0, nullable=False)]

class Producto(SQLModel, table=True):
    id_producto: Annotated[Optional[int], Field(default=None, primary_key=True)]
    modelo: Annotated[str, Field(nullable=False, min_length=3, max_length=50)]
    talla: Annotated[float, Field(nullable=False, ge=15, le=50)]
    color: Annotated[str, Field(nullable=False, min_length=1, max_length=30)]
    precio: Annotated[float, Field(nullable=False, ge=0)]
    stock_actual: Annotated[int, Field(default=0, nullable=False, ge=0)]

class DetalleCompra(SQLModel, table=True):
    id_detalle_compra: Annotated[Optional[int], Field(default=None, primary_key=True)]
    id_compra: Annotated[int, Field(foreign_key="compra.id_compra")]
    id_producto: Annotated[int, Field(foreign_key="producto.id_producto")]
    cantidad: Annotated[int, Field(nullable=False, ge=0)]
    costo_unitario: Annotated[float, Field(nullable=False, ge=0)]
    subtotal: Annotated[float, Field(nullable=False, ge=0)]

class Venta(SQLModel, table=True):
    id_venta: Annotated[Optional[int], Field(default=None, primary_key=True)]
    fecha_venta: Annotated[date, Field(default_factory=date.today, nullable=False)]
    id_cliente: Annotated[int, Field(foreign_key="cliente.id_cliente")]
    total_venta: Annotated[float, Field(default=0.0, nullable=False)]

class DetalleVenta(SQLModel, table=True):
    id_detalle_venta: Annotated[Optional[int], Field(default=None, primary_key=True)]
    id_venta: Annotated[int, Field(foreign_key="venta.id_venta")]
    id_producto: Annotated[int, Field(foreign_key="producto.id_producto")]
    cantidad: Annotated[int, Field(nullable=False, ge=0)]
    precio_unitario: Annotated[float, Field(nullable=False, ge=0)]
    subtotal: Annotated[float, Field(nullable=False, ge=0)]