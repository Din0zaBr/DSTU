SELECT 
    p.product_id,
    p.product_name,
    pg.group_name,
    p.retail_price,
    p.quantity
FROM products p
JOIN product_groups pg ON p.group_id = pg.group_id
ORDER BY p.product_id;
