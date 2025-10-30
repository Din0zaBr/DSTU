-- lb5.7.sql - Тестовые данные
INSERT INTO product_groups (group_id, group_name, markup) VALUES
(1, 'Электроника', 0.20),    -- Наценка 20%
(2, 'Одежда', 0.30),         -- Наценка 30%
(3, 'Книги', 0.15);          -- Наценка 15%

INSERT INTO products (product_name, group_id, purchase_price, quantity) VALUES
('Смартфон', 1, 500.00, 10),
('Ноутбук', 1, 1000.00, 5),
('Футболка', 2, 15.00, 50),
('Джинсы', 2, 40.00, 30),
('Роман', 3, 10.00, 100),
('Учебник', 3, 20.00, 75);

-- Проверка товаров (должны быть автоматически рассчитаны розничные цены)
SELECT * FROM products;

-- Проверка групп (должны быть автоматически рассчитаны итоговые количества и стоимости)
SELECT * FROM product_groups;

-- Проверка изменения наценки
UPDATE product_groups SET markup = 0.25 WHERE group_id = 1;
SELECT * FROM products WHERE group_id = 1; -- Цены должны пересчитаться

