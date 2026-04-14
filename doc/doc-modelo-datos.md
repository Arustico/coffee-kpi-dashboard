# Modelo de Datos

## Algunas generalidades: 

* *Turn* (turno) será la entidad central. Será la únidad de análisis primaria para la cafetería. A partir de este se podrá realizar análisis diarios, semanales y mensuales. El *turn_id* en Sale se asigna automáticamente comparando sold_at contra los rangos *start_time/end_time*, sin que el barista tenga que seleccionarlo.

* *WasteLog* para registrar desperdicio por insumo/turno. Se liga directamente a *Ingredient* (no a *Product*) porque el desperdicio ocurre a nivel de insumo: **se bota leche, no un latte**. Esto permite calcular waste_ratio con precisión real.

* *SaleItem.unit_price* se guarda como snapshot del precio vigente en el momento de venta. Así, si mañana sube el precio del latte, los reportes históricos no se ven alterados.

* El costo teórico vs real se resuelve con dos **VIEWs**: una desde *ProductIngredient + IngredientCostHistory*, otra desde *IngredientPurchase + WasteLog*. 

* *Target* ahora tiene turn_type opcional (mañana/tarde/noche) además de período semanal/mensual

## Variables del modelo explicadas
A continuación se muestran las variables del modelo para el cafe, sus variables y cómo deben obtenerse. 

### Dimensionales
Son ingresadas una vez por definición o acuerdo y cambian poco. 

| Variable | Significado | Cómo se obtiene |
|----------|-------------|-----------------|
|```product.name```       | Nombre del producto vendido (ej. "Latte 12oz") | Definido / Manual |
|```product.category```   | Categoría (café, té, comida, otro) | Definido / Manual |
|```product.base_price``` | Precio de venta vigente | Definido / Manual |
|```ingredient.name```    | Nombre del insumo (ej. "Leche entera") | Definido / Manual |
|```ingredient.unit```    | Unidad de medida (ml, g, oz, unidad) | Definido / Manual |
|```ingredient.cost_per_unit```     | Costo actual del insumo por unidad | Se actualiza al registrar cada compra |
|```product_ingredient.quantity```  | Cantidad de insumo que usa 1 unidad del producto | Definido / Manual (la "receta") | 
|```employee.name```  | Nombre del barista o gerente | Definido / Manual |
|```employee.role```  | Rol: barista o manager | Definido / Manual |                         |
|```turn.label```    | Nombre del turno (Mañana / Tarde / Noche) | Definido / Manual |      |
|```turn.start_time / end_time``` | Horario de inicio y fin del turno | Definido / Manual | |
------------------

### Transaccionales
Son aquellas que se ingresan en la operación diaria. 

| Variable | Significado | Cómo se obtiene | 
|----------|-------------|-----------------|
|```sale.sold_at```     | Fecha y hora exacta de la venta   | Automático (timestamp al registrar)   |
|```sale.turn_id```     | Turno en que ocurrió la venta     | Calculado automáticamente según hora  |
|```sale.employee_id``` | Barista que registró la venta  | Login del barista en la app |
|```sale_item.product_id```  | Producto vendido         | Selección en la app         |
|```sale_item.quantity```    | Cuántas unidades se vendieron  | Ingreso por barista    |
| ```sale_item.unit_price``` | Precio al momento de la venta  | Copiado automáticamente desde ```product.base_price``` |
| ```ingredient_purchase.ingredient_id``` | Insumo comprado   | Selección al registrar compra |
| ```ingredient_purchase.quantity```      | Cantidad comprada | Ingreso por gerente o barista |
| ```ingredient_purchase.unit_cost```     | Costo pagado en esa compra        | Ingreso manual (desde factura/boleta) |
| ```ingredient_purchase.purchased_at```  | Fecha y hora exacta de la compra  | Automático (timestamp al registrar)   |
| ```waste_log.ingredient_id```           | Insumo desperdiciado              | Registrado por barista al final del turno |
| ```waste_log.quantity```  | Cantidad desperdiciada | Ingreso por barista | 
|```waste_log.reason```     | Motivo (caducidad, error de preparación, derrame) | Selección de lista por barista |
------------------


### KPIs derivados 
Estas se calculan, no se guardan — viven en VIEWs.

| KPI | Significado | Fórmula |
|-----|-------------|---------|
| ```revenue_per_turn``` | Ingresos totales por turno | ```SUM(sale_item.quantity × unit_price)``` agrupado por ```turn``` |
|```cost_per_cup``` | Costo de ingredientes por unidad vendida | ```SUM(ingredient.cost_per_unit × product_ingredient.quantity)``` por producto
| ```gross_margin```| Margen bruto por producto o turno | ```(unit_price − cost_per_cup) / unit_price × 100``` |```ingredient_consumption``` | Insumos consumidos por período | ```SUM(sale_item.quantity × product_ingredient.quantity)``` por ingrediente
|```waste_value```   | Valor económico del desperdicio  |  ```SUM(waste_log.quantity × ingredient.cost_per_unit)```
|```waste_ratio``` | % de insumo desperdiciado vs consumido | ```waste_value / (consumption_value + waste_value) × 100```
------------------

## Esquema del Modelo (ERD)

```mermaid
erDiagram
    Supplier ||--o{ IngredientPurchase : provee
    Supplier {
        int id PK
        string name
        string contact
    }
    Ingredient ||--o{ IngredientPurchase : comprado-en
    Ingredient ||--o{ ProductIngredient : usado-en
    Ingredient ||--|| WasteLog : desperdiciado
    Ingredient {
        int id PK
        string name
        string unit
        float cost_per_unit
    }
    
    Turn ||--o{ WasteLog : en-el-Turno
    Turn ||--o{ Sale : agrupa
    Turn {
        int id PK
        string label
        time start_time
        time end_time
    }
    
    Employee ||--o{ WasteLog : registra
    Employee ||--o{ Sale : registra
    Employee {
        int id PK
        string name
        string role
        bool active
    }
    
    IngredientPurchase {
        int id PK
        int ingredient_id FK
        int supplier_id FK
        date purchased_at
        float quantity
        float unit_cost    
    }
    
    WasteLog {
        int id PK
        int ingredient_id FK
        int employee_id FK
        int turn_id FK
        date logged_at 
        float quantity
        string reason
    }
    
    Sale ||--o{ SaleItem : contiene
    Sale {
        int id PK
        int employee_id FK
        int turn_id FK
        datetime sold_at
        float total_amount
    }
    
    SaleItem ||--o{ Product : es
    SaleItem {
        int id PK
        int sale_id FK
        int product_id FK
        int quantity
        float unit_price
    }
    
    Product ||--o{ ProductIngredient : requiere
    Product{
        int id PK
        string name
        string category
        float base_price
        bool active
    }
    
    ProductIngredient{
        int product_id FK
        int ingredient_id FK
        float quantity    
    }

```




