
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
    """Limpieza mínima y cálculo del total por pedido."""
    # Correos en minúsculas y sin espacios
    clientes["correo"] = clientes["correo"].str.lower().str.strip()

    # Precios: reemplazar nulos por 0 y forzar no negativos
    productos["precio"] = productos["precio"].fillna(0)
    productos.loc[productos["precio"] < 0, "precio"] = 0

    # Cantidad: asegurar > 0 (si hay valores inválidos, forzar a 1)
    pedidos.loc[pedidos["cantidad"] <= 0, "cantidad"] = 1

    # Validación simple de fecha (YYYY-MM-DD). Si no cumple, poner NaN.
    # Nota: esto no rompe el ETL; solo marca fechas inválidas como NaN.
    pedidos["fecha"] = pd.to_datetime(pedidos["fecha"], errors="coerce").dt.strftime("%Y-%m-%d")

    # Calcular total: cantidad * precio del producto
    precios = productos.set_index("id_producto")["precio"]
    pedidos["total"] = pedidos["cantidad"] * pedidos["id_producto"].map(precios)

    return clientes, productos, pedidos

def load(clientes, productos, pedidos, db_path=DB_PATH):
    """Carga los DataFrames en tablas SQLite (replace)."""
    db_path.parent.mkdir(parents=True, exist_ok=True)
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
    print(f"✅ ETL ejecutado con éxito → {DB_PATH}")

if __name__ == "__main__":
    run_etl()
