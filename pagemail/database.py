import sqlite3
from os import path
from flask import g

DB_FILENAME = "content.db"

def get_db():
	db = getattr(g, "_database", None)
	if db is None:
		db = _open_database_connection()
		db.execute('pragma foreign_keys=ON')
		g._database = db
	return db

def _open_database_connection():
	db_path = path.join(path.dirname(__file__), '..', DB_FILENAME)
	return sqlite3.connect(db_path)

def close_db():
	db = getattr(g, "_database", None)
	if db is not None:
		db.close()
