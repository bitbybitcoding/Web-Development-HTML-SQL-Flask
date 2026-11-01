INSERT INTO category (category_id, name) VALUES (1, 'Microcontrollers'), (2, 'Sensors'), (3, 'Motors and wheels'), (4, 'Tools');

INSERT INTO kit (kit_id, name, category_id, total_qty, notes) VALUES
    (1, 'Arduino Uno',            1, 10, 'Includes USB cable'),
    (2, 'micro:bit v2',           1, 12, NULL),
    (3, 'Ultrasonic sensor',      2, 8,  NULL),
    (4, 'Line-follower sensor',   2, 6,  'Calibrate before use'),
    (5, 'DC motor pair',          3, 6,  NULL),
    (6, 'Wheel and tyre set',     3, 6,  NULL),
    (7, 'Soldering iron',         4, 3,  'Ask a teacher first'),
    (8, 'Multimeter',             4, 2,  NULL);

-- Dates are relative to today so there is always an overdue loan.
INSERT INTO loan (loan_id, kit_id, borrower, qty, borrowed_on, due_on, returned_on) VALUES
    (1, 1, 'Mei Lin', 2, date('now', '-20 days'), date('now', '-13 days'), NULL),
    (2, 1, 'Arjun',   1, date('now', '-3 days'),  date('now', '+4 days'),  NULL),
    (3, 3, 'Zoe',     2, date('now', '-10 days'), date('now', '-3 days'),  date('now', '-4 days')),
    (4, 7, 'Daniel',  1, date('now', '-2 days'),  date('now', '+5 days'),  NULL),
    (5, 5, 'Mei Lin', 1, date('now', '-30 days'), date('now', '-23 days'), date('now', '-25 days')),
    (6, 2, 'Arjun',   3, date('now', '-1 days'),  date('now', '+6 days'),  NULL);
