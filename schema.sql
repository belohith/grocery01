DROP TABLE IF EXISTS groceries;

CREATE TABLE groceries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    quantity INTEGER NOT NULL DEFAULT 1,
    units TEXT DEFAULT '',
    category TEXT DEFAULT '',             -- New: category column
    notes TEXT DEFAULT '',                -- New: notes column
    purchased INTEGER NOT NULL DEFAULT 0
);