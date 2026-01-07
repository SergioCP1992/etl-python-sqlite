
import pandas as pd
import sqlite3

# 1) EXTRACT
clientes = pd.read_csv("data/clientes.csv")
productos = pd.read_csv("data/productos.csv")
pedidos = pd.read_csv("data/pedidos.csv")

# 2) TRANSFORM (limpieza mínima y cálculo de total)
clientes["correo"] = clientes["correo"].str.lower()
productos["precio"] = productos["precio"].fillna(0)
precios = productos.set_index("id_producto")["precio"]
pedidos["total"] = pedidos["cantidad"] * pedidos["id_producto"].map(precios)

# 3) LOAD (crear/reescribir tablas en SQLite)
conn = sqlite3.connect("database/ecommerce.db")
clientes.to_sql("clientes", conn, if_exists="replace", index=False)
productos.to_sql("productos", conn, if_exists="replace", index=False)
pedidos.to_sql("pedidos", conn, if_exists="replace", index=False)
conn.close()

print("ETL ejecutado con éxito → database/ecommerce.db")
