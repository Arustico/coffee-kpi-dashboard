-- =============================================================================
-- coffee-kpi-dashboard · schema.sql
-- Motor:        SQLite 3.52.0
-- Normalización: 3FN con desnormalización selectiva en tablas de hechos
-- Sucursales:   1 (sucursal.id = 1 siempre)
-- Roles:        'admin' | 'barista'

-- =========================
-- DIMENSIONALES
-- =========================

CREATE TABLE Role (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL UNIQUE
);

CREATE TABLE Employee (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    role_id INTEGER NOT NULL,
    active INTEGER DEFAULT 1,
    FOREIGN KEY (role_id) REFERENCES Role(id)
);

CREATE TABLE Turn (
    id INTEGER PRIMARY KEY,
    label TEXT NOT NULL,
    start_time TEXT NOT NULL,
    end_time TEXT NOT NULL
);

CREATE TABLE Product (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT,
    base_price REAL NOT NULL,
    active INTEGER DEFAULT 1
);

CREATE TABLE IngredientUnit (
    unit TEXT PRIMARY KEY,
    description TEXT
);

CREATE TABLE Ingredient (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    unit TEXT NOT NULL,
    active INTEGER DEFAULT 1,
    FOREIGN KEY (unit) REFERENCES IngredientUnit(unit)
);

-- Receta
CREATE TABLE ProductIngredient (
    product_id INTEGER,
    ingredient_id INTEGER,
    quantity REAL NOT NULL,
    PRIMARY KEY (product_id, ingredient_id),
    FOREIGN KEY (product_id) REFERENCES Product(id),
    FOREIGN KEY (ingredient_id) REFERENCES Ingredient(id)
);

-- =========================
-- TRANSACCIONALES
-- =========================

CREATE TABLE Sale (
    id INTEGER PRIMARY KEY,
    employee_id INTEGER NOT NULL,
    turn_id INTEGER NOT NULL,
    sold_at TEXT NOT NULL,
    total_amount REAL NOT NULL,
    FOREIGN KEY (employee_id) REFERENCES Employee(id),
    FOREIGN KEY (turn_id) REFERENCES Turn(id)
);

CREATE TABLE SaleItem (
    id INTEGER PRIMARY KEY,
    sale_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    quantity INTEGER NOT NULL CHECK(quantity > 0),
    unit_price REAL NOT NULL,
    FOREIGN KEY (sale_id) REFERENCES Sale(id),
    FOREIGN KEY (product_id) REFERENCES Product(id)
);

CREATE TABLE Supplier (
    id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);

CREATE TABLE IngredientPurchase (
    id INTEGER PRIMARY KEY,
    ingredient_id INTEGER NOT NULL,
    supplier_id INTEGER,
    quantity REAL NOT NULL CHECK(quantity > 0),
    unit_cost REAL NOT NULL CHECK(unit_cost >= 0),
    purchased_at TEXT NOT NULL,
    FOREIGN KEY (ingredient_id) REFERENCES Ingredient(id),
    FOREIGN KEY (supplier_id) REFERENCES Supplier(id)
);

CREATE TABLE WasteLog (
    id INTEGER PRIMARY KEY,
    ingredient_id INTEGER NOT NULL,
    employee_id INTEGER NOT NULL,
    turn_id INTEGER NOT NULL,
    logged_at TEXT NOT NULL,
    quantity REAL NOT NULL CHECK(quantity >= 0),
    reason TEXT,
    FOREIGN KEY (ingredient_id) REFERENCES Ingredient(id),
    FOREIGN KEY (employee_id) REFERENCES Employee(id),
    FOREIGN KEY (turn_id) REFERENCES Turn(id)
);

-- =========================
-- ÍNDICES
-- =========================

CREATE INDEX idx_sale_turn ON Sale(turn_id);
CREATE INDEX idx_sale_employee ON Sale(employee_id);
CREATE INDEX idx_saleitem_product ON SaleItem(product_id);
CREATE INDEX idx_purchase_ingredient ON IngredientPurchase(ingredient_id);
CREATE INDEX idx_waste_turn ON WasteLog(turn_id);
