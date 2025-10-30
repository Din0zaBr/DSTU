-- 3. Создание таблицы "Товары"
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY DEFAULT nextval('products_product_id_seq'),
    product_name TEXT NOT NULL,
    group_id INTEGER REFERENCES product_groups(group_id) ON UPDATE CASCADE,
    purchase_price NUMERIC(15,2) NOT NULL DEFAULT 0.00,
    retail_price NUMERIC(15,2) NOT NULL DEFAULT 0.00,
    quantity INTEGER NOT NULL DEFAULT 0
);

