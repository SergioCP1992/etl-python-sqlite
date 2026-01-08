
-- ============================
-- ANALYTICS BÁSICO (OBLIGATORIO)
-- ============================

-- 1. Ingresos por producto
SELECT 
    pr.nombre AS producto,
    SUM(p.total) AS ingresos
FROM pedidos p
JOIN productos pr ON pr.id_producto = p.id_producto
GROUP BY pr.nombre
ORDER BY ingresos DESC;

-- 2. Top clientes por gasto
SELECT 
    c.nombre AS cliente,
    SUM(p.total) AS gasto_total
FROM pedidos p
JOIN clientes c ON c.id = p.id_cliente
GROUP BY c.nombre
ORDER BY gasto_total DESC;

-- 3. Ticket promedio (promedio del total por pedido)
SELECT 
    ROUND(AVG(total), 2) AS ticket_promedio
FROM pedidos;

-- 4. Pedidos por fecha
SELECT 
    fecha,
    COUNT(*) AS cantidad_pedidos
FROM pedidos
WHERE fecha IS NOT NULL
GROUP BY fecha
ORDER BY fecha;

--- Ejecutar sqlite3 database/ecommerce.db < analytics.sql
