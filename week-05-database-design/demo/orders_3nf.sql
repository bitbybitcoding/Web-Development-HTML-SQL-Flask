-- Week 5 demo: the order form from the normalisation walk-through, in 3NF.
-- Run:   sqlite3 my-work/orders.db      then      .read week-05-database-design/demo/orders_3nf.sql

PRAGMA foreign_keys = ON;

DROP TABLE IF EXISTS order_item;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS customer;
DROP TABLE IF EXISTS product;

CREATE TABLE customer (
    customer_id    TEXT PRIMARY KEY,
    customer_name  TEXT NOT NULL,
    customer_phone TEXT
);

CREATE TABLE product (
    product_id    TEXT PRIMARY KEY,
    product_name  TEXT NOT NULL,
    unit_price    REAL NOT NULL
);

CREATE TABLE orders (                         -- "order" is a reserved word, so we use "orders"
    order_id     INTEGER PRIMARY KEY,
    order_date   TEXT NOT NULL,
    customer_id  TEXT NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customer (customer_id)
);

CREATE TABLE order_item (
    order_id    INTEGER,
    product_id  TEXT,
    qty         INTEGER NOT NULL,
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id)   REFERENCES orders (order_id),
    FOREIGN KEY (product_id) REFERENCES product (product_id)
);

INSERT INTO customer VALUES ('C1', 'Ahmad bin Ali', '91234567');
INSERT INTO customer VALUES ('C2', 'Mei Ling Tan', '98765432');

INSERT INTO product VALUES ('P1', 'Pen',      1.20);
INSERT INTO product VALUES ('P2', 'Notebook', 3.50);
INSERT INTO product VALUES ('P3', 'Ruler',    0.90);
INSERT INTO product VALUES ('P4', 'Eraser',   0.60);     -- no order needed: no insert anomaly

INSERT INTO orders VALUES (1001, '2026-03-02', 'C1');
INSERT INTO orders VALUES (1002, '2026-03-03', 'C2');
INSERT INTO orders VALUES (1003, '2026-03-05', 'C1');

INSERT INTO order_item VALUES (1001, 'P1', 10);
INSERT INTO order_item VALUES (1001, 'P2', 2);
INSERT INTO order_item VALUES (1002, 'P1', 5);
INSERT INTO order_item VALUES (1003, 'P3', 4);
INSERT INTO order_item VALUES (1003, 'P2', 1);

-- Re-assemble the original order form with joins
SELECT o.order_id, o.order_date, c.customer_name, p.product_name, p.unit_price, i.qty
FROM orders AS o
JOIN customer AS c ON c.customer_id = o.customer_id
JOIN order_item AS i ON i.order_id = o.order_id
JOIN product AS p ON p.product_id = i.product_id
ORDER BY o.order_id, p.product_id;

-- Update anomaly gone: change a phone number in ONE place
UPDATE customer SET customer_phone = '90000000' WHERE customer_id = 'C1';

-- Delete anomaly gone: deleting an order does not delete the product
DELETE FROM order_item WHERE order_id = 1003;
DELETE FROM orders WHERE order_id = 1003;
SELECT * FROM product;        -- the Ruler is still there
