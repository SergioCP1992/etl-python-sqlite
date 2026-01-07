
import pandas as pd
import sqlite3
from pathlib import Path

DATA_DIR = Path("data")
DB_PATH = Path("database/ecommerce.db")

def extract():
    """Lee los CSV desde la carpeta data y devuelve DataFrames."""
    clientes = pd.read_csv(DATA_DIR / "clientes.csv")
    productos = pd.read_csv(DATA_DIR / "productos.csv")
    pedidos = pd.read_csv(DATA_DIR / "pedidos.csv")
    return clientes, productos, pedidos

def transform(clientes, productos, pedidos):
    """Aplica limpieza mínima y calcula el total por pedido."""
    # Normalizaciones básicas
    clientes["correo"] = clientes["correo"].str.lower().str.strip()
    productos["precio"] = productos["precio"].fillna(0)

    # Mapeo de precios por id_producto
    precios = productos.set_index("id_producto")["precio"]
    pedidos["total"] = pedidos["cantidad"] * pedidos["id_producto"].map(precios)

    return clientes, productos, pedidos

def load(clientes, productos, pedidos, db_path=DB_PATH):
    """Carga los DataFrames en tablas SQLite (replace)."""
    db_path.parent.mkdir(parents=True, exist_ok=True)  # crea /database si no existe
    conn = sqlite3.connect(db_path)
    try:
        clientes.to_sql("clientes", conn, if_exists="replace", index=False)
        productos.to_sql("productos", conn, if_exists="replace", index=False)
        pedidos.to_sql("pedidos", conn, if_exists="replace", index=False)
    finally:
        conn.close()

def run_etl():
    """Pipeline completo: Extract → Transform → Load."""
    clientes, productos, pedidos = extract()
    clientes, productos, pedidos = transform(clientes, productos, pedidos)
    load(clientes, productos, pedidos)
    print(f"ETL ejecutado con éxito → {DB_PATH}")

# Permite que el archivo sea ejecutable como script,
# pero también importable como módulo sin correr automáticamente.
if __name__ == "__main__":
    run_etl()
``
