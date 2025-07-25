from sqlmodel import SQLModel, create_engine
from sqlmodel import SQLModel, Field
from typing import Annotated
from datetime import date

class Cliente(SQLModel, table=True):
    id_cliente: Annotated[int, Field(primary_key=True)]
    nombre: Annotated[str, Field(nullable=False, min_length=3, max_length=50)]
    apellidos: Annotated[str, Field(nullable=False, min_length=3, max_length=50)]
    email: Annotated[str, Field(nullable=False, unique=True)]
    fecha_registro: Annotated[date, Field(nullable=False)]  = date.today()

class Proveedor(SQLModel, table=True):
    id_proveedor: Annotated[int, Field(primary_key=True)]
    nombre_proveedor: Annotated[str, Field(nullable=False, min_length=3, max_length=100)]
    telefono: Annotated[str, Field(nullable=False, max_length=10)]
    email_proveedor: Annotated[str, Field(nullable=False, unique=True)]
    fecha_alta: Annotated[date, Field(nullable=False)] = date.today()

class Compra(SQLModel, table=True):
    id_compra: Annotated[int, Field(primary_key=True)]
    fecha_compra: Annotated[date, Field(nullable=False)] = date.today()
    id_proveedor: Annotated[int, Field(foreign_key=Proveedor().id_proveedor)]
    total_compra: Annotated[float, Field(nullable=False)]

class Producto(SQLModel, table=True):
    id_producto: Annotated[int, Field(primary_key=True)]
    modelo: Annotated[str, Field(nullable=False, min_length=3, max_length=50)]
    talla: Annotated[float, Field(nullable=False, ge=15, le=30)]
    color: Annotated[str, Field(nullable=False, min_length=3, max_length=30)]
    precio: Annotated[float, Field(nullable=False, ge=0)]
    stock_actual: Annotated[int, Field(nullable=False, gt=0)]

class DetalleCompra(SQLModel, table=True):
    id_detalle_compra: Annotated[int, Field(primary_key=True)]
    id_compra: Annotated[int, Field(foreign_key=Compra().id_compra)]
    id_producto: Annotated[int, Field(foreign_key=Producto().id_producto)]
    cantidad: Annotated[int, Field(nullable=False, ge=0)]
    costo_unitario: Annotated[float, Field(nullable=False, ge=0)]
    subtotal: Annotated[float, Field(nullable=False, ge=0)]

class Venta(SQLModel, table=True):
    id_venta: Annotated[int, Field(primary_key=True)]
    fecha_venta: Annotated[date, Field(nullable=False)] = date.today()
    id_cliente: Annotated[int, Field(foreign_key=Cliente().id_cliente)]
    total_venta: Annotated[float, Field(ge=0, nullable=False)]

class DetalleVenta(SQLModel, table=True):
    id_detalle_venta: Annotated[int, Field(primary_key=True)]
    id_venta: Annotated[int, Field(foreign_key=Venta().id_venta)]
    id_producto: Annotated[int, Field(foreign_key=Producto().id_producto)]
    cantidad: Annotated[int, Field(nullable=False, ge=0)]
    precio_unitario: Annotated[float, Field(nullable=False, ge=0)]
    subtotal: Annotated[float, Field(nullable=False, gt=0)]


sqlite_file_name = "prueba.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def main():
    create_db_and_tables()

if __name__ == "__main__":
    main()