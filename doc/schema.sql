CREATE TABLE emails (
       id INTEGER PRIMARY KEY,
       view_uuid TEXT NOT NULL,
       admin_uuid TEXT NOT NULL,
       sentfrom TEXT NOT NULL,
       subject TEXT NOT NULL,
       content TEXT NOT NULL
);

CREATE TABLE views (
       email INTEGER NOT NULL,
       viewed INTEGER NOT NULL,
       ip TEXT NOT NULL,
       user_agent TEXT NOT NULL,
       cookie_uuid TEXT NOT NULL,
       FOREIGN KEY (email) REFERENCES emails(id)
);
