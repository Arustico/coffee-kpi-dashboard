-- =====================================
-- INFORMACIÓN:
-- coffee-kpi-dashboard · views.sql
-- Motor:        SQLite 3.52.0
-- Normalización: 3FN con desnormalización selectiva en tablas de hechos
-- Sucursales:   1 (sucursal.id = 1 siempre)
-- Roles:        'admin' | 'barista'
-- =====================================
-- DESRIPCIÓN
-- Vistas en SQL para ser utilizadas por el dashboard
-- =====================================

-- =====================================
-- 1. COSTO PROMEDIO POR INGREDIENTE
-- =====================================

CREATE VIEW v_avg_ingredient_cost AS
SELECT
    ingredient_id,
    SUM(quantity * unit_cost) / SUM(quantity) AS avg_cost
FROM IngredientPurchase
GROUP BY ingredient_id;


-- =====================================
-- 2. COSTO TEÓRICO POR PRODUCTO
-- =====================================

CREATE VIEW v_product_cost AS
SELECT
    p.id AS product_id,
    p.name,
    SUM(pi.quantity * aic.avg_cost) AS cost_per_unit
FROM Product p
JOIN ProductIngredient pi ON p.id = pi.product_id
JOIN v_avg_ingredient_cost aic ON pi.ingredient_id = aic.ingredient_id
GROUP BY p.id;


-- =====================================
-- 3. REVENUE POR PRODUCTO
-- =====================================

CREATE VIEW v_product_revenue AS
SELECT
    si.product_id,
    SUM(si.quantity) AS total_units,
    SUM(si.quantity * si.unit_price) AS revenue
FROM SaleItem si
GROUP BY si.product_id;


-- =====================================
-- 4. VENTAS POR TURNO
-- =====================================

CREATE VIEW v_sales_by_turn AS
SELECT
    s.turn_id,
    DATE(s.sold_at) AS date,
    SUM(si.quantity * si.unit_price) AS revenue,
    SUM(si.quantity) AS units_sold
FROM Sale s
JOIN SaleItem si ON s.id = si.sale_id
GROUP BY s.turn_id, DATE(s.sold_at);


-- =====================================
-- 5. CONSUMO TEÓRICO DE INGREDIENTES
-- =====================================

CREATE VIEW v_ingredient_consumption AS
SELECT
    pi.ingredient_id,
    SUM(si.quantity * pi.quantity) AS total_used
FROM SaleItem si
JOIN ProductIngredient pi ON si.product_id = pi.product_id
GROUP BY pi.ingredient_id;


-- =====================================
-- 6. VALOR DEL CONSUMO
-- =====================================

CREATE VIEW v_consumption_value AS
SELECT
    ic.ingredient_id,
    ic.total_used,
    aic.avg_cost,
    ic.total_used * aic.avg_cost AS total_cost
FROM v_ingredient_consumption ic
JOIN v_avg_ingredient_cost aic
    ON ic.ingredient_id = aic.ingredient_id;


-- =====================================
-- 7. DESPERDICIO
-- =====================================

CREATE VIEW v_waste_value AS
SELECT
    w.ingredient_id,
    SUM(w.quantity) AS total_waste,
    aic.avg_cost,
    SUM(w.quantity * aic.avg_cost) AS waste_cost
FROM WasteLog w
JOIN v_avg_ingredient_cost aic
    ON w.ingredient_id = aic.ingredient_id
GROUP BY w.ingredient_id;


-- =====================================
-- 8. MARGEN POR PRODUCTO
-- =====================================

CREATE VIEW v_product_margin AS
SELECT
    pr.product_id,
    pr.total_units,
    pr.revenue,
    pc.cost_per_unit,
    (pr.total_units * pc.cost_per_unit) AS total_cost,
    pr.revenue - (pr.total_units * pc.cost_per_unit) AS gross_profit,
    (pr.revenue - (pr.total_units * pc.cost_per_unit)) * 1.0 / pr.revenue AS margin
FROM v_product_revenue pr
JOIN v_product_cost pc ON pr.product_id = pc.product_id;


-- =====================================
-- 9. KPI GLOBAL DE DESPERDICIO
-- =====================================

CREATE VIEW v_waste_ratio AS
SELECT
    SUM(wv.waste_cost) AS total_waste_cost,
    SUM(cv.total_cost) AS total_consumption_cost,
    SUM(wv.waste_cost) * 1.0 /
    (SUM(cv.total_cost) + SUM(wv.waste_cost)) AS waste_ratio
FROM v_waste_value wv
JOIN v_consumption_value cv;
