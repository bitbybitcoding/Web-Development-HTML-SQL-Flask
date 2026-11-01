-- Sample data so every page has something to show. Use realistic data, at least 8 rows in your main table.
INSERT INTO category (category_id, name) VALUES (1, 'Tools'), (2, 'Books'), (3, 'Games');

INSERT INTO item (name, category_id, quantity, notes) VALUES
    ('Screwdriver set', 1, 4, NULL),
    ('Glue gun',        1, 2, 'Needs a new battery'),
    ('Python for Kids', 2, 3, NULL),
    ('Chess set',       3, 1, NULL);
