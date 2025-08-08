from sqlmodel import Session, select
from models.entities import Producto, Proveedor, Cliente
def map_products(session: Session) -> tuple[list[str], dict[str,int]]:
    prods = session.exec(select(Producto)).all()
    items = []
    mapping = {}
    for p in prods:
        label = f"{p.id_producto} - {p.modelo} (t:{p.talla} stock:{p.stock_actual})"
        items.append(label)
        mapping[label] = p.id_producto
    return items, mapping

def map_proveedores(session: Session) -> tuple[list[str], dict[str,int]]:
    provs = session.exec(select(Proveedor)).all()
    items = []
    mapping = {}
    for p in provs:
        label = f"{p.id_proveedor} - {p.nombre_proveedor}"
        items.append(label)
        mapping[label] = p.id_proveedor
    return items, mapping

def map_clientes(session: Session) -> tuple[list[str], dict[str,int]]:
    cls = session.exec(select(Cliente)).all()
    items = []
    mapping = {}
    for c in cls:
        label = f"{c.id_cliente} - {c.nombre} {c.apellidos}"
        items.append(label)
        mapping[label] = c.id_cliente
    return items, mapping